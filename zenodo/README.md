# Zenodo release metadata

The root [.zenodo.json](../.zenodo.json) describes this package as a preprint
and overrides CITATION.cff during GitHub release ingestion. The importer accepts
one license category, so it uses **Other (Open)** for this mixed-license archive.
Its description and notes explicitly specify **CC-BY-4.0** for the manuscript
and **MIT** for original code and accompanying software documentation.
[LICENSE.md](../LICENSE.md) and the complete license texts govern each file.
This category does not replace those licenses or dual-license every file.

After ingestion, verify the record's title, author, resource type and license
description. Zenodo's editor can also display both scoped license entries:
[mixed-license upload guidance](https://help.zenodo.org/docs/deposit/describe-records/licenses/#mixed-license-uploads).
No DOI is supplied before Zenodo assigns it. The publication date is assigned
by ingestion. The older [metadata-template.json](metadata-template.json) remains
a descriptive manual-entry reference, not an API request.
