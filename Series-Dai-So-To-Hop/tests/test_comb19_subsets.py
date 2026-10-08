"""Independent exhaustive tests for sets and Fibonacci constraint models."""
import unittest
from itertools import combinations
from math import comb
from pathlib import Path
from comb19_lesson_data import (BEATS,CHAPTERS,FORMULAS,subset_masks,size_counts,
    distinguished,parity_sizes,nonadjacent_subsets,nonadjacent_count,endpoint_breakdown,validate)

class TestCOMB19(unittest.TestCase):
    def test_structure(self):self.assertTrue(validate())
    def test_8_chapters_48_beats(self):self.assertEqual((len(CHAPTERS),len(BEATS)),(8,48))
    def test_48_math_formulas(self):self.assertEqual((len(FORMULAS),len(set(FORMULAS))), (48,48))
    def test_minimum_runtime(self):self.assertGreaterEqual(sum(x.min_seconds for x in BEATS),1152)
    def test_speech_length(self):self.assertTrue(all(len(x.narration.split())>=50 for x in BEATS))
    def test_correct_vietnamese(self):self.assertTrue(all(any(q in x.narration for q in ('tập','phần','chọn')) for x in BEATS))
    def test_formulas_have_requested_notation(self):
        self.assertIn('C^(n)_(k)',FORMULAS['sizes_2'])
        self.assertIn('C^(n-k+1)_(k)',FORMULAS['separated_3'])
    def test_no_binom(self):self.assertNotIn('\\binom',str(FORMULAS))
    def test_set_zero(self):self.assertEqual(subset_masks(0),((),))
    def test_set_three(self):self.assertEqual(len(subset_masks(3)),8)
    def test_set_eight(self):self.assertEqual(len(set(subset_masks(8))),256)
    def test_each_subset_unique(self):
        for n in range(9):
            s=subset_masks(n)
            self.assertEqual(len(s),len(set(s)))
            self.assertEqual(len(s),2**n)
    def test_size_counts(self):
        for n in range(10):
            self.assertEqual(size_counts(n),tuple(comb(n,k) for k in range(n+1)))
    def test_power_of_two(self):
        for n in range(10):self.assertEqual(sum(size_counts(n)),2**n)
    def test_example_n5(self):self.assertEqual(size_counts(5),(1,5,10,10,5,1))
    def test_contains_A(self):self.assertEqual(distinguished(5)['contains_A'],16)
    def test_excludes_A(self):self.assertEqual(distinguished(5)['excludes_A'],16)
    def test_A_not_B(self):self.assertEqual(distinguished(5)['A_not_B'],8)
    def test_exact_one_AB(self):self.assertEqual(distinguished(5)['exact_one'],16)
    def test_at_least_one_AB(self):self.assertEqual(distinguished(5)['at_least_one'],24)
    def test_conditions_general(self):
        for n in range(2,10):
            vals=distinguished(n)
            self.assertEqual(vals['contains_A'],2**(n-1))
            self.assertEqual(vals['excludes_A'],2**(n-1))
            self.assertEqual(vals['A_not_B'],2**(n-2))
            self.assertEqual(vals['exact_one'],2**(n-1))
            self.assertEqual(vals['at_least_one'],3*2**(n-2))
    def test_parity_zero_exception(self):self.assertEqual(parity_sizes(0),(1,0))
    def test_parity_equal(self):
        for n in range(1,10):self.assertEqual(parity_sizes(n),(2**(n-1),2**(n-1)))
    def test_special_3_of_5(self):
        ss=subset_masks(5)
        self.assertEqual(sum(len(set(s)&{0,1,2})==2 for s in ss),12)
    def test_special_general(self):
        for n in range(2,8):
            for m in range(0,n+1):
                for k in range(m+1):
                    observed=sum(len(set(s)&set(range(m)))==k for s in subset_masks(n))
                    self.assertEqual(observed,comb(m,k)*2**(n-m))
    def test_nonadjacent_small(self):self.assertEqual([len(nonadjacent_subsets(n)) for n in range(7)], [1,2,3,5,8,13,21])
    def test_nonadjacent_recurrence(self):
        for n in range(2,11):self.assertEqual(nonadjacent_count(n),nonadjacent_count(n-1)+nonadjacent_count(n-2))
    def test_nonadjacent_bruteforce(self):
        for n in range(11):self.assertEqual(nonadjacent_count(n),len(nonadjacent_subsets(n)))
    def test_fixed_k_nonadjacent(self):
        for n in range(1,11):
            for k in range((n+1)//2+1):
                actual=sum(len(s)==k for s in nonadjacent_subsets(n))
                self.assertEqual(actual,comb(n-k+1,k))
    def test_n5_nonadjacent_levels(self):
        self.assertEqual(tuple(sum(len(s)==k for s in nonadjacent_subsets(5)) for k in range(4)),(1,5,6,1))
    def test_eight_positions_total(self):self.assertEqual(len(nonadjacent_subsets(8)),55)
    def test_endpoints(self):self.assertEqual(endpoint_breakdown(),(13,13,8,21))
    def test_endpoint_sum(self):
        left,right,both,neither=endpoint_breakdown()
        self.assertEqual(left+right+both,34)
        self.assertEqual(left+right+both+neither,55)
    def test_line_not_circle(self):
        self.assertTrue(any(0 in s and 7 in s for s in nonadjacent_subsets(8)))
    def test_workflow(self):
        s=(Path(__file__).resolve().parent.parent.parent / '.github/workflows/render-comb19-v2.yml').read_text(encoding='utf8')
        self.assertIn('episodes/comb19_subsets.py COMB19',s)
        self.assertIn('prepare_comb19_v2.py',s)
        self.assertIn('qa_comb19_v2.py',s)
    def test_separate_sources(self):
        self.assertTrue(Path('comb19_beats.json').exists())
        self.assertTrue(Path('comb19_formulas.json').exists())
        self.assertTrue(Path('episodes/comb18_pascal_triangle.py').exists())

if __name__=='__main__':unittest.main()
