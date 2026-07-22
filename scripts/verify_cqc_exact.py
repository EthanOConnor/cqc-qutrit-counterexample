#!/usr/bin/env python3
"""Exact symbolic verification of the qutrit CQC counterexample.

Requires SymPy 1.14.0. State, measurement, entropy, and sign identities are
checked exactly. Decimal evaluation is used only for human-readable output.
This script was generated within the same model-assisted workflow documented
in PROVENANCE.md; it is not independent expert replication.
Basis ordering: |00>, |01>, ..., |22>.
"""

from math import lcm

import sympy as sp


R = sp.Rational
sqrt = sp.sqrt
imaginary_unit = sp.I
kron = sp.kronecker_product


def matrix_is_zero(mat: sp.Matrix) -> bool:
    return mat.applyfunc(sp.simplify) == sp.zeros(*mat.shape)


def partial_trace_over_b(mat: sp.Matrix, d: int = 3) -> sp.Matrix:
    """Trace out B and retain A."""
    return sp.Matrix(
        d,
        d,
        lambda a, ap: sp.simplify(
            sum(mat[d * a + b, d * ap + b] for b in range(d))
        ),
    )


def partial_trace_over_a(mat: sp.Matrix, d: int = 3) -> sp.Matrix:
    """Trace out A and retain B."""
    return sp.Matrix(
        d,
        d,
        lambda b, bp: sp.simplify(
            sum(mat[d * a + b, d * a + bp] for a in range(d))
        ),
    )


def joint_probabilities(rho: sp.Matrix, basis: list[sp.Matrix]) -> sp.Matrix:
    return sp.Matrix(
        3,
        3,
        lambda a, b: sp.simplify(
            sp.expand_complex(
                (
                    kron(basis[a], basis[b]).conjugate().T
                    * rho
                    * kron(basis[a], basis[b])
                )[0]
            )
        ),
    )


def h2(q):
    q = sp.sympify(q)
    return -q * sp.log(q, 2) - (1 - q) * sp.log(1 - q, 2)


def shannon(values):
    return -sum(v * sp.log(v, 2) for v in values if v != 0)


def classical_mi(p: sp.Matrix):
    rows = [sum(p[i, j] for j in range(p.cols)) for i in range(p.rows)]
    cols = [sum(p[i, j] for i in range(p.rows)) for j in range(p.cols)]
    return shannon(rows) + shannon(cols) - shannon(list(p))


def entropy_log_terms(values, multiplier=R(1)):
    """Return (coefficient, rational argument) terms for multiplier*H(values)."""
    return [(-multiplier * v, v) for v in values if v != 0]


def exact_positive_log_certificate(terms):
    """Prove sum(c*log2(q)) > 0 by reducing it to an integer comparison."""
    terms = [(R(c), R(q)) for c, q in terms]
    scale = lcm(*(int(c.q) for c, _ in terms))
    prime_exponents: dict[int, int] = {}

    for coefficient, argument in terms:
        integer_coefficient = int(coefficient * scale)
        assert R(integer_coefficient, scale) == coefficient
        for prime, exponent in sp.factorint(int(argument.p)).items():
            prime_exponents[prime] = (
                prime_exponents.get(prime, 0) + integer_coefficient * exponent
            )
        for prime, exponent in sp.factorint(int(argument.q)).items():
            prime_exponents[prime] = (
                prime_exponents.get(prime, 0) - integer_coefficient * exponent
            )

    numerator = 1
    denominator = 1
    for prime, exponent in prime_exponents.items():
        if exponent > 0:
            numerator *= prime**exponent
        elif exponent < 0:
            denominator *= prime ** (-exponent)

    assert numerator > denominator
    return scale, numerator, denominator, prime_exponents


# Logical qubit embedded in a qutrit.
ket0 = sp.Matrix([1, 0, 0])
ket1 = sp.Matrix([0, 1 / sqrt(2), 1 / sqrt(2)])
support_projector = ket0 * ket0.T + ket1 * ket1.T

