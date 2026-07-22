#!/usr/bin/env python3
"""High-precision physical-basis verification of the CQC counterexample,
plus checks of Iqbal's (arXiv:2509.08286) Proposition-3 sufficient condition
and the extended CQC (ECQC) conjecture over all four qutrit MUBs.

This implementation was generated within the same model-assisted workflow as
the other repository artifacts. It is structurally separate, not an
independent expert replication.

Design differences from the first two scripts:
  - state amplitudes entered directly in the physical |ab> basis
    (separately expanded, not generated via logical-qubit kron products);
  - all arithmetic in mpmath at 60 significant digits;
  - measurement bases built from the standard prime-d MUB family
    v^m_k = 3^{-1/2} sum_j w^{jk+m j^2} |j>, m = 0,1,2, plus computational;
  - Holevo quantities I(M^A:B) computed for the Coles-Piani/Iqbal condition.

Basis ordering |ab> -> index 3a+b.
"""
from fractions import Fraction
from itertools import combinations
from mpmath import mp, matrix, sqrt, log, exp, pi, mpf, mpc

mp.dps = 60
LOG2 = log(2)
I3 = matrix(3, 3)
for j in range(3):
    I3[j, j] = 1


def dag(A):
    return A.transpose_conj()


def kron(A, B):
    C = matrix(A.rows * B.rows, A.cols * B.cols)
    for i in range(A.rows):
        for j in range(A.cols):
            for k in range(B.rows):
                for l in range(B.cols):
                    C[i * B.rows + k, j * B.cols + l] = A[i, j] * B[k, l]
    return C


def herm_eigs(A):
    try:
        return mp.eighe(A, eigvals_only=True)
    except TypeError:
        E, _ = mp.eighe(A)
        return E


def entropy_bits(eigs):
    s = mpf(0)
    for x in eigs:
        if x > mpf("1e-45"):
            s -= x * log(x) / LOG2
    return s


def cmi_bits(P):
    ra = [sum(P[i, j] for j in range(P.cols)) for i in range(P.rows)]
    cb = [sum(P[i, j] for i in range(P.rows)) for j in range(P.cols)]
    s = mpf(0)
    for i in range(P.rows):
        for j in range(P.cols):
            if P[i, j] > mpf("1e-45"):
                s += P[i, j] * log(P[i, j] / (ra[i] * cb[j])) / LOG2
    return s


def ptrace_B(r):
    out = matrix(3, 3)
    for a in range(3):
        for ap in range(3):
            out[a, ap] = sum(r[3 * a + b, 3 * ap + b] for b in range(3))
    return out


def ptrace_A(r):
    out = matrix(3, 3)
    for b in range(3):
        for bp in range(3):
            out[b, bp] = sum(r[3 * a + b, 3 * a + bp] for a in range(3))
    return out


# ---------------------------------------------------------------- state
# phi = (|00> + (|11>+|12>+|21>+|22>)/2)/sqrt(2)
# chi = |00>/sqrt(3) - (|01>+|02>+|10>+|20>)/sqrt(12)
#       - (|11>+|12>+|21>+|22>)/(2 sqrt(3))
s2, s3, s12 = sqrt(2), sqrt(3), sqrt(12)
phi = matrix(9, 1)
chi = matrix(9, 1)
phi[0] = 1 / s2
for idx in (4, 5, 7, 8):
    phi[idx] = 1 / (2 * s2)
chi[0] = 1 / s3
for idx in (1, 2, 3, 6):
    chi[idx] = -1 / s12
for idx in (4, 5, 7, 8):
    chi[idx] = -1 / (2 * s3)

rho = mpf(9) / 10 * (phi * dag(phi)) + mpf(1) / 10 * (chi * dag(chi))

# sanity: normalization, orthogonality, trace, PSD, spectrum {9/10, 1/10}
assert abs((dag(phi) * phi)[0, 0] - 1) < mpf("1e-50")
assert abs((dag(chi) * chi)[0, 0] - 1) < mpf("1e-50")
assert abs((dag(phi) * chi)[0, 0]) < mpf("1e-50")
tr = sum(rho[i, i] for i in range(9))
assert abs(tr - 1) < mpf("1e-50")
spec = sorted((mp.re(x) for x in herm_eigs(rho)), reverse=True)
tol = mpf("1e-45")
assert abs(spec[0] - mpf("0.9")) < tol
assert abs(spec[1] - mpf("0.1")) < tol
assert all(abs(x) < tol for x in spec[2:])

# ------------------------------------------------------------- MUB bases
w = exp(mpc(0, 1) * 2 * pi / 3)


def mub_basis(m):
    if m == "comp":
        return I3.copy()
    U = matrix(3, 3)
    for k in range(3):
        for j in range(3):
            U[j, k] = w ** ((j * k + m * j * j) % 3) / s3
    return U


BASES = [("Z(comp)", mub_basis("comp")), ("X(Fourier)", mub_basis(0)),
         ("M2", mub_basis(1)), ("M3", mub_basis(2))]

# verify every pair of distinct bases is mutually unbiased in C^3
for (na, Ua), (nb, Ub) in combinations(BASES, 2):
    G = dag(Ua) * Ub
    for i in range(3):
        for j in range(3):
            ov = G[i, j].real ** 2 + G[i, j].imag ** 2
            assert abs(ov - mpf(1) / 3) < mpf("1e-45"), (na, nb, i, j)
