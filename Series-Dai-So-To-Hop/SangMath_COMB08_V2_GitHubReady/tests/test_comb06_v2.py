"""Independent COMB06 tests: enumerate ordered triples and digit strings."""
import ast,json,sys,unittest
from pathlib import Path
from itertools import permutations
from math import factorial, perm, comb
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb06_lesson_data import (BEATS,CHAPTER_IDS,FORMULAS,
  ordered_awards,restricted_awards,named_participant_not_first,
  valid_digit_numbers,validate)
from series_config import symbol

class Maths(unittest.TestCase):
    def test_awards_6_3(self):self.assertEqual(len(ordered_awards()),120)
    def test_awards_unique(self):self.assertEqual(len(set(ordered_awards())),120)
    def test_awards_no_repeat(self):self.assertTrue(all(len(set(q))==3 for q in ordered_awards()))
    def test_7_3(self):self.assertEqual(len(ordered_awards('ABCDEFG',3)),210)
    def test_winner_6(self):self.assertEqual({x[0] for x in ordered_awards()},set('ABCDEF'))
    def test_first_6_second_5_third_4(self):self.assertEqual(6*5*4,120)
    def test_each_first_choice_20(self):self.assertEqual(Counter(p[0] for p in ordered_awards()),{c:20 for c in 'ABCDEF'})
    def test_restrict_180(self):self.assertEqual(len(restricted_awards()),180)
    def test_restrict_complement_180(self):self.assertEqual(210-30,180)
    def test_restrict_no_a_first(self):self.assertTrue(all(p[0]!='A' for p in restricted_awards()))
    def test_banned_30(self):self.assertEqual(sum(p[0]=='A' for p in permutations('ABCDEFG',3)),30)
    def test_name_can_still_work(self):self.assertIn(('B','A','C'),restricted_awards())
    def test_name_must_work_but_not_first(self):self.assertEqual(len(named_participant_not_first()),60)
    def test_name_excluded_all_roles(self):self.assertEqual(sum('A' not in p for p in permutations('ABCDEFG',3)),120)
    def test_twenty_from_five(self):self.assertEqual(perm(5,2),20)
    def test_no_selection_one_empty(self):self.assertEqual(perm(7,0),1)
    def test_all_people_permutation(self):self.assertEqual(perm(6,6),factorial(6))
    def test_small_falling_product(self):
        for n in range(1,9):
            for k in range(n+1):self.assertEqual(perm(n,k),factorial(n)//factorial(n-k))
    def test_order_vs_group(self):self.assertEqual(perm(6,3),comb(6,3)*factorial(3))
    def test_digit_set_48(self):self.assertEqual(len(valid_digit_numbers()),48)
    def test_digits_all_three_places(self):self.assertTrue(all(100<=x<=999 for x in valid_digit_numbers()))
    def test_digits_no_repeat(self):self.assertTrue(all(len(set(str(x)))==3 for x in valid_digit_numbers()))
    def test_digits_by_complement(self):self.assertEqual(perm(5,3)-perm(4,2),48)
    def test_even_digit_count(self):self.assertEqual(sum(n%2==0 for n in valid_digit_numbers()),30)
    def test_even_split_zero(self):self.assertEqual(sum(n%10==0 for n in valid_digit_numbers()),12)
    def test_even_split_2_or_4(self):self.assertEqual(sum(n%10 in (2,4) for n in valid_digit_numbers()),18)
    def test_digit_first_four_choices(self):self.assertEqual({str(n)[0] for n in valid_digit_numbers()},set('1234'))

class Production(unittest.TestCase):
    def test_validates(self):self.assertTrue(validate())
    def test_48_beats(self):self.assertEqual(len(BEATS),48)
    def test_8_chapters(self):self.assertEqual(len(CHAPTER_IDS),8)
    def test_six_beats_each(self):self.assertEqual(Counter(b.section for b in BEATS),{s:6 for s in CHAPTER_IDS})
    def test_minimum_15_minutes(self):self.assertGreater(sum(x.min_seconds for x in BEATS),900)
    def test_original_words(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),2800)
    def test_narration_complete(self):self.assertTrue(all(len(b.narration.split())>=38 for b in BEATS))
    def test_formulas_reference(self):self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
    def test_symbols_user_convention(self):
        self.assertTrue(symbol('A',6,3).startswith('A^(6)_(3)') or symbol('A',6,3).startswith('A_(6)^(3)'))
    def test_markdown_generated(self):self.assertTrue((ROOT/'narration_COMB06_v2.md').is_file())
    def test_subtitles_generated(self):self.assertGreater((ROOT/'subtitles_COMB06_v2.srt').read_text().count('-->'),100)
    def test_manifest_beats(self):
        m=json.loads((ROOT/'voice/comb06_voice_manifest.json').read_text())
        self.assertEqual(m['beats'],48)
        self.assertGreater(m['target_seconds'],900)
    def test_scripts_parse(self):
        for name in ('episodes/comb06_arrangements.py','scripts/prepare_comb06_v2.py','scripts/qa_comb06_v2.py'):
            with self.subTest(script=name):ast.parse((ROOT/name).read_text())
    def test_workflow_wired(self):
        s=(ROOT/'.github/workflows/render-comb06-v2.yml').read_text()
        for expected in ('COMB06','comb06_arrangements.py','prepare_comb06_v2.py','qa_comb06_v2.py','workflow_dispatch'):
            self.assertIn(expected,s)
    def test_old_files_preserved(self):
        for name in ('comb01_rule_of_sum.py','comb02_rule_of_product.py','comb03_tree_sample_space.py','comb04_order_matters.py','comb05_permutations.py','geo01_point_inside_triangle.py'):
            self.assertTrue((ROOT/'episodes'/name).exists())

if __name__=='__main__':unittest.main()
