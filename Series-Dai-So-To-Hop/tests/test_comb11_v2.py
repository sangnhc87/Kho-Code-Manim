"""Mathematical and source checks for COMB11, independent of Manim runtime."""
import ast
import json
import math
import pathlib
import sys
import unittest
from itertools import permutations
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb11_lesson_data import (BEATS, CHAPTER_LABELS, FORMULAS, circular_representatives,
    neighbors,alternating,opposite,no_couple_adjacent,validate)

class TestCOMB11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.six=circular_representatives(6)
        cls.seven=circular_representatives(7)
    def test_validate(self):self.assertTrue(validate())
    def test_beats(self):self.assertEqual(len(BEATS),48)
    def test_chapters(self):self.assertEqual(len(CHAPTER_LABELS),8)
    def test_each_chapter_six(self):
        for k in CHAPTER_LABELS:self.assertEqual([b.state for b in BEATS if b.section==k],list(range(6)))
    def test_total_narration_words(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),2700)
    def test_no_empty_narrations(self):self.assertTrue(all(len(b.narration.split())>=43 for b in BEATS))
    def test_duration(self):self.assertGreater(sum(b.min_seconds for b in BEATS),1030)
    def test_formula_references(self):self.assertTrue(all(b.formula in FORMULAS for b in BEATS))
    def test_four(self):self.assertEqual(len(circular_representatives(4)),6)
    def test_six(self):self.assertEqual(len(self.six),120)
    def test_seven(self):self.assertEqual(len(self.seven),720)
    def test_six_canonical_A(self):self.assertTrue(all(p[0]==0 for p in self.six))
    def test_unique_representatives(self):self.assertEqual(len(set(self.six)),len(self.six))
    def test_adjacency_symmetric(self):
        self.assertTrue(all(neighbors(p,0,1)==neighbors(p,1,0) for p in self.six))
    def test_adjacency_48(self):self.assertEqual(sum(neighbors(p,0,1) for p in self.six),48)
    def test_nonadjacency_72(self):self.assertEqual(sum(not neighbors(p,0,1) for p in self.six),72)
    def test_partition_120(self):
        self.assertEqual(sum(neighbors(p,0,1) for p in self.six)+sum(not neighbors(p,0,1) for p in self.six),120)
    def test_adjacency_7(self):self.assertEqual(sum(neighbors(p,0,1) for p in self.seven),240)
    def test_nonadjacency_7(self):self.assertEqual(sum(not neighbors(p,0,1) for p in self.seven),480)
    def test_alt_12(self):self.assertEqual(sum(alternating(p) for p in self.six),12)
    def test_alt_formula(self):self.assertEqual(math.factorial(2)*math.factorial(3),12)
    def test_opposite_24(self):self.assertEqual(sum(opposite(p,0,1) for p in self.six),24)
    def test_opposite_symmetric(self):self.assertTrue(all(opposite(p,0,1)==opposite(p,1,0) for p in self.six))
    def test_couples_nonadjacent_32(self):self.assertEqual(sum(no_couple_adjacent(p) for p in self.six),32)
    def test_couples_events_each_48(self):
        for j in range(3):self.assertEqual(sum(neighbors(p,j,j+3) for p in self.six),48)
    def test_couples_pair_events_24(self):
        for a,b in ((0,1),(0,2),(1,2)):
            self.assertEqual(sum(neighbors(p,a,a+3) and neighbors(p,b,b+3) for p in self.six),24)
    def test_couples_three_events_16(self):self.assertEqual(sum(all(neighbors(p,j,j+3) for j in range(3)) for p in self.six),16)
    def test_inclusion_exclusion(self):self.assertEqual(120-3*48+3*24-16,32)
    def test_three_consecutive_seven_144(self):
        self.assertEqual(sum(any(set((p[i],p[(i+1)%7],p[(i+2)%7]))=={0,1,2} for i in range(7)) for p in self.seven),144)
    def test_flip_distinct_all_six(self):
        # Mirror reflection of six uniquely labelled people is never a mere rotation.
        st=set(self.six)
        for p in self.six:
            self.assertNotEqual(p,(p[0],)+tuple(reversed(p[1:])))
            self.assertIn((p[0],)+tuple(reversed(p[1:])),st)
    def test_mirror_orbits_60(self):
        unordered={min(p,(p[0],)+tuple(reversed(p[1:]))) for p in self.six}
        self.assertEqual(len(unordered),60)
    def test_scene_source(self):
        tree=ast.parse((ROOT/'episodes/comb11_circular_permutations.py').read_text(encoding='utf8'))
        self.assertIn('COMB11',[node.name for node in tree.body if isinstance(node,ast.ClassDef)])
    def test_workflow(self):
        wf=(ROOT/'.github/workflows/render-comb11-v2.yml').read_text()
        for s in ('workflow_dispatch:', 'quality:', 'voice:', 'comb11_circular_permutations.py','qa_comb11_v2.py','COMB11.mp4'):
            self.assertIn(s,wf)
    def test_typst_sources(self):
        self.assertEqual(len(list((ROOT/'assets/comb11v2').glob('*.typ'))),len(FORMULAS))
    def test_voice_manifest(self):
        m=json.loads((ROOT/'voice/comb11_voice_manifest.json').read_text(encoding='utf8'))
        self.assertEqual(m['beats'],48)
        self.assertGreater(m['target_seconds'],1030)
    def test_previous_episodes_preserved(self):
        for n in range(1,11):self.assertTrue(list((ROOT/'episodes').glob(f'comb{n:02}*.py')))
    def test_scripts_syntax(self):
        import py_compile
        for r in ('comb11_lesson_data.py','episodes/comb11_circular_permutations.py',
                  'scripts/prepare_comb11_v2.py','scripts/qa_comb11_v2.py'):
            py_compile.compile(str(ROOT/r),doraise=True)
    def test_documents(self):
        for r in ('HUONG_DAN_RENDER_COMB11_V2.md','narration_COMB11_v2.md','storyboard_COMB11_v2.md'):
            self.assertTrue((ROOT/r).is_file())

if __name__=='__main__':unittest.main()