phi = (kron(ket0, ket0) + kron(ket1, ket1)) / sqrt(2)
chi = (
    kron(ket0, ket0) / sqrt(3)
    - (kron(ket0, ket1) + kron(ket1, ket0)) / sqrt(6)
    - kron(ket1, ket1) / sqrt(3)
)

assert sp.simplify((phi.conjugate().T * phi)[0]) == 1
assert sp.simplify((chi.conjugate().T * chi)[0]) == 1
assert sp.simplify((phi.conjugate().T * chi)[0]) == 0

rho = R(9, 10) * phi * phi.conjugate().T + R(1, 10) * chi * chi.conjugate().T
assert sp.trace(rho) == 1
assert rho.rank() == 2
assert matrix_is_zero(rho * phi - R(9, 10) * phi)
assert matrix_is_zero(rho * chi - R(1, 10) * chi)

rho_a = partial_trace_over_b(rho)
rho_b = partial_trace_over_a(rho)
assert matrix_is_zero(rho_a - support_projector / 2)
assert matrix_is_zero(rho_b - support_projector / 2)

# Exact computational and Fourier qutrit bases.
z_basis = [sp.eye(3).col(j) for j in range(3)]
omega = -R(1, 2) + imaginary_unit * sqrt(3) / 2
x_basis = [
    sp.Matrix([1, omega**j, omega ** (2 * j)]) / sqrt(3) for j in range(3)
]

for z in z_basis:
    for x in x_basis:
        assert sp.simplify(sp.Abs((z.conjugate().T * x)[0]) ** 2) == R(1, 3)


# Verify the logical-support mechanism used in the note. The Fourier basis
# restricts to a rotated logical binary basis with the second outcome split in
# half, and the coefficient matrices are invariant up to global phase.
def logical_coordinates(vector: sp.Matrix) -> sp.Matrix:
    return sp.Matrix(
        [
            (ket0.conjugate().T * vector)[0],
            (ket1.conjugate().T * vector)[0],
        ]
    ).applyfunc(sp.simplify)


u = sp.Matrix([1 / sqrt(3), sqrt(R(2, 3))])
u_perp = sp.Matrix([sqrt(R(2, 3)), -1 / sqrt(3)])
assert matrix_is_zero(logical_coordinates(x_basis[0]) - u)
assert matrix_is_zero(logical_coordinates(x_basis[1]) - u_perp / sqrt(2))
assert matrix_is_zero(logical_coordinates(x_basis[2]) - u_perp / sqrt(2))

o = sp.Matrix.hstack(u, u_perp)
a_phi = sp.eye(2) / sqrt(2)
a_chi = sp.Matrix(
    [[1 / sqrt(3), -1 / sqrt(6)], [-1 / sqrt(6), -1 / sqrt(3)]]
)
assert matrix_is_zero(o.T * o - sp.eye(2))
assert matrix_is_zero(o.T * a_phi * o - a_phi)
assert matrix_is_zero(o.T * a_chi * o + a_chi)

p_z = joint_probabilities(rho, z_basis)
p_x = joint_probabilities(rho, x_basis)
expected = sp.Matrix(
    [
        [R(29, 60), R(1, 120), R(1, 120)],
        [R(1, 120), R(29, 240), R(29, 240)],
        [R(1, 120), R(29, 240), R(29, 240)],
    ]
)
assert p_z == expected
assert p_x == expected

measurement_marginal = [R(1, 2), R(1, 4), R(1, 4)]
assert list(p_z * sp.ones(3, 1)) == measurement_marginal
assert list(p_z.T * sp.ones(3, 1)) == measurement_marginal

# The fine outcomes 1 and 2 are independent fair refinements of a binary
# symmetric channel. Check the entropy identity directly from the 3x3 table.
i_z_direct = classical_mi(p_z)
i_x_direct = classical_mi(p_x)
i_measurement = 1 - h2(R(1, 30))
assert sp.simplify(sp.expand_log(i_z_direct - i_measurement, force=True)) == 0
assert sp.simplify(sp.expand_log(i_x_direct - i_measurement, force=True)) == 0

