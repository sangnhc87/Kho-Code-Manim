"""Regression tests: Pearson/OLS arithmetic, scene hygiene and reproducible delivery."""
import ast,json,math,unittest
from pathlib import Path
from stat17.lesson import (X,Y,NEGATIVE_Y,CURVED_Y,OUTLIER_Y,PRACTICE_X,PRACTICE_Y,
    BEATS,CHAPTERS,statistics,fitted,residuals,losses,pairs,decimal,validate)
from scripts.build_stat17_typst import FORMULAS,create_sources
ROOT=Path(__file__).resolve().parents[1]

class TestSTAT17(unittest.TestCase):
    def setUp(self):self.s=statistics()
    def test_data_count(self):self.assertEqual((len(X),len(Y)),(8,8))
    def test_exact_data(self):self.assertEqual((X,Y),((1,2,3,4,5,6,7,8),(2,4,3,5,4,6,7,9)))
    def test_mean(self):self.assertEqual((self.s['mx'],self.s['my']),(4.5,5))
    def test_sums(self):self.assertEqual((self.s['sxx'],self.s['sxy'],self.s['syy']),(42,36,36))
    def test_slope(self):self.assertAlmostEqual(self.s['slope'],6/7)
    def test_intercept(self):self.assertAlmostEqual(self.s['intercept'],8/7)
    def test_r(self):self.assertAlmostEqual(self.s['r'],math.sqrt(6/7))
    def test_r2(self):self.assertAlmostEqual(self.s['r2'],6/7)
    def test_prediction(self):self.assertAlmostEqual(fitted(5),38/7)
    def test_y_at_mean(self):self.assertAlmostEqual(fitted(self.s['mx']),self.s['my'])
    def test_residual_sum_zero(self):self.assertAlmostEqual(sum(residuals()),0)
    def test_residual_x_orthogonality(self):self.assertAlmostEqual(sum(x*e for x,e in zip(X,residuals())),0)
    def test_sum_square_error(self):self.assertAlmostEqual(losses(),36/7)
    def test_r2_from_sse(self):self.assertAlmostEqual(1-losses()/self.s['syy'],self.s['r2'])
    def test_negative_correlation(self):self.assertAlmostEqual(statistics(X,NEGATIVE_Y)['r'],-self.s['r'])
    def test_negative_slope(self):self.assertAlmostEqual(statistics(X,NEGATIVE_Y)['slope'],-self.s['slope'])
    def test_nonlinear_zero_r(self):self.assertAlmostEqual(statistics(X,CURVED_Y)['r'],0)
    def test_nonlinear_nonconstant(self):self.assertGreater(statistics(X,CURVED_Y)['syy'],0)
    def test_outlier_changes_slope(self):self.assertNotAlmostEqual(statistics(X,OUTLIER_Y)['slope'],self.s['slope'])
    def test_outlier_changes_r(self):self.assertNotAlmostEqual(statistics(X,OUTLIER_Y)['r'],self.s['r'])
    def test_practice_slope(self):self.assertAlmostEqual(statistics(PRACTICE_X,PRACTICE_Y)['slope'],2)
    def test_practice_intercept(self):self.assertAlmostEqual(statistics(PRACTICE_X,PRACTICE_Y)['intercept'],1)
    def test_practice_perfect_r(self):self.assertAlmostEqual(statistics(PRACTICE_X,PRACTICE_Y)['r'],1)
    def test_practice_perfect_fit(self):self.assertAlmostEqual(losses(PRACTICE_X,PRACTICE_Y),0)
    def test_no_pair_truncation(self):
        for x,y in [((1,2),(1,)),((1,),(2,)),((),()),((1,),(2,))]:
            with self.subTest(x=x,y=y),self.assertRaises(ValueError):statistics(x,y)
    def test_reject_bool_and_nan(self):
        for y in ((1,True), (1,float('nan')), (1,float('inf')), (1,'hello')):
            with self.subTest(y=y),self.assertRaises(ValueError):pairs((1,2),y)
    def test_constant_x_fails(self):
        with self.assertRaisesRegex(ValueError,'vary'):statistics((2,2,2),(1,2,3))
    def test_constant_y_fails(self):
        with self.assertRaisesRegex(ValueError,'vary'):statistics((1,2,3),(4,4,4))
    def test_two_point_valid(self):self.assertAlmostEqual(statistics((1,2),(3,6))['r'],1)
    def test_formatter(self):self.assertEqual((decimal(.92582,3),decimal(5.42857,2)),('0,926','5,43'))
    def test_formatter_inf(self):
        with self.assertRaises(ValueError):decimal(float('inf'))
    def test_lesson_validate(self):self.assertTrue(validate())
    def test_structure(self):
        self.assertEqual(len(CHAPTERS),8);self.assertEqual(len(BEATS),32)
        self.assertEqual(sum(b.duration for b in BEATS),1216)
        self.assertGreaterEqual(sum(len(b.voice.split()) for b in BEATS),2200)
        self.assertTrue(all(b.chapter==(i//4+1) and b.step==(i%4+1) for i,b in enumerate(BEATS)))
    def test_no_early_answer(self):
        self.assertNotIn('bằng hai',BEATS[28].voice)
        self.assertNotIn('r bằng một',BEATS[28].voice)
    def test_causality_guard(self):
        s=' '.join(b.voice for b in BEATS).lower()
        self.assertIn('nhân quả',s)
        self.assertIn('ngoại suy',s)
        self.assertIn('phần dư',s)
    def test_scene_source_clean(self):
        s=(ROOT/'stat17/scene.py').read_text(encoding='utf8');ast.parse(s)
        for x in ('NHỊP','MANIM-TYPST','MANIM–TYPST','DEBUG','BEAT 2/4'):
            with self.subTest(x=x):self.assertNotIn(x,s.upper())
        self.assertIn('Thầy Nguyễn Văn Sang',s)
        self.assertIn('STAT17_SMOKE',s)
    def test_visual_functions(self):
        s=(ROOT/'stat17/scene.py').read_text(encoding='utf8')
        for key in ('VISUALS=(two_clouds','axes(','cloud(','residuals,losses','always_redraw','tracker.animate.set_value'):
            with self.subTest(key=key):self.assertIn(key,s)
    def test_voice(self):
        s=(ROOT/'scripts/prepare_stat17.py').read_text(encoding='utf8')
        self.assertIn('vi-VN-NamMinhNeural',s)
        self.assertNotIn('HoaiMyNeural',s)
    def test_workflow(self):
        s=(ROOT/'.github/workflows/render-stat17.yml').read_text(encoding='utf8')
        for key in ('unittest discover','check_stat17_states.py','build_stat17_typst.py','prepare_stat17.py',
                    'STAT17_SMOKE','qa_stat17.py','854,480','1920,1080','upload-artifact'):
            with self.subTest(key=key):self.assertIn(key,s)
    def test_typst_sources(self):
        self.assertEqual(len(FORMULAS),8);create_sources()
        for key in FORMULAS:self.assertTrue((ROOT/'typst/stat17'/f'{key}.typ').is_file())
    def test_plan(self):
        p=json.loads((ROOT/'stat17/runtime_plan.json').read_text(encoding='utf8'))
        self.assertEqual((p['scene'],len(p['beats']),p['duration_expected']),('STAT17',32,1216))
    def test_subtitles(self):
        s=(ROOT/'STAT17_vi.srt').read_text(encoding='utf8')
        self.assertIn('00:00:00,000',s);self.assertIn('-->',s)
        self.assertNotIn('NHỊP',s.upper())
    def test_manifest(self):
        p=json.loads((ROOT/'STAT17_MANIFEST.json').read_text(encoding='utf8'))
        self.assertEqual(p['footer'],'Thầy Nguyễn Văn Sang')
        self.assertEqual((p['scenes'],p['chapters']),(32,8))
        self.assertEqual(p['render_status'].split(':')[0],'PENDING')
    def test_files_exist(self):
        for f in ('stat17/scene.py','stat17/lesson.py','stat17/runtime_plan.json','STAT17_vi.srt',
            'LOI_GIANG_STAT17.md','STORYBOARD_STAT17.md','STAT17_MANIFEST.json',
            'preview/stat17/STAT17_storyboard_8_chapters.png',
            '.github/workflows/render-stat17.yml','scripts/prepare_stat17.py',
            'scripts/build_stat17_typst.py','scripts/stat17_docs.py','scripts/stat17_preview.py',
            'scripts/check_stat17_states.py','scripts/qa_stat17.py'):
            with self.subTest(f=f):self.assertTrue((ROOT/f).is_file())

if __name__=='__main__':unittest.main()
