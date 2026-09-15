import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Tactic.NoncommRing
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith

/-!
Partial formalization: concrete bounded operators on complex Hilbert space.
This file does not define a quantum channel or assert a recovery theorem.
-/
noncomputable section
open ContinuousLinearMap

namespace FiniteQuestionRecovery

variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable {K : Type*} [NormedAddCommGroup K] [InnerProductSpace ℂ K] [CompleteSpace K]

/-- Rectangular version: logical and physical Hilbert spaces may differ. -/
theorem rectangular_reflection_defect_identity
    (T : K →L[ℂ] K) (V : H →L[ℂ] K) (R : H →L[ℂ] H)
    (hT : adjoint T = T) (hR : adjoint R = R)
    (hTT : T ∘L T = 1) (hRR : R ∘L R = 1) (hV : adjoint V ∘L V = 1) :
    adjoint (T ∘L V - V ∘L R) ∘L (T ∘L V - V ∘L R) =
      -(adjoint V ∘L T ∘L V - R) ∘L R - R ∘L (adjoint V ∘L T ∘L V - R) := by
  have hTV : T ∘L (T ∘L V) = V := by rw [← comp_assoc, hTT, one_def, id_comp]
  have hVR : adjoint V ∘L (V ∘L R) = R := by rw [← comp_assoc, hV, one_def, id_comp]
  simp only [map_sub, adjoint_comp, hT, hR, sub_comp, comp_sub,
    comp_assoc, hTV, hVR, hRR, hV]
  abel

/-- The calibrated compression gives squared operator-norm error, with no
assumed intertwiner estimate and no restriction on physical dimension. -/
theorem rectangular_reflection_defect_norm_sq
    (T : K →L[ℂ] K) (V : H →L[ℂ] K) (R : H →L[ℂ] H)
    (hT : adjoint T = T) (hR : adjoint R = R)
    (hTT : T ∘L T = 1) (hRR : R ∘L R = 1) (hV : adjoint V ∘L V = 1)
    (hRn : ‖R‖ ≤ 1) :
    ‖T ∘L V - V ∘L R‖ ^ 2 ≤ 2 * ‖adjoint V ∘L T ∘L V - R‖ := by
  rw [pow_two, ← norm_adjoint_comp_self,
    rectangular_reflection_defect_identity T V R hT hR hTT hRR hV]
  calc
    ‖-(adjoint V ∘L T ∘L V - R) ∘L R - R ∘L (adjoint V ∘L T ∘L V - R)‖
      ≤ ‖-(adjoint V ∘L T ∘L V - R) ∘L R‖ + ‖R ∘L (adjoint V ∘L T ∘L V - R)‖ := norm_sub_le _ _
    _ ≤ ‖adjoint V ∘L T ∘L V - R‖ * ‖R‖ + ‖R‖ * ‖adjoint V ∘L T ∘L V - R‖ := by
      simpa only [neg_comp, norm_neg] using add_le_add (opNorm_comp_le (-(adjoint V ∘L T ∘L V - R)) R)
        (opNorm_comp_le R (adjoint V ∘L T ∘L V - R))
    _ ≤ 2 * ‖adjoint V ∘L T ∘L V - R‖ := by
      nlinarith [norm_nonneg (adjoint V ∘L T ∘L V - R)]

/-- Exact squared-intertwiner identity, with a genuine Hilbert-space isometry V.
The common ambient Hilbert space permits isometric (not necessarily unitary)
embeddings and includes the finite-dimensional padded setting. -/
theorem reflection_defect_identity (T V R : H →L[ℂ] H)
    (hT : star T = T) (hR : star R = R)
    (hTT : T * T = 1) (hRR : R * R = 1) (hV : star V * V = 1) :
    star (T * V - V * R) * (T * V - V * R) =
      -(star V * T * V - R) * R - R * (star V * T * V - R) := by
  simp only [star_sub, star_mul, hT, hR]
  have hTV : T * (T * V) = V := by rw [← mul_assoc, hTT, one_mul]
  have hVR : star V * (V * R) = R := by rw [← mul_assoc, hV, one_mul]
  noncomm_ring [hTV, hVR, hRR, hV]

