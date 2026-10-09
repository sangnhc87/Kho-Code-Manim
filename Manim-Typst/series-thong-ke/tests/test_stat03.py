"""Independent mathematical and production-structure tests for STAT03."""
from __future__ import annotations
import ast
import unittest
from collections import Counter
from itertools import permutations
from math import fsum
from pathlib import Path
from statistics import mean, median, multimode
from stat01.lesson import SCORES as OLD_SCORES
from stat03.lesson import *
ROOT=Path(__file__).resolve().parents[1]

class TestNumericalStatistics(unittest.TestCase):
    def test_source_identity(self):self.assertIs(SCORES,OLD_SCORES)
    def test_count(self):self.assertEqual(N,40)
    def test_actual_counts(self):self.assertEqual(dict(Counter(SCORES)),FREQUENCY)
    def test_weighted_total(self):self.assertEqual(WEIGHTED_SUM,284)
    def test_plain_total(self):self.assertEqual(sum(SCORES),284)
    def test_mean(self):self.assertAlmostEqual(MEAN,7.1)
    def test_median(self):self.assertEqual(MEDIAN,7)
    def test_median_20_21(self):self.assertEqual((SORTED[19],SORTED[20]),(7,7))
    def test_modes(self):self.assertEqual(MODES,(7,))
    def test_counter_peak(self):self.assertEqual(max(FREQUENCY.values()),10)
    def test_mean_deviations_balance(self):self.assertAlmostEqual(fsum(x-MEAN for x in SCORES),0)
    def test_sorted_invariant(self):self.assertEqual(Counter(SORTED),Counter(SCORES))
    def test_total_weight_matches_mean(self):self.assertAlmostEqual(WEIGHTED_SUM/N,MEAN)
    def test_base_nine(self):self.assertEqual(len(BASE),9)
    def test_base_total(self):self.assertEqual(sum(BASE),63)
    def test_base_mean(self):self.assertEqual(mean(BASE),7)
    def test_base_median(self):self.assertEqual(median(BASE),7)
    def test_base_mode(self):self.assertEqual(multimode(BASE),[7])
    def test_extreme_is_single_replacement(self):self.assertEqual(CHANGED[:-1],BASE[:-1])
    def test_extreme_total(self):self.assertEqual(sum(CHANGED),81)
    def test_extreme_mean(self):self.assertEqual(mean(CHANGED),9)
    def test_extreme_median(self):self.assertEqual(median(CHANGED),7)
    def test_extreme_mode(self):self.assertEqual(multimode(CHANGED),[7])
    def test_extreme_mean_change(self):self.assertEqual(mean(CHANGED)-mean(BASE),2)
    def test_extreme_median_invariance(self):self.assertEqual(median(CHANGED)-median(BASE),0)
    def test_shift_40(self):self.assertEqual(len(TRANSFORMED),40)
    def test_shift_items(self):self.assertTrue(all(y-x==2 for x,y in zip(SCORES,TRANSFORMED)))
    def test_shift_average(self):self.assertAlmostEqual(mean(TRANSFORMED),9.1)
    def test_shift_median(self):self.assertEqual(median(TRANSFORMED),9)
    def test_shift_mode(self):self.assertEqual(multimode(TRANSFORMED),[9])
    def test_unimodal_versus_multimodal(self):self.assertEqual(multimode((2,2,3,3,4)),[2,3])
    def test_reverse_5_numbers(self):self.assertEqual(5*7-sum((5,6,7,8)),9)
    def test_reconstruct_5(self):self.assertEqual(mean((5,6,7,8,9)),7)
    def test_odd_median_by_position(self):self.assertEqual(sorted(BASE)[4],7)
    def test_median_permutation_invariant(self):
        for row in (BASE,BASE[::-1],tuple(reversed(BASE))):
            self.assertEqual(median(row),7)

class TestProduction(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_beats(self):self.assertEqual(len(BEATS),32)
    def test_4_per_chapter(self):self.assertEqual([b.chapter for b in BEATS],[j for j in range(1,9) for _ in range(4)])
    def test_step_order(self):self.assertEqual([b.step for b in BEATS],list(range(1,5))*8)
    def test_no_duplicate_titles(self):self.assertEqual(len({b.title for b in BEATS}),32)
    def test_narration_substantial(self):self.assertTrue(all(len(b.voice.split())>=42 for b in BEATS))
    def test_total_duration(self):self.assertEqual(sum(b.duration for b in BEATS),800)
    def test_synthetic_disclosure(self):self.assertIn('giả lập',BEATS[0].voice)
    def test_outlier_not_original_scores(self):self.assertIn('độc lập',BEATS[16].voice)
    def test_source_pure_python(self):self.assertNotIn('from manim import',(ROOT/'stat03/lesson.py').read_text())
    def test_scenes_name(self):self.assertIn('class STAT03(Scene)',(ROOT/'stat03/scene.py').read_text())
    def test_typst_count(self):
        from scripts.build_stat03_typst import FORMULAS
        self.assertEqual(len(FORMULAS),8)
    def test_workflow(self):
        wf = ROOT/'.github/workflows/render-stat03.yml'
        if not wf.exists():
            wf = ROOT.parent.parent/'.github/workflows/render-stat03.yml'
        contents = wf.read_text(encoding='utf-8')
        self.assertIn('scripts/prepare_stat03.py',contents)
        self.assertIn('scripts/qa_stat03.py',contents)
        self.assertIn('stat03/scene.py STAT03',contents)
    def test_audio_fail_if_unavailable(self):
        s=(ROOT/'scripts/prepare_stat03.py').read_text()
        self.assertIn("if speech<=1:raise RuntimeError",s)
    def test_can_parse_scene_without_manim(self):
        ast.parse((ROOT/'stat03/scene.py').read_text(encoding='utf-8'))

if __name__=='__main__':unittest.main()
