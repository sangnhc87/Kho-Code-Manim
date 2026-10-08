"""Independent exact checks for Episode 20. No Manim dependency."""
from fractions import Fraction
from math import comb, factorial
from pathlib import Path
import unittest
from comb20_lesson_data import (BEATS, CHAPTERS, FORMULAS, row, ordinary, alternating, parity,
    falling, weighted, power_weighted, reciprocal, partial_alternating, challenge_terms, validate)

class TestCOMB20(unittest.TestCase):
    def test_lesson_structure(self):self.assertTrue(validate())
    def test_chapters_beats(self):self.assertEqual((len(CHAPTERS),len(BEATS),len(FORMULAS)),(8,48,48))
    def test_timing(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),1200)
    def test_vietnamese_narration(self):self.assertTrue(all(len(b.narration.split())>=45 for b in BEATS))
    def test_formula_notation(self):self.assertIn('C^(n)_(k)',FORMULAS['foundation_2'])
    def test_no_tex_binom(self):self.assertNotIn('\\binom',str(FORMULAS))
    def test_row_zero(self):self.assertEqual(row(0),(1,))
    def test_row_five(self):self.assertEqual(row(5),(1,5,10,10,5,1))
    def test_ordinary(self):
        for n in range(13):self.assertEqual(ordinary(n),2**n)
    def test_alternating(self):
        self.assertEqual(alternating(0),1)
        for n in range(1,13):self.assertEqual(alternating(n),0)
    def test_parity(self):
        self.assertEqual(parity(0),(1,0))
        for n in range(1,13):self.assertEqual(parity(n),(2**(n-1),)*2)
    def test_weighted_k_independent(self):
        for n in range(1,12):self.assertEqual(weighted(n,1),n*2**(n-1))
    def test_falling_weights(self):
        for k in range(8):
            for r in range(8):self.assertEqual(falling(k,r),factorial(k)//factorial(k-r) if k>=r else 0)
    def test_mark_two(self):
        for n in range(2,12):self.assertEqual(weighted(n,2),n*(n-1)*2**(n-2))
    def test_k_square(self):
        for n in range(1,12):self.assertEqual(power_weighted(n,2),n*(n+1)*2**(n-2))
    def test_k_cubed(self):
        for n in range(3,12):self.assertEqual(power_weighted(n,3),n*n*(n+3)*2**(n-3))
    def test_k_cubed_falling(self):
        for k in range(17):self.assertEqual(k**3,falling(k,3)+3*falling(k,2)+k)
    def test_general_marked(self):
        for n in range(2,10):
            for r in range(n+1):self.assertEqual(weighted(n,r),falling(n,r)*2**(n-r))
    def test_general_ab(self):
        for n in range(2,9):
            for a,b in [(2,3),(3,2),(1,4),(0,2)]:
                self.assertEqual(weighted(n,1,a,b),n*b*(a+b)**(n-1))
    def test_reciprocal_fraction(self):
        for n in range(11):self.assertEqual(reciprocal(n),Fraction(2**(n+1)-1,n+1))
    def test_reciprocal_example(self):self.assertEqual(reciprocal(3),Fraction(15,4))
    def test_partial_alternating(self):
        for n in range(1,13):
            for r in range(n):self.assertEqual(partial_alternating(n,r),(-1)**r*comb(n-1,r))
    def test_partial_total(self):
        for n in range(1,13):self.assertEqual(partial_alternating(n,n),0)
    def test_partial_example(self):self.assertEqual(partial_alternating(6,3),-10)
    def test_invalid(self):
        for f,args in [(row,(-1,)),(falling,(2,-1)),(weighted,(-1,2)),(partial_alternating,(3,4))]:
            with self.assertRaises(ValueError):f(*args)
    def test_challenge_terms_exact(self):
        expected=[(k,k*k*comb(6,k)*2**k*3**(6-k)) for k in range(7)]
        self.assertEqual(list(challenge_terms()),expected)
    def test_challenge_total(self):self.assertEqual(sum(v for _,v in challenge_terms()),112500)
    def test_challenge_two_derivatives(self):self.assertEqual(weighted(6,1,3,2)+weighted(6,2,3,2),112500)
    def test_workflow_exists(self):
        content=Path('.github/workflows/render-comb20-v2.yml').read_text(encoding='utf8')
        for needle in ('comb20_binomial_sums.py COMB20','prepare_comb20_v2.py','qa_comb20_v2.py','upload-artifact'):
            self.assertIn(needle,content)
    def test_series_preserved(self):
        for i in range(1,20):
            self.assertTrue(any(p.name.startswith(f'comb{i:02}_') for p in Path('episodes').glob('*.py')))

if __name__=='__main__':unittest.main()