/-- Calibration bounds an actual squared operator-norm intertwining defect. -/
theorem reflection_defect_norm_sq (T V R : H →L[ℂ] H)
    (hT : star T = T) (hR : star R = R)
    (hTT : T * T = 1) (hRR : R * R = 1) (hV : star V * V = 1)
    (hRn : ‖R‖ ≤ 1) :
    ‖T * V - V * R‖ ^ 2 ≤ 2 * ‖star V * T * V - R‖ := by
  rw [pow_two, ← CStarRing.norm_star_mul_self, reflection_defect_identity T V R hT hR hTT hRR hV]
  calc
    ‖-(star V * T * V - R) * R - R * (star V * T * V - R)‖
      ≤ ‖-(star V * T * V - R) * R‖ + ‖R * (star V * T * V - R)‖ := norm_sub_le _ _
    _ ≤ ‖star V * T * V - R‖ * ‖R‖ + ‖R‖ * ‖star V * T * V - R‖ := by
      simpa only [norm_neg] using add_le_add (norm_mul_le (-(star V * T * V - R)) R)
        (norm_mul_le R (star V * T * V - R))
    _ ≤ 2 * ‖star V * T * V - R‖ := by
      nlinarith [norm_nonneg (star V * T * V - R)]

#print axioms reflection_defect_identity
#print axioms reflection_defect_norm_sq
#print axioms rectangular_reflection_defect_identity
#print axioms rectangular_reflection_defect_norm_sq

/-- Self-adjoint involutions are contractions, including the zero Hilbert space. -/
theorem reflection_norm_le_one (R : H →L[ℂ] H)
    (hR : adjoint R = R) (hRR : R ∘L R = 1) : ‖R‖ ≤ 1 := by
  have h := norm_adjoint_comp_self R
  rw [hR, hRR] at h
  have hn : ‖(1 : H →L[ℂ] H)‖ ≤ 1 := norm_id_le
  nlinarith [norm_nonneg R]

variable {ι : Type*}

/-- Words act rightmost first, in the same convention as Section 3. -/
def word (T : ι → H →L[ℂ] H) : List ι → H →L[ℂ] H
  | [] => 1
  | a :: w => T a ∘L word T w

omit [CompleteSpace H] in
theorem word_norm_le_one (R : ι → H →L[ℂ] H) (hR : ∀ y, ‖R y‖ ≤ 1)
    (w : List ι) : ‖word R w‖ ≤ 1 := by
  induction w with
  | nil => exact norm_id_le
  | cons a w ih =>
    change ‖R a ∘L word R w‖ ≤ 1
    calc
      _ ≤ ‖R a‖ * ‖word R w‖ := opNorm_comp_le _ _
      _ ≤ 1 := by nlinarith [norm_nonneg (R a), norm_nonneg (word R w), hR a]

omit [CompleteSpace H] [CompleteSpace K] in
/-- The finite-word intertwining estimate for genuine bounded operators. -/
theorem word_stability (T : ι → K →L[ℂ] K) (R : ι → H →L[ℂ] H)
    (V : H →L[ℂ] K) (a : ℝ)
    (hT : ∀ y, ‖T y‖ ≤ 1) (hR : ∀ y, ‖R y‖ ≤ 1)
    (hstep : ∀ y, ‖T y ∘L V - V ∘L R y‖ ≤ a) (w : List ι) :
    ‖word T w ∘L V - V ∘L word R w‖ ≤ (w.length : ℝ) * a := by
  induction w with
  | nil => simp [word, one_def]
  | cons y w ih =>
    have hid : word T (y :: w) ∘L V - V ∘L word R (y :: w) =
        T y ∘L (word T w ∘L V - V ∘L word R w) +
          (T y ∘L V - V ∘L R y) ∘L word R w := by
      simp only [word, comp_sub, sub_comp, comp_assoc]
      abel
    rw [hid]
    have hw := word_norm_le_one R hR w
    have hp := hstep y
    have ht := hT y
    calc
      _ ≤ ‖T y ∘L (word T w ∘L V - V ∘L word R w)‖ +
          ‖(T y ∘L V - V ∘L R y) ∘L word R w‖ := norm_add_le _ _
      _ ≤ ‖T y‖ * ‖word T w ∘L V - V ∘L word R w‖ +
          ‖T y ∘L V - V ∘L R y‖ * ‖word R w‖ :=
        add_le_add (opNorm_comp_le _ _) (opNorm_comp_le _ _)
      _ ≤ ((y :: w).length : ℝ) * a := by
        simp only [List.length_cons, Nat.cast_add, Nat.cast_one]
        have hfirst := mul_le_mul_of_nonneg_right ht (norm_nonneg (word T w ∘L V - V ∘L word R w))
        have hsecond := mul_le_mul_of_nonneg_left hw (norm_nonneg (T y ∘L V - V ∘L R y))
        nlinarith

