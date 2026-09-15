"""Focused negative tests for the certificate gate; no Lean rebuild."""
import unittest
from check_lean import ROOT, validate_output


class CertificateGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'verification/lean/FiniteQuestionRecovery.lean').read_text(encoding='utf-8')
        cls.output = (ROOT / 'verification/lean/kernel-check.txt').read_text(encoding='utf-8')

    def test_actual_certificate(self):
        validate_output(self.output, self.source)

    def test_scientific_axiom_rejected(self):
        with self.assertRaises(ValueError):
            validate_output(self.output.replace('Quot.sound', 'inventedRecovery', 1), self.source)

    def test_missing_headline_rejected(self):
        with self.assertRaises(ValueError):
            validate_output('\n'.join(line for line in self.output.splitlines()
                                     if 'calibrated_projection_words' not in line), self.source)

    def test_duplicate_report_rejected(self):
        with self.assertRaises(ValueError):
            validate_output(self.output + self.output.splitlines()[0] + '\n', self.source)

    def test_admission_rejected(self):
        with self.assertRaises(ValueError):
            validate_output(self.output.replace('Quot.sound', 'sorryAx', 1), self.source)

    def test_missing_print_request_rejected(self):
        with self.assertRaises(ValueError):
            validate_output(self.output, self.source.replace('#print axioms calibrated_projection_words', ''))

    def test_unexpected_diagnostic_rejected(self):
        with self.assertRaises(ValueError):
            validate_output(self.output + '\nwarning: synthetic diagnostic', self.source)


if __name__ == '__main__':
    unittest.main()
