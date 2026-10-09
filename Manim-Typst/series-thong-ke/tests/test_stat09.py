"""STAT09 numerical invariants and failure cases, with independent rank checks."""
import unittest
from math import isclose
from statistics import median
from stat01.lesson import SCORES
from stat07.lesson import (CLASSES,FREQ,CUM,ASYM,ASYM_FREQ,Interval,
                           PCLASSES,PFREQ,PRACTICE,grouped)
from stat09.lesson import (grouped_median,MedianEstimate,RAW_MEDIAN,MAIN,
                           ALTERNATIVE,EXERCISE,EXERCISE_RAW,BOUND,BOUND_CLASSES,
                           BOUND_COUNTS,BEATS,CHAPTERS,validate)

class STAT09Tests(unittest.TestCase):
    def test_01(self):self.assertTrue(validate())
    def test_02(self):self.assertEqual(len(SCORES),40)
    def test_03(self):self.assertEqual(tuple(FREQ),(6,18,14,2))
    def test_04(self):self.assertEqual(tuple(CUM),(6,24,38,40))
    def test_05(self):self.assertEqual(sum(FREQ),40)
    def test_06(self):self.assertEqual(median(SCORES),7)
    def test_07(self):self.assertEqual(RAW_MEDIAN,7)
    def test_08(self):self.assertEqual(MAIN.rank,20)
    def test_09(self):self.assertEqual(MAIN.class_index,1)
    def test_10(self):self.assertEqual(MAIN.before,6)
    def test_11(self):self.assertEqual(MAIN.frequency,18)
    def test_12(self):self.assertEqual(MAIN.lower,6)
    def test_13(self):self.assertEqual(MAIN.width,2)
    def test_14(self):self.assertAlmostEqual(MAIN.value,6+14/18*2)
    def test_15(self):self.assertTrue(6<MAIN.value<8)
    def test_16(self):self.assertNotEqual(RAW_MEDIAN,MAIN.value)
    def test_17(self):self.assertEqual(tuple(ASYM_FREQ),(6,8,18,8))
    def test_18(self):self.assertEqual(ALTERNATIVE.class_index,2)
    def test_19(self):self.assertAlmostEqual(ALTERNATIVE.value,7+6/18*2)
    def test_20(self):self.assertTrue(7<ALTERNATIVE.value<9)
    def test_21(self):self.assertEqual(sum(ASYM_FREQ),40)
    def test_22(self):self.assertEqual(tuple(PFREQ),(5,7,6,2))
    def test_23(self):self.assertAlmostEqual(EXERCISE.value,4+5/7*2)
    def test_24(self):self.assertEqual(EXERCISE_RAW,5)
    def test_25(self):self.assertEqual(BOUND.value,4)
    def test_26(self):self.assertEqual(BOUND.class_index,2)
    def test_27(self):self.assertEqual(BOUND.before,10)
    def test_28(self):self.assertEqual(BOUND.frequency,7)
    def test_29(self):self.assertEqual(len(BEATS),32)
    def test_30(self):self.assertEqual(len(CHAPTERS),8)
    def test_31(self):self.assertEqual(sum(b.duration for b in BEATS),992)
    def test_32(self):self.assertEqual([b.step for b in BEATS],[1,2,3,4]*8)
    def test_33(self):self.assertEqual(len({b.title for b in BEATS}),32)
    def test_34(self):self.assertTrue(all(len(b.voice.split())>=65 for b in BEATS))
    def test_35(self):
        with self.assertRaises(ValueError):grouped_median(CLASSES,(0,0,0,0))
    def test_36(self):
        with self.assertRaises(ValueError):grouped_median(CLASSES,(6,18,14))
    def test_37(self):
        with self.assertRaises(ValueError):grouped_median(CLASSES,(6,-1,14,2))
    def test_38(self):
        with self.assertRaises(ValueError):grouped_median(CLASSES,(6,18.5,14,2))
    def test_39(self):
        with self.assertRaises(ValueError):grouped_median(CLASSES,(6,float('nan'),14,2))
    def test_40(self):
        with self.assertRaises(ValueError):grouped_median(CLASSES,(6,float('inf'),14,2))
    def test_41(self):
        with self.assertRaises(ValueError):grouped_median((Interval(0,2),Interval(3,5)),(1,3))
    def test_42(self):
        with self.assertRaises(ValueError):grouped_median((Interval(0,2),Interval(1,3)),(1,3))
    def test_43(self):self.assertAlmostEqual(grouped_median((Interval(0,2),),(5,)).value,1)
    def test_44(self):self.assertAlmostEqual(grouped_median((Interval(0,1),Interval(1,2),Interval(2,3)),(0,0,10)).value,2.5)
    def test_45(self):self.assertAlmostEqual(grouped_median((Interval(0,1),Interval(1,2),Interval(2,3)),(1,1,1)).value,1.5)
    def test_46(self):self.assertEqual(grouped(PRACTICE,PCLASSES),PFREQ)
    def test_47(self):self.assertEqual(20,sum(PFREQ))
    def test_48(self):
        # Distinct raw data inside the same intervals may have distinct exact medians.
        a=(4,)*6+(6,)*18+(8,)*14+(10,)*2
        b=(5,)*6+(7,)*18+(9,)*14+(10,)*2
        self.assertEqual(grouped(a,CLASSES),grouped(b,CLASSES))
        self.assertNotEqual(median(a),median(b))
    def test_49(self):
        # Reproduces direct piecewise-linear cumulative interpolation.
        base=6; end=24; left=6;right=8
        x=left+(20-base)/(end-base)*(right-left)
        self.assertTrue(isclose(MAIN.value,x))
    def test_50(self):
        self.assertTrue(all(MAIN.class_index != i or FREQ[i] > 0 for i in range(4)))

if __name__=='__main__':unittest.main()
