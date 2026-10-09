"""STAT15 numerical, instructional, UI, workflow and file-contract regression checks."""
import ast,unittest,json
from math import isclose,sqrt
from pathlib import Path
from stat15.lesson import (BAR_VALUES,BAR_CROP,YEARS,YEAR_VALUES,PICTOGRAM_VALUES,CLASSES,
    CLASS_COUNTS,CLASS_TOTALS,TREND_YEARS,TREND_VALUES,CHALLENGE_VALUES,
    percentages,ratio,exaggerated_height,histogram_densities,time_slopes,changes,
    BEATS,CHAPTERS,validate)
from scripts.build_stat15_typst import FORMULAS,create_sources
ROOT=Path(__file__).resolve().parents[1]

class TestSTAT15(unittest.TestCase):
 def test_datasets(self):
  self.assertEqual(BAR_VALUES,(80,100))
  self.assertEqual((len(YEARS),len(YEAR_VALUES)),(4,4))
  self.assertEqual(PICTOGRAM_VALUES,(20,40))
  self.assertEqual((len(TREND_YEARS),len(TREND_VALUES)),(6,6))
 def test_truncation(self):self.assertEqual(exaggerated_height(BAR_VALUES,BAR_CROP),5)
 def test_real_ratio(self):self.assertEqual(ratio(100,80),1.25)
 def test_percentage_increase(self):self.assertEqual(100*(100-80)/80,25)
 def test_crop_not_values(self):self.assertEqual(BAR_VALUES[1]-BAR_VALUES[0],20)
 def test_wrong_crop_rejected(self):
  for baseline in (80,81,100,999,float('nan'),float('inf')):
   with self.subTest(baseline=baseline),self.assertRaises(ValueError):exaggerated_height(BAR_VALUES,baseline)
 def test_ratio_invalid(self):
  for x in (0,-1,float('nan'),float('inf')):
   with self.subTest(x=x),self.assertRaises(ValueError):ratio(100,x)
 def test_time_gaps(self):self.assertEqual(tuple(YEARS[i+1]-YEARS[i] for i in range(3)),(1,3,1))
 def test_time_slopes(self):
  for a,b in zip(time_slopes(),(4,8/3,4)):self.assertTrue(isclose(a,b))
 def test_repeated_year(self):
  with self.assertRaises(ValueError):time_slopes((2020,2020),(3,4))
 def test_reverse_year(self):
  with self.assertRaises(ValueError):time_slopes((2022,2020),(3,4))
 def test_mismatched_time(self):
  with self.assertRaises(ValueError):time_slopes((2020,2021),(3,))
 def test_pictogram_scaling(self):
  self.assertTrue(isclose((2)**2,4))
  self.assertTrue(isclose((sqrt(2))**2,2))
 def test_count_vs_percentage(self):
  self.assertEqual(CLASS_COUNTS,(18,24));self.assertEqual(CLASS_TOTALS,(30,80))
  self.assertEqual(percentages(),(60,30))
 def test_percentage_boundary(self):self.assertEqual(percentages((0,10),(10,10)),(0,100))
 def test_percentage_invalid(self):
  for c,n in [((1,),(0,)),((4,),(3,)),((-1,),(10,)),((True,),(5,)),((2,),()),((2,),(2,3))]:
   with self.subTest(c=c,n=n),self.assertRaises(ValueError):percentages(c,n)
 def test_trend_sliding(self):
  self.assertEqual(changes(),(28.000000000000004,-10.0))
 def test_trend_bad_zero(self):
  with self.assertRaises(ValueError):changes((0,5,6,7,8,9))
 def test_histogram_densities(self):self.assertEqual(histogram_densities(),(4,3,6,3))
 def test_histogram_frequency_total(self):self.assertEqual(sum(c for _,_,c in CLASSES),35)
 def test_histogram_area_invariant(self):
  self.assertEqual(sum((right-left)*h for (left,right,_),h in zip(CLASSES,histogram_densities())),35)
 def test_histogram_non_contiguous(self):
  with self.assertRaises(ValueError):histogram_densities(((0,2,8),(3,5,7)))
 def test_histogram_bad_width(self):
  with self.assertRaises(ValueError):histogram_densities(((0,0,2),))
 def test_histogram_boolean_reject(self):
  with self.assertRaises(ValueError):histogram_densities(((0,2,True),))
 def test_challenge_difference(self):self.assertEqual(CHALLENGE_VALUES[1]-CHALLENGE_VALUES[0],6)
 def test_challenge_percentage_points(self):self.assertAlmostEqual((68-62)/62*100,9.6774193548)
 def test_challenge_truncated_ratio(self):self.assertEqual(exaggerated_height(CHALLENGE_VALUES,60),4)
 def test_challenge_true_ratio(self):self.assertAlmostEqual(ratio(68,62),1.09677419355)
 def test_lecture_complete(self):
  self.assertTrue(validate());self.assertEqual(len(BEATS),32)
  self.assertEqual(len(CHAPTERS),8)
  self.assertEqual(len({(b.chapter,b.step) for b in BEATS}),32)
  self.assertGreaterEqual(sum(b.duration for b in BEATS),1100)
  self.assertGreater(sum(len(b.voice.split()) for b in BEATS),2000)
  self.assertTrue(all(len(b.voice.split())>=45 for b in BEATS))
 def test_formula_source_files(self):
  self.assertEqual(len(FORMULAS),8);create_sources()
  self.assertTrue(all((ROOT/f'typst/stat15/{x}.typ').is_file() for x in FORMULAS))
 def test_on_screen_labels_clean(self):
  s=(ROOT/'stat15/scene.py').read_text(encoding='utf8');ast.parse(s)
  for forbidden in ('NHỊP','MANIM-TYPST','MANIM–TYPST','STEP 2/4','DEBUG'):
   with self.subTest(forbidden=forbidden):self.assertNotIn(forbidden,s.upper())
  self.assertIn('Thầy Nguyễn Văn Sang',s)
  self.assertIn('STAT15_SMOKE',s)
 def test_male_voice(self):
  s=(ROOT/'scripts/prepare_stat15.py').read_text(encoding='utf8')
  self.assertIn('vi-VN-NamMinhNeural',s)
  self.assertNotIn('HoaiMyNeural',s)
 def test_workflow(self):
  s=(ROOT/'.github/workflows/render-stat15.yml').read_text(encoding='utf8')
  for f in ('unittest discover','build_stat15_typst.py','check_stat15_states.py',
   'prepare_stat15.py','STAT15_SMOKE','qa_stat15.py','854,480','1920,1080','voice','upload-artifact'):
   with self.subTest(token=f):self.assertIn(f,s)
 def test_scene_plot_correct_time_x(self):
  s=(ROOT/'stat15/scene.py').read_text(encoding='utf8')
  self.assertIn('tick_labels=YEARS',s)
  self.assertIn('histogram_densities()',s)
 def test_plan(self):
  data=json.loads((ROOT/'stat15/runtime_plan.json').read_text(encoding='utf8'))
  self.assertEqual((data['scene'],len(data['beats'])),('STAT15',32))
  self.assertEqual(data['duration_expected'],1152)
 def test_deliverables(self):
  for f in ('stat15/scene.py','stat15/lesson.py','stat15/runtime_plan.json',
    'LOI_GIANG_STAT15.md','STORYBOARD_STAT15.md','STAT15_vi.srt',
    '.github/workflows/render-stat15.yml','scripts/stat15_preview.py',
    'scripts/qa_stat15.py','scripts/build_stat15_typst.py','scripts/prepare_stat15.py'):
   with self.subTest(path=f):self.assertTrue((ROOT/f).is_file())
if __name__=='__main__':unittest.main()
