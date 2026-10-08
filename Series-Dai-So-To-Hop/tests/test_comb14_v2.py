"""Independent tests: complement sets, inclusion-exclusion and production metadata."""
import unittest,sys,json
from pathlib import Path
from itertools import product,permutations,combinations
from math import comb, perm
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb14_lesson_data import BEATS,FORMULAS,CHAPTERS,validate,mathematical_checks,derangements,no_adjacent,team_captain_valid

class TestCOMB14Math(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_complement_partition_of_81(self):
        allc=list(product('ABC',repeat=4))
        yes={p for p in allc if 'A' in p};no=set(allc)-yes
        self.assertFalse(yes&no);self.assertEqual((len(yes),len(no)),(65,16))
    def test_one_A_not_at_least_one(self):self.assertEqual(sum(p.count('A')==1 for p in product('ABC',repeat=4)),32)
    def test_choose_with_girls(self):
        teams=list(combinations(range(9),3))
        yes=[t for t in teams if any(x>=5 for x in t)];no=[t for t in teams if all(x<5 for x in t)]
        self.assertEqual((len(yes),len(no),len(teams)),(74,10,84))
    def test_choose_three_proof(self):self.assertEqual(4*comb(5,2)+comb(4,2)*5+comb(4,3),74)
    def test_positions(self):
        p=list(permutations(range(6)))
        a={x for x in p if x[0]==0}
        b={x for x in p if abs(x.index(0)-x.index(1))==1}
        self.assertEqual((len(a),len(b),len(a&b),len(set(p)-a-b)),(120,240,24,384))
    def test_pin_differentiation(self):self.assertEqual((10000-perm(10,4),9000-9*9*8*7),(4960,4464))
    def test_fixed_points_all_n(self):self.assertEqual([derangements(i) for i in range(1,6)],[0,1,2,9,44])
    def test_binary_no11(self):
        for n,exp in enumerate([1,2,3,5,8,13,21]):
            self.assertEqual(sum(no_adjacent(p) for p in product((0,1),repeat=n)),exp)
    def test_either_and_both(self):
        teams=list(combinations(range(8),3))
        yes={t for t in teams if 0 in t or 1 in t}
        exactly={t for t in teams if (0 in t)!=(1 in t)}
        both={t for t in teams if 0 in t and 1 in t}
        self.assertEqual((len(yes),len(exactly),len(both)),(36,30,6))
        self.assertEqual(yes,exactly|both)
    def test_capstone_two_independent_ways(self):
        results={(t,c) for t in combinations(range(8),4) for c in t}
        missing={(t,c) for t,c in results if 0 not in t and 1 not in t}
        banned={(t,c) for t,c in results if c==0}
        valid={(t,c) for t,c in results if team_captain_valid(t,c)}
        self.assertFalse(missing&banned)
        self.assertEqual(valid,results-missing-banned)
        self.assertEqual((len(results),len(missing),len(banned),len(valid)),(280,60,35,185))
        self.assertEqual(comb(7,3)+6*(comb(7,3)-comb(5,3)),185)

class TestCOMB14Production(unittest.TestCase):
    def test_beats_and_chapters(self):self.assertEqual((len(BEATS),len(CHAPTERS)),(48,8))
    def test_all_formula_keys(self):self.assertTrue(all(b.formula in FORMULAS for b in BEATS))
    def test_long_enough(self):self.assertGreater(sum(b.min_seconds for b in BEATS),1100)
    def test_real_narration(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),3500)
    def test_typst_sources(self):self.assertTrue((ROOT/'scripts/prepare_comb14_v2.py').exists())
    def test_scene_code(self):self.assertIn('class COMB14(Scene)',(ROOT/'episodes/comb14_complement.py').read_text())
    def test_workflow(self):
        y=(ROOT.parent/'.github/workflows/render-comb14-v2.yml').read_text()
        for x in ('comb14_complement.py','COMB14','prepare_comb14_v2.py','qa_comb14_v2.py'):self.assertIn(x,y)
    def test_filenames(self):
        self.assertTrue((ROOT/'comb14_beats.json').exists())
        self.assertTrue((ROOT/'comb14_formulas.json').exists())

if __name__=='__main__':unittest.main()
