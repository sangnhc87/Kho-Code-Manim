"""STAT10 grouped-quartile mathematics, boundary tests, and lesson invariants."""
import unittest
from math import isclose
from statistics import median
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ,ASYM,ASYM_FREQ,Interval,grouped
from stat10.lesson import (grouped_quantile,three_quartiles,school_raw_quartiles,
    RAW,MAIN,ALT,BOUND,BOUND_FREQ,REVERSE,REVERSE_FREQ,IQR,CHAPTERS,BEATS,validate)

class STAT10Tests(unittest.TestCase):
    def test_lesson(self):self.assertTrue(validate())
    def test_size(self):self.assertEqual(len(SCORES),40)
    def test_freq(self):self.assertEqual(FREQ,(6,18,14,2))
    def test_sum(self):self.assertEqual(sum(FREQ),40)
    def test_raw(self):self.assertEqual(RAW,(6,7,8))
    def test_raw_reverse(self):self.assertEqual(school_raw_quartiles(tuple(reversed(SCORES))),RAW)
    def test_raw_odd(self):self.assertEqual(school_raw_quartiles([1,2,3,4,5]),(1.5,3,4.5))
    def test_raw_empty(self):
        with self.assertRaises(ValueError):school_raw_quartiles([])
    def test_raw_single(self):
        with self.assertRaises(ValueError):school_raw_quartiles([3])
    def test_parts(self):self.assertEqual([x.part for x in MAIN],[1,2,3])
    def test_ranks(self):self.assertEqual([x.rank for x in MAIN],[10,20,30])
    def test_indices(self):self.assertEqual([x.index for x in MAIN],[1,1,2])
    def test_before(self):self.assertEqual([x.before for x in MAIN],[6,6,24])
    def test_class_freq(self):self.assertEqual([x.frequency for x in MAIN],[18,18,14])
    def test_lower(self):self.assertEqual([x.left for x in MAIN],[6,6,8])
    def test_width(self):self.assertEqual([x.width for x in MAIN],[2,2,2])
    def test_q1(self):self.assertAlmostEqual(MAIN[0].value,58/9)
    def test_q2(self):self.assertAlmostEqual(MAIN[1].value,68/9)
    def test_q3(self):self.assertAlmostEqual(MAIN[2].value,62/7)
    def test_iqr(self):self.assertAlmostEqual(IQR,152/63)
    def test_order(self):self.assertLessEqual(MAIN[0].value,MAIN[1].value)
    def test_order2(self):self.assertLessEqual(MAIN[1].value,MAIN[2].value)
    def test_inside(self):
        for q in MAIN:self.assertTrue(CLASSES[q.index].left<=q.value<=CLASSES[q.index].right)
    def test_raw_vs_group(self):self.assertNotEqual(RAW,tuple(q.value for q in MAIN))
    def test_alt_freq(self):self.assertEqual(ASYM_FREQ,(6,8,18,8))
    def test_alt_q1(self):self.assertAlmostEqual(ALT[0].value,6.5)
    def test_alt_q2(self):self.assertAlmostEqual(ALT[1].value,23/3)
    def test_alt_q3(self):self.assertAlmostEqual(ALT[2].value,79/9)
    def test_alt_distinct(self):self.assertNotEqual(tuple(q.value for q in ALT),tuple(q.value for q in MAIN))
    def test_bound(self):self.assertEqual(tuple(q.value for q in BOUND),(6,8,10))
    def test_bound_indices(self):self.assertEqual(tuple(q.index for q in BOUND),(1,2,3))
    def test_bound_freq(self):self.assertEqual(BOUND_FREQ,(10,10,10,10))
    def test_reverse_freq(self):self.assertEqual(REVERSE_FREQ,(6,16,16,2))
    def test_reverse_values(self):self.assertEqual(tuple(q.value for q in REVERSE),(6.5,7.75,9.))
    def test_reverse_iqr(self):self.assertAlmostEqual(REVERSE[2].value-REVERSE[0].value,2.5)
    def test_reverse_uniqueness(self):
        candidates=[]
        for x in range(1,33):
            f=(6,x,32-x,2)
            if isclose(grouped_quantile(CLASSES,f,1).value,6.5,abs_tol=1e-11):
                candidates.append(x)
        self.assertEqual(candidates,[16])
    def test_ogive(self):
        knots=((4,0),(6,6),(8,24),(10,38),(12,40))
        for q in MAIN:
            j=q.index
            xa,ya=knots[j];xb,yb=knots[j+1]
            horizontal=xa+(q.rank-ya)/(yb-ya)*(xb-xa)
            self.assertAlmostEqual(horizontal,q.value)
    def test_nondivisible_n(self):
        res=three_quartiles((Interval(0,1),Interval(1,2)),(2,3))
        self.assertEqual([q.rank for q in res],[1.25,2.5,3.75])
        self.assertTrue(res[0].value<=res[1].value<=res[2].value)
    def test_single_nonempty(self):
        q=three_quartiles((Interval(2,4),),(8,))
        self.assertEqual(tuple(x.value for x in q),(2.5,3,3.5))
    def test_zero_frequency(self):
        q=three_quartiles((Interval(0,1),Interval(1,2),Interval(2,3)),(0,0,8))
        self.assertEqual(tuple(x.value for x in q),(2.25,2.5,2.75))
    def test_gap_at_rank(self):
        q=grouped_quantile((Interval(0,1),Interval(1,2),Interval(2,3)),(4,0,12),1)
        self.assertEqual(q.value,2)  # convention: next nonempty bin, boundary nonunique
    def test_bad_empty(self):
        with self.assertRaises(ValueError):grouped_quantile([],[],1)
    def test_bad_length(self):
        with self.assertRaises(ValueError):grouped_quantile(CLASSES,(2,3),1)
    def test_bad_total(self):
        with self.assertRaises(ValueError):grouped_quantile(CLASSES,(0,0,0,0),1)
    def test_bad_negative(self):
        with self.assertRaises(ValueError):grouped_quantile(CLASSES,(1,-1,3,4),1)
    def test_bad_float(self):
        with self.assertRaises(ValueError):grouped_quantile(CLASSES,(1,2.5,3,4),1)
    def test_bad_bool(self):
        with self.assertRaises(ValueError):grouped_quantile(CLASSES,(True,2,3,4),1)
    def test_bad_nan(self):
        with self.assertRaises(ValueError):grouped_quantile(CLASSES,(1,float('nan'),3,4),1)
    def test_bad_inf(self):
        with self.assertRaises(ValueError):grouped_quantile(CLASSES,(1,float('inf'),3,4),1)
    def test_bad_part(self):
        for p in (0,4,False,-1):
            with self.assertRaises(ValueError):grouped_quantile(CLASSES,FREQ,p)
    def test_gap(self):
        with self.assertRaises(ValueError):grouped_quantile((Interval(1,2),Interval(3,4)),(2,4),1)
    def test_overlap(self):
        with self.assertRaises(ValueError):grouped_quantile((Interval(1,3),Interval(2,4)),(2,4),1)
    def test_beats(self):self.assertEqual(len(BEATS),32)
    def test_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_beat_sequence(self):self.assertEqual([b.step for b in BEATS],[1,2,3,4]*8)
    def test_beat_titles(self):self.assertEqual(len({b.title for b in BEATS}),32)
    def test_voice(self):self.assertTrue(all(len(b.voice.split())>48 for b in BEATS))
    def test_duration(self):self.assertEqual(sum(b.duration for b in BEATS),1088)
    def test_bijection_raw_table(self):self.assertEqual(grouped(SCORES,CLASSES),FREQ)
    def test_regroup_same_raw(self):self.assertEqual(grouped(SCORES,ASYM),ASYM_FREQ)
    def test_same_group_different_raw_quartiles(self):
        a=(4,)*6+(6,)*18+(8,)*14+(10,)*2
        b=(5,)*6+(7,)*18+(9,)*14+(10,)*2
        self.assertEqual(grouped(a,CLASSES),grouped(b,CLASSES))
        self.assertNotEqual(school_raw_quartiles(a),school_raw_quartiles(b))

if __name__=='__main__':unittest.main()
