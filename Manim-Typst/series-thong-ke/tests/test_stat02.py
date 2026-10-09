from __future__ import annotations
import unittest
import math
import itertools
from collections import Counter
from stat02.lesson import *

class TestSTAT02Mathematics(unittest.TestCase):
    def test_source_is_stat01(self):
        from stat01.lesson import SCORES as OLD
        self.assertIs(SCORES,OLD)
    def test_frequency_40(self):self.assertEqual(sum(FREQUENCY.values()),40)
    def test_frequency_identical(self):self.assertEqual(dict(Counter(SCORES)),FREQUENCY)
    def test_7_count(self):self.assertEqual(FREQUENCY[7],10)
    def test_9_count(self):self.assertEqual(FREQUENCY[9],6)
    def test_percent_7(self):self.assertEqual(PERCENT[7],25)
    def test_percent_8(self):self.assertEqual(PERCENT[8],20)
    def test_percent_sum(self):self.assertAlmostEqual(sum(PERCENT.values()),100)
    def test_angle_7(self):self.assertEqual(PIE_ANGLES[7],90)
    def test_angle_9(self):self.assertEqual(PIE_ANGLES[9],54)
    def test_angles_total(self):self.assertAlmostEqual(sum(PIE_ANGLES.values()),360)
    def test_all_angles_positive(self):self.assertTrue(all(v>0 for v in PIE_ANGLES.values()))
    def test_group_count(self):self.assertEqual(GROUP_COUNT,(6,18,14,2))
    def test_group_sum(self):self.assertEqual(sum(GROUP_COUNT),40)
    def test_each_record_in_one_interval(self):
        self.assertTrue(all(sum(a<=x<b for a,b in zip(GROUP_EDGES,GROUP_EDGES[1:]))==1 for x in SCORES))
    def test_group_density_equal_intervals(self):self.assertEqual(GROUP_DENSITY,(3,9,7,1))
    def test_group_areas(self):
        for i,c in enumerate(GROUP_COUNT):
            self.assertEqual(GROUP_DENSITY[i]*(GROUP_EDGES[i+1]-GROUP_EDGES[i]),c)
    def test_second_class_count(self):self.assertEqual(CLASS_B_N,50)
    def test_second_class_ge8(self):self.assertEqual(sum(CLASS_B[x] for x in (8,9,10)),25)
    def test_first_class_ge8(self):self.assertEqual(sum(FREQUENCY[x] for x in (8,9,10)),16)
    def test_second_class_ge8_percent(self):self.assertEqual(sum(CLASS_B_PCT[x] for x in (8,9,10)),50)
    def test_percent_b_7(self):self.assertEqual(CLASS_B_PCT[7],20)
    def test_class_b_total_percentage(self):self.assertEqual(sum(CLASS_B_PCT.values()),100)
    def test_month_count(self):self.assertEqual(len(MONTHS),len(MONTHLY_MEAN))
    def test_month_values(self):self.assertEqual(MONTHLY_MEAN,(6.1,6.5,6.4,7.2,7.,7.6))
    def test_month3_decrease(self):self.assertLess(MONTHLY_MEAN[2],MONTHLY_MEAN[1])
    def test_time_bins(self):self.assertEqual(TIME_CLASSES,((0,10,12),(10,20,8),(20,40,20)))
    def test_time_density(self):
        for (a,b,n),h in zip(TIME_CLASSES,TIME_DENSITY):self.assertAlmostEqual((b-a)*h,n)
    def test_time_density_values(self):self.assertEqual(TIME_DENSITY,(1.2,.8,1.0))

class TestSTAT02Lesson(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_beats(self):self.assertEqual(len(BEATS),32)
    def test_step(self):self.assertEqual([b.step for b in BEATS],[n for _ in range(8) for n in range(1,5)])
    def test_chapter_order(self):self.assertEqual([b.chapter for b in BEATS],[n for n in range(1,9) for _ in range(4)])
    def test_no_duplicate_title(self):self.assertEqual(len({b.title for b in BEATS}),32)
    def test_narration_length(self):self.assertTrue(all(len(b.voice.split())>=44 for b in BEATS))
    def test_total_run_time(self):self.assertGreaterEqual(sum(b.duration for b in BEATS),700)
    def test_synthetic_disclosure(self):self.assertIn('giả lập',BEATS[0].voice)
    def test_histogram_concept(self):self.assertIn('mật độ', ' '.join(b.voice for b in BEATS if b.chapter==5))
    def test_time_is_independent(self):self.assertIn('độc lập',' '.join(b.voice for b in BEATS if b.chapter==6))
    def test_no_manim_import_in_data(self):
        from pathlib import Path
        source=Path(__file__).resolve().parents[1]/'stat02'/'lesson.py'
        self.assertNotIn('from manim import',source.read_text(encoding='utf-8'))

if __name__=='__main__':unittest.main()
