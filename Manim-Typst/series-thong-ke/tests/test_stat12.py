import unittest, math, ast
from pathlib import Path
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ,Interval
from stat12.lesson import (grouped_stats,raw_stats,MAIN,RAW,OTHER,OTHER_FREQ,
   OUTLIER_RAW,PRACTICE,PRACTICE_CLASSES,PRACTICE_FREQ,inverse_counts,
   BEATS,CHAPTERS,validate)
from scripts.build_stat12_typst import FORMULAS
ROOT=Path(__file__).resolve().parents[1]

class TestSTAT12(unittest.TestCase):
    def test_main_moments(self):
        self.assertEqual((MAIN.n,RAW.n),(40,40))
        self.assertAlmostEqual(MAIN.mean,7.6)
        self.assertAlmostEqual(MAIN.variance,2.44)
        self.assertAlmostEqual(MAIN.second,60.2)
        self.assertAlmostEqual(MAIN.sd,math.sqrt(2.44))
        self.assertAlmostEqual(RAW.mean,7.1)
        self.assertAlmostEqual(RAW.variance,2.29)
    def test_independent_expand_grouped(self):
        data=[cl.midpoint for cl,f in zip(CLASSES,FREQ) for _ in range(f)]
        self.assertAlmostEqual(raw_stats(data).variance,MAIN.variance)
        self.assertAlmostEqual(sum(x*x for x in data)/len(data)-MAIN.mean**2,MAIN.variance)
    def test_same_mean_different_spread(self):
        self.assertEqual(OTHER_FREQ,(9,19,3,9))
        self.assertAlmostEqual(MAIN.mean,OTHER.mean)
        self.assertAlmostEqual(OTHER.variance,4.44)
        self.assertGreater(OTHER.sd,MAIN.sd)
        data=[cl.midpoint for cl,f in zip(CLASSES,OTHER_FREQ) for _ in range(f)]
        self.assertAlmostEqual(raw_stats(data).variance,4.44)
    def test_outlier_replace_exact_one_ten(self):
        data=list(SCORES);data[data.index(10)]=30
        res=raw_stats(data)
        self.assertAlmostEqual(res.mean,7.6)
        self.assertAlmostEqual(res.variance,14.94)
        self.assertAlmostEqual(OUTLIER_RAW.variance,res.variance)
    def test_transform_formula(self):
        base=[cl.midpoint for cl,f in zip(CLASSES,FREQ) for _ in range(f)]
        for a,b in ((1,3),(2,0),(-2,3),(.5,-1)):
            t=raw_stats([a*x+b for x in base])
            self.assertAlmostEqual(t.variance,a*a*MAIN.variance)
            self.assertAlmostEqual(t.sd,abs(a)*MAIN.sd)
    def test_practice_and_inverse(self):
        self.assertEqual(PRACTICE_FREQ,(2,8,6,4))
        self.assertEqual(inverse_counts(2),PRACTICE_FREQ)
        self.assertAlmostEqual(PRACTICE.mean,4.2)
        self.assertAlmostEqual(PRACTICE.second,21)
        self.assertAlmostEqual(PRACTICE.variance,3.36)
        for x in range(7):
            f=inverse_counts(x);self.assertEqual(sum(f),20)
            self.assertAlmostEqual(grouped_stats(PRACTICE_CLASSES,f).mean,4.8-.3*x)
    def test_invalid_inputs(self):
        invalid=[(),(0,0,0,0),(1,-1,2,2),(1,1.5,2,2),(True,1,2,2),(1,2,3)]
        for freq in invalid:
            with self.subTest(freq=freq),self.assertRaises(ValueError):grouped_stats(CLASSES,freq)
        with self.assertRaises(ValueError):grouped_stats([Interval(0,1),Interval(2,3)],(2,2))
        with self.assertRaises(ValueError):raw_stats([])
        for x in (-1,7,2.5,True):
            with self.assertRaises(ValueError):inverse_counts(x)
    def test_script_and_typst_presence(self):
        self.assertTrue(validate())
        self.assertEqual(len(BEATS),32)
        self.assertEqual(len(CHAPTERS),8)
        self.assertEqual(len(FORMULAS),8)
        self.assertEqual(sum(b.duration for b in BEATS),1152)
        files=['scripts/prepare_stat12.py','scripts/build_stat12_typst.py',
               'scripts/check_stat12_states.py','scripts/qa_stat12.py',
               '.github/workflows/render-stat12.yml','stat12/scene.py']
        for f in files:self.assertTrue((ROOT/f).is_file(),f)
    def test_classroom_display(self):
        text=(ROOT/'stat12/scene.py').read_text(encoding='utf-8')
        ast.parse(text)
        self.assertNotIn('NHỊP',text.upper())
        self.assertNotIn('MANIM-TYPST',text.upper())
        self.assertIn('Thầy Nguyễn Văn Sang',text)
        self.assertIn('THỐNG KÊ 12 / PHƯƠNG SAI',text)
        script=(ROOT/'scripts/prepare_stat12.py').read_text(encoding='utf-8')
        self.assertIn('vi-VN-NamMinhNeural',script)
        self.assertNotIn('HoaiMyNeural',script)

if __name__=='__main__':unittest.main()
