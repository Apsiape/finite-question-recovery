# Reproducibility

Run commands from this distribution's root directory. No network access is
needed for the default snapshot verifier or source generation.

## Verify the shipped snapshot first

```text
python -B tools/check_export.py
python -B tools/test_check_lean.py
```

Requirements: Python 3.10 or newer, standard library only. The seven unit tests
exercise saved-certificate validation and synthetic rejection cases. They
do not rerun Lean. The manifest hashes the delivered artifacts; subsequent
PDF builds can differ because of TeX timestamps. Verify before rebuilding.

## Build the manuscript

```text
python -B tools/build_manuscript.py
python -B tools/build_typeset.py
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=output/pdf paper/latex/manuscript.tex
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=output/pdf paper/latex/manuscript.tex
python -B tools/build_manuscript.py --check
python -B tools/build_typeset.py --check
```

Use an installed LaTeX distribution with article, fontenc, inputenc,
Latin Modern, geometry, amsmath, amssymb, needspace and hyperref.
For MiKTeX, add `-disable-installer -disable-write18` to prevent automatic
installation and shell execution. For TeX Live, use `-no-shell-escape`.
Quote options containing `=` when forwarding them through PowerShell wrappers.
The inspected artifact was built with pdfTeX / MiKTeX 25.12 and Latin Modern.

The converter retains every source mathematical fragment verbatim and all
numbered equations. The combined manuscript includes the entire appendix.
These are fidelity checks, not proof checks.

## Inspect a rebuilt PDF

Install Pillow and pypdf in a suitable Python environment and have Poppler's
`pdftoppm` on PATH. Then run:

```text
python -B tools/qa_pdf.py
```

This extracts all theorem/appendix headings, equation labels, reference and
contact links, verifies author metadata and embedded vector fonts, checks
the compiler log and renders every page under `tmp/pdfs/`.
Inspect the resulting pages after every layout change. A successful text
check alone is not visual approval.

## Optional offline Lean rebuild

Lean **4.30.0** and dependencies at the exact revisions in
`verification/lean/lake-manifest.json` are required. With an existing compiled
Lake packages directory:

```text
python -B tools/check_lean.py --packages PATH_TO_EXISTING_LAKE_PACKAGES --timeout 170
```

The checker downloads nothing and preserves the last successful artifacts
if compilation or certificate validation fails. It requires all twelve
declarations to report exactly `propext`, `Classical.choice` and `Quot.sound`.
A new environment may require dependency installation before this command;
initial Lake dependency acquisition can access the network.

The source was previously compiled successfully at the pinned versions.
This publication-preparation pass changes no Lean source and does not
represent a new kernel run. See [coverage](verification/lean/COVERAGE.md)
for the exact mathematical boundary.

## Resource and artifact policy

Use a process memory/time limiter appropriate to your operating system.
Ordinary checks and PDF builds were run with 512 MiB / 60-second caps.
The earlier Lean rebuild used 768 MiB / 180 seconds; its inner timeout was
170 seconds. Do not retry failed bounded jobs without understanding the cause.

Track sources, generated complete Markdown/TeX, the inspected PDF, small
verification logs, dependency locks, tools, citation metadata and licenses.
Ignore TeX auxiliaries, compiled Lean objects, dependency caches and scratch
page images. No compiled `.olean` or third-party dependency is shipped.
Git attributes preserve the exact manifest, dependency-lock and saved QA
bytes; ordinary editable text uses LF line endings.

`MANIFEST.json` identifies this exact local staging snapshot, not a DOI,
Git tag or semantic release version. Public repository and archive identifiers
can be added after they actually exist.
