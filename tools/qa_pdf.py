"""Bounded PDF extraction and page contact sheets; run with bundled Python."""
from pathlib import Path
import hashlib
import re
import subprocess
from PIL import Image, ImageDraw
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
pdf = ROOT / 'output/pdf/manuscript.pdf'
folder = ROOT / 'tmp/pdfs' / hashlib.sha256(pdf.read_bytes()).hexdigest()[:12]
folder.mkdir(parents=True, exist_ok=True)
reader = PdfReader(pdf)
text = '\n'.join(page.extract_text() or '' for page in reader.pages)
assert len(reader.pages) >= 10
assert 'A.15' in text and 'A.1' in text and '7.2' in text
assert all((page.extract_text() or '').strip() for page in reader.pages)
normalized = re.sub(r'\s+', ' ', text)
source = (ROOT / 'paper/manuscript.md').read_text(encoding='utf-8')
title = source.splitlines()[0].removeprefix('# ')
author = source.splitlines()[2].split(' — working manuscript, ', 1)[0]
assert reader.metadata.title == title and reader.metadata.author == author
email = re.search(r'^Contact: \[([^\]]+)\]', source, re.M)[1]
assert reader.metadata.subject == 'Contact: ' + email
assert email in normalized
assert 'Creative Commons Attribution 4.0 International' in normalized
assert 'Publication and final author approval remain on hold' not in normalized
for heading in ['Theorem 3.1', 'Corollary 3.2', 'Theorem 4.1', 'Corollary 4.2',
                'Theorem 5.1', 'Theorem 5.2', 'Proposition 5.3', 'Theorem 6.1',
                'Lemma 7.1', 'Theorem 7.2', 'References', 'Acknowledgements and disclosure',
                'Appendix A.', 'A.1.', 'A.2.', 'A.3.', 'A.4.', 'A.5.']:
    assert heading in normalized, f'Missing PDF heading: {heading}'
keys = re.findall(r'^- \[([A-Z][A-Za-z0-9]*)\]', source, re.M)
assert all('[' + key + ']' in normalized for key in keys), 'Missing bibliography key'
uris = set()
for page in reader.pages:
    for annotation in page.get('/Annots', []):
        action = annotation.get_object().get('/A')
        if action and action.get('/URI'):
            uris.add(str(action['/URI']))
    for resource in page['/Resources'].get('/Font', {}).values():
        font = resource.get_object()
        assert font.get('/Subtype') != '/Type3', 'Bitmap font in PDF'
        descriptor = font.get('/FontDescriptor')
        assert descriptor is not None, 'Font lacks embedded descriptor'
        assert any(k in descriptor.get_object() for k in ['/FontFile', '/FontFile2', '/FontFile3'])
expected_uris = set(re.findall(r'\]\((https?://[^)]+)\)', source))
expected_uris.add('mailto:' + email)
assert expected_uris <= uris, f'Missing PDF link targets: {expected_uris - uris}'
tags = re.findall(r'\\tag\{([^}]+)\}', (ROOT / 'paper/latex/manuscript.tex').read_text(encoding='utf-8'))
assert all('(' + tag + ')' in text for tag in tags), [t for t in tags if '(' + t + ')' not in text]
log = (ROOT / 'output/pdf/manuscript.log').read_text(encoding='utf-8', errors='replace')
assert not any(w in log for w in ['Overfull', 'undefined references', 'Missing character:', 'LaTeX Warning:'])
subprocess.run(['pdftoppm', '-scale-to', '1500', '-png', str(pdf), str(folder / 'page')], check=True, timeout=45)
pages = sorted(folder.glob('page-*.png'))
assert len(pages) == len(reader.pages)
for first in range(0, len(pages), 6):
    sheet = Image.new('RGB', (1530, 2050), 'white')
    draw = ImageDraw.Draw(sheet)
    for offset, path in enumerate(pages[first:first+6]):
        im = Image.open(path).convert('RGB')
        im.thumbnail((500, 970))
        x, y = (offset % 3) * 510, (offset // 3) * 1025
        sheet.paste(im, (x, y + 30))
        draw.text((x+10,y+10), f'Page {first+offset+1}', fill='black')
    sheet.save(folder / f'contact-{first//6+1}.png')
report = (f'PASS: {len(reader.pages)} nonempty PDF pages; all {len(tags)} equation tags, '
          f'{len(keys)} reference entries and {len(expected_uris)} reference/contact link targets extracted.\n'
          'PASS: all theorem/appendix headings, title/author/contact metadata, manuscript license, embedded vector fonts; no missing glyphs, overfull boxes or LaTeX warnings.\n'
          f'PDF SHA-256: {hashlib.sha256(pdf.read_bytes()).hexdigest().upper()}\n'
          f'Rendered pages: tmp/pdfs/{folder.name}\nVisual review is separately required.\n')
(ROOT / 'output/pdf/qa-check.txt').write_text(report, encoding='utf-8')
print(report)
