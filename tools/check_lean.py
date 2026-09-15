"""Check Lean with an existing dependency cache; preserve last success on failure."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = (
    'reflection_defect_identity', 'reflection_defect_norm_sq',
    'rectangular_reflection_defect_identity', 'rectangular_reflection_defect_norm_sq',
    'reflection_norm_le_one', 'word_norm_le_one', 'word_stability',
    'calibrated_reflection_words', 'projection_reflection_selfadjoint',
    'projection_reflection_involution', 'projection_compression_calibration',
    'calibrated_projection_words',
)
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}


def validate_output(output, source):
    """Require every advertised certificate, not merely successful compilation."""
    if re.search(r'\b(sorry|admit|axiom)\b', source):
        raise ValueError('Forbidden proof escape in source')
    if 'sorryAx' in output:
        raise ValueError('Kernel output contains an admitted proof')
    printed = re.findall(r'^#print axioms (\w+)\s*$', source, re.M)
    if len(printed) != len(EXPECTED) or set(printed) != set(EXPECTED):
        raise ValueError('Missing, duplicate or unexpected source axiom request')
    reports = re.findall(r"'FiniteQuestionRecovery\.(\w+)' depends on axioms:\s*\[([^\]]*)\]", output)
    if len(reports) != len(EXPECTED) or {name for name, _ in reports} != set(EXPECTED):
        raise ValueError('Missing, duplicate or unexpected kernel axiom report')
    for name, items in reports:
        axioms = [item.strip() for item in items.split(',') if item.strip()]
        if len(axioms) != len(ALLOWED_AXIOMS) or set(axioms) != ALLOWED_AXIOMS:
            raise ValueError(f'Unexpected axiom set for {name}: {axioms}')
    remainder = re.sub(r"'FiniteQuestionRecovery\.\w+' depends on axioms:\s*\[[^\]]*\]", '', output)
    if remainder.strip():
        raise ValueError('Unexpected diagnostic text in kernel output')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packages', required=True, type=Path)
    parser.add_argument('--timeout', type=int, default=170)
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    paths = sorted(str(p / '.lake/build/lib/lean') for p in args.packages.iterdir()
                   if p.is_dir() and (p / '.lake/build/lib/lean').is_dir())
    if not paths:
        raise ValueError('No installed package oleans found')
    source_path = ROOT / 'verification/lean/FiniteQuestionRecovery.lean'
    source = source_path.read_text(encoding='utf-8')
    env = dict(os.environ, LEAN_PATH=os.pathsep.join(paths))
    scratch = ROOT / 'tmp'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='lean-check-', dir=scratch) as directory:
        compiled = Path(directory) / 'FiniteQuestionRecovery.olean'
        result = subprocess.run(['lean', '-o', str(compiled), str(source_path)],
                                cwd=source_path.parent, env=env, text=True, capture_output=True,
                                encoding='utf-8', timeout=args.timeout)
        output = result.stdout + result.stderr
        print(output, end='')
        if result.returncode:
            raise RuntimeError(f'Lean exited {result.returncode}; previous success artifacts preserved')
        validate_output(output, source)
        if not compiled.is_file():
            raise ValueError('Lean did not produce the compiled artifact')
        compiled.replace(source_path.with_suffix('.olean'))
        log = Path(directory) / 'kernel-check.txt'
        log.write_text(output, encoding='utf-8', newline='\n')
        log.replace(source_path.parent / 'kernel-check.txt')
    print(f'PASS: all {len(EXPECTED)} declarations; exact approved axiom sets. Coverage remains PARTIAL.')


if __name__ == '__main__':
    main()