print("all 4 bases pairwise mutually unbiased in C^3: OK")


def joint_table(r, U):
    rr = dag(kron(U, U)) * r * kron(U, U)
    P = matrix(3, 3)
    for a in range(3):
        for b in range(3):
            P[a, b] = rr[3 * a + b, 3 * a + b].real
    return P


def holevo_A_measured(r, U):
    """I(M^A : B) for measurement of basis U on A (Holevo quantity)."""
    rr = dag(kron(U, I3)) * r * kron(U, I3)
    SB = entropy_bits(herm_eigs(ptrace_A(r)))
    acc = mpf(0)
    for a in range(3):
        blk = matrix(3, 3)
        for b in range(3):
            for bp in range(3):
                blk[b, bp] = rr[3 * a + b, 3 * a + bp]
        p = sum(blk[b, b] for b in range(3)).real
        if p > mpf("1e-45"):
            acc += p * entropy_bits(herm_eigs(blk / p))
    return SB - acc


def report(r, label):
    print(f"\n===== {label} =====")
    SA = entropy_bits(herm_eigs(ptrace_B(r)))
    SB = entropy_bits(herm_eigs(ptrace_A(r)))
    SAB = entropy_bits(herm_eigs(r))
    IQ = SA + SB - SAB
    print(f"S(A)={mp.nstr(SA,20)}  S(B)={mp.nstr(SB,20)}  S(AB)={mp.nstr(SAB,20)}")
    print(f"I(A:B) = {mp.nstr(IQ,20)} bits")

    Is = []
    for name, U in BASES:
        P = joint_table(r, U)
        Im = cmi_bits(P)
        Is.append(Im)
        snapped = [[Fraction(float(P[i, j])).limit_denominator(10**8)
                    for j in range(3)] for i in range(3)]
        print(f"I({name}^A:{name}^B) = {mp.nstr(Im,20)}   table {snapped}")

    cqc = Is[0] + Is[1] - IQ
    print(f"CQC gap  I_Z + I_X - I(A:B) = {mp.nstr(cqc,20)}"
          f"   -> {'VIOLATED' if cqc > 0 else 'satisfied'}")

    # Iqbal arXiv:2509.08286 Proposition 3 sufficient condition:
    # I(Z^A:B) - I(Z:Z) + I(X^A:B) - I(X:X) >= log d - H(A)  ==> CQC holds
    IZB = holevo_A_measured(r, BASES[0][1])
    IXB = holevo_A_measured(r, BASES[1][1])
    lhs = IZB - Is[0] + IXB - Is[1]
    rhs = log(3) / LOG2 - SA
    print(f"Iqbal Prop 3: I(Z^A:B)={mp.nstr(IZB,20)}  I(X^A:B)={mp.nstr(IXB,20)}")
    print(f"  condition LHS={mp.nstr(lhs,20)}  RHS=log2(3)-S(A)={mp.nstr(rhs,20)}"
          f"   -> sufficient condition {'HOLDS (contradiction!)' if lhs >= rhs else 'fails (consistent)'}")
    # Coles-Piani proven bound must hold regardless:
    cp = IZB + IXB - (log(3) / LOG2 - (SAB - SB))
    print(f"  Coles-Piani check I(Z^A:B)+I(X^A:B) <= log d - S(A|B): "
          f"slack={mp.nstr(-cp,20)} {'OK' if cp <= mpf('1e-40') else 'BROKEN'}")

    # ECQC (Conjecture 3.1): I(A:B) >= min over size-d subsets of the d+1
    # per-MUB classical MIs of their sum; d=3, so min over 4 choose 3 triples.
    best = None
    for S in combinations(range(4), 3):
        tot = sum(Is[i] for i in S)
        if best is None or tot < best[0]:
            best = (tot, S)
    names = [BASES[i][0] for i in best[1]]
    print(f"ECQC: min 3-subset sum = {mp.nstr(best[0],20)} over {names}")
    print(f"  ECQC gap (min-sum - I(A:B)) = {mp.nstr(best[0]-IQ,20)}"
          f"   -> {'VIOLATED' if best[0] > IQ else 'satisfied'}")
    return IQ, Is


IQ, Is = report(rho, "rank-2 state rho = 0.9|phi><phi| + 0.1|chi><chi|")

# residual uncertainty (Schneeloch et al. Eq. 5 bracket) must be > 0,
# and neither measurement may be minimally disturbing, else a proven case applies
HZ = entropy_bits([mpf(1) / 2, mpf(1) / 4, mpf(1) / 4])
resid = 2 * HZ - log(3) / LOG2 - 1
print(f"\nresidual uncertainty H(Z^A)+H(X^A)-log2(3)-S(A) = {mp.nstr(resid,20)} (>0: outside proven cases)")
rhoA = ptrace_B(rho)
for name, U in BASES[:2]:
    rot = dag(U) * rhoA * U
    off = max(abs(rot[i, j]) for i in range(3) for j in range(3) if i != j)
    print(f"max off-diagonal of rho_A in {name} eigenbasis = {mp.nstr(off,10)} (nonzero: not minimally disturbing)")

# full-rank 1% white-noise perturbation
Ifull = matrix(9, 9)
for i in range(9):
    Ifull[i, i] = mpf(1) / 9
rho_full = mpf(99) / 100 * rho + mpf(1) / 100 * Ifull
report(rho_full, "full-rank state 0.99*rho + 0.01*I/9")

print("\ndone.")
