"""Mathematically independent tests of COMB21, no Manim needed."""
import unittest
from itertools import product
from fractions import Fraction
from math import comb
from pathlib import Path
from comb21_lesson_data import (
    BEATS, FORMULAS, CHAPTERS, convolve, geom_coeff, bound_two,
    bound_two_direct,tilings,tiled_sequences,onto,stirling2,
    exponential_product_coeff,coin_ways,coin_ways_direct,validate)

class TestCOMB21(unittest.TestCase):
    def test_lesson_valid(self):self.assertTrue(validate())
    def test_beats_chapters(self):self.assertEqual((len(CHAPTERS),len(BEATS),len(FORMULAS)),(8,48,48))
    def test_duration(self):self.assertGreaterEqual(sum(x.min_seconds for x in BEATS),1200)
    def test_vietnamese(self):self.assertTrue(all(len(x.narration.split())>=38 for x in BEATS))
    def test_unique_narration(self):self.assertEqual(len(set(x.narration for x in BEATS)),48)
    def test_formula_notation(self):self.assertIn('C^(8)_(2)',FORMULAS['stars_1'])
    def test_polynomial_product(self):self.assertEqual(convolve([1,1,1],[1,0,1]),[1,1,2,1,1])
    def test_general_product(self):
        for a in ([1],[1,2],[0,1,3],[1,0,2]):
            for b in ([1,1],[0,2],[3,0,1]):
                for n in range(len(a)+len(b)-1):
                    self.assertEqual(convolve(a,b)[n],sum(a[i]*b[n-i] for i in range(len(a)) if 0<=n-i<len(b)))
    def test_empty_product(self):self.assertEqual(convolve([],[]),[])
    def test_stars_bars(self):
        for n in range(0,9):
            for k in range(1,5):
                direct=sum(sum(items)==n for items in product(range(n+1),repeat=k))
                self.assertEqual(geom_coeff(n,k),direct)
    def test_bounded_via_direct(self):
        for n in range(26):self.assertEqual(bound_two(n),bound_two_direct(n))
    def test_bounded_zero(self):self.assertEqual(bound_two(0),1)
    def test_bounded_final(self):self.assertEqual(bound_two(12),600)
    def test_bounded_pie(self):self.assertEqual(bound_two(12),comb(16,4)-2*comb(13,4)+comb(10,4))
    def test_tiling_small(self):self.assertEqual([tilings(i) for i in range(9)],[1,1,2,3,5,8,13,21,34])
    def test_tiling_sequences(self):
        for n in range(9):self.assertEqual(len(tiled_sequences(n)),tilings(n))
    def test_onto_independent(self):
        for n in range(1,6):
            for k in range(1,5):
                brute=sum(len(set(t))==k for t in product(range(k),repeat=n))
                self.assertEqual(onto(n,k),brute)
    def test_onto_egf(self):
        for n in range(1,8):
            for k in range(1,5):self.assertEqual(exponential_product_coeff(n,k),onto(n,k))
    def test_onto_final(self):self.assertEqual(onto(4,3),36)
    def test_stirling_4_2(self):self.assertEqual(stirling2(4,2),7)
    def test_onto_zero(self):self.assertEqual(onto(0,0),1)
    def test_coin_direct(self):
        for n in range(25):self.assertEqual(coin_ways(n),coin_ways_direct(n))
    def test_coin_final(self):self.assertEqual(coin_ways(12),19)
    def test_coin_not_ordered(self):self.assertEqual(coin_ways(3),3)
    def test_invalid_arguments(self):
        calls=[(geom_coeff,(-1,2)),(geom_coeff,(1,0)),(tilings,(-1,)),
               (onto,(-1,3)),(coin_ways,(-1,)),(coin_ways,(4,(0,1))),
               (bound_two,(-1,))]
        for f,args in calls:
            with self.subTest(f=f.__name__,args=args):
                with self.assertRaises(ValueError):f(*args)
    def test_workflow(self):
        w=Path('.github/workflows/render-comb21-v2.yml').read_text()
        for s in ('prepare_comb21_v2.py','comb21_generating_functions.py COMB21','qa_comb21_v2.py','upload-artifact'):
            self.assertIn(s,w)
    def test_previous_videos(self):
        for i in range(1,21):
            self.assertTrue(any(p.name.startswith(f'comb{i:02}_') for p in Path('episodes').glob('*.py')))

if __name__=='__main__':unittest.main()
