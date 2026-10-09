"""Independent numerical invariants plus production regression tests (no Manim needed)."""
import ast,json,re,subprocess,sys,unittest
from collections import Counter
from pathlib import Path
from stat01.lesson import SCORES
from stat04.lesson import quartiles
from stat05.lesson import (box_summary,BEATS,CHAPTERS,BASE,EXTREME,EXTREME_DATA,
                           COMPARE,GROUPS,SPREAD,SAME_RANGE,CONSTANT,EXERCISE,
                           EXERCISE_DATA,validate)
ROOT=Path(__file__).resolve().parents[1]

class TestStat05Math(unittest.TestCase):
    def test_data_original(self):self.assertEqual(len(SCORES),40)
    def test_original_frequency(self):self.assertEqual(dict(Counter(SCORES)),{4:2,5:4,6:8,7:10,8:8,9:6,10:2})
    def test_original_summary(self):self.assertEqual(tuple(BASE[x] for x in ('minimum','q1','median','q3','maximum')),(4,6,7,8,10))
    def test_quartile_procedure(self):self.assertEqual(quartiles(SCORES),(6,7,8))
    def test_original_range(self):self.assertEqual(BASE['range'],6)
    def test_original_iqr(self):self.assertEqual(BASE['iqr'],2)
    def test_original_fences(self):self.assertEqual((BASE['lower_fence'],BASE['upper_fence']),(3,11))
    def test_original_whiskers(self):self.assertEqual((BASE['lower_whisker'],BASE['upper_whisker']),(4,10))
    def test_original_outliers(self):self.assertEqual(BASE['outliers'],())
    def test_replace_only_one(self):self.assertEqual(Counter(EXTREME_DATA),Counter(SCORES)-Counter([10])+Counter([30]))
    def test_extreme_still_forty(self):self.assertEqual(len(EXTREME_DATA),40)
    def test_extreme_quartiles(self):self.assertEqual((EXTREME['q1'],EXTREME['median'],EXTREME['q3']),(6,7,8))
    def test_extreme_range(self):self.assertEqual(EXTREME['range'],26)
    def test_extreme_iqr(self):self.assertEqual(EXTREME['iqr'],2)
    def test_extreme_outlier(self):self.assertEqual(EXTREME['outliers'],(30,))
    def test_extreme_whiskers_not_fences(self):self.assertEqual((EXTREME['lower_whisker'],EXTREME['upper_whisker']),(4,10))
    def test_first_comparison_median(self):self.assertEqual(COMPARE[0]['median'],5.5)
    def test_second_comparison_median(self):self.assertEqual(COMPARE[1]['median'],5.5)
    def test_comparison_iqr(self):self.assertEqual(tuple(x['iqr'] for x in COMPARE),(4,8))
    def test_spread_min_max(self):self.assertEqual(tuple((x['minimum'],x['maximum']) for x in SPREAD),((1,9),(1,9)))
    def test_spread_range(self):self.assertEqual(tuple(x['range'] for x in SPREAD),(8,8))
    def test_spread_iqr(self):self.assertEqual(tuple(x['iqr'] for x in SPREAD),(8,2))
    def test_constant_zero(self):self.assertEqual((CONSTANT['range'],CONSTANT['iqr']), (0,0))
    def test_constant_whiskers(self):self.assertEqual((CONSTANT['lower_whisker'],CONSTANT['upper_whisker']),(5,5))
    def test_empty_rejected(self):
        with self.assertRaises(ValueError):box_summary(())
    def test_singleton(self):self.assertEqual(box_summary((7,))['outliers'],())
    def test_reordering(self):self.assertEqual(box_summary(tuple(reversed(SCORES))),BASE)
    def test_translate(self):
        tr=box_summary(tuple(x+3 for x in SCORES))
        self.assertEqual((tr['range'],tr['iqr'],tr['q1'],tr['median'],tr['q3']),(6,2,9,10,11))
    def test_scale(self):
        sc=box_summary(tuple(2*x for x in SCORES))
        self.assertEqual((sc['range'],sc['iqr']),(12,4))
    def test_exercise_n(self):self.assertEqual(EXERCISE['n'],11)
    def test_exercise_quartiles(self):self.assertEqual((EXERCISE['q1'],EXERCISE['median'],EXERCISE['q3']),(4,6,8))
    def test_exercise_iqr_and_range(self):self.assertEqual((EXERCISE['iqr'],EXERCISE['range']),(4,18))
    def test_exercise_fences(self):self.assertEqual((EXERCISE['lower_fence'],EXERCISE['upper_fence']),(-2,14))
    def test_exercise_whiskers(self):self.assertEqual((EXERCISE['lower_whisker'],EXERCISE['upper_whisker']),(2,9))
    def test_exercise_outlier(self):self.assertEqual(EXERCISE['outliers'],(20,))
    def test_independent_scan_outliers(self):
        vals=sorted(EXERCISE_DATA)
        self.assertEqual(tuple(x for x in vals if x< -2 or x>14),(20,))
    def test_validate_all(self):self.assertTrue(validate())

