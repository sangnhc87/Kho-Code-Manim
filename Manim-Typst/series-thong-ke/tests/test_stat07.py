"""Data, boundary, histogram area, consistency and lesson validation tests."""
import unittest
from collections import Counter
from math import isclose
from stat01.lesson import SCORES
from stat07.lesson import *

class TestSTAT07(unittest.TestCase):
    def test_lesson(self):self.assertTrue(validate())
    def test_n(self):self.assertEqual(len(SCORES),40)
    def test_frequency(self):self.assertEqual(FREQ,(6,18,14,2))
    def test_cum(self):self.assertEqual(CUM,(6,24,38,40))
    def test_relative(self):self.assertEqual(REL,(.15,.45,.35,.05))
    def test_rel_sum(self):self.assertAlmostEqual(sum(REL),1)
    def test_15percent(self):self.assertEqual(REL[0]*100,15)
    def test_45percent(self):self.assertEqual(REL[1]*100,45)
    def test_35percent(self):self.assertEqual(REL[2]*100,35)
    def test_5percent(self):self.assertEqual(REL[3]*100,5)
    def test_above_eight(self):self.assertEqual(FREQ[-2]+FREQ[-1],16)
    def test_below_eight(self):self.assertEqual(sum(FREQ[:2]),24)
    def test_total_from_cum(self):self.assertEqual(CUM[-1],len(SCORES))
    def test_freq_nonnegative(self):self.assertTrue(all(i>=0 for i in FREQ))
    def test_cum_monotonic(self):self.assertEqual(tuple(sorted(CUM)),CUM)
    def test_half_open_six(self):self.assertEqual([c.contains(6) for c in CLASSES],[False,True,False,False])
    def test_half_open_eight(self):self.assertEqual([c.contains(8) for c in CLASSES],[False,False,True,False])
    def test_half_open_ten(self):self.assertEqual([c.contains(10) for c in CLASSES],[False,False,False,True])
    def test_right_endpoint(self):self.assertFalse(CLASSES[0].contains(6))
    def test_left_endpoint(self):self.assertTrue(CLASSES[0].contains(4))
    def test_sample_cover(self):self.assertTrue(all(sum(c.contains(x) for c in CLASSES)==1 for x in SCORES))
    def test_exact_mean(self):self.assertAlmostEqual(sum(SCORES)/40,7.1)
    def test_grouped_mean(self):self.assertAlmostEqual(grouped_mean(FREQ,CLASSES),7.6)
    def test_grouped_not_exact(self):self.assertNotAlmostEqual(grouped_mean(FREQ,CLASSES),sum(SCORES)/40)
    def test_grouped_density_equalwidth(self):self.assertEqual(DENS,(3,9,7,1))
    def test_histogram_equalwidth_area(self):self.assertAlmostEqual(sum(d*c.width for d,c in zip(DENS,CLASSES)),40)
    def test_asym_frequencies(self):self.assertEqual(ASYM_FREQ,(6,8,18,8))
    def test_asym_width(self):self.assertEqual(tuple(c.width for c in ASYM),(2,1,2,2))
    def test_asym_density(self):self.assertEqual(ASYM_DENS,(3,8,9,4))
    def test_asym_area(self):self.assertAlmostEqual(sum(d*c.width for d,c in zip(ASYM_DENS,ASYM)),40)
    def test_practice_frequency(self):self.assertEqual(PFREQ,(5,7,6,2))
    def test_practice_cum(self):self.assertEqual(PCUM,(5,12,18,20))
    def test_practice_n(self):self.assertEqual(len(PRACTICE),20)
    def test_practice_relative(self):self.assertEqual(relative(PFREQ),(.25,.35,.3,.1))
    def test_practice_below_six(self):self.assertEqual(PCUM[1],12)
    def test_practice_at_least_six(self):self.assertEqual(sum(PFREQ[2:]),8)
    def test_no_n(self):
        with self.assertRaises(ValueError):grouped((),CLASSES)
    def test_outside_range(self):
        with self.assertRaises(ValueError):grouped((99,),CLASSES)
    def test_gapped(self):
        with self.assertRaises(ValueError):grouped((3,),(Interval(0,2),Interval(3,5)))
    def test_invalid_interval(self):
        with self.assertRaises(ValueError):Interval(2,2)
    def test_invalid_interval_reverse(self):
        with self.assertRaises(ValueError):Interval(2,1)
    def test_cumulative_negative(self):
        with self.assertRaises(ValueError):cumulative((1,-1,1))
    def test_relative_zero(self):
        with self.assertRaises(ValueError):relative((0,0))
    def test_density_mismatch(self):
        with self.assertRaises(ValueError):density((1,2),CLASSES)
    def test_mean_zero(self):
        with self.assertRaises(ValueError):grouped_mean((0,0,0,0),CLASSES)
    def test_multiple_original_same_table(self):
        low=(4,)*6+(6,)*18+(8,)*14+(10,)*2
        high=(5,)*6+(7,)*18+(9,)*14+(10,)*2
        self.assertEqual(grouped(low,CLASSES),FREQ)
        self.assertEqual(grouped(high,CLASSES),FREQ)
        self.assertAlmostEqual(sum(low)/40,6.6)
        self.assertAlmostEqual(sum(high)/40,7.55)
        self.assertNotEqual(sum(low),sum(high))
    def test_beat_titles(self):self.assertEqual(len(set(b.title for b in BEATS)),32)
    def test_eight_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_beat_duration(self):self.assertEqual(sum(b.duration for b in BEATS),928)
    def test_beat_chapters(self):self.assertEqual(tuple(b.chapter for b in BEATS),tuple(c for c in range(1,9) for _ in range(4)))
    def test_voice_coverage(self):self.assertTrue(all(len(b.voice.split())>=55 for b in BEATS))
    def test_no_score_11(self):self.assertNotIn(11,SCORES)
    def test_all_int_scores(self):self.assertTrue(all(isinstance(x,int) for x in SCORES))
