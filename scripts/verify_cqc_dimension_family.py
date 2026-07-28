#!/usr/bin/env python3
"""Verify an all-dimension family related to the CQC counterexample.

For each d >= 2, the script embeds a logical qubit in C^d, constructs a
rank-two bipartite state rho_{d,eps}, and evaluates quantum mutual information
and matched computational/Fourier classical mutual informations.

The exact formulas are
    I(A:B) = 2 - h2(eps),
    I_Z = I_X = 1 - h2(eps/d),
    gap = h2(eps) - 2 h2(eps/d).

At eps = 1/10 the sign is exactly equivalent to
    (10d - 1)^(20d - 2) > 10^(10d) d^(20d) 3^(18d).
"""

from __future__ import annotations

import argparse
import math
from typing import Tuple

import numpy as np


def h2(p: float) -> float:
    """Binary Shannon entropy in bits."""
    if p == 0.0 or p == 1.0:
        return 0.0
    if not 0.0 < p < 1.0:
        raise ValueError("p must lie in [0,1]")
    return -p * math.log2(p) - (1.0 - p) * math.log2(1.0 - p)


def fourier_basis(d: int) -> np.ndarray:
    """Columns are the d-dimensional Fourier basis vectors."""
    omega = np.exp(2j * np.pi / d)
    return np.array(
        [[omega ** (j * k) / math.sqrt(d) for k in range(d)] for j in range(d)],
        dtype=np.complex128,
    )


def construct_state(d: int, eps: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    if d < 2:
        raise ValueError("d must be at least 2")
    if not 0.0 <= eps <= 1.0:
        raise ValueError("eps must lie in [0,1]")

    zero_l = np.zeros(d, dtype=np.complex128)
    zero_l[0] = 1.0
    one_l = np.zeros(d, dtype=np.complex128)
    one_l[1:] = 1.0 / math.sqrt(d - 1)

    c = 1.0 / math.sqrt(d)
    s = math.sqrt((d - 1) / d)

    phi = (
        np.kron(zero_l, zero_l) + np.kron(one_l, one_l)
    ) / math.sqrt(2)

    chi = (
        s * np.kron(zero_l, zero_l)
        - c * np.kron(zero_l, one_l)
        - c * np.kron(one_l, zero_l)
        - s * np.kron(one_l, one_l)
    ) / math.sqrt(2)

    rho = (1.0 - eps) * np.outer(phi, phi.conj()) + eps * np.outer(chi, chi.conj())
    return rho, phi, chi


def entropy(rho: np.ndarray, tol: float = 1e-13) -> float:
    vals = np.linalg.eigvalsh((rho + rho.conj().T) / 2)
    if vals.min() < -1e-10:
        raise ValueError("matrix is not positive semidefinite")
    vals = vals[vals > tol]
    return float(-np.sum(vals * np.log2(vals)))


def partial_trace(rho: np.ndarray, d: int, keep: str) -> np.ndarray:
    r = rho.reshape(d, d, d, d)
    if keep == "A":
        return np.einsum("abcb->ac", r)
    if keep == "B":
        return np.einsum("abad->bd", r)
    raise ValueError("keep must be 'A' or 'B'")


def joint_probabilities(rho: np.ndarray, basis: np.ndarray) -> np.ndarray:
    d = basis.shape[0]
    out = np.empty((d, d), dtype=np.float64)
    for i in range(d):
        for j in range(d):
            ket = np.kron(basis[:, i], basis[:, j])
            out[i, j] = float(np.real(ket.conj() @ rho @ ket))
    out[np.abs(out) < 1e-15] = 0.0
    return out


def classical_mutual_information(p: np.ndarray) -> float:
    pa = p.sum(axis=1)
    pb = p.sum(axis=0)
    total = 0.0
    for i in range(p.shape[0]):
        for j in range(p.shape[1]):
            if p[i, j] > 0:
                total += p[i, j] * math.log2(p[i, j] / (pa[i] * pb[j]))
    return total


def exact_sign_certificate_eps_tenth(d: int) -> bool:
    lhs = pow(10 * d - 1, 20 * d - 2)
    rhs = pow(10, 10 * d) * pow(d, 20 * d) * pow(3, 18 * d)
    return lhs > rhs


def verify_dimension(d: int, eps: float = 0.1) -> None:
    rho, phi, chi = construct_state(d, eps)
    z_basis = np.eye(d, dtype=np.complex128)
    x_basis = fourier_basis(d)

    rho_a = partial_trace(rho, d, "A")
    rho_b = partial_trace(rho, d, "B")
    i_quantum = entropy(rho_a) + entropy(rho_b) - entropy(rho)

    pz = joint_probabilities(rho, z_basis)
    px = joint_probabilities(rho, x_basis)
    iz = classical_mutual_information(pz)
    ix = classical_mutual_information(px)
    gap = iz + ix - i_quantum

    expected_iq = 2.0 - h2(eps)
    expected_ic = 1.0 - h2(eps / d)
    expected_gap = h2(eps) - 2.0 * h2(eps / d)

    assert abs(np.vdot(phi, phi) - 1) < 1e-12
    assert abs(np.vdot(chi, chi) - 1) < 1e-12
    assert abs(np.vdot(phi, chi)) < 1e-12
    assert abs(np.trace(rho) - 1) < 1e-12
    assert np.linalg.eigvalsh(rho).min() > -1e-11
    assert abs(i_quantum - expected_iq) < 2e-11
    assert abs(iz - expected_ic) < 2e-11
    assert abs(ix - expected_ic) < 2e-11
    assert abs(gap - expected_gap) < 3e-11
    assert np.max(np.abs(pz - px)) < 2e-11

    cert = exact_sign_certificate_eps_tenth(d) if abs(eps - 0.1) < 1e-15 else None
    print(
        f"d={d:2d}  Iq={i_quantum:.15f}  "
        f"IZ=IX={iz:.15f}  gap={gap:+.15f}"
        + (f"  exact-positive={cert}" if cert is not None else "")
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--min-d", type=int, default=2)
    parser.add_argument("--max-d", type=int, default=10)
    parser.add_argument("--eps", type=float, default=0.1)
    args = parser.parse_args()

    if args.min_d < 2 or args.max_d < args.min_d:
        parser.error("require 2 <= min-d <= max-d")

    for d in range(args.min_d, args.max_d + 1):
        verify_dimension(d, args.eps)


if __name__ == "__main__":
    main()
