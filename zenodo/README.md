# Zenodo metadata preparation

[metadata-template.json](metadata-template.json) provides descriptive fields
for a manuscript-preprint record. It is a manual-entry reference, not an
automatically imported GitHub metadata file or a complete API deposit request.
No DOI, release version, public URL or publication date is invented.

Use a **manual draft deposit** for this combined package. Before publishing,
declare **both CC-BY-4.0 and MIT** in its license selection and explain their file scopes using
[LICENSE.md](../LICENSE.md): manuscript/TeX/PDF under CC BY 4.0, original code
and accompanying software documentation under MIT. Verify the displayed
metadata before publishing. This mixed-license package does not require
two separate records or two DOIs.

Do not enable GitHub-triggered automatic publication until mixed-license
ingestion has been verified: a tag-triggered integration may publish before
there is an opportunity to inspect a draft.

There is deliberately no root `.zenodo.json` with a blanket scalar license.
Automatic import of that field could misrepresent the scoped split.
Use Zenodo's [mixed-license upload guidance](https://help.zenodo.org/docs/deposit/describe-records/licenses/#mixed-license-uploads).
