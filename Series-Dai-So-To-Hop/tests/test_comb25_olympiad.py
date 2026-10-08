"""Pure Python verification of Burnside, Pólya, weighted orbit counts and DFT filtering."""
import unittest
from math import comb
from collections import Counter
from comb25_lesson_data import (
  BEATS,FORMULAS,CHAPTERS,CHAPTER_LABELS,validate,
  ring_permutations,cycles,fixed_colorings,orbit_count_formula,
  orbit_count_enumerated,cube_rotations,residue_choose,cycle_class_counts)

class TestComb25(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_beats(self):self.assertEqual(len(BEATS),48)
    def test_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_formula_count(self):self.assertEqual(len(FORMULAS),48)
    def test_long_narrations(self):self.assertTrue(all(len(b.narration.split())>37 for b in BEATS))
    def test_exact_six_beats_per_chapter(self):
        for chapter,_ in CHAPTERS:self.assertEqual(sum(x.section==chapter for x in BEATS),6)
    def test_independent_not_empty(self):
        for b in BEATS:self.assertTrue(b.takeaway and all(b.lines) and FORMULAS[b.formula])
    def test_identity_perm_cycles(self):self.assertEqual(cycles(tuple(range(6))),[1]*6)
    def test_reflection_permutation_cycle_types(self):
        p=ring_permutations(6,True)
        self.assertEqual(len(p),12)
        self.assertEqual(Counter(tuple(cycles(x)) for x in p[6:]),Counter({(1,1,2,2):3,(2,2,2):3}))
    def test_necklace_6_two_colors_formula(self):self.assertEqual(orbit_count_formula(ring_permutations(6),2),14)
    def test_necklace_6_two_colors_independent(self):self.assertEqual(orbit_count_enumerated(ring_permutations(6),2),14)
    def test_bracelet_6_two_colors_formula(self):self.assertEqual(orbit_count_formula(ring_permutations(6,True),2),13)
    def test_bracelet_6_independent(self):self.assertEqual(orbit_count_enumerated(ring_permutations(6,True),2),13)
    def test_necklace_weight_3(self):self.assertEqual(orbit_count_formula(ring_permutations(6),2,3),4)
    def test_weight_3_independent(self):self.assertEqual(orbit_count_enumerated(ring_permutations(6),2,3),4)
    def test_square_three_colors_rotations(self):self.assertEqual(orbit_count_formula(ring_permutations(4),3),24)
    def test_square_three_colors_mirrors(self):self.assertEqual(orbit_count_formula(ring_permutations(4,True),3),21)
    def test_square_independent(self):
        for refl,ans in ((False,24),(True,21)):
            self.assertEqual(orbit_count_enumerated(ring_permutations(4,refl),3),ans)
    def test_square_dihedral_cycle_index(self):
        self.assertEqual(Counter(tuple(cycles(x)) for x in ring_permutations(4,True)),
             Counter({(1,1,1,1):1,(1,1,2):2,(2,2):3,(4,):2}))
    def test_roots_sum(self):self.assertEqual(residue_choose(9,3),170)
    def test_roots_general_mod(self):
        for n in range(15):
            for m in (2,3,4,5):
                for r in range(m):
                    self.assertEqual(residue_choose(n,m,r),sum(comb(n,k) for k in range(n+1) if k%m==r))
    def test_weighted_8_four_rot(self):self.assertEqual(orbit_count_formula(ring_permutations(8),2,4),10)
    def test_weighted_8_four_refl(self):self.assertEqual(orbit_count_formula(ring_permutations(8,True),2,4),8)
    def test_weighted_8_brute(self):
        for reflect,expect in ((False,10),(True,8)):
            self.assertEqual(orbit_count_enumerated(ring_permutations(8,reflect),2,4),expect)
    def test_cube_24_rotations(self):self.assertEqual(len(cube_rotations()),24)
    def test_cube_all_unique(self):self.assertEqual(len(set(cube_rotations())),24)
    def test_cube_cycle_classes(self):
        self.assertEqual(Counter(tuple(cycles(x)) for x in cube_rotations()),
            Counter({(1,1,1,1,1,1):1,(1,1,4):6,(1,1,2,2):3,(3,3):8,(2,2,2):6}))
    def test_cube_burnside_two_colors(self):self.assertEqual(orbit_count_formula(cube_rotations(),2),10)
    def test_cube_burnside_three_colors(self):self.assertEqual(orbit_count_formula(cube_rotations(),3),57)
    def test_cube_enumerate_two_colors(self):self.assertEqual(orbit_count_enumerated(cube_rotations(),2),10)
    def test_cube_enumerate_three_colors(self):self.assertEqual(orbit_count_enumerated(cube_rotations(),3),57)
    def test_cube_fixed_sum(self):self.assertEqual(sum(3**len(cycles(x)) for x in cube_rotations()),1368)
    def test_fixed_weight_full(self):
        for n in (4,6,8):
            perms=ring_permutations(n)
            for k in range(n+1):
                self.assertEqual(orbit_count_formula(perms,2,k),orbit_count_enumerated(perms,2,k))
    def test_bad_n(self):
        with self.assertRaises(ValueError):ring_permutations(0)
    def test_bad_weight_q(self):
        with self.assertRaises(ValueError):fixed_colorings((0,1,2),3,1)

if __name__=='__main__':unittest.main()