/-- End-to-end formalized input to Theorem 3.1: calibrated sharp reflections
imply finite-word stability for arbitrary logical/physical Hilbert spaces.
The conclusion is proved, not included among the assumptions. -/
theorem calibrated_reflection_words (T : ι → K →L[ℂ] K) (R : ι → H →L[ℂ] H)
    (V : H →L[ℂ] K) (e : ℝ) (he : 0 ≤ e)
    (hT : ∀ y, adjoint (T y) = T y) (hTT : ∀ y, T y ∘L T y = 1)
    (hR : ∀ y, adjoint (R y) = R y) (hRR : ∀ y, R y ∘L R y = 1)
    (hV : adjoint V ∘L V = 1)
    (hcal : ∀ y, ‖adjoint V ∘L T y ∘L V - R y‖ ≤ 2 * e)
    (w : List ι) :
    ‖word T w ∘L V - V ∘L word R w‖ ≤ 2 * (w.length : ℝ) * Real.sqrt e := by
  have hRn := fun y => reflection_norm_le_one (R y) (hR y) (hRR y)
  have hTn := fun y => reflection_norm_le_one (T y) (hT y) (hTT y)
  have hs : ∀ y, ‖T y ∘L V - V ∘L R y‖ ≤ 2 * Real.sqrt e := by
    intro y
    have hd := rectangular_reflection_defect_norm_sq (T y) V (R y)
      (hT y) (hR y) (hTT y) (hRR y) hV (hRn y)
    have hc := hcal y
    nlinarith [Real.sq_sqrt he, Real.sqrt_nonneg e,
      norm_nonneg (T y ∘L V - V ∘L R y)]
  have h := word_stability T R V (2 * Real.sqrt e) hTn hRn hs w
  nlinarith

#print axioms reflection_norm_le_one
#print axioms word_norm_le_one
#print axioms word_stability
#print axioms calibrated_reflection_words

/-- Reflection associated to an actual sharp binary effect. -/
def reflection (P : H →L[ℂ] H) : H →L[ℂ] H := 2 • P - 1

theorem projection_reflection_selfadjoint (P : H →L[ℂ] H)
    (hP : adjoint P = P) : adjoint (reflection P) = reflection P := by
  simp only [reflection, two_smul, map_sub, map_add, hP, one_def, adjoint_id]

omit [CompleteSpace H] in
theorem projection_reflection_involution (P : H →L[ℂ] H)
    (hP : P * P = P) : reflection P * reflection P = 1 := by
  unfold reflection
  noncomm_ring [hP]

theorem projection_compression_calibration (Q : K →L[ℂ] K) (P : H →L[ℂ] H)
    (V : H →L[ℂ] K) (e : ℝ) (hV : adjoint V ∘L V = 1)
    (hcal : ‖adjoint V ∘L Q ∘L V - P‖ ≤ e) :
    ‖adjoint V ∘L reflection Q ∘L V - reflection P‖ ≤ 2 * e := by
  have hid : adjoint V ∘L reflection Q ∘L V - reflection P =
      (adjoint V ∘L Q ∘L V - P) + (adjoint V ∘L Q ∘L V - P) := by
    simp only [reflection, two_smul, comp_sub, sub_comp, comp_add, add_comp,
      one_def, id_comp]
    have hV' : adjoint V ∘L V = ContinuousLinearMap.id ℂ H := hV
    rw [hV']
    abel
  rw [hid]
  exact (norm_add_le _ _).trans (by linarith)

/-- A complete checked chain from independently calibrated projection effects
to finite-word stability. No commutation among the physical effects is assumed.
Physical effects are projections here; dilation of arbitrary effects is outside
this theorem's coverage and must not be inferred from its name. -/
theorem calibrated_projection_words (Q : ι → K →L[ℂ] K) (P : ι → H →L[ℂ] H)
    (V : H →L[ℂ] K) (e : ℝ) (he : 0 ≤ e)
    (hQ : ∀ y, adjoint (Q y) = Q y) (hQQ : ∀ y, Q y * Q y = Q y)
    (hP : ∀ y, adjoint (P y) = P y) (hPP : ∀ y, P y * P y = P y)
    (hV : adjoint V ∘L V = 1)
    (hcal : ∀ y, ‖adjoint V ∘L Q y ∘L V - P y‖ ≤ e)
    (w : List ι) :
    ‖word (fun y => reflection (Q y)) w ∘L V -
      V ∘L word (fun y => reflection (P y)) w‖ ≤ 2 * (w.length : ℝ) * Real.sqrt e := by
  apply calibrated_reflection_words _ _ V e he
  · exact fun y => projection_reflection_selfadjoint (Q y) (hQ y)
  · exact fun y => projection_reflection_involution (Q y) (hQQ y)
  · exact fun y => projection_reflection_selfadjoint (P y) (hP y)
  · exact fun y => projection_reflection_involution (P y) (hPP y)
  · exact hV
  · exact fun y => projection_compression_calibration (Q y) (P y) V e hV (hcal y)

#print axioms projection_reflection_selfadjoint
#print axioms projection_reflection_involution
#print axioms projection_compression_calibration
#print axioms calibrated_projection_words

end FiniteQuestionRecovery
