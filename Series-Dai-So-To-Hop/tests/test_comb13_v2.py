"""COMB13: independent exact enumeration and GitHub production regression tests."""
import ast
import json
import math
import pathlib
import py_compile
import sys
import unittest
from itertools import permutations, combinations
from collections import Counter
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb13_lesson_data import (
 BEATS,CHAPTER_LABELS,FORMULAS,adjacent,on_circle_adjacent,
 none_adjacent,nonconsecutive_positions,distinct_gaps,normalized_cycles,validate)

class TestCOMB13(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.p5=list(permutations(range(5)))
  cls.p6=list(permutations(range(6)))
  cls.p8=list(permutations(range(8)))
 def test_validate(self):self.assertTrue(validate())
 def test_48_beats(self):self.assertEqual(len(BEATS),48)
 def test_eight_chapters(self):self.assertEqual(len(CHAPTER_LABELS),8)
 def test_chapter_state_order(self):
  for k in CHAPTER_LABELS:
   self.assertEqual([b.state for b in BEATS if b.section==k],list(range(6)))
 def test_voice_words(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),3950)
 def test_per_beat_minimum(self):self.assertTrue(all(len(b.narration.split())>=38 for b in BEATS))
 def test_base_duration(self):self.assertGreater(sum(b.min_seconds for b in BEATS),1100)
 def test_formulas(self):self.assertEqual(len(FORMULAS),48)
 def test_unique_formula_keys(self):self.assertEqual(len({b.formula for b in BEATS}),48)
 def test_notation_n_above_k(self):
  self.assertIn('C^(6)_(3)',str(FORMULAS))
 def test_5_no_ab(self):
  self.assertEqual(sum(not adjacent(p,0,1) for p in self.p5),72)
 def test_5_ab_adj(self):self.assertEqual(sum(adjacent(p,0,1) for p in self.p5),48)
 def test_two_methods_agree(self):self.assertEqual(120-2*math.factorial(4),math.factorial(3)*math.comb(4,2)*2)
 def test_6_none_ab_cd(self):
  self.assertEqual(sum(none_adjacent(p,((0,1),(2,3))) for p in self.p6),336)
 def test_6_ab_cd_intersection(self):
  self.assertEqual(sum(adjacent(p,0,1) and adjacent(p,2,3) for p in self.p6),96)
 def test_6_ab_cd_exactly_one(self):
  self.assertEqual(sum(adjacent(p,0,1)!=adjacent(p,2,3) for p in self.p6),288)
 def test_6_ab_cd_union(self):
  self.assertEqual(sum(adjacent(p,0,1) or adjacent(p,2,3) for p in self.p6),384)
 def test_6_partition(self):self.assertEqual(336+288+96,math.factorial(6))
 def test_6_shared_B_none(self):
  self.assertEqual(sum(not adjacent(p,0,1) and not adjacent(p,1,2) for p in self.p6),288)
 def test_6_shared_B_intersection(self):
  self.assertEqual(sum(adjacent(p,0,1) and adjacent(p,1,2) for p in self.p6),48)
 def test_6_A_B_C_pairwise_none(self):
  self.assertEqual(sum(none_adjacent(p,((0,1),(1,2),(0,2))) for p in self.p6),144)
 def test_6_A_B_C_gap_solution(self):
  self.assertEqual(math.factorial(3)*math.comb(4,3)*math.factorial(3),144)
 def test_identical_letters_A4_B5(self):
  from itertools import combinations
  seqs=set()
  for subset in combinations(range(9),4):
   seq=''.join('A' if j in subset else 'B' for j in range(9))
   if 'AA' not in seq:seqs.add(seq)
  self.assertEqual(len(seqs),15)
 def test_choose_positions_formula(self):
  for n in range(1,11):
   for k in range(n+1):
    count=sum(all(b-a>=2 for a,b in zip(s,s[1:])) for s in combinations(range(n),k))
    self.assertEqual(count,nonconsecutive_positions(n,k),(n,k))
 def test_no_possible_4_of_6(self):self.assertEqual(nonconsecutive_positions(6,4),0)
 def test_gap_5_4(self):self.assertEqual(distinct_gaps(5,4),15)
 def test_distinct_groups(self):self.assertEqual(math.factorial(5)*15*math.factorial(4),43200)
 def test_5_boys_3_girls(self):self.assertEqual(math.factorial(5)*math.comb(6,3)*math.factorial(3),14400)
 def test_4_boys_4_girls_alternating(self):self.assertEqual(2*math.factorial(4)**2,1152)
 def test_6_circle_total(self):self.assertEqual(len(list(normalized_cycles(6))),120)
 def test_6_circle_A_B_none(self):
  self.assertEqual(sum(not on_circle_adjacent(p,0,1) for p in normalized_cycles(6)),72)
 def test_6_circle_A_B_C_all_nonadjacent(self):
  self.assertEqual(sum(all(not on_circle_adjacent(p,x,y) for x,y in ((0,1),(1,2),(0,2))) for p in normalized_cycles(6)),12)
 def test_4_boys_3_girls_circle(self):self.assertEqual(math.factorial(3)*math.comb(4,3)*math.factorial(3),144)
 def test_8_total(self):self.assertEqual(len(self.p8),40320)
 def test_8_single_forbidden(self):
  self.assertEqual(sum(adjacent(p,0,1) for p in self.p8),10080)
 def test_8_double_forbidden(self):
  self.assertEqual(sum(adjacent(p,0,1) and adjacent(p,2,3) for p in self.p8),2880)
 def test_8_triple_forbidden(self):
  self.assertEqual(sum(all(adjacent(p,a,b) for a,b in ((0,1),(2,3),(4,5))) for p in self.p8),960)
 def test_8_three_none(self):
  self.assertEqual(sum(none_adjacent(p,((0,1),(2,3),(4,5))) for p in self.p8),17760)
 def test_inclusion_exclusion(self):
  self.assertEqual(40320-3*10080+3*2880-960,17760)
 def test_typst_files(self):self.assertEqual(len(list((ROOT/'assets/comb13v2').glob('*.typ'))),48)
 def test_voice_manifest(self):
  meta=json.loads((ROOT/'voice/comb13_voice_manifest.json').read_text(encoding='utf8'))
  self.assertEqual(meta['beats'],48);self.assertGreater(meta['target_seconds'],1100)
 def test_python_syntax(self):
  for path in ('comb13_lesson_data.py','episodes/comb13_not_adjacent.py',
               'scripts/prepare_comb13_v2.py','scripts/qa_comb13_v2.py'):
   py_compile.compile(str(ROOT/path),doraise=True)
 def test_scene_class(self):
  tree=ast.parse((ROOT/'episodes/comb13_not_adjacent.py').read_text(encoding='utf8'))
  self.assertIn('COMB13',[x.name for x in tree.body if isinstance(x,ast.ClassDef)])
 def test_workflow(self):
  w=(ROOT.parent/'.github/workflows/render-comb13-v2.yml').read_text(encoding='utf8')
  for x in ('workflow_dispatch:','COMB13','comb13_not_adjacent.py','qa_comb13_v2.py','quality:','voice:','upload-artifact'):
   self.assertIn(x,w)
 def test_legacy_episodes(self):
  for j in range(1,13):self.assertTrue(list((ROOT/'episodes').glob(f'comb{j:02d}*.py')))
 def test_docs(self):
  for filename in ('HUONG_DAN_RENDER_COMB13_V2.md','storyboard_COMB13_v2.md','narration_COMB13_v2.md'):
   self.assertTrue((ROOT/filename).exists())
 def test_previews(self):self.assertEqual(len(list((ROOT/'preview/comb13_v2').glob('COMB13_*.png'))),8)

if __name__=='__main__':unittest.main()
