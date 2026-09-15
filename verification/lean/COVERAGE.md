# Lean coverage: PARTIAL

Date: 15 September 2026. This is not a formalization of the paper's recovery
theorems. The selected vertical result proves actual operator inequalities
from calibrated sharp projections, not from assumed recovery conclusions.

## Kernel-checked scope

`calibrated_projection_words` uses genuine complex Hilbert spaces H and K,
an isometry V : H -> K, self-adjoint idempotent operators P_y on H and Q_y on
K, and the unamplified operator norm of V-adjoint Q_y V - P_y. With this norm
at most e independently for every y, it proves

\[
\|T_w V-VR_w\|\le 2|w|\sqrt e,
\qquad T_y=2Q_y-I_K,\quad R_y=2P_y-I_H.
\]

The physical projections need not commute. Logical and physical dimensions
are independent; the proof also works in complete infinite-dimensional
Hilbert spaces. The isometry, projections and norm are mathlib objects.
Self-adjointness, idempotence, isometry and calibration are the substantive
hypotheses; no word bound, recovery map or fidelity input is assumed.

The dependency chain derives reflection involution and norm bounds,
the exact squared intertwiner identity, the squared operator norm estimate,
single-letter amplitude control, and arbitrary finite-word propagation.
`calibrated_reflection_words` exposes the intermediate reflection formulation.
The source includes `#print axioms` for every exported proof. The checker
requires all twelve reports, including `calibrated_projection_words`, and
the exact axiom set `propext`, `Classical.choice`, and `Quot.sound` in each.
Missing, duplicate and unexpected reports or axioms fail; previous success
artifacts are preserved when compilation or certificate validation fails.
These are standard Lean foundations, not scientific assumptions.

## Paper-to-formalization matrix

All declaration names below have namespace `FiniteQuestionRecovery`.

| Paper statement | Lean declaration | Coverage / remaining gap |
|---|---|---|
| Section 3, calibrated projections to word intertwiners | `calibrated_projection_words` | Checked at actual Hilbert-operator level for physical projection effects. Halmos dilation of arbitrary effects and identification with a channel pullback remain analytic. |
| Section 3, reflection defect and word telescoping | `reflection_defect_identity`, `reflection_defect_norm_sq`, `rectangular_reflection_defect_identity`, `rectangular_reflection_defect_norm_sq`, `word_stability`, `calibrated_reflection_words` | Checked. Includes different logical and physical Hilbert spaces, no hidden dimension constant. |
| Theorem 3.1 positive-word recovery | No Lean recovery declaration | NOT formalized: probability-word averaging, CP floor, complementary channels, Bures contraction, common Stinespring alignment, polar correction, diamond estimate. |
| Corollary 3.2 gap-to-recovery | None | NOT formalized: normalized Choi comparison, CP minorization, binomial second moment, Theorem 3.1. |
| Theorem 4.1 / Corollary 4.2 | None | NOT formalized: word filtration, dephasing channel, trace-distance contraction and minimax optimization. |
| Theorems 5.1 and 5.2 | None | NOT formalized: anchor isometry, polar extension, covariance estimate and diamond conclusions. |
| Proposition 5.3 | None | NOT formalized: dephasing recovery, complete geometry and positive-word separation. |
| Theorem 6.1 / Appendix A | None | NOT formalized: Halmos dilation, sign/kernel completion, Pauli representation, CP covariance, complete-to-diamond conversion. |
| Lemma 7.1 / Theorem 7.2 | None | NOT formalized: retained-output compression/leakage bound, binary cyclicity, circuit semantics and tester access. Finite executable controls are tests, not proof-assistant certificates. |
| Section 2 complete geometry and Hermitian dilation equality | None | NOT formalized: amplified conditional expectation and block operator norms. |

## Infrastructure boundary and reproducibility

Toolchain: Lean 4.30.0, compiler commit
`d024af099ca4bf2c86f649261ebf59565dc8c622`.
Mathlib: `c5ea00351c28e24afc9f0f84379aa41082b1188f` (v4.30.0).
The Lake manifest pins the existing dependency revisions. The local check
uses installed compiled dependencies read-only and downloads nothing.
On a machine with the pinned dependencies installed, `lake build` or
`lake env lean FiniteQuestionRecovery.lean` checks the source. Portable commands and resource guidance are in
[REPRODUCIBILITY.md](../../REPRODUCIBILITY.md).
