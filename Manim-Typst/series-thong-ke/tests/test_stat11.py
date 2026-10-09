import unittest
import math
from pathlib import Path
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ,Interval
from stat11.lesson import (MAIN,RAW_R,RAW_Q,RAW_IQR,COMPARE,UNIFORM,SHIFTED_MAIN,
                           SCALED_MAIN,EDGE_SPAN,BEATS,CHAPTERS,grouped_range,
                           grouped_spread,validate)

ROOT=Path(__file__).resolve().parents[1]
class TestSTAT11(unittest.TestCase):
    def test_main_data(self):
        self.assertEqual(FREQ,(6,18,14,2))
        self.assertEqual(RAW_R,6)
        self.assertEqual(RAW_Q,(6,7,8))
        self.assertEqual(RAW_IQR,2)
        self.assertEqual(MAIN.span,8)
        self.assertAlmostEqual(MAIN.q1,58/9)
        self.assertAlmostEqual(MAIN.q3,62/7)
        self.assertAlmostEqual(MAIN.iqr,152/63)
    def test_uniform(self):
        self.assertEqual(UNIFORM,(10,10,10,10))
        self.assertEqual(COMPARE.span,MAIN.span)
        self.assertAlmostEqual(COMPARE.q1,6)
        self.assertAlmostEqual(COMPARE.q3,10)
        self.assertAlmostEqual(COMPARE.iqr,4)
    def test_shift_scale(self):
        self.assertEqual(SHIFTED_MAIN.span,8)
        self.assertAlmostEqual(SHIFTED_MAIN.iqr,MAIN.iqr)
        self.assertEqual(SCALED_MAIN.span,16)
        self.assertAlmostEqual(SCALED_MAIN.iqr,2*MAIN.iqr)
    def test_empty_first_and_last(self):
        self.assertEqual(EDGE_SPAN,6)
        self.assertEqual(grouped_range(CLASSES,(0,5,5,0)),4)
        self.assertEqual(grouped_range(CLASSES,(0,0,4,0)),2)
    def test_invalid(self):
        for freq in ((),(0,0,0,0),(1,2),(-1,2,3,4),(1,2,3,4.2)):
            with self.assertRaises(ValueError):grouped_range(CLASSES,freq)
        with self.assertRaises(ValueError):grouped_range((Interval(4,6),Interval(7,8)),(1,1))
        with self.assertRaises(ValueError):grouped_spread(CLASSES,(0,0,0,0))
    def test_beats(self):
        self.assertTrue(validate())
        self.assertEqual(len(BEATS),32)
        self.assertEqual(len(CHAPTERS),8)
        self.assertEqual(sum(x.duration for x in BEATS),1024)
        self.assertEqual(len(set(x.title for x in BEATS)),32)
    def test_male_default_and_credits(self):
        for n in range(1,12):
            s=(ROOT/f'stat{n:02d}'/'scene.py').read_text(encoding='utf-8')
            self.assertIn('Thầy Nguyễn Văn Sang',s)
            # Only enforce footer/credits branding, not docstrings about code technology
            for line in s.splitlines():
                if '0,-3.5' in line or '0,-3.58' in line:
                    self.assertNotIn('MANIM',line.upper())
        for file in (ROOT/'scripts').glob('prepare*.py'):
            text=file.read_text(encoding='utf-8')
            self.assertIn('vi-VN-NamMinhNeural',text)
            self.assertNotIn('HoaiMyNeural',text)

if __name__=='__main__':unittest.main()
