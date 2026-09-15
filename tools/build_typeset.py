"""Deterministic conservative Markdown-to-LaTeX conversion for this manuscript.

Math fragments are copied verbatim. The sole table becomes a sequence of
theorem-map entries so its long formulas remain readable at normal type size.
No external converter or network package installation is used.
"""
from pathlib import Path
import argparse
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'paper/latex/manuscript.tex'

def prose(s):
    tokens = []
    def keep(value):
        tokens.append(value)
        return f'ZZTOKEN{len(tokens)-1}ZZ'
    s = re.sub(r'\\\(.*?\\\)', lambda m: keep(m[0]), s, flags=re.S)
    s = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',
               lambda m: keep('\\href{' + m[2].replace('%', r'\%') + '}{' + prose(m[1]) + '}'), s)
    s = re.sub(r'`([^`]+)`', lambda m: keep(r'\texttt{' + prose(m[1]) + '}'), s)
    s = s.replace('\\', r'\textbackslash{}')
    for char, replacement in [('&', r'\&'), ('%', r'\%'), ('#', r'\#'), ('_', r'\_')]:
        s = s.replace(char, replacement)
    s = s.replace('∎', r'\hfill\(\square\)').replace('—', '---').replace('–', '--')
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s, flags=re.S)
    s = re.sub(r'\*([^*]+)\*', r'\\emph{\1}', s, flags=re.S)
    for i, token in enumerate(tokens):
        s = s.replace(f'ZZTOKEN{i}ZZ', token)
    return s

def convert(text):
    lines = text.splitlines()
    result = []
    i = 0
    in_list = False
    while i < len(lines):
        line = lines[i]
        if line == '## References':
            result.append(r'\begin{thebibliography}{SBWS18}\raggedright')
            i += 1
            while i < len(lines) and not lines[i].startswith('#'):
                if not lines[i].strip():
                    i += 1
                    continue
                entry = re.fullmatch(r'- \[([A-Z][A-Za-z0-9]*)\] (.*)', lines[i])
                assert entry, f'Unexpected bibliography line: {lines[i]}'
                key, first = entry.groups()
                paragraph = [first]
                i += 1
                while i < len(lines) and lines[i].startswith('  '):
                    paragraph.append(lines[i].strip()); i += 1
                result.append(r'\bibitem[' + key + ']{' + key + '} ' + prose(' '.join(paragraph)))
            result.append(r'\end{thebibliography}')
            continue
        if line == r'\[':
            block = [line]
            i += 1
            while i < len(lines) and lines[i] != r'\]':
                block.append(lines[i]); i += 1
            assert i < len(lines), 'Unclosed display equation'
            result.append('\n'.join(block + [lines[i]])); i += 1
            continue
        if line.startswith('|'):
            rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([x.strip() for x in lines[i].strip('|').split('|')]); i += 1
            headers = rows[0]
            result.append(r'\begin{description}')
            for row in rows[2:]:
                assert len(row) == len(headers)
                result.append(r'\item[' + prose(row[0]) + '] ' +
                    '; '.join(prose(headers[j]) + ': ' + prose(row[j]) for j in range(1, len(row))) + '.')
            result.append(r'\end{description}')
            continue
        if line.startswith('- '):
            if not in_list:
                result.append(r'\begin{itemize}\raggedright'); in_list = True
            paragraph = [line[2:]]; i += 1
            while i < len(lines) and lines[i].startswith('  '):
                paragraph.append(lines[i].strip()); i += 1
            result.append(r'\item{} ' + prose(' '.join(paragraph)))
            continue
        if in_list:
            result.append(r'\end{itemize}'); in_list = False
        if line.startswith('# Appendix A.'):
            result.append(r'\clearpage\section*{' + prose(line[2:]) + '}')
        elif line.startswith('### '):
            result.append(r'\Needspace{9\baselineskip}\subsection*{' + prose(line[4:]) + '}')
        elif line.startswith('## '):
            result.append(r'\Needspace{9\baselineskip}\section*{' + prose(line[3:]) + '}')
        elif line == '':
            result.append('')
        else:
            paragraph = [line]; i += 1
            while i < len(lines) and lines[i] and not lines[i].startswith(('#', '|', '- ', r'\[')):
                paragraph.append(lines[i]); i += 1
            result.append(prose('\n'.join(paragraph)))
            continue
        i += 1
    if in_list:
        result.append(r'\end{itemize}')
    return '\n'.join(result)

