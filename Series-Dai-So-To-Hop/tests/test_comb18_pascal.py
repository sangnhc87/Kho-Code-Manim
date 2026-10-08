"""Independent checks for Pascal, binomial identities, algebra and video structure."""
import unittest
from collections import Counter
from itertools import combinations
from math import comb
from comb18_lesson_data import (BEATS,CHAPTERS,FORMULAS,triangle,
    select_two_cases,hockey_stick,alternating_sum,odd_cells,vandermonde_splits,validate)

class TestCOMB18(unittest.TestCase):
    def test_structure(self):self.assertTrue(validate())
    def test_count(self):self.assertEqual((len(BEATS),len(CHAPTERS),len(FORMULAS)),(48,8,48))
    def test_minimum_runtime(self):self.assertGreaterEqual(sum(x.min_seconds for x in BEATS),1100)
    def test_narration_length(self):self.assertTrue(all(len(x.narration.split())>=38 for x in BEATS))
    def test_notation(self):self.assertIn('C^(n)_(k)',FORMULAS['parents_1'])
    def test_no_binomial_alias(self):self.assertNotIn('\\binom',str(FORMULAS))
    def test_row_zero(self):self.assertEqual(triangle(0),((1,),))
    def test_row_four(self):self.assertEqual(triangle(4)[4],(1,4,6,4,1))
    def test_row_six(self):self.assertEqual(triangle(6)[6],(1,6,15,20,15,6,1))
    def test_row_eight(self):self.assertEqual(triangle(8)[8],(1,8,28,56,70,56,28,8,1))
    def test_parent_rule(self):
        for n in range(2,13):
            for k in range(1,n):
                self.assertEqual(triangle(n)[n][k],triangle(n-1)[n-1][k-1]+triangle(n-1)[n-1][k])
    def test_comb_independent(self):
        for n in range(0,13):
            self.assertEqual(triangle(n)[n],tuple(comb(n,k) for k in range(n+1)))
    def test_two_cases_6_3(self):self.assertEqual(select_two_cases(6,3),(10,10))
    def test_two_cases_general(self):
        for n in range(2,9):
            for k in range(1,n):
                a,b=select_two_cases(n,k)
                self.assertEqual((a,b),(comb(n-1,k-1),comb(n-1,k)))
    def test_no_double_count(self):
        groups=list(combinations(range(6),3))
        a={g for g in groups if 0 in g};b={g for g in groups if 0 not in g}
        self.assertEqual((len(a),len(b),len(a&b),len(a|b)),(10,10,0,20))
    def test_symmetry(self):
        for n in range(1,13):self.assertEqual(tuple(reversed(triangle(n)[n])),triangle(n)[n])
    def test_sum_of_row(self):
        for n in range(0,14):self.assertEqual(sum(triangle(n)[n]),2**n)
    def test_alternating(self):
        for n in range(1,14):self.assertEqual(alternating_sum(n),0)
    def test_n0_exception(self):self.assertEqual(alternating_sum(0),1)
    def test_even_odd_32(self):
        r=triangle(6)[6];self.assertEqual(sum(r[::2]),32);self.assertEqual(sum(r[1::2]),32)
    def test_hockey_one(self):self.assertEqual(hockey_stick(2,5),comb(6,3))
    def test_hockey_two(self):self.assertEqual(hockey_stick(1,4),comb(5,2))
    def test_hockey_three(self):self.assertEqual(hockey_stick(3,7),comb(8,4))
    def test_hockey_general(self):
        for n in range(1,10):
            for k in range(n+1):self.assertEqual(hockey_stick(k,n),comb(n+1,k+1))
    def test_parity_seven(self):self.assertTrue(all((7,k) in odd_cells(8) for k in range(8)))
    def test_parity_eight(self):self.assertEqual({k for (n,k) in odd_cells(8) if n==8},{0,8})
    def test_vandermonde_terms(self):self.assertEqual(vandermonde_splits(),(1,15,30,10))
    def test_vandermonde_56(self):self.assertEqual(sum(vandermonde_splits()),comb(8,3))
    def test_vandermonde_general(self):
        for a in range(1,7):
            for b in range(1,7):
                for r in range(0,a+b+1):
                    cases=sum(comb(a,i)*comb(b,r-i) for i in range(max(0,r-b),min(r,a)+1))
                    self.assertEqual(cases,comb(a+b,r))
    def test_screen_chapter_text(self):self.assertTrue(all(len(b.lines)==3 for b in BEATS))
    def test_no_empty_explanations(self):self.assertTrue(all(b.narration.endswith(('.', '?', '!')) for b in BEATS))
    def test_formulas_present(self):self.assertEqual(len(set(b.formula for b in BEATS)),48)
    def test_expected_total_seconds(self):self.assertEqual(sum(x.min_seconds for x in BEATS)+5.2,1157.2)

if __name__=='__main__':unittest.main()
