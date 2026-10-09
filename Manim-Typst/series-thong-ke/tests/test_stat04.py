"""Numerical + production tests for STAT04; no Manim dependency."""
from __future__ import annotations
import ast,unittest,json,subprocess,sys
from collections import Counter
from pathlib import Path
from statistics import median
from stat01.lesson import SCORES as BASE
from stat04.lesson import *
ROOT=Path(__file__).resolve().parents[1]

class TestQuartiles(unittest.TestCase):
    def test_source_same(self):self.assertIs(SCORES,BASE)
    def test_source_size(self):self.assertEqual(N,40)
    def test_scores_match_frequency(self):self.assertEqual(dict(Counter(SCORES)),FREQUENCY)
    def test_quartiles(self):self.assertEqual((Q1,Q2,Q3),(6,7,8))
    def test_quartile_range(self):self.assertEqual(IQR,2)
    def test_position_10(self):self.assertEqual(SORTED[9],6)
    def test_position_11(self):self.assertEqual(SORTED[10],6)
    def test_position_20(self):self.assertEqual(SORTED[19],7)
    def test_position_21(self):self.assertEqual(SORTED[20],7)
    def test_position_30(self):self.assertEqual(SORTED[29],8)
    def test_position_31(self):self.assertEqual(SORTED[30],8)
    def test_quartile_in_sorted_order(self):self.assertLessEqual(Q1,Q2);self.assertLessEqual(Q2,Q3)
    def test_even_8(self):self.assertEqual(quartiles(EVEN),(2.5,4.5,6.5))
    def test_odd_9(self):self.assertEqual(quartiles(ODD),(2.5,5,7.5))
    def test_median_omitted_odd(self):self.assertEqual((median(ODD[:4]),median(ODD[5:])),(2.5,7.5))
    def test_singleton(self):self.assertEqual(quartiles((42,)),(42,42,42))
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):quartiles(())
    def test_two_values(self):self.assertEqual(quartiles((7,9)),(7,8,9))
    def test_permutation(self):self.assertEqual(quartiles(tuple(reversed(SCORES))),(6,7,8))
    def test_with_repetition(self):self.assertEqual(quartiles((1,1,1,2,2,2,3,3)),(1,2,2.5))
    def test_extreme_replacement(self):self.assertEqual(quartiles(EXTREME),(6,7,8))
    def test_extreme_change_one(self):self.assertEqual(len(EXTREME),40)
    def test_extreme_mean_change(self):self.assertAlmostEqual((sum(EXTREME)-sum(SCORES))/40,.5)
    def test_shift(self):self.assertEqual(quartiles(SHIFTED),(8,9,10))
    def test_shift_iqr(self):self.assertEqual(quartiles(SHIFTED)[2]-quartiles(SHIFTED)[0],2)
    def test_cumulative_last(self):self.assertEqual(CUMULATIVE[-1],(10,40))
    def test_cumulative_6(self):self.assertIn((6,14),CUMULATIVE)
    def test_cumulative_7(self):self.assertIn((7,24),CUMULATIVE)
    def test_cumulative_8(self):self.assertIn((8,32),CUMULATIVE)
    def test_compare_a(self):self.assertEqual(quartiles(GROUP_A),(3.5,5.5,7.5))
    def test_compare_b(self):self.assertEqual(quartiles(GROUP_B),(2,5.5,10))
    def test_compare_iqr(self):
        a=quartiles(GROUP_A);b=quartiles(GROUP_B)
        self.assertEqual((a[2]-a[0],b[2]-b[0]),(4,8))
    def test_reverse_missing(self):self.assertEqual(2*6.5-7,6)
    def test_reverse_quartiles(self):self.assertEqual(quartiles(UNKNOWN_ANSWER),(4.5,6.5,8.5))
    def test_monotone_transform(self):
        self.assertEqual(quartiles(tuple(v*3 for v in BASE)),(18,21,24))
    def test_original_range(self):self.assertEqual(max(SCORES)-min(SCORES),6)

class TestProduction(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_beat_count(self):self.assertEqual(len(BEATS),32)
    def test_4_each(self):self.assertEqual([b.chapter for b in BEATS],[i for i in range(1,9) for _ in range(4)])
    def test_step_order(self):self.assertEqual([b.step for b in BEATS],list(range(1,5))*8)
    def test_beat_titles_unique(self):self.assertEqual(len({b.title for b in BEATS}),32)
    def test_narration_length(self):self.assertTrue(all(len(b.voice.split())>=42 for b in BEATS))
    def test_duration(self):self.assertGreaterEqual(sum(b.duration for b in BEATS),820)
    def test_source_pure(self):self.assertNotIn('from manim import',(ROOT/'stat04/lesson.py').read_text())
    def test_scene_parse(self):ast.parse((ROOT/'stat04/scene.py').read_text())
    def test_scene_class(self):self.assertIn('class STAT04(Scene)',(ROOT/'stat04/scene.py').read_text())
    def test_visual_types(self):self.assertIn('VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)',(ROOT/'stat04/scene.py').read_text())
    def test_typst_formulas(self):
        from scripts.build_stat04_typst import FORMULAS
        self.assertEqual(len(FORMULAS),8)
    def test_workflow(self):
        s=(ROOT.parent.parent/'.github/workflows/render-stat04.yml').read_text()
        for key in ('scripts/prepare_stat04.py','scripts/qa_stat04.py','stat04/scene.py STAT04'):
            self.assertIn(key,s)
    def test_qa_audio_check(self):self.assertIn("if a.voice=='on' and not audio",(ROOT/'scripts/qa_stat04.py').read_text())
    def test_tts_failure(self):self.assertIn("if speech<=1:raise RuntimeError",(ROOT/'scripts/prepare_stat04.py').read_text())
    def test_runtime(self):
        p=ROOT/'stat04/runtime_plan.json'
        self.assertTrue(p.exists())
        data=json.loads(p.read_text());self.assertEqual(data['scene'],'STAT04')
        self.assertEqual(len(data['beats']),32)
        self.assertGreaterEqual(data['duration_expected'],820)
    def test_subtitles(self):self.assertIn('00:00:',(ROOT/'STAT04_vi.srt').read_text())

if __name__=='__main__':unittest.main()