def build():
    main_text = (ROOT / 'paper/manuscript.md').read_text(encoding='utf-8')
    appendix = (ROOT / 'paper/appendix-qubit.md').read_text(encoding='utf-8')
    # Derive the complete masthead from source; do not silently drop its edition note.
    masthead = main_text[:main_text.index('## Abstract')].splitlines()
    title = masthead[0].removeprefix('# ')
    author, date = masthead[2].split(' — working manuscript, ', 1)
    contact = next(line for line in masthead if line.startswith('Contact: '))
    match = re.fullmatch(r'Contact: \[([^\]]+)\]\(mailto:([^\)]+)\)', contact)
    assert match and match[1] == match[2], 'Malformed author contact'
    email = match[1]
    assert re.fullmatch(r'[A-Za-z0-9.+_-]+@[A-Za-z0-9.-]+', email), 'Invalid contact email'
    note = '\n'.join(line for line in masthead[3:] if line != contact).strip()
    body = main_text[main_text.index('## Abstract'):]
    tex = r'''\documentclass[11pt]{article}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage{lmodern}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{needspace}
\usepackage{hyperref}
\hypersetup{hidelinks,pdftitle={TITLECONTENT},pdfauthor={AUTHORCONTENT},pdfsubject={Contact: EMAILCONTENT}}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt}
\setlength{\emergencystretch}{3em}
\allowdisplaybreaks
\title{TITLECONTENT}
\author{AUTHORCONTENT\\\small\href{mailto:EMAILCONTENT}{\texttt{EMAILCONTENT}}}
\date{DATECONTENT}
\begin{document}
\maketitle
'''
    tex = tex.replace('TITLECONTENT', prose(title)).replace('AUTHORCONTENT', prose(author))
    tex = tex.replace('EMAILCONTENT', email)
    tex = tex.replace('DATECONTENT', prose(date))
    tex += convert(note) + '\n\n' + convert(body) + '\n\n' + convert(appendix) + '\n\\end{document}\n'
    source_math = re.findall(r'\\\[(.*?)\\\]|\\\((.*?)\\\)', body + '\n' + appendix, re.S)
    output_math = re.findall(r'\\\[(.*?)\\\]|\\\((.*?)\\\)', tex, re.S)
    # Only generated QED squares may be additional math; every source fragment must survive.
    from collections import Counter
    missing = Counter(source_math) - Counter(output_math)
    assert not missing, f'Mathematical fragments changed or omitted: {missing}'
    source_tags = re.findall(r'\\tag\{([^}]+)\}', body + appendix)
    assert source_tags == re.findall(r'\\tag\{([^}]+)\}', tex)
    assert 'Creative Commons Attribution 4.0 International' in tex
    assert 'final author approval remain on hold' not in tex
    return tex, len(source_math), len(source_tags)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    tex, math_count, tag_count = build()
    if args.check:
        if OUT.read_text(encoding='utf-8') != tex:
            raise ValueError('LaTeX is stale relative to both authoritative Markdown sources')
    else:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        (ROOT / 'output/pdf').mkdir(parents=True, exist_ok=True)
        OUT.write_text(tex, encoding='utf-8', newline='\n')
    print(f'PASS: {math_count} verbatim math fragments; {tag_count} equation tags; complete Appendix A and masthead.')
    print('LaTeX SHA256 ' + hashlib.sha256(OUT.read_bytes()).hexdigest().upper())

if __name__ == '__main__':
    main()
