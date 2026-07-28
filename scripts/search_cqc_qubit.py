#!/usr/bin/env python3
"""Exploratory random search for a two-qubit CQC violation.

This script samples induced random density matrices of selected ranks and
computes

    gap = I(Z^A:Z^B) + I(X^A:X^B) - I(A:B)

for Pauli Z and X measurements on both qubits. Fixing the MUB pair to Z and X
is without loss of generality up to local unitaries.

The search is evidence only. Failure to find a positive gap is not a proof of
the two-qubit CQC inequality.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

import numpy as np


HADAMARD = np.array([[1.0, 1.0], [1.0, -1.0]], dtype=np.complex128) / math.sqrt(2.0)
HADAMARD_PAIR = np.kron(HADAMARD, HADAMARD)


def entropy_eigenvalues(values: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    """Von Neumann/Shannon entropy, vectorized over the final axis."""
    clipped = np.clip(np.real(values), 0.0, None)
    terms = np.where(clipped > tol, -clipped * np.log2(np.maximum(clipped, tol)), 0.0)
    return terms.sum(axis=-1)


def partial_traces(rho: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    reshaped = rho.reshape(-1, 2, 2, 2, 2)
    rho_a = np.einsum("nabcb->nac", reshaped)
    rho_b = np.einsum("nabad->nbd", reshaped)
    return rho_a, rho_b


def classical_mutual_information(prob: np.ndarray, tol: float = 1e-14) -> np.ndarray:
    pa = prob.sum(axis=2)
    pb = prob.sum(axis=1)
    h_a = entropy_eigenvalues(pa, tol)
    h_b = entropy_eigenvalues(pb, tol)
    h_ab = entropy_eigenvalues(prob.reshape(prob.shape[0], -1), tol)
    return h_a + h_b - h_ab


def cqc_values(rho: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return gap, I_Z, I_X, and quantum I(A:B) for a batch of states."""
    rho = (rho + np.swapaxes(rho.conj(), -1, -2)) / 2.0

    rho_a, rho_b = partial_traces(rho)
    s_a = entropy_eigenvalues(np.linalg.eigvalsh(rho_a))
    s_b = entropy_eigenvalues(np.linalg.eigvalsh(rho_b))
    s_ab = entropy_eigenvalues(np.linalg.eigvalsh(rho))
    i_quantum = s_a + s_b - s_ab

    pz = np.real(np.diagonal(rho, axis1=1, axis2=2)).reshape(-1, 2, 2)
    rotated = HADAMARD_PAIR.conj().T @ rho @ HADAMARD_PAIR
    px = np.real(np.diagonal(rotated, axis1=1, axis2=2)).reshape(-1, 2, 2)

    i_z = classical_mutual_information(pz)
    i_x = classical_mutual_information(px)
    return i_z + i_x - i_quantum, i_z, i_x, i_quantum


def random_induced_states(
    rng: np.random.Generator,
    count: int,
    rank: int,
) -> np.ndarray:
    matrix = rng.normal(size=(count, 4, rank)) + 1j * rng.normal(size=(count, 4, rank))
    rho = matrix @ np.swapaxes(matrix.conj(), -1, -2)
    traces = np.real(np.trace(rho, axis1=1, axis2=2))
    return rho / traces[:, None, None]


def parse_ranks(text: str) -> list[int]:
    values = [int(item.strip()) for item in text.split(",") if item.strip()]
    if not values or any(rank < 1 for rank in values):
        raise argparse.ArgumentTypeError("ranks must be a comma-separated list of positive integers")
    return values


def search_rank(
    rng: np.random.Generator,
    rank: int,
    samples: int,
    batch_size: int,
) -> tuple[float, float, float, float, np.ndarray]:
    best_gap = -math.inf
    best_values = (math.nan, math.nan, math.nan)
    best_state = np.eye(4, dtype=np.complex128) / 4.0

    remaining = samples
    while remaining > 0:
        count = min(batch_size, remaining)
        rho = random_induced_states(rng, count, rank)
        gap, i_z, i_x, i_quantum = cqc_values(rho)
        index = int(np.argmax(gap))
        if float(gap[index]) > best_gap:
            best_gap = float(gap[index])
            best_values = (float(i_z[index]), float(i_x[index]), float(i_quantum[index]))
            best_state = rho[index].copy()
        remaining -= count

    return best_gap, *best_values, best_state


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ranks", type=parse_ranks, default=parse_ranks("1,2,3,4"))
    parser.add_argument("--samples-per-rank", type=int, default=25000)
    parser.add_argument("--batch-size", type=int, default=2500)
    parser.add_argument("--seed", type=int, default=20260723)
    parser.add_argument("--save-best", type=Path)
    args = parser.parse_args()

    if args.samples_per_rank < 1 or args.batch_size < 1:
        parser.error("sample counts must be positive")

    rng = np.random.default_rng(args.seed)
    global_best: tuple[float, int, np.ndarray] | None = None

    print("Exploratory two-qubit CQC random search")
    print(f"seed={args.seed}, samples_per_rank={args.samples_per_rank}")
    print("rank         max gap              I_Z              I_X           I(A:B)")

    for rank in args.ranks:
        gap, i_z, i_x, i_quantum, state = search_rank(
            rng,
            rank,
            args.samples_per_rank,
            args.batch_size,
        )
        print(f"{rank:4d}  {gap:+.15e}  {i_z:.12f}  {i_x:.12f}  {i_quantum:.12f}")
        if global_best is None or gap > global_best[0]:
            global_best = (gap, rank, state)

    assert global_best is not None
    print(f"best sampled gap={global_best[0]:+.15e} at induced rank {global_best[1]}")
    print("No positive sample is evidence only, not a proof.")

    if args.save_best is not None:
        np.savez_compressed(
            args.save_best,
            rho=global_best[2],
            gap=global_best[0],
            rank=global_best[1],
            seed=args.seed,
            samples_per_rank=args.samples_per_rank,
        )
        print(f"saved best sampled state to {args.save_best}")


if __name__ == "__main__":
    main()
