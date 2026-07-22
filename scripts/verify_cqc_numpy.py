#!/usr/bin/env python3
"""Separate NumPy check of an explicit counterexample to the CQC conjecture.

This script was generated within the same model-assisted workflow as the other
repository artifacts; it is not independent expert replication. Uses only NumPy.  Basis ordering is |00>,|01>,...,|22>.
"""

import numpy as np


def entropy(eigenvalues: np.ndarray) -> float:
    x = np.asarray(eigenvalues, dtype=float)
    x = x[x > 1e-14]
    return float(-np.sum(x * np.log2(x)))


def classical_mutual_information(p: np.ndarray) -> float:
    p = np.asarray(p, dtype=float)
    pa = p.sum(axis=1, keepdims=True)
    pb = p.sum(axis=0, keepdims=True)
    mask = p > 0
    ratio = p / (pa @ pb)
    return float(np.sum(p[mask] * np.log2(ratio[mask])))


def partial_traces(rho: np.ndarray, d: int = 3) -> tuple[np.ndarray, np.ndarray]:
    r = rho.reshape(d, d, d, d)  # indices a,b,a',b'
    rho_a = np.einsum("abcb->ac", r)
    rho_b = np.einsum("abad->bd", r)
    return rho_a, rho_b


# Logical qubit inside each qutrit.
e = np.eye(3, dtype=complex)
ket0 = e[:, 0]
ket1 = (e[:, 1] + e[:, 2]) / np.sqrt(2)
K = np.kron

# Two orthonormal Schmidt-rank-2 maximally entangled states.
phi = (K(ket0, ket0) + K(ket1, ket1)) / np.sqrt(2)
chi = (
    K(ket0, ket0) / np.sqrt(3)
    - (K(ket0, ket1) + K(ket1, ket0)) / np.sqrt(6)
    - K(ket1, ket1) / np.sqrt(3)
)

rho = (9 / 10) * np.outer(phi, phi.conj()) + (1 / 10) * np.outer(chi, chi.conj())

# Computational and Fourier qutrit bases.
omega = np.exp(2j * np.pi / 3)
F = np.array([[omega ** (i * j) for j in range(3)] for i in range(3)]) / np.sqrt(3)
FF = K(F, F)

assert np.allclose(F.conj().T @ F, np.eye(3), atol=1e-12)
assert np.allclose(np.abs(F) ** 2, np.ones((3, 3)) / 3, atol=1e-12)

p_z = np.real(np.diag(rho)).reshape(3, 3)
p_x = np.real(np.diag(FF.conj().T @ rho @ FF)).reshape(3, 3)

rho_a, rho_b = partial_traces(rho)
I_quantum = (
    entropy(np.linalg.eigvalsh(rho_a))
    + entropy(np.linalg.eigvalsh(rho_b))
    - entropy(np.linalg.eigvalsh(rho))
)
I_z = classical_mutual_information(p_z)
I_x = classical_mutual_information(p_x)
delta = I_z + I_x - I_quantum

expected_p = np.array(
    [
        [29 / 60, 1 / 120, 1 / 120],
        [1 / 120, 29 / 240, 29 / 240],
        [1 / 120, 29 / 240, 29 / 240],
    ]
)

assert np.allclose(phi.conj() @ phi, 1)
assert np.allclose(chi.conj() @ chi, 1)
assert np.allclose(phi.conj() @ chi, 0)
assert np.allclose(np.trace(rho), 1)
assert np.linalg.eigvalsh(rho).min() > -1e-12
assert np.allclose(p_z, expected_p, atol=1e-12)
assert np.allclose(p_x, expected_p, atol=1e-12)
assert delta > 0.047

# Full-rank robustness check, recomputed directly from the perturbed state.
rho_full = (99 / 100) * rho + (1 / 100) * np.eye(9) / 9
p_full_z = np.real(np.diag(rho_full)).reshape(3, 3)
p_full_x = np.real(np.diag(FF.conj().T @ rho_full @ FF)).reshape(3, 3)
rho_full_a, rho_full_b = partial_traces(rho_full)
I_quantum_full = (
    entropy(np.linalg.eigvalsh(rho_full_a))
    + entropy(np.linalg.eigvalsh(rho_full_b))
    - entropy(np.linalg.eigvalsh(rho_full))
)
I_z_full = classical_mutual_information(p_full_z)
I_x_full = classical_mutual_information(p_full_x)
delta_full = I_z_full + I_x_full - I_quantum_full

expected_p_full = np.array(
    [
        [8633 / 18000, 337 / 36000, 337 / 36000],
        [337 / 36000, 8693 / 72000, 8693 / 72000],
        [337 / 36000, 8693 / 72000, 8693 / 72000],
    ]
)

assert np.linalg.eigvalsh(rho_full).min() > 0
assert np.allclose(p_full_z, expected_p_full, atol=1e-12)
assert np.allclose(p_full_x, expected_p_full, atol=1e-12)
assert delta_full > 0.036

np.set_printoptions(precision=12, suppress=True)
print("P_Z =\n", p_z)
print("P_X =\n", p_x)
print(f"I(Z^A:Z^B) = {I_z:.12f} bits")
print(f"I(X^A:X^B) = {I_x:.12f} bits")
print(f"I(A:B)       = {I_quantum:.12f} bits")
print(f"violation    = {delta:.12f} bits")
print(f"full-rank violation = {delta_full:.12f} bits")

# Exact sign certificate for h_2(1/10) - 2 h_2(1/30) > 0.
lhs = 29**58
rhs = 3**114 * 10**30
assert lhs > rhs
print("exact integer check: 29^58 > 3^114 * 10^30 is", lhs > rhs)
