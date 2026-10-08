"""COMB10 — independent combinatorics enumeration + production checks."""
import itertools
import json
import pathlib
import sys
import unittest
from collections import Counter
from math import factorial, comb

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb10_lesson_data import BEATS, FORMULAS, CHAPTER_LABELS, unique_words, multiset_count, validate

class TestCOMB10(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_chapters(self):self.assertEqual(len(CHAPTER_LABELS),8)
    def test_beats(self):self.assertEqual(len(BEATS),48)
    def test_narrative(self):self.assertTrue(all(len(b.narration.split())>=43 for b in BEATS))
    def test_duration(self):self.assertGreater(sum(b.min_seconds for b in BEATS),1030)
    def test_equations(self):self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
    def test_aabc(self):self.assertEqual(len(unique_words('AABC')),12)
    def test_mama(self):self.assertEqual(len(unique_words('MAMA')),6)
    def test_banana(self):self.assertEqual(len(unique_words('BANANA')),60)
    def test_multiset_general(self):
        for w in ['AAAA','ABC','AAAB','AABBC','BANANA','MAMA','AAABBBC']:
            self.assertEqual(multiset_count(w),len(unique_words(w)))
    def test_banana_distinct_labels(self):self.assertEqual(factorial(6)//(factorial(3)*factorial(2)),60)
    def test_banana_block(self):self.assertEqual(sum('AAA' in w for w in unique_words('BANANA')),12)
    def test_banana_no_block(self):self.assertEqual(sum('AAA' not in w for w in unique_words('BANANA')),48)
    def test_banana_no_adjacent(self):self.assertEqual(sum('AA' not in w for w in unique_words('BANANA')),12)
    def test_banana_gaps(self):self.assertEqual(factorial(3)//factorial(2)*comb(4,3),12)
    def test_banana_midcase(self):
        words=unique_words('BANANA')
        self.assertEqual(sum('AA' in w and 'AAA' not in w for w in words),36)
    def test_banana_begin_b(self):self.assertEqual(sum(w[0]=='B' for w in unique_words('BANANA')),10)
    def test_banana_end_a(self):self.assertEqual(sum(w[-1]=='A' for w in unique_words('BANANA')),30)
    def test_banana_both(self):self.assertEqual(sum(w[0]=='B' and w[-1]=='A' for w in unique_words('BANANA')),6)
    def test_banana_union(self):self.assertEqual(sum(w[0]=='B' or w[-1]=='A' for w in unique_words('BANANA')),34)
    def test_aabbc(self):self.assertEqual(len(unique_words('AABBC')),30)
    def test_aabbc_adjacent_a(self):self.assertEqual(sum('AA' in w for w in unique_words('AABBC')),12)
    def test_aabbc_adjacent_b(self):self.assertEqual(sum('BB' in w for w in unique_words('AABBC')),12)
    def test_aabbc_free(self):self.assertEqual(sum('AA' not in w for w in unique_words('AABBC')),18)
    def test_aabbc_intersection(self):self.assertEqual(sum('AA' in w and 'BB' in w for w in unique_words('AABBC')),6)
    def test_aabbc_no_adjacent_either(self):self.assertEqual(sum('AA' not in w and 'BB' not in w for w in unique_words('AABBC')),12)
    def test_typst_notation(self):self.assertIn('C^(4)_(3)',FORMULAS['gaps4'])
    def test_scene(self):self.assertIn('class COMB10(Scene):',(ROOT/'episodes/comb10_multiset_permutations.py').read_text())
    def test_workflow(self):
        wf=(ROOT.parent/'.github/workflows/render-comb10-v2.yml').read_text()
        for t in ('workflow_dispatch:', 'quality:', 'voice:', 'COMB10.mp4','prepare_comb10_v2.py','qa_comb10_v2.py'):
            self.assertIn(t,wf)
    def test_docs(self):self.assertTrue((ROOT/'HUONG_DAN_RENDER_COMB10_V2.md').is_file())
    def test_legacy(self):
        for i in range(1,10):self.assertTrue(list((ROOT/'episodes').glob(f'comb{i:02}*.py')))
    def test_syntax(self):
        import py_compile
        for f in ['episodes/comb10_multiset_permutations.py','scripts/prepare_comb10_v2.py','scripts/qa_comb10_v2.py','comb10_lesson_data.py']:
            py_compile.compile(str(ROOT/f),doraise=True)
    def test_manifest(self):
        d=json.loads((ROOT/'voice/comb10_voice_manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(d['beats'],48)
        self.assertGreater(d['target_seconds'],1030)

if __name__=='__main__':unittest.main()
