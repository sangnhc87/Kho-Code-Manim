"""STAT16 regression tests: arithmetic, teaching logic, video hygiene and build artifacts."""
import ast,json,unittest
from math import isclose
from pathlib import Path
from stat16.lesson import (MAIN,CHALLENGE,METHODS,GROUPS,CHAPTERS,BEATS,
    aggregate,rate,weight_easy,mix,pooled_easy_weight,paradox,as_pct,validate_table,validate)
from scripts.build_stat16_typst import FORMULAS,create_sources
ROOT=Path(__file__).resolve().parents[1]

class TestSTAT16(unittest.TestCase):
    def test_main_data(self):
        self.assertEqual(MAIN['A']['easy'],(18,20))
        self.assertEqual(MAIN['B']['easy'],(72,90))
        self.assertEqual(MAIN['A']['hard'],(28,80))
        self.assertEqual(MAIN['B']['hard'],(3,10))
    def test_easy_rates(self):
        self.assertEqual(rate(MAIN['A']['easy']),.9)
        self.assertEqual(rate(MAIN['B']['easy']),.8)
    def test_hard_rates(self):
        self.assertEqual(rate(MAIN['A']['hard']),.35)
        self.assertEqual(rate(MAIN['B']['hard']),.3)
    def test_strata_order(self):
        for g in GROUPS:self.assertGreater(rate(MAIN['A'][g]),rate(MAIN['B'][g]))
    def test_aggregate_counts(self):
        self.assertEqual(aggregate(MAIN,'A'),(46,100))
        self.assertEqual(aggregate(MAIN,'B'),(75,100))
    def test_reversal(self):
        self.assertTrue(paradox(MAIN))
        self.assertLess(rate(aggregate(MAIN,'A')),rate(aggregate(MAIN,'B')))
    def test_main_weights(self):
        self.assertAlmostEqual(weight_easy(MAIN,'A'),.2)
        self.assertAlmostEqual(weight_easy(MAIN,'B'),.9)
    def test_weighted_equal_raw(self):
        for m in METHODS:self.assertAlmostEqual(mix(MAIN,m,weight_easy(MAIN,m)),rate(aggregate(MAIN,m)))
    def test_fifty_fifty(self):
        self.assertAlmostEqual(mix(MAIN,'A',.5),.625)
        self.assertAlmostEqual(mix(MAIN,'B',.5),.55)
    def test_pooled_weights(self):
        w=pooled_easy_weight(MAIN)
        self.assertAlmostEqual(w,.55)
        self.assertAlmostEqual(mix(MAIN,'A',w),.6525)
        self.assertAlmostEqual(mix(MAIN,'B',w),.575)
    def test_common_weight_no_reversal(self):
        for j in range(101):
            w=j/100
            with self.subTest(w=w):self.assertGreater(mix(MAIN,'A',w),mix(MAIN,'B',w))
    def test_weight_extremes(self):
        self.assertEqual(mix(MAIN,'A',0),.35)
        self.assertEqual(mix(MAIN,'A',1),.9)
    def test_challenge_counts(self):
        self.assertEqual(aggregate(CHALLENGE,'A'),(17,50))
        self.assertEqual(aggregate(CHALLENGE,'B'),(25,40))
    def test_challenge_rates(self):
        self.assertAlmostEqual(rate(CHALLENGE['A']['easy']),.9)
        self.assertAlmostEqual(rate(CHALLENGE['B']['easy']),.8)
        self.assertAlmostEqual(rate(CHALLENGE['A']['hard']),.2)
        self.assertAlmostEqual(rate(CHALLENGE['B']['hard']),.1)
    def test_challenge_paradox(self):self.assertTrue(paradox(CHALLENGE))
    def test_challenge_overall(self):
        self.assertAlmostEqual(rate(aggregate(CHALLENGE,'A')),.34)
        self.assertAlmostEqual(rate(aggregate(CHALLENGE,'B')),.625)
    def test_challenge_standardization(self):
        self.assertAlmostEqual(mix(CHALLENGE,'A'),.55)
        self.assertAlmostEqual(mix(CHALLENGE,'B'),.45)
    def test_format_percent_boundaries(self):
        for v,s in [(0,'0%'),(.02,'2%'),(.1,'10%'),(.2,'20%'),(.35,'35%'),(.5,'50%'),(.9,'90%'),(1,'100%'),(.625,'62,5%')]:
            with self.subTest(value=v):self.assertEqual(as_pct(v),s)
    def test_format_zero_decimal(self):
        for v,s in [(.1,'10%'),(.2,'20%'),(.9,'90%'),(1,'100%'),(.5,'50%')]:
            with self.subTest(value=v):self.assertEqual(as_pct(v,0),s)
    def test_bad_nan_rate(self):
        with self.assertRaises(ValueError):as_pct(float('nan'))
    def test_bad_rate(self):
        for pair in ((True,3),(1,True),(4,3),(0,0),(-1,3),(1,2.3)):
            with self.subTest(pair=pair),self.assertRaises(ValueError):rate(pair)
    def test_bad_weights(self):
        for w in (True,-.01,1.01,float('nan'),float('inf'),'0.5'):
            with self.subTest(w=w),self.assertRaises(ValueError):mix(MAIN,'A',w)
    def test_bad_table(self):
        for data in ({},{'A':MAIN['A']},{'A':{'easy':(0,1),'hard':(0,1)},'B':{'easy':(1,True),'hard':(0,1)}},
                     {'A':{'easy':(1,0),'hard':(2,4)},'B':MAIN['B']}):
            with self.subTest(data=data),self.assertRaises(ValueError):validate_table(data)
    def test_no_paradox_for_equal_weights(self):
        fake={'A':{'easy':(9,10),'hard':(4,10)},'B':{'easy':(8,10),'hard':(3,10)}}
        self.assertFalse(paradox(fake))
    def test_voice_text(self):
        self.assertEqual(len(BEATS),32);self.assertEqual(len(CHAPTERS),8)
        self.assertTrue(validate())
        self.assertGreater(sum(len(b.voice.split()) for b in BEATS),2200)
        self.assertEqual(sum(b.duration for b in BEATS),1216)
        self.assertTrue(all(len(b.voice.split())>=46 for b in BEATS))
        for b in BEATS:self.assertEqual((b.chapter-1)*4+b.step,list(BEATS).index(b)+1)
    def test_mathematical_story(self):
        script=' '.join(b.voice for b in BEATS)
        for phrase in ('bốn mươi sáu','bảy mươi lăm','sáu mươi hai phẩy năm','trọng số','nhân quả'):
            self.assertIn(phrase,script)
    def test_no_early_challenge_answer(self):
        self.assertNotIn('ba mươi bốn phần trăm',BEATS[28].voice)
        self.assertNotIn('sáu mươi hai phẩy năm phần trăm',BEATS[28].voice)
    def test_scene_screen_clean(self):
        src=(ROOT/'stat16/scene.py').read_text(encoding='utf8');ast.parse(src)
        for forbidden in ('NHỊP','MANIM-TYPST','MANIM–TYPST','DEBUG','BEAT 2/4'):
            with self.subTest(forbidden=forbidden):self.assertNotIn(forbidden,src.upper())
        self.assertIn('Thầy Nguyễn Văn Sang',src)
        self.assertIn('STAT16_SMOKE',src)
    def test_scene_chapters(self):
        src=(ROOT/'stat16/scene.py').read_text(encoding='utf8')
        for token in ('VISUALS=(vis1','composition(MAIN)','rate_bars','standardized_bars','CHALLENGE','0,2'):
            self.assertIn(token,src)
    def test_typst_sources(self):
        self.assertEqual(len(FORMULAS),8);create_sources()
        for name in FORMULAS:self.assertTrue((ROOT/'typst/stat16'/f'{name}.typ').is_file())
    def test_narration(self):
        src=(ROOT/'scripts/prepare_stat16.py').read_text(encoding='utf8')
        self.assertIn('vi-VN-NamMinhNeural',src)
        self.assertNotIn('HoaiMyNeural',src)
    def test_workflow(self):
        src=(ROOT/'.github/workflows/render-stat16.yml').read_text(encoding='utf8')
        for name in ('unittest discover','check_stat16_states.py','build_stat16_typst.py','prepare_stat16.py',
                     'STAT16_SMOKE','qa_stat16.py','854,480','1920,1080','upload-artifact'):
            with self.subTest(name=name):self.assertIn(name,src)
    def test_runtime_plan(self):
        data=json.loads((ROOT/'stat16/runtime_plan.json').read_text(encoding='utf8'))
        self.assertEqual((data['scene'],len(data['beats'])),('STAT16',32))
        self.assertEqual(data['duration_expected'],1216)
    def test_subtitles(self):
        s=(ROOT/'STAT16_vi.srt').read_text(encoding='utf8')
        self.assertIn('00:00:00,000',s)
        self.assertIn('-->',s)
        self.assertNotIn('NHỊP',s.upper())
    def test_files(self):
        for f in ('stat16/scene.py','stat16/lesson.py','stat16/runtime_plan.json',
                  'STAT16_vi.srt','LOI_GIANG_STAT16.md','STORYBOARD_STAT16.md',
                  'preview/stat16/STAT16_storyboard_8_chapters.png','STAT16_MANIFEST.json',
                  '.github/workflows/render-stat16.yml','scripts/prepare_stat16.py',
                  'scripts/build_stat16_typst.py','scripts/stat16_docs.py','scripts/stat16_preview.py',
                  'scripts/check_stat16_states.py','scripts/qa_stat16.py'):
            with self.subTest(path=f):self.assertTrue((ROOT/f).is_file())

if __name__=='__main__':unittest.main()
