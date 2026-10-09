"""STAT06 regression tests; do not depend on optional Manim or Typst install."""
from __future__ import annotations
import ast,json,math,statistics,unittest
from pathlib import Path
from stat01.lesson import SCORES
from stat06.lesson import (stats,variance_from_freq,FREQ,BASE,A,B,SA,SB,
                           OUTLIER,OUTLIER_DATA,EX,EX2,SEX,SEX2,BEATS,CHAPTERS,validate)
ROOT=Path(__file__).resolve().parents[1]

class MathTests(unittest.TestCase):
    def test_forty_points(self):self.assertEqual(len(SCORES),40)
    def test_frequency(self):self.assertEqual(FREQ,{4:2,5:4,6:8,7:10,8:8,9:6,10:2})
    def test_stats_total(self):self.assertEqual(BASE['total'],284)
    def test_stats_squares(self):self.assertEqual(BASE['sumsq'],2108)
    def test_mean(self):self.assertAlmostEqual(BASE['mean'],7.1)
    def test_var(self):self.assertAlmostEqual(BASE['variance'],2.29)
    def test_standard_deviation(self):self.assertAlmostEqual(BASE['sd'],math.sqrt(2.29))
    def test_independent_python_pvariance(self):self.assertAlmostEqual(statistics.pvariance(SCORES),2.29)
    def test_independent_python_pstdev(self):self.assertAlmostEqual(statistics.pstdev(SCORES),math.sqrt(2.29))
    def test_not_n_minus_one(self):self.assertNotAlmostEqual(statistics.variance(SCORES),BASE['variance'])
    def test_freq_independent(self):self.assertAlmostEqual(variance_from_freq(FREQ),2.29)
    def test_variance_from_freq_rejects_empty(self):
        with self.assertRaises(ValueError):variance_from_freq({})
    def test_freq_rejects_negative(self):
        with self.assertRaises(ValueError):variance_from_freq({1:-1,2:2})
    def test_freq_rejects_fraction(self):
        with self.assertRaises(ValueError):variance_from_freq({1:1.5,2:2})
    def test_stats_rejects_empty(self):
        with self.assertRaises(ValueError):stats([])
    def test_singleton(self):self.assertEqual(stats([7])['variance'],0.0)
    def test_all_equal(self):self.assertEqual(stats([3,3,3,3])['sd'],0.0)
    def test_reorder_invariance(self):self.assertAlmostEqual(stats(reversed(SCORES))['variance'],2.29)
    def test_comparison_means(self):self.assertEqual((SA['mean'],SB['mean']),(7.0,7.0))
    def test_comparison_variances(self):self.assertEqual((SA['variance'],SB['variance']),(2.0,18.0))
    def test_comparison_stdev(self):self.assertAlmostEqual(SB['sd'],3*SA['sd'])
    def test_deviation_cancel(self):self.assertEqual(sum(x-SA['mean'] for x in A),0)
    def test_squares_A(self):self.assertEqual(sum((x-7)**2 for x in A),10)
    def test_affine_translation(self):self.assertAlmostEqual(stats([x+3 for x in A])['variance'],2)
    def test_affine_dilation(self):self.assertAlmostEqual(stats([2*x for x in A])['variance'],8)
    def test_affine_negative(self):self.assertAlmostEqual(stats([-3*x+2 for x in A])['variance'],18)
    def test_affine_stdev(self):self.assertAlmostEqual(stats([3*x+1 for x in A])['sd'],3*SA['sd'])
    def test_outlier_replace_one(self):self.assertEqual(len(OUTLIER_DATA),40)
    def test_outlier_total(self):self.assertEqual(OUTLIER['total'],304)
    def test_outlier_sumsq(self):self.assertEqual(OUTLIER['sumsq'],2908)
    def test_outlier_mean(self):self.assertAlmostEqual(OUTLIER['mean'],7.6)
    def test_outlier_var(self):self.assertAlmostEqual(OUTLIER['variance'],14.94)
    def test_outlier_sd(self):self.assertAlmostEqual(OUTLIER['sd'],math.sqrt(14.94))
    def test_exercise_mean(self):self.assertEqual(SEX['mean'],6)
    def test_exercise_var(self):self.assertEqual(SEX['variance'],8)
    def test_exercise_changed_mean(self):self.assertEqual(SEX2['mean'],8)
    def test_exercise_changed_var(self):self.assertEqual(SEX2['variance'],40)
    def test_validate(self):self.assertTrue(validate())

class ProductionTests(unittest.TestCase):
    def test_eight_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_thirty_two_beats(self):self.assertEqual(len(BEATS),32)
    def test_order_chapters(self):self.assertEqual([b.chapter for b in BEATS], [i for i in range(1,9) for _ in range(4)])
    def test_order_steps(self):self.assertEqual([b.step for b in BEATS],[1,2,3,4]*8)
    def test_minimum_narration(self):self.assertTrue(all(len(b.voice.split())>=40 for b in BEATS))
    def test_unique_titles(self):self.assertEqual(len(set(b.title for b in BEATS)),32)
    def test_duration(self):self.assertEqual(sum(b.duration for b in BEATS),912)
    def test_independent_lesson(self):self.assertNotIn('from manim import',(ROOT/'stat06/lesson.py').read_text())
    def test_scene_ast(self):ast.parse((ROOT/'stat06/scene.py').read_text())
    def test_scene_names(self):
        s=(ROOT/'stat06/scene.py').read_text()
        for needle in ['class STAT06(Scene):','class STAT06_SMOKE(STAT06):','VISUALS=(chap1,chap2,chap3,chap4,chap5,chap6,chap7,chap8)']:
            self.assertIn(needle,s)
    def test_formula_count(self):
        from scripts.build_stat06_typst import FORMULAS
        self.assertEqual(len(FORMULAS),8)
    def test_typst_sources(self):self.assertEqual(len(list((ROOT/'typst/stat06').glob('*.typ'))),8)
    def test_prepared_plan(self):
        data=json.loads((ROOT/'stat06/runtime_plan.json').read_text())
        self.assertEqual((data['scene'],data['chapters'],len(data['beats'])),('STAT06',8,32))
        self.assertEqual(data['duration_expected'],912)
    @unittest.skipUnless((ROOT/"STAT06_vi.srt").exists(),"skip")
    def test_srt(self):self.assertIn('00:00:00,000 -->',(ROOT/'STAT06_vi.srt').read_text())
    def test_workflow_smoke(self):self.assertIn('STAT06_SMOKE',(ROOT.parent.parent/'.github/workflows/render-stat06.yml').read_text())
    def test_workflow_qa(self):self.assertIn('scripts/qa_stat06.py',(ROOT.parent.parent/'.github/workflows/render-stat06.yml').read_text())
    def test_workflow_typst(self):self.assertIn('scripts/build_stat06_typst.py',(ROOT.parent.parent/'.github/workflows/render-stat06.yml').read_text())
    def test_voice_on_fails(self):self.assertIn('if speech<=1:raise RuntimeError',(ROOT/'scripts/prepare_stat06.py').read_text())
    def test_qa_checks_sound(self):self.assertIn("a.voice=='on' and audio is None",(ROOT/'scripts/qa_stat06.py').read_text())
    def test_numerical_tolerance_qa(self):self.assertIn('abs(length-expected)>3.0',(ROOT/'scripts/qa_stat06.py').read_text())

if __name__=='__main__':unittest.main()
