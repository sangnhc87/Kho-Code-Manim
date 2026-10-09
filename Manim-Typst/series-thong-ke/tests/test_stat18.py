"""Math, reproducible simulations, pedagogy, and delivery integrity of STAT18."""
import ast,json,math,unittest
from pathlib import Path
from stat18.lesson import (POPULATION,N,TRUE_P,BEATS,CHAPTERS,estimate,sample,trials,
                           sd_sample_proportion,approx_interval,percent,validate)
from scripts.build_stat18_typst import FORMULAS,create_sources
ROOT=Path(__file__).resolve().parents[1]

class STAT18Tests(unittest.TestCase):
    def test_population(self):
        self.assertEqual((N,len(POPULATION),sum(POPULATION),TRUE_P),(1000,1000,400,.4))
    def test_sample_n20(self):self.assertEqual((sum(sample(20)),estimate(sample(20))),(7,.35))
    def test_sample_n80(self):self.assertEqual((sum(sample(80)),estimate(sample(80))),(37,.4625))
    def test_sample_n200(self):self.assertEqual((sum(sample(200)),estimate(sample(200))),(88,.44))
    def test_reproducible(self):self.assertEqual(sample(80),sample(80))
    def test_population_limit(self):self.assertEqual(len(sample(1000)),1000)
    def test_sample_seed(self):self.assertNotEqual(sample(80,15),sample(80,16))
    def test_sample_invalid(self):
        for n in (0,-1,1001,True,4.5):
            with self.subTest(n=n),self.assertRaises(ValueError):sample(n)
    def test_estimate_invalid(self):
        for vals in ((),(1,True),(2,0),('yes','no')):
            with self.subTest(vals=vals),self.assertRaises(ValueError):estimate(vals)
    def test_repeat_counts(self):
        self.assertEqual(len(trials(20)),300)
        self.assertEqual(len(trials(80)),300)
        self.assertTrue(all(0<=x<=1 for x in trials(20)+trials(80)))
    def test_repeat_reproducible(self):self.assertEqual(trials(20),trials(20))
    def test_simulation_center(self):
        self.assertLess(abs(sum(trials(20))/300-.4),.025)
        self.assertLess(abs(sum(trials(80))/300-.4),.025)
    def test_simulation_dispersion(self):
        v20=sum((x-TRUE_P)**2 for x in trials(20))/300
        v80=sum((x-TRUE_P)**2 for x in trials(80))/300
        self.assertGreater(v20,v80*3)
    def test_exact_finite_pop_sd(self):
        self.assertAlmostEqual(sd_sample_proportion(20),math.sqrt(.4*.6/20*980/999))
        self.assertAlmostEqual(sd_sample_proportion(80),math.sqrt(.4*.6/80*920/999))
        self.assertLess(sd_sample_proportion(80),sd_sample_proportion(20))
        self.assertAlmostEqual(sd_sample_proportion(1000),0)
    def test_sd_invalid(self):
        for n in (0,1001):
            with self.assertRaises(ValueError):sd_sample_proportion(n)
    def test_wald_interval(self):
        p,lo,hi=approx_interval(88,200)
        self.assertEqual(p,.44)
        self.assertAlmostEqual(lo,.44-1.96*math.sqrt(.44*.56/200))
        self.assertLess(lo,.4)
        self.assertGreater(hi,.4)
    def test_wald_interval_bound(self):
        self.assertEqual(approx_interval(0,20),(0,0,0))
        for a,n in ((21,20),(-1,10),(0,0)):
            with self.subTest(a=a,n=n),self.assertRaises(ValueError):approx_interval(a,n)
    def test_format(self):self.assertEqual((percent(.4),percent(.4625,2)),('40%','46,25%'))
    def test_validate(self):self.assertTrue(validate())
    def test_beats(self):
        self.assertEqual(len(BEATS),32)
        self.assertEqual(len(CHAPTERS),8)
        self.assertEqual(sum(x.duration for x in BEATS),1216)
        self.assertGreater(sum(len(x.voice.split()) for x in BEATS),2200)
        self.assertTrue(all(b.chapter==(j//4+1) and b.step==(j%4+1) for j,b in enumerate(BEATS)))
    def test_practice_answer_is_delayed(self):
        self.assertNotIn('bốn mươi bốn phần trăm',BEATS[28].voice)
        self.assertNotIn('bảy mươi lăm phần trăm',BEATS[28].voice)
        self.assertIn('bốn mươi bốn phần trăm',BEATS[30].voice)
    def test_guardrails(self):
        body=' '.join(b.voice for b in BEATS).lower()
        for phrase in ('không hoàn lại','không phản hồi','thiên lệch','mô phỏng','không đảm bảo'):
            with self.subTest(phrase=phrase):self.assertIn(phrase,body)
    def test_scene_hygiene(self):
        s=(ROOT/'stat18/scene.py').read_text(encoding='utf8')
        ast.parse(s)
        for prohibited in ('NHỊP','MANIM-TYPST','MANIM–TYPST','DEBUG','2/4'):
            self.assertNotIn(prohibited,s.upper())
        for required in ('Thầy Nguyễn Văn Sang','STAT18_SMOKE','ValueTracker','always_redraw',
                         'tracker.animate.set_value','VISUALS=','approx_interval'):
            self.assertIn(required,s)
    def test_narration(self):
        s=(ROOT/'scripts/prepare_stat18.py').read_text(encoding='utf8')
        self.assertIn('vi-VN-NamMinhNeural',s)
        self.assertNotIn('HoaiMyNeural',s)
        self.assertIn('speech<=1',s)
    def test_workflow(self):
        s=(ROOT/'.github/workflows/render-stat18.yml').read_text(encoding='utf8')
        for val in ('test', 'check_stat18_states.py','build_stat18_typst.py','prepare_stat18.py',
                    'STAT18_SMOKE','qa_stat18.py','854,480','1920,1080','upload-artifact'):
            self.assertIn(val,s)
    def test_typst_sources(self):
        self.assertEqual(len(FORMULAS),8)
        create_sources()
        for x in FORMULAS:self.assertTrue((ROOT/f'typst/stat18/{x}.typ').is_file())
    def test_plan(self):
        plan=json.loads((ROOT/'stat18/runtime_plan.json').read_text(encoding='utf8'))
        self.assertEqual((plan['scene'],len(plan['beats']),plan['duration_expected']),('STAT18',32,1216))
    def test_subtitles(self):
        s=(ROOT/'STAT18_vi.srt').read_text(encoding='utf8')
        self.assertIn('00:00:00,000',s)
        self.assertIn('-->',s)
        self.assertNotIn('NHỊP',s.upper())
    def test_manifest(self):
        data=json.loads((ROOT/'STAT18_MANIFEST.json').read_text(encoding='utf8'))
        self.assertEqual(data['footer'],'Thầy Nguyễn Văn Sang')
        self.assertEqual((data['chapters'],data['scenes'],data['formula_count']),(8,32,8))
        self.assertEqual((data['random_20_yes'],data['random_80_yes']),(7,37))
        self.assertEqual(data['series_complete'],True)
        self.assertTrue(data['render_status'].startswith('PENDING'))
    def test_files(self):
        fs=('stat18/scene.py','stat18/lesson.py','stat18/runtime_plan.json',
            'STAT18_vi.srt','STORYBOARD_STAT18.md','LOI_GIANG_STAT18.md',
            'HUONG_DAN_RENDER_STAT18.md','STAT18_MANIFEST.json',
            'preview/stat18/STAT18_storyboard_8_chapters.png',
            '.github/workflows/render-stat18.yml','scripts/prepare_stat18.py',
            'scripts/build_stat18_typst.py','scripts/stat18_docs.py','scripts/stat18_preview.py',
            'scripts/check_stat18_states.py','scripts/qa_stat18.py')
        for path in fs:
            with self.subTest(path=path):self.assertTrue((ROOT/path).is_file())

if __name__=='__main__':unittest.main()
