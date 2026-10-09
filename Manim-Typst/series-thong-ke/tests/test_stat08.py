"""Independent numerical checks, formula guards, pedagogy and flow integrity."""
import unittest
from math import isclose
from collections import Counter
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ,ASYM,ASYM_FREQ,PCLASSES,PFREQ,Interval,grouped
from stat08.lesson import *

class TestSTAT08(unittest.TestCase):
    def test_validation(self):self.assertTrue(validate())
    def test_scores_length(self):self.assertEqual(len(SCORES),40)
    def test_total(self):self.assertEqual(sum(SCORES),284)
    def test_exact_mean(self):self.assertEqual(sum(SCORES)/len(SCORES),7.1)
    def test_exact_mode(self):self.assertEqual(Counter(SCORES).most_common(1)[0][0],7)
    def test_groups(self):self.assertEqual(grouped(SCORES,CLASSES),FREQ)
    def test_n(self):self.assertEqual(sum(FREQ),40)
    def test_midpoints(self):self.assertEqual(tuple(i.midpoint for i in CLASSES),(5,7,9,11))
    def test_group_mean(self):self.assertAlmostEqual(estimate_mean(CLASSES,FREQ),7.6)
    def test_group_sum(self):self.assertEqual(sum(i.midpoint*f for i,f in zip(CLASSES,FREQ)),304)
    def test_group_bias(self):self.assertAlmostEqual(GROUPED_MEAN-EXACT_MEAN,.5)
    def test_equalwidth_mode(self):self.assertAlmostEqual(interpolate_mode(CLASSES,FREQ),7.5)
    def test_mode_index(self):self.assertEqual(modal_index(FREQ),1)
    def test_class_interval(self):self.assertEqual((CLASSES[1].left,CLASSES[1].right),(6,8))
    def test_left_difference(self):self.assertEqual(FREQ[1]-FREQ[0],12)
    def test_right_difference(self):self.assertEqual(FREQ[1]-FREQ[2],4)
    def test_mode_midpoint_not_inferred(self):self.assertNotEqual(GROUPED_MODE,CLASSES[1].midpoint)
    def test_asym_groups(self):self.assertEqual(ASYM_FREQ,(6,8,18,8))
    def test_asym_midpoints(self):self.assertEqual(tuple(i.midpoint for i in ASYM),(5,6.5,8,10))
    def test_asym_n(self):self.assertEqual(sum(ASYM_FREQ),40)
    def test_asym_mean(self):self.assertAlmostEqual(ASYM_MEAN,7.65)
    def test_asym_weighted_sum(self):self.assertEqual(sum(i.midpoint*f for i,f in zip(ASYM,ASYM_FREQ)),306)
    def test_asym_density(self):self.assertEqual(tuple(f/i.width for i,f in zip(ASYM,ASYM_FREQ)),(3,8,9,4))
    def test_asym_mode_density(self):self.assertAlmostEqual(ASYM_MODE,22/3)
    def test_asym_modal_index(self):self.assertEqual((3,8,9,4).index(9),2)
    def test_practice_counts(self):self.assertEqual(PFREQ,(5,7,6,2))
    def test_practice_mean(self):self.assertAlmostEqual(PRACTICE_MEAN,5.5)
    def test_practice_mode(self):self.assertAlmostEqual(PRACTICE_MODE,16/3)
    def test_practice_n(self):self.assertEqual(sum(PFREQ),20)
    def test_practice_sum(self):self.assertEqual(sum(i.midpoint*f for i,f in zip(PCLASSES,PFREQ)),110)
    def test_missing_count(self):self.assertEqual(40-6-14-2,18)
    def test_zero_n(self):
        with self.assertRaises(ValueError):estimate_mean(CLASSES,(0,0,0,0))
    def test_missing_interval(self):
        with self.assertRaises(ValueError):estimate_mean(CLASSES,(6,18))
    def test_fractional_count(self):
        with self.assertRaises(ValueError):estimate_mean(CLASSES,(6,18.5,14,2))
    def test_negative_count(self):
        with self.assertRaises(ValueError):estimate_mean(CLASSES,(6,-1,14,2))
    def test_tie_modal_class(self):
        with self.assertRaises(ValueError):modal_index((2,4,4,1))
    def test_all_zero_modal(self):
        with self.assertRaises(ValueError):modal_index((0,0,0))
    def test_reject_unequal_widths_direct_mode(self):
        with self.assertRaises(ValueError):interpolate_mode(ASYM,ASYM_FREQ)
    def test_density_empty(self):
        with self.assertRaises(ValueError):density_modal_mode([],[])
    def test_asym_dense_area(self):
        self.assertEqual(sum(i.width*f/i.width for i,f in zip(ASYM,ASYM_FREQ)),40)
    def test_mode_at_first(self):
        ints=(Interval(0,2),Interval(2,4),Interval(4,6))
        self.assertAlmostEqual(interpolate_mode(ints,(10,5,1)),0+10/15*2)
    def test_mode_at_last(self):
        ints=(Interval(0,2),Interval(2,4),Interval(4,6))
        self.assertAlmostEqual(interpolate_mode(ints,(1,5,10)),4+5/15*2)
    def test_32_beats(self):self.assertEqual(len(BEATS),32)
    def test_8_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_4_beats_chapter(self):self.assertEqual([sum(b.chapter==i for b in BEATS) for i in range(1,9)],[4]*8)
    def test_beat_order(self):self.assertEqual([b.step for b in BEATS],[1,2,3,4]*8)
    def test_unique_titles(self):self.assertEqual(len({b.title for b in BEATS}),32)
    def test_voice(self):self.assertTrue(all(len(b.voice.split())>=55 for b in BEATS))
    def test_duration(self):self.assertEqual(sum(b.duration for b in BEATS),960)
    def test_estimate_bounded(self):self.assertTrue(5<=GROUPED_MEAN<=11)
    def test_sample_minmax(self):self.assertEqual((min(SCORES),max(SCORES)),(4,10))
    def test_distinct_origin_same_group(self):
        low=(4,)*6+(6,)*18+(8,)*14+(10,)*2
        high=(5,)*6+(7,)*18+(9,)*14+(10,)*2
        self.assertEqual(grouped(low,CLASSES),grouped(high,CLASSES))
        self.assertNotEqual(sum(low),sum(high))
    def test_asym_mode_inside_modal_class(self):self.assertTrue(ASYM[2].left<ASYM_MODE<ASYM[2].right)
    def test_grouped_mode_inside_modal_class(self):self.assertTrue(CLASSES[1].left<GROUPED_MODE<CLASSES[1].right)

if __name__=='__main__':unittest.main()
