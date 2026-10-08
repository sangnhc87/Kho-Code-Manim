"""Combinatorial proof and coefficient tests for COMB17."""
import unittest
from math import comb
from itertools import product
from comb17_lesson_data import (BEATS,FORMULAS,CHAPTERS,paths,grouped,
  binomial_coefficients,polynomial_power,product_capstone_coefficient,
  coefficient_choose_splits,validate)

class TestBinomialNewton(unittest.TestCase):
    def test_01_structure(self):self.assertTrue(validate())
    def test_02_sections(self):self.assertEqual([sum(b.section==c for b in BEATS) for c,_ in CHAPTERS],[6]*8)
    def test_03_narrations(self):self.assertTrue(all(len(b.narration.split())>=40 for b in BEATS))
    def test_04_formula_count(self):self.assertEqual(len(FORMULAS),48)
    def test_05_binary_paths(self):self.assertEqual(len(paths(2)),4)
    def test_06_cube_paths(self):self.assertEqual(len(paths(3)),8)
    def test_07_four_paths(self):self.assertEqual(len(paths(4)),16)
    def test_08_cube_groups(self):self.assertEqual(tuple(grouped(3)[i] for i in range(4)),(1,3,3,1))
    def test_09_binomial_n4(self):self.assertEqual(binomial_coefficients(4),(1,4,6,4,1))
    def test_10_binomial_n5(self):self.assertEqual(binomial_coefficients(5),(1,5,10,10,5,1))
    def test_11_choose_all(self):self.assertTrue(all(sum(binomial_coefficients(n))==2**n for n in range(0,9)))
    def test_12_independent_choose(self):self.assertTrue(all(binomial_coefficients(n)==tuple(comb(n,k) for k in range(n+1)) for n in range(9)))
    def test_13_symmetry(self):self.assertTrue(all(binomial_coefficients(n)==binomial_coefficients(n)[::-1] for n in range(9)))
    def test_14_pascal(self):self.assertTrue(all(comb(n,k)==comb(n-1,k-1)+comb(n-1,k) for n in range(2,9) for k in range(1,n)))
    def test_15_coefficient_x3(self):self.assertEqual(polynomial_power(-2,1,5)[3],40)
    def test_16_negative_sign(self):self.assertEqual(polynomial_power(1,-1,5)[3],-10)
    def test_17_harder_x3(self):self.assertEqual(polynomial_power(-1,2,6)[3],-160)
    def test_18_harder_x2(self):self.assertEqual(polynomial_power(-1,2,6)[2],60)
    def test_19_capstone_splits(self):self.assertEqual(coefficient_choose_splits(3),[(0,8),(1,48),(2,36),(3,4)])
    def test_20_capstone_sum(self):self.assertEqual(sum(v for _,v in coefficient_choose_splits(3)),96)
    def test_21_capstone_poly(self):self.assertEqual(product_capstone_coefficient(3),96)
    def test_22_capstone_other(self):self.assertEqual(product_capstone_coefficient(0),1)
    def test_23_symbol(self):self.assertIn('C^(n)_(k)',FORMULAS['theorem_3'])
    def test_24_no_binomial_alt(self):self.assertNotIn('\\binom',str(FORMULAS))

if __name__=='__main__':unittest.main()