i_quantum = 2 - h2(R(1, 10))
violation = h2(R(1, 10)) - 2 * h2(R(1, 30))
assert sp.simplify(i_z_direct + i_x_direct - i_quantum - violation) == 0

# Exact main sign certificate.
main_numerator = 29**58
main_denominator = 3**114 * 10**30
assert main_numerator > main_denominator
assert (
    sp.simplify(
        30 * violation - sp.log(R(main_numerator, main_denominator), 2)
    )
    == 0
)

# Full-rank robustness check, derived directly from rho_full.
rho_full = R(99, 100) * rho + R(1, 100) * sp.eye(9) / 9
assert sp.trace(rho_full) == 1
assert rho_full.rank() == 9
assert rho_full.is_positive_definite

rho_full_a = partial_trace_over_b(rho_full)
rho_full_b = partial_trace_over_a(rho_full)
full_marginal_eigs = [R(299, 600), R(299, 600), R(1, 300)]
full_joint_eigs = [R(8029, 9000), R(901, 9000)] + [R(1, 900)] * 7
assert sorted(rho_full_a.eigenvals().keys()) == sorted(set(full_marginal_eigs))
assert sorted(rho_full_b.eigenvals().keys()) == sorted(set(full_marginal_eigs))
assert rho_full_a.eigenvals()[R(299, 600)] == 2
assert rho_full_b.eigenvals()[R(299, 600)] == 2
assert sorted(rho_full.eigenvals().keys()) == sorted(set(full_joint_eigs))
assert rho_full.eigenvals()[R(1, 900)] == 7

p_full_z = joint_probabilities(rho_full, z_basis)
p_full_x = joint_probabilities(rho_full, x_basis)
expected_full = sp.Matrix(
    [
        [R(8633, 18000), R(337, 36000), R(337, 36000)],
        [R(337, 36000), R(8693, 72000), R(8693, 72000)],
        [R(337, 36000), R(8693, 72000), R(8693, 72000)],
    ]
)
assert p_full_z == expected_full
assert p_full_x == expected_full

full_measurement_rows = list(p_full_z * sp.ones(3, 1))
full_measurement_cols = list(p_full_z.T * sp.ones(3, 1))
full_i_z = classical_mi(p_full_z)
full_i_x = classical_mi(p_full_x)
full_i_quantum = 2 * shannon(full_marginal_eigs) - shannon(full_joint_eigs)
full_gap = full_i_z + full_i_x - full_i_quantum

# Build the same full_gap as a rational linear combination of logarithms and
# prove its sign by one exact integer comparison.
full_gap_terms = []
full_gap_terms += entropy_log_terms(full_measurement_rows, 2)
full_gap_terms += entropy_log_terms(full_measurement_cols, 2)
full_gap_terms += entropy_log_terms(list(p_full_z), -2)
full_gap_terms += entropy_log_terms(full_marginal_eigs, -2)
full_gap_terms += entropy_log_terms(full_joint_eigs, 1)
full_gap_from_terms = sum(c * sp.log(q, 2) for c, q in full_gap_terms)
assert sp.simplify(full_gap - full_gap_from_terms) == 0
full_scale, full_num, full_den, full_prime_exponents = (
    exact_positive_log_certificate(full_gap_terms)
)

print("Exact P_Z = P_X =")
sp.pprint(expected)
print()
print("I(Z^A:Z^B) = I(X^A:X^B) =", sp.N(i_measurement, 16), "bits")
print("I(A:B) =", sp.N(i_quantum, 16), "bits")
print("violation =", sp.N(violation, 16), "bits")
print("main exact sign certificate:", main_numerator > main_denominator)
print("1%-white-noise full-rank gap =", sp.N(full_gap, 16), "bits")
print("full-rank exact sign certificate:", full_num > full_den)
print("full-rank certificate scale:", full_scale)
print(
    "full-rank prime exponents:",
    {
        prime: exponent
        for prime, exponent in sorted(full_prime_exponents.items())
        if exponent
    },
)
