"""Checks that run without Manim, Typst or network, on every produced Short."""
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from common import shortlib, voice  # noqa: E402
from scripts.finalize import metadata  # noqa: E402

STANDARD = {'hook', 'guess', 'answer', 'outro'}


class Shorts(unittest.TestCase):
    def test_problem_lines_fit(self):
        import subprocess
        out = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'wrap_problems.py'), '--check'],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout)

    def test_each_short(self):
        made = shortlib.produced()
        self.assertTrue(made)
        for code in made:
            with self.subTest(short=code):
                mod = shortlib.load(code)  # answer must equal the verified plan
                src = (ROOT / 'xss' / f'{code}.py').read_text('utf-8')
                n = int(code[3:])
                self.assertIn(f'N = {n}\n', src)
                self.assertNotRegex(src, r'self\.paths\b', 'self.paths belongs to ShortScene (file locations)')
                self.assertNotIn('shift=[', src, 'FadeIn(shift=[...]) breaks: a list times 0 becomes []')
                for b in mod.BEATS:
                    if b.id not in STANDARD:
                        self.assertRegex(src, rf'def beat_{b.id}\(self, T\)')
                    self.assertGreaterEqual(len(b.text.split()), 6, b.id)
                    self.assertNotRegex(b.text, r'[=√∫]', 'narration must be spoken words')
                if hasattr(mod, 'OPTIONS'):
                    self.assertEqual(mod.FORMULAS[f'opt{mod.CORRECT}'], mod.FORMULAS['answer'])
                used = set(re.findall(r"self\.M\('([A-Za-z0-9_]+)'", src)) | {'answer'} | \
                    {k for k in mod.FORMULAS if k.startswith('opt')}
                self.assertEqual(set(mod.FORMULAS) - used, set(), 'unused formulas')
                self.assertTrue(used <= set(mod.FORMULAS), used - set(mod.FORMULAS))
                total = sum(voice.estimate(b.text)[0] + voice.LEAD + voice.PAD for b in mod.BEATS)
                self.assertLess(total, 170, 'a Short must stay under 3 minutes')
                self.assertLessEqual(len(metadata(n)['title']), 100)


if __name__ == '__main__':
    unittest.main()
