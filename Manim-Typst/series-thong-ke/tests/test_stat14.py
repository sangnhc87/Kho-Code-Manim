"""STAT14 math, instructional accuracy, build checks, and visible UI regression."""
import ast
import unittest
from math import isclose, sqrt
from pathlib import Path
from stat14.lesson import (QUEUE_A, QUEUE_B, QUEUE_OUTLIER, PA, PB, PO,
  RAW, GROUPED, EA, EB, EXERCISE_A, EXERCISE_B, COHORTS,
  count_at_most, weighted_mean, decision, BEATS, CHAPTERS,validate)
from scripts.build_stat14_typst import FORMULAS,create_sources

ROOT=Path(__file__).resolve().parents[1]
class TestSTAT14(unittest.TestCase):
    def test_dataset_integrity(self):
        self.assertEqual(len(QUEUE_A),10);self.assertEqual(len(QUEUE_B),10)
        self.assertEqual(sum(QUEUE_A),80);self.assertEqual(sum(QUEUE_B),80)
        self.assertTrue(all(v>=0 for v in QUEUE_A+QUEUE_B))
    def test_center(self):
        self.assertEqual((PA.mean,PB.mean,PA.median,PB.median),(8,8,8,8))
    def test_quartiles(self):
        self.assertEqual((PA.q1,PA.q3,PA.iqr),(7,9,2))
        self.assertEqual((PB.q1,PB.q3,PB.iqr),(5,10,5))
    def test_ranges(self):
        self.assertEqual((PA.value_range,PB.value_range),(4,13))
    def test_dispersion(self):
        self.assertTrue(isclose(PA.variance,1.2))
        self.assertTrue(isclose(PB.variance,15))
        self.assertTrue(isclose(PA.sd,sqrt(1.2)))
        self.assertTrue(isclose(PB.sd,sqrt(15)))
    def test_threshold_10(self):
        self.assertEqual((count_at_most(QUEUE_A,10),count_at_most(QUEUE_B,10)),(10,8))
    def test_threshold_5(self):
        self.assertEqual((count_at_most(QUEUE_A,5),count_at_most(QUEUE_B,5)),(0,3))
    def test_limit_inclusive(self):
        self.assertEqual(count_at_most(QUEUE_B,2),1)
        self.assertEqual(count_at_most(QUEUE_B,3),2)
        self.assertEqual(count_at_most(QUEUE_B,15),10)
    def test_empty_limit(self):
        self.assertEqual(count_at_most([],10),0)
    def test_nonfinite_threshold_rejected(self):
        for v in (float('nan'),float('inf'),float('-inf')):
            with self.subTest(v=v),self.assertRaises(ValueError):count_at_most(QUEUE_A,v)
    def test_decision_dispersion(self):
        winner,first,second=decision(QUEUE_A,QUEUE_B,'consistency')
        self.assertEqual(winner,'A');self.assertLess(first,second)
    def test_decision_goals(self):
        self.assertEqual(decision(QUEUE_A,QUEUE_B,'at_most',10),('A',10,8))
        self.assertEqual(decision(QUEUE_A,QUEUE_B,'at_most',5),('B',0,3))
        self.assertEqual(decision(QUEUE_A,QUEUE_A,'at_most',10),('TIE',10,10))
        self.assertEqual(decision(QUEUE_A,QUEUE_B,'at_most',0),('TIE',0,0))
    def test_invalid_objective(self):
        with self.assertRaises(ValueError):decision(QUEUE_A,QUEUE_B,'fast')
        with self.assertRaises(ValueError):decision(QUEUE_A,QUEUE_B,'at_most')
    def test_outlier_one_edit_only(self):
        self.assertEqual(QUEUE_OUTLIER[:-1],QUEUE_A[:-1])
        self.assertEqual(QUEUE_OUTLIER[-1],30)
        self.assertEqual((PO.mean,PO.median,PO.iqr),(10,8,2))
        self.assertTrue(isclose(PO.variance,45.2))
    def test_grouped_vs_raw(self):
        self.assertTrue(isclose(RAW.mean,7.1))
        self.assertTrue(isclose(RAW.variance,2.29))
        self.assertTrue(isclose(GROUPED.mean,7.6))
        self.assertTrue(isclose(GROUPED.variance,2.44))
        self.assertEqual(GROUPED.n,40)
    def test_weighted_mean(self):
        self.assertTrue(isclose(weighted_mean(COHORTS),6.5))
        self.assertTrue(isclose(weighted_mean(((10,8),(10,6))),7))
        self.assertTrue(isclose(weighted_mean(((3,1.0),(1,5.0))),2.0))
    def test_weighted_invalid(self):
        for data in ((),((0,8),),((-1,8),),((True,8),),((10,float('nan')),),((2,float('inf')),),((1,'8'),)):
            with self.subTest(data=data),self.assertRaises(ValueError):weighted_mean(data)
    def test_exercise_correct(self):
        self.assertEqual((EA.n,EB.n),(8,8))
        self.assertEqual((EA.mean,EB.mean,EA.median,EB.median),(8,8,8,8))
        self.assertEqual((EA.q1,EA.q3,EB.q1,EB.q3),(7,8.5,6,10))
        self.assertEqual((EA.iqr,EB.iqr),(1.5,4))
        self.assertEqual((EA.value_range,EB.value_range),(5,12))
        self.assertTrue(isclose(EA.variance,2))
        self.assertTrue(isclose(EB.variance,11.5))
    def test_exercise_threshold(self):
        self.assertEqual((count_at_most(EXERCISE_A,5),count_at_most(EXERCISE_B,5)),(0,2))
    def test_complete_lesson(self):
        self.assertTrue(validate())
        self.assertEqual(len(CHAPTERS),8)
        self.assertEqual(len(BEATS),32)
        self.assertEqual({(x.chapter,x.step) for x in BEATS},
                 {(i,j) for i in range(1,9) for j in range(1,5)})
        self.assertGreater(sum(len(x.voice.split()) for x in BEATS),2000)
        self.assertGreaterEqual(sum(x.duration for x in BEATS),1100)
    def test_formula_sources(self):
        self.assertEqual(len(FORMULAS),8)
        create_sources()
        for key in FORMULAS:
            self.assertTrue((ROOT/f'typst/stat14/{key}.typ').exists())
    def test_no_internal_labels_and_footer(self):
        scene=(ROOT/'stat14/scene.py').read_text(encoding='utf-8')
        ast.parse(scene)
        for forbidden in ('NHỊP','MANIM-TYPST','MANIM–TYPST','DEBUG','STEP 2/4'):
            self.assertNotIn(forbidden,scene.upper())
        self.assertIn('Thầy Nguyễn Văn Sang',scene)
        self.assertIn('THỐNG KÊ 14 / BÀI TOÁN VẬN DỤNG',scene)
        self.assertIn('STAT14_SMOKE',scene)
    def test_male_voice_config(self):
        p=(ROOT/'scripts/prepare_stat14.py').read_text(encoding='utf-8')
        self.assertIn('vi-VN-NamMinhNeural',p)
        self.assertNotIn('HoaiMyNeural',p)
    def test_action_pipeline(self):
        workflow=(ROOT/'.github/workflows/render-stat14.yml').read_text(encoding='utf-8')
        for token in ('test','check_stat14_states.py','build_stat14_typst.py','prepare_stat14.py',
                'STAT14_SMOKE','qa_stat14.py','1920,1080','854,480','voice','upload-artifact'):
            self.assertIn(token,workflow)
    def test_complete_delivery(self):
        for filename in ('stat14/lesson.py','stat14/scene.py','stat14/runtime_plan.json',
           '.github/workflows/render-stat14.yml','scripts/prepare_stat14.py',
           'scripts/qa_stat14.py','scripts/build_stat14_typst.py','scripts/check_stat14_states.py'):
            with self.subTest(filename=filename):self.assertTrue((ROOT/filename).is_file())
if __name__=='__main__':unittest.main()
