"""Verify a shipped public snapshot without network access or a Lean rebuild."""
import fnmatch
import hashlib
import json
from pathlib import Path
import re
from build_typeset import build as build_tex
from build_manuscript import build as build_markdown
from check_lean import validate_output

ROOT = Path(__file__).resolve().parents[1]


def main():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text(encoding='utf-8'))
    assert manifest['author'] == {'name': 'Seth Douglas', 'email': 'seth.douglas@gmail.com'}
    assert manifest['licenses'] == {'manuscript': 'CC-BY-4.0', 'code': 'MIT'}
    expected = {'MANIFEST.json'}
    for row in manifest['files']:
        relative = Path(row['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        path = ROOT / relative
        assert path.stat().st_size == row['bytes'] <= 8 * 1024 * 1024
        assert hashlib.sha256(path.read_bytes()).hexdigest().upper() == row['sha256']
        assert relative.as_posix() not in expected, 'Duplicate manifest entry'
        expected.add(relative.as_posix())
    # Permit only documented local build products beyond the delivered snapshot.
    ignored = ['*.pyc', '*.aux', '*.log', '*.out', '*.toc', '*.synctex.gz',
               '*.fls', '*.fdb_latexmk', '*.olean', '*.ilean', '*.trace']
    extras = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()} - expected
    for name in extras:
        assert name.startswith(('tmp/', '.git/', 'verification/lean/.lake/')) or any(
            fnmatch.fnmatch(name, pattern) for pattern in ignored), f'Unexpected public file: {name}'
    assert not any(name.startswith(('sources/', 'reviews/', 'audit/')) for name in expected)
    main_text = (ROOT / 'paper/manuscript.md').read_text(encoding='utf-8')
    assert 'Seth Douglas — working manuscript, 15 September 2026' in main_text
    assert 'Contact: [seth.douglas@gmail.com](mailto:seth.douglas@gmail.com)' in main_text
    assert 'Creative Commons Attribution 4.0 International' in main_text
    assert 'final author approval remain on hold' not in main_text
    assert 'awaits final author' not in main_text
    tex, math_count, tag_count = build_tex()
    assert (ROOT / 'paper/latex/manuscript.tex').read_text(encoding='utf-8') == tex
    assert (ROOT / 'paper/manuscript-complete.md').read_text(encoding='utf-8') == build_markdown()
    lean = ROOT / 'verification/lean'
    validate_output((lean / 'kernel-check.txt').read_text(encoding='utf-8'),
                    (lean / 'FiniteQuestionRecovery.lean').read_text(encoding='utf-8'))
    citation = json.loads((ROOT / 'CITATION.cff').read_text(encoding='utf-8'))
    author = [{'family-names': 'Douglas', 'given-names': 'Seth', 'email': 'seth.douglas@gmail.com'}]
    assert citation['cff-version'] == '1.2.0' and citation['authors'] == author
    assert citation['preferred-citation']['authors'] == author
    assert citation['title'] == citation['preferred-citation']['title'] == main_text.splitlines()[0][2:]
    assert citation['license'] == ['CC-BY-4.0', 'MIT']
    assert not ({'doi', 'version', 'date-released', 'url', 'repository-code'} & citation.keys())
    release = json.loads((ROOT / '.zenodo.json').read_text(encoding='utf-8'))
    assert release['license'] == 'other-open'
    assert release['title'] == citation['title']
    assert release['creators'] == [{'name': 'Douglas, Seth'}]
    assert release['upload_type'] == 'publication' and release['publication_type'] == 'preprint'
    assert all(term in release['description'] for term in ['CC-BY-4.0', 'MIT', 'partial'])
    zenodo = json.loads((ROOT / 'zenodo/metadata-template.json').read_text(encoding='utf-8'))
    assert zenodo['upload_type'] == 'publication' and zenodo['publication_type'] == 'preprint'
    assert zenodo['title'] == citation['title']
    assert zenodo['creators'] == [{'name': 'Douglas, Seth'}]
    assert 'license' not in zenodo and 'licenses' not in zenodo
    assert 'MIT' in zenodo['description'] and 'partial' in zenodo['description']
    assert not ({'doi', 'version', 'publication_date', 'related_identifiers'} & zenodo.keys())
    guidance = (ROOT / 'zenodo/README.md').read_text(encoding='utf-8')
    assert 'CC-BY-4.0' in guidance and 'MIT' in guidance and 'Other (Open)' in guidance
    for name in expected:
        path = ROOT / name
        if path.suffix in {'.md', '.py', '.tex', '.lean', '.json', '.cff', '.toml', '.txt'}:
            text = path.read_text(encoding='utf-8')
            assert not re.search(r'[A-Z]:[/\\](?:Infanox|Users)', text), f'Machine path: {name}'
            assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', text), f'Control character: {name}'
            assert all(line == line.rstrip() for line in text.splitlines()), f'Whitespace: {name}'
        if path.suffix == '.md':
            for target in re.findall(r'\]\(([^)]+)\)', text):
                if '://' not in target and not target.startswith(('#', 'mailto:')):
                    assert (path.parent / target.split('#')[0]).exists(), f'Broken link: {name} -> {target}'
    pdf_hash = hashlib.sha256((ROOT / 'output/pdf/manuscript.pdf').read_bytes()).hexdigest().upper()
    qa = (ROOT / 'output/pdf/qa-check.txt').read_text(encoding='utf-8')
    assert 'PDF SHA-256: ' + pdf_hash in qa, 'Stale PDF QA record'
    print(f'PASS: {len(expected)-1} exact artifact hashes; licenses; author/citation metadata; public paths and local links.')
    print(f'PASS: {math_count} preserved math fragments; {tag_count} equation tags; complete source/TeX; twelve saved axiom reports.')
    print('LIMIT: this does not rerun the Lean kernel or certify analytic proofs, novelty or publication.')


if __name__ == '__main__':
    main()
