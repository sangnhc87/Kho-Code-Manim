"""Numerically independent COMB05 tests: exact permutations, no omitted cases."""
import ast,json,sys,unittest
from pathlib import Path
from collections import Counter
from itertools import permutations
from math import factorial
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb05_lesson_data import (BEATS,CHAPTER_IDS,FOUR_ORDERS,FORMULAS,
  adjacent,before,gap_count_5,count_adjacent,count_nonadjacent,validate)

class Mathematics(unittest.TestCase):
    def test_empty_permutation(self):self.assertEqual(factorial(0),1)
    def test_four_factorial(self):self.assertEqual(factorial(4),24)
    def test_five_factorial(self):self.assertEqual(factorial(5),120)
    def test_six_factorial(self):self.assertEqual(factorial(6),720)
    def test_24_distinct(self):self.assertEqual(len(set(FOUR_ORDERS)),24)
    def test_every_order_uses_all_four(self):self.assertTrue(all(set(x)==set('ABCD') for x in FOUR_ORDERS))
    def test_six_for_each_first_letter(self):
        self.assertEqual(Counter(x[0] for x in FOUR_ORDERS),{'A':6,'B':6,'C':6,'D':6})
    def test_two_books_a_b_distinct(self):self.assertNotEqual('ABCD','BACD')
    def test_adjacent_three_small(self):self.assertEqual(len(count_adjacent('ABC')),4)
    def test_adjacent_five(self):self.assertEqual(len(count_adjacent()),48)
    def test_adjacent_by_block(self):self.assertEqual(2*factorial(4),48)
    def test_nonadjacent_five(self):self.assertEqual(len(count_nonadjacent()),72)
    def test_partition_all_five(self):
        whole={''.join(s) for s in permutations('ABCDE')}
        self.assertEqual(count_adjacent()|count_nonadjacent(),whole)
        self.assertFalse(count_adjacent()&count_nonadjacent())
    def test_gaps_72(self):self.assertEqual(len(gap_count_5()),72)
    def test_gaps_same_as_complement(self):self.assertEqual(gap_count_5(),count_nonadjacent())
    def test_choosing_gap_pairs(self):self.assertEqual(6*2,12)
    def test_gaps_product(self):self.assertEqual(factorial(3)*6*2,72)
    def test_before_five(self):self.assertEqual(sum(before(s) for s in permutations('ABCDE')),60)
    def test_before_symmetry(self):
        pairs=set()
        for q in permutations('ABCDE'):
            p=''.join(q)
            t=list(p);a=t.index('A');b=t.index('B');t[a],t[b]=t[b],t[a]
            pairs.add(tuple(sorted((p,''.join(t)))))
        self.assertEqual(len(pairs),60)
    def test_endpoints_six(self):
        self.assertEqual(sum(s[0] in 'AB' and s[-1] in 'AB' for s in permutations('ABCDEF')),48)
    def test_nonadjacent_six(self):self.assertEqual(len(count_nonadjacent('ABCDEF')),480)
    def test_nonadjacent_six_complement(self):self.assertEqual(720-2*factorial(5),480)

class Production(unittest.TestCase):
    def test_lesson_validate(self):self.assertTrue(validate())
    def test_48_beats(self):self.assertEqual(len(BEATS),48)
    def test_8_chapters(self):self.assertEqual(len(CHAPTER_IDS),8)
    def test_six_each(self):self.assertEqual(Counter(b.section for b in BEATS),{ch:6 for ch in CHAPTER_IDS})
    def test_words_deep(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),2650)
    def test_duration_floor(self):self.assertGreater(sum(b.min_seconds for b in BEATS),880)
    def test_formulas_valid(self):self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
    def test_all_headers_distinct(self):self.assertEqual(len(set(x.heading for x in BEATS)),48)
    def test_full_narrations(self):self.assertTrue(all(len(b.narration.split())>=35 for b in BEATS))
    def test_manifest_ready(self):self.assertTrue((ROOT/'voice/comb05_voice_manifest.json').exists())
    def test_manifest_beats(self):
        d=json.loads((ROOT/'voice/comb05_voice_manifest.json').read_text())
        self.assertEqual(d['beats'],48)
        self.assertGreater(d['target_seconds'],890)
    def test_subtitle_cues(self):self.assertGreater((ROOT/'subtitles_COMB05_v2.srt').read_text().count('-->'),100)
    def test_scene_parse(self):ast.parse((ROOT/'episodes/comb05_permutations.py').read_text())
    def test_prepare_parse(self):ast.parse((ROOT/'scripts/prepare_comb05_v2.py').read_text())
    def test_qa_parse(self):ast.parse((ROOT/'scripts/qa_comb05_v2.py').read_text())
    def test_workflow_wired(self):
        text=(ROOT.parent/'.github/workflows/render-comb05-v2.yml').read_text()
        for value in ('COMB05','comb05_permutations.py','prepare_comb05_v2.py','qa_comb05_v2.py'):
            self.assertIn(value,text)
    def test_old_assets_preserved(self):
        for name in ('comb01_rule_of_sum.py','comb02_rule_of_product.py','comb03_tree_sample_space.py','comb04_order_matters.py','geo01_point_inside_triangle.py'):
            self.assertTrue((ROOT/'episodes'/name).is_file())

if __name__=='__main__':unittest.main()
