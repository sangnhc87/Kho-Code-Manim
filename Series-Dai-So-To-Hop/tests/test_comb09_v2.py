"""COMB09: independent finite enumerations, narration and production contracts."""
import itertools
import json
import math
import pathlib
import sys
import unittest

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb09_lesson_data import BEATS,FORMULAS,CHAPTER_LABELS,words,nonadjacent,multiset_choices,validate,four_digit_numbers_no_repeat

class TestCOMB09(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_eight_chapters(self):self.assertEqual(len(CHAPTER_LABELS),8)
    def test_48_beats(self):self.assertEqual(len(BEATS),48)
    def test_all_have_substantive_narration(self):self.assertTrue(all(len(b.narration.split())>=43 for b in BEATS))
    def test_16_minute_floor(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),960)
    def test_all_formula_keys(self):self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
    def test_ordered_2_letters(self):self.assertEqual(len(words(2)),9)
    def test_ordered_3_letters(self):self.assertEqual(len(words(3)),27)
    def test_ordered_4_letters(self):self.assertEqual(len(words(4)),81)
    def test_order_matters(self):self.assertIn('AB',words(2));self.assertIn('BA',words(2))
    def test_repetition_allowed(self):self.assertIn('AA',words(2));self.assertIn('AAAA',words(4))
    def test_codes_4_digit(self):self.assertEqual(len(tuple(itertools.product(range(10),repeat=4))),10000)
    def test_codes_zero_prefix(self):self.assertIn((0,0,7,3),set(itertools.product(range(10),repeat=4)))
    def test_4_digit_numbers_allow_repeat(self):self.assertEqual(9*10**3,9000)
    def test_nonrepeated_codes(self):self.assertEqual(len(tuple(itertools.permutations(range(10),4))),5040)
    def test_distinct_numbers(self):self.assertEqual(len(four_digit_numbers_no_repeat()),4536)
    def test_all_distinct_numbers_have_valid_thousands(self):self.assertTrue(all(1000<=x<10000 for x in four_digit_numbers_no_repeat()))
    def test_multisets_10(self):self.assertEqual(len(multiset_choices()),10)
    def test_multisets_canonical(self):self.assertIn('ABC',multiset_choices());self.assertNotIn('BAC',multiset_choices())
    def test_three_types_all_equal(self):self.assertEqual(sum(len(set(w))==1 for w in multiset_choices()),3)
    def test_three_types_two_equal(self):self.assertEqual(sum(len(set(w))==2 for w in multiset_choices()),6)
    def test_three_types_three_distinct(self):self.assertEqual(sum(len(set(w))==3 for w in multiset_choices()),1)
    def test_at_least_one_A(self):self.assertEqual(sum('A' in w for w in words(4)),65)
    def test_zero_A(self):self.assertEqual(sum('A' not in w for w in words(4)),16)
    def test_exactly_two_A(self):self.assertEqual(sum(w.count('A')==2 for w in words(4)),24)
    def test_exactly_one_A(self):self.assertEqual(sum(w.count('A')==1 for w in words(4)),32)
    def test_exactly_three_A(self):self.assertEqual(sum(w.count('A')==3 for w in words(4)),8)
    def test_exactly_four_A(self):self.assertEqual(sum(w.count('A')==4 for w in words(4)),1)
    def test_partition_by_A_count(self):self.assertEqual(sum(sum(w.count('A')==k for w in words(4)) for k in range(5)),81)
    def test_nonadjacent_0(self):self.assertEqual(len(nonadjacent(0)),1)
    def test_nonadjacent_1(self):self.assertEqual(len(nonadjacent(1)),3)
    def test_nonadjacent_2(self):self.assertEqual(len(nonadjacent(2)),8)
    def test_nonadjacent_3(self):self.assertEqual(len(nonadjacent(3)),22)
    def test_nonadjacent_4(self):self.assertEqual(len(nonadjacent(4)),60)
    def test_nonadjacent_recurrence(self):
        counts=[len(nonadjacent(k)) for k in range(9)]
        self.assertTrue(all(counts[k]==2*counts[k-1]+2*counts[k-2] for k in range(2,9)))
    def test_nonadjacent_4_no_bad_strings(self):self.assertTrue(all('AA' not in s for s in nonadjacent(4)))
    def test_multiset_formula(self):self.assertEqual(math.comb(5,3),10)
    def test_choose_positions_two_A(self):self.assertEqual(math.comb(4,2)*2**2,24)
    def test_at_least_1_3_letters(self):self.assertEqual(sum('A' in w for w in words(3)),19)
    def test_instructions_exist(self):self.assertTrue((ROOT/'HUONG_DAN_RENDER_COMB09_V2.md').exists())
    def test_scene_name(self):
        text=(ROOT/'episodes/comb09_repetition.py').read_text(encoding='utf-8')
        self.assertIn('class COMB09(Scene):',text)
    def test_workflow_inputs(self):
        text=(ROOT.parent/'.github/workflows/render-comb09-v2.yml').read_text(encoding='utf-8')
        self.assertIn('quality:',text);self.assertIn('voice:',text)
    def test_typst_notation(self):self.assertIn('C^(4)_(2)',FORMULAS['positions'])
    def test_script_compiles(self):
        import py_compile
        for f in ('episodes/comb09_repetition.py','scripts/prepare_comb09_v2.py','scripts/qa_comb09_v2.py'):
            py_compile.compile(str(ROOT/f),doraise=True)
    def test_manifest(self):
        p=ROOT/'voice/comb09_voice_manifest.json'
        self.assertTrue(p.exists())
        d=json.loads(p.read_text(encoding='utf-8'))
        self.assertEqual(d['beats'],48)
        self.assertGreater(d['target_seconds'],960)

if __name__=='__main__':unittest.main()
