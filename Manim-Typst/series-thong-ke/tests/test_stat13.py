"""STAT13 math, UI-safety and GitHub source regression tests."""
import unittest,math,ast,re
from pathlib import Path
from stat01.lesson import SCORES
from stat07.lesson import CLASSES,FREQ
from stat13.lesson import (A,B,PA,PB,EA,EB,EXERCISE_A,EXERCISE_B,
  profile,compare,count_at_least,GROUPED_A,GROUPED_B,ORIGINAL,BEATS,CHAPTERS,validate)
from scripts.build_stat13_typst import FORMULAS,create_sources
ROOT=Path(__file__).resolve().parents[1]

class STAT13Tests(unittest.TestCase):
    def test_validate(self):
        self.assertTrue(validate())
    def test_sizes_and_scores_range(self):
        self.assertEqual((len(A),len(B)),(10,10))
        self.assertTrue(all(0<=v<=10 for v in A+B))
    def test_means(self):
        self.assertEqual(sum(A),sum(B))
        self.assertAlmostEqual(PA.mean,7)
        self.assertAlmostEqual(PB.mean,7)
    def test_median(self):
        self.assertEqual((PA.median,PB.median),(7,7))
    def test_modes(self):
        self.assertEqual((PA.mode,PB.mode),((7,), (7,)))
    def test_quartiles_even(self):
        self.assertEqual((PA.q1,PA.q3,PB.q1,PB.q3),(6,8,4,10))
    def test_quartiles_odd_skip_middle(self):
        vals=[2,3,4,5,7,8,9,11,12]
        p=profile(vals)
        self.assertEqual((p.q1,p.median,p.q3),(3.5,7,10))
    def test_ranges_and_iqrs(self):
        self.assertEqual((PA.value_range,PA.iqr,PB.value_range,PB.iqr),(4,2,6,6))
    def test_population_style_variance(self):
        self.assertAlmostEqual(PA.variance,12/10)
        self.assertAlmostEqual(PB.variance,54/10)
        self.assertAlmostEqual(PA.sd,math.sqrt(1.2))
        self.assertAlmostEqual(PB.sd,math.sqrt(5.4))
    def test_shuffled_input_invariant(self):
        self.assertEqual(PA,profile(tuple(reversed(A))))
        self.assertEqual(PB,profile(tuple(reversed(B))))
    def test_all_constant(self):
        p=profile((7,)*10)
        self.assertEqual((p.variance,p.sd,p.iqr,p.value_range),(0,0,0,0))
        self.assertEqual(p.mode,(7,))
    def test_two_observations(self):
        p=profile([1,9])
        self.assertEqual((p.q1,p.median,p.q3),(1,5,9))
    def test_empty_and_non_numeric(self):
        for vals in ([],[True,8],['7',8],[None,5],[1]):
            with self.subTest(vals=vals),self.assertRaises(ValueError):profile(vals)
    def test_shift_invariance_and_scale(self):
        for t in (-3,0,7):
            p=profile([v+t for v in A])
            self.assertAlmostEqual(p.sd,PA.sd)
            self.assertAlmostEqual(p.iqr,PA.iqr)
        p=profile([2*v for v in A])
        self.assertAlmostEqual(p.variance,4*PA.variance)
        self.assertAlmostEqual(p.sd,2*PA.sd)
    def test_comparison_returns_numbers_not_value_judgments(self):
        c=compare(A,B)
        self.assertAlmostEqual(c['mean_delta'],0)
        self.assertLess(c['sd_delta'],0)
        self.assertLess(c['iqr_delta'],0)
        self.assertTrue(c['same_n'])
    def test_threshold_6(self):
        self.assertEqual((count_at_least(A,6),count_at_least(B,6)),(9,7))
    def test_threshold_9(self):
        self.assertEqual((count_at_least(A,9),count_at_least(B,9)),(1,3))
    def test_edge_thresholds(self):
        self.assertEqual(count_at_least(A,0),len(A))
        self.assertEqual(count_at_least(B,100),0)
    def test_grouped_approximations(self):
        self.assertEqual(FREQ,(6,18,14,2))
        self.assertEqual((GROUPED_A.n,GROUPED_B.n),(40,40))
        self.assertAlmostEqual(GROUPED_A.mean,GROUPED_B.mean)
        self.assertAlmostEqual(GROUPED_A.variance,2.44)
        self.assertAlmostEqual(GROUPED_B.variance,4.44)
        self.assertAlmostEqual(ORIGINAL.mean,7.1)
    def test_exercise_mean_median_quartiles(self):
        self.assertEqual((EA.n,EB.n),(8,8))
        self.assertEqual((EA.mean,EB.mean),(7,7))
        self.assertEqual((EA.median,EB.median),(7,7))
        self.assertEqual((EA.q1,EA.q3),(6,8))
        self.assertEqual((EB.q1,EB.q3),(4.5,9.5))
    def test_exercise_variance(self):
        self.assertAlmostEqual(EA.variance,1.5)
        self.assertAlmostEqual(EB.variance,5.5)
    def test_lesson_complete(self):
        self.assertEqual(len(BEATS),32)
        self.assertEqual(len(CHAPTERS),8)
        self.assertEqual(set((b.chapter,b.step) for b in BEATS),
                         {(i,j) for i in range(1,9) for j in range(1,5)})
        self.assertGreater(sum(len(b.voice.split()) for b in BEATS),1900)
        self.assertGreaterEqual(sum(b.duration for b in BEATS),1000)
    def test_formula_generation(self):
        self.assertEqual(len(FORMULAS),8)
        create_sources()
        for key in FORMULAS:self.assertTrue((ROOT/f'typst/stat13/{key}.typ').exists())
    def test_scene_ast_and_classroom_ui(self):
        scene=(ROOT/'stat13/scene.py').read_text(encoding='utf-8')
        ast.parse(scene)
        self.assertNotIn('NHỊP',scene.upper())
        self.assertNotIn('MANIM-TYPST',scene.upper())
        self.assertNotIn('MANIM–TYPST',scene.upper())
        self.assertIn('Thầy Nguyễn Văn Sang',scene)
        self.assertIn('THỐNG KÊ 12 / SO SÁNH HAI MẪU',scene)
        self.assertIn('STAT13_SMOKE',scene)
    def test_male_voice(self):
        prep=(ROOT/'scripts/prepare_stat13.py').read_text(encoding='utf-8')
        self.assertIn('vi-VN-NamMinhNeural',prep)
        self.assertNotIn('HoaiMyNeural',prep)
    def test_workflow_prerequisites(self):
        wf=(ROOT/'.github/workflows/render-stat13.yml').read_text(encoding='utf-8')
        for required in ('check_stat13_states.py','build_stat13_typst.py',
              'prepare_stat13.py','STAT13_SMOKE','qa_stat13.py','1920,1080',
              '854,480','voice','upload-artifact'):
            self.assertIn(required,wf)
    def test_required_files(self):
        required=['stat13/lesson.py','stat13/scene.py','stat13/runtime_plan.json',
            'scripts/build_stat13_typst.py','scripts/prepare_stat13.py',
            'scripts/check_stat13_states.py','scripts/qa_stat13.py',
            '.github/workflows/render-stat13.yml']
        for name in required:
            with self.subTest(name=name):self.assertTrue((ROOT/name).is_file())

if __name__=='__main__':unittest.main()
