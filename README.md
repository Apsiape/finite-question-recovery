# Quantum recovery from finitely many sharp questions

Seth Douglas · [seth.douglas@gmail.com](mailto:seth.douglas@gmail.com)

This paper studies when approximate recovery of finitely many sharp binary
observables guarantees recovery of the entire quantum input. It proves
matching fixed-gap minimax bounds, separates positive-word certificate cost
from achievable recovery, and constructs uniform and coherent-tester decoders
under explicitly stated access assumptions.

## Read the paper

- [Complete PDF](output/pdf/manuscript.pdf)
- [Complete Markdown](paper/manuscript-complete.md)
- [Main source](paper/manuscript.md), [Appendix A](paper/appendix-qubit.md),
  and [standalone LaTeX](paper/latex/manuscript.tex)

The PDF includes all proofs and Appendix A. The mathematical source files
are authoritative; the combined Markdown and TeX are generated from them.

## Reproduce and verify

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for portable build commands,
dependencies, resource guidance, PDF inspection and offline Lean checks.
For the shipped snapshot, run:

```text
python -B tools/check_export.py
```

This verifies the exact-byte manifest, source/TeX correspondence, citation
metadata, local links, license scope and the saved twelve-declaration Lean
axiom certificate. It does not rerun the Lean kernel or certify the paper's
analytic proofs.

Lean coverage is **partial**. The code formalizes calibrated projections
implying finite-word operator-norm stability. No numbered recovery theorem
is fully formalized. Read the [coverage matrix](verification/lean/COVERAGE.md).

## Citation and licenses

Suggested citation: Seth Douglas, *Quantum recovery from finitely many sharp
questions*, manuscript, 2026. Machine-readable metadata is provided in
[CITATION.cff](CITATION.cff). The initial public release is version 1.0.0;
its DOI will be added after assignment. [Zenodo metadata guidance](zenodo/README.md)
explains the preprint classification and scoped mixed-license description.

The manuscript is **CC BY 4.0**; original code and accompanying software
documentation are **MIT**. See [LICENSE.md](LICENSE.md) for exact file scope
and both complete license texts. Dependencies retain their own licenses.

## Research disclosure

Language models assisted proof exploration, refutation-oriented checking
and editorial assembly. Independent AI sessions are not human external
peer review or formal proof certification. The human author retains
responsibility for the claims. The paper contains the complete disclosure.
