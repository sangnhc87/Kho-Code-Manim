from __future__ import annotations
import json,sys,unittest
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from int01.lesson import (CHAPTERS,SEGMENTS,FORMULAS,F,f,C,t,VELOCITY,POSITION,
                           PRACTICE_PRIMITIVE,PRACTICE_DERIVATIVE,validate,x)
from scripts.prepare_int01 import chunks,timestamp

class MathematicalChecks(unittest.TestCase):
    def test_storyboard_complete(self):
        self.assertTrue(validate());self.assertEqual(len(CHAPTERS),8);self.assertEqual(len(SEGMENTS),32)
        self.assertEqual(sorted({(q.chapter,q.step) for q in SEGMENTS}),[(i,j) for i in range(1,9) for j in range(1,5)])
    def test_formulas_referenced(self):
        self.assertTrue(all(q.formula in FORMULAS for q in SEGMENTS))
        self.assertEqual(len({q.title for q in SEGMENTS}),32)
    def test_derivative_and_family(self):
        self.assertEqual(sp.diff(F+C,x),2*x)
        for c in (-7,-1,0,2,5,25):self.assertEqual(sp.diff(F+c,x),2*x)
    def test_tangent_slope_family(self):
        for xc in [-2,-1,0,sp.Rational(1,2),1,2]:
            values={sp.diff(F+c,x).subs(x,xc) for c in [-2,0,2]}
            self.assertEqual(values,{2*xc})
    def test_difference_three_everywhere(self):
        self.assertEqual(sp.simplify((F+2)-(F-1)),3)
    def test_condition_unique(self):
        self.assertEqual(sp.solve(sp.Eq((F+C).subs(x,1),3),C),[2])
    def test_motion_velocity(self):
        self.assertEqual(sp.diff(POSITION,t),VELOCITY);self.assertEqual(POSITION.subs(t,0),2)
    def test_worked_example(self):
        self.assertEqual(sp.diff(PRACTICE_PRIMITIVE,x),PRACTICE_DERIVATIVE)
        self.assertEqual(PRACTICE_PRIMITIVE.subs(x,1),5)
    def test_source_clean(self):
        scene=(ROOT/'int01/scene.py').read_text(encoding='utf-8')
        self.assertIn('Thầy Nguyễn Văn Sang',scene)
        self.assertNotIn("tx('nhịp",scene);self.assertNotIn('Text("Manim–Typst"',scene)
    def test_no_answer_spoiler(self):
        self.assertEqual(SEGMENTS[28].formula,'practice')
        self.assertEqual(SEGMENTS[29].formula,'practice_primitive')
        self.assertEqual(SEGMENTS[30].formula,'practice_condition')
        self.assertEqual(SEGMENTS[31].formula,'practice_final')
    def test_narration_present(self):
        for s in SEGMENTS:
            self.assertGreaterEqual(len(s.voice),85)
            self.assertGreaterEqual(len(s.takeaway),10)
            self.assertGreaterEqual(s.duration,20)
    def test_subtitle_timestamps(self):
        self.assertEqual(timestamp(0),'00:00:00,000')
        self.assertEqual(timestamp(61.231),'00:01:01,231')
        self.assertGreater(len(chunks(SEGMENTS[0].voice)),1)
    def test_runtime_plan(self):
        data=json.loads((ROOT/'int01/runtime_plan.json').read_text(encoding='utf8'))
        self.assertEqual(len(data['segments']),32)
        self.assertEqual(data['total_duration'],sum(a['duration'] for a in data['segments']))
        self.assertEqual(data['voice'],'off')
    def test_all_graph_variants_exist(self):
        source=(ROOT/'int01/scene.py').read_text(encoding='utf8')
        for kind in sorted({q.visual for q in SEGMENTS}):self.assertIn(repr(kind),source)
if __name__=='__main__':unittest.main()