class TestStat05Production(unittest.TestCase):
    def test_eight_chapters(self):self.assertEqual(len(CHAPTERS),8)
    def test_32_beats(self):self.assertEqual(len(BEATS),32)
    def test_chapter_order(self):self.assertEqual([b.chapter for b in BEATS],[c for c in range(1,9) for _ in range(4)])
    def test_step_order(self):self.assertEqual([b.step for b in BEATS],[1,2,3,4]*8)
    def test_narration(self):self.assertTrue(all(len(b.voice.split())>=42 for b in BEATS))
    def test_titles_unique(self):self.assertEqual(len(set(b.title for b in BEATS)),32)
    def test_14_minutes(self):self.assertEqual(sum(b.duration for b in BEATS),864)
    def test_no_manim_math(self):self.assertNotIn('from manim import',(ROOT/'stat05/lesson.py').read_text())
    def test_scene_compiles(self):ast.parse((ROOT/'stat05/scene.py').read_text())
    def test_eight_visuals(self):self.assertIn('VISUALS=(chapter1,chapter2,chapter3,chapter4,chapter5,chapter6,chapter7,chapter8)',(ROOT/'stat05/scene.py').read_text())
    def test_main_and_smoke_scenes(self):
        s=(ROOT/'stat05/scene.py').read_text()
        self.assertIn('class STAT05(Scene):',s)
        self.assertIn('class STAT05_SMOKE(STAT05):',s)
    def test_typst_asset_map(self):
        from scripts.build_stat05_typst import FORMULAS
        self.assertEqual(len(FORMULAS),8)
    @unittest.skipUnless((ROOT/'stat05/runtime_plan.json').exists(),"no runtime")
    def test_prepared_runtime(self):
        doc=json.loads((ROOT/'stat05/runtime_plan.json').read_text())
        self.assertEqual((doc['scene'],doc['chapters'],len(doc['beats'])),('STAT05',8,32))
        self.assertGreaterEqual(doc['duration_expected'],860)
    @unittest.skipUnless((ROOT/'STAT05_vi.srt').exists(),"no srt")
    def test_srt(self):self.assertIn('00:00:00,000 -->',(ROOT/'STAT05_vi.srt').read_text())
    def test_workflow_has_smoke(self):self.assertIn('stat05/scene.py STAT05_SMOKE',(ROOT.parent.parent/'.github/workflows/render-stat05.yml').read_text())
    def test_workflow_has_compile(self):self.assertIn('python scripts/build_stat05_typst.py',(ROOT.parent.parent/'.github/workflows/render-stat05.yml').read_text())
    def test_workflow_has_qa(self):self.assertIn('python scripts/qa_stat05.py',(ROOT.parent.parent/'.github/workflows/render-stat05.yml').read_text())
    def test_no_silent_TTS(self):self.assertIn("if speech<=1:raise RuntimeError",(ROOT/'scripts/prepare_stat05.py').read_text())
    def test_qa_checks_stream(self):self.assertIn("a.voice=='on' and audio is None",(ROOT/'scripts/qa_stat05.py').read_text())
    def test_pins_compatible(self):self.assertIn('manim>=0.19,<0.20',(ROOT/'requirements.txt').read_text())

if __name__=='__main__':unittest.main()
