import math
import unittest
from collections import Counter
from statistics import mean,median,multimode
from stat01.lesson import (
    SCORES,SORTED_SCORES,FREQUENCY,RELATIVE,CUMULATIVE,
    N,BEATS,CHAPTERS,validate
)

class TestSTAT01Data(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_count(self):self.assertEqual(N,40)
    def test_allowed_scores(self):self.assertTrue(all(0<=x<=10 for x in SCORES))
    def test_raw_length_preserved(self):self.assertEqual(len(SORTED_SCORES),N)
    def test_sorted_preserves_multiset(self):self.assertEqual(Counter(SCORES),Counter(SORTED_SCORES))
    def test_sorted_ascending(self):self.assertEqual(SORTED_SCORES,tuple(sorted(SCORES)))
    def test_exact_frequency(self):
        self.assertEqual(FREQUENCY,{4:2,5:4,6:8,7:10,8:8,9:6,10:2})
    def test_mode(self):self.assertEqual(multimode(SCORES),[7])
    def test_sum(self):self.assertEqual(sum(SCORES),284)
    def test_mean_teaser(self):self.assertEqual(mean(SCORES),7.1)
    def test_median_teaser(self):self.assertEqual(median(SCORES),7)
    def test_frequency_sum(self):self.assertEqual(sum(FREQUENCY.values()),40)
    def test_relative(self):
        for x,c in FREQUENCY.items():self.assertAlmostEqual(RELATIVE[x],c/40)
    def test_relative_sum(self):self.assertAlmostEqual(sum(RELATIVE.values()),1.)
    def test_seven_percent(self):self.assertEqual(100*RELATIVE[7],25)
    def test_eight_percent(self):self.assertEqual(100*RELATIVE[8],20)
    def test_ge_8_count(self):self.assertEqual(sum(1 for x in SCORES if x>=8),16)
    def test_ge_8_ratio(self):self.assertEqual(sum(RELATIVE[x] for x in (8,9,10)),.4)
    def test_nine_exact(self):self.assertEqual(FREQUENCY[9],6)
    def test_cumulative_at_seven(self):self.assertEqual(CUMULATIVE[7],24)
    def test_cumulative_final(self):self.assertEqual(CUMULATIVE[10],N)
    def test_classes_non_overlap(self):
        intervals=[(0,3),(4,5),(6,7),(8,10)]
        self.assertEqual(sum(sum(lo<=x<=hi for x in SCORES) for lo,hi in intervals),40)

class TestStoryboard(unittest.TestCase):
    def test_chapter_count(self):self.assertEqual(len(CHAPTERS),8)
    def test_beat_count(self):self.assertEqual(len(BEATS),32)
    def test_four_beats_per_chapter(self):
        self.assertEqual([sum(b.chapter==c for b in BEATS) for c in range(1,9)],[4]*8)
    def test_steps_are_in_order(self):
        self.assertEqual([b.step for b in BEATS],[i for _ in range(8) for i in range(1,5)])
    def test_title_nonempty(self):self.assertTrue(all(b.title.strip() for b in BEATS))
    def test_voice_lesson_complete(self):self.assertTrue(all(len(b.narration.split())>=28 for b in BEATS))
    def test_beat_duration(self):self.assertTrue(all(b.duration>=16 for b in BEATS))
    def test_total_duration_not_short(self):self.assertGreaterEqual(sum(b.duration for b in BEATS),640)
    def test_no_recycled_beat_titles(self):self.assertEqual(len(set(b.title for b in BEATS)),32)
    def test_text_utf8_vi(self):self.assertIn('thống kê', ' '.join(x.narration for x in BEATS).lower())
    def test_synthetic_disclosure(self):
        self.assertIn('không phải dữ liệu cá nhân',BEATS[3].narration)

if __name__=='__main__':unittest.main()
