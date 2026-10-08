"""Independent exhaustive verification and packaging contracts for COMB15."""
import unittest,sys,json
from itertools import permutations,product
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb15_lesson_data import BEATS,FORMULAS,CHAPTERS,validate,enumerate_numbers,mathematical_checks
class TestCOMB15Math(unittest.TestCase):
    def test_model_validation(self):self.assertTrue(validate())
    def test_hundreds_not_zero(self):
        p=enumerate_numbers('012345',3)
        self.assertEqual((len(p),min(p),max(p)),(100,102,543))
    def test_repeat_allowed_three_digit(self):self.assertEqual(len(enumerate_numbers('012345',3,False)),180)
    def test_even_split(self):
        p=enumerate_numbers('01234',3)
        self.assertEqual((sum(x%2==0 for x in p),sum(x%2 for x in p)),(30,18))
        self.assertEqual((sum(x%10==0 for x in p),sum(x%10 in (2,4) for x in p)),(12,18))
    def test_divisible_five_cases(self):
        p=enumerate_numbers('0123456',4)
        self.assertEqual((len(p),sum(x%10==0 for x in p),sum(x%10==5 for x in p)),(720,120,100))
    def test_div_three_remainder_sets(self):
        p=enumerate_numbers('012345',3)
        valid=[x for x in p if x%3==0]
        self.assertEqual(len(valid),40)
        self.assertEqual((sum('0' in str(x) for x in valid),sum('0' not in str(x) for x in valid)),(16,24))
        self.assertEqual(Counter(x//100 for x in valid),{1:8,2:8,3:8,4:8,5:8})
    def test_even_greater_than_three_hundred(self):
        p=enumerate_numbers('012345',3)
        counts=Counter(x//100 for x in p if x>300 and x%2==0)
        self.assertEqual(dict(counts),{3:12,4:8,5:12})
    def test_repeated_four_digit(self):
        distinct=set(enumerate_numbers('012345',4));allx=set(enumerate_numbers('012345',4,False))
        self.assertEqual((len(allx),len(distinct),len(allx-distinct)),(1080,300,780))
        self.assertTrue(distinct <= allx)
    def test_divisible_four_ends(self):
        p=enumerate_numbers('012345',4)
        tails=Counter(str(x)[-2:] for x in p if x%4==0)
        self.assertEqual(dict(sorted(tails.items())),{'04':12,'12':9,'20':12,'24':9,'32':9,'40':12,'52':9})
    def test_divisible_fifteen_capstone(self):
        p=enumerate_numbers('012345',4)
        good=[x for x in p if x>3000 and x%15==0]
        self.assertEqual(len(good),24)
        self.assertEqual(Counter((x//1000,x%10) for x in good),{(3,0):8,(3,5):4,(4,0):4,(4,5):4,(5,0):4})
        self.assertTrue(all(len(set(str(x)))==4 for x in good))
    def test_pure_math_selfcheck(self):self.assertTrue(mathematical_checks())
class TestCOMB15Production(unittest.TestCase):
    def test_sections(self):self.assertEqual((len(BEATS),len(CHAPTERS)),(48,8))
    def test_formula_count(self):self.assertEqual(len(FORMULAS),48)
    def test_narration_substantial(self):self.assertGreaterEqual(sum(len(b.narration.split()) for b in BEATS),3400)
    def test_duration_floor(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),1100)
    def test_scene_exists(self):self.assertIn('class COMB15(Scene)',(ROOT/'episodes/comb15_number_formation.py').read_text())
    def test_workflow(self):
        s=(ROOT/'.github/workflows/render-comb15-v2.yml').read_text()
        for k in ('comb15_number_formation.py','COMB15','prepare_comb15_v2.py','qa_comb15_v2.py','upload-artifact'):
            self.assertIn(k,s)
    def test_expected_files(self):
        for f in ('comb15_beats.json','comb15_formulas.json','comb15_chapters.json','scripts/prepare_comb15_v2.py'):
            self.assertTrue((ROOT/f).is_file(),f)
if __name__=='__main__':unittest.main()
