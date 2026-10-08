"""Pure Python maths tests: run without Manim, Typst or network."""
import itertools
import json
import math
import sys
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb02_lesson_data import BEATS,CHAPTER_LABELS,FORMULAS,validate

class TestPedagogy(unittest.TestCase):
    def test_storyboard_valid(self):self.assertTrue(validate())
    def test_44_beats(self):self.assertEqual(len(BEATS),44)
    def test_eight_chapters(self):self.assertEqual(len(CHAPTER_LABELS),8)
    def test_first_and_last(self):
        self.assertEqual((BEATS[0].section,BEATS[-1].section),('outfit','quiz'))
    def test_minimum_duration(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS)+5.2,750)
    def test_formulas_referenced(self):
        self.assertEqual({b.formula for b in BEATS if b.formula}-set(FORMULAS),set())
    def test_full_narration(self):
        self.assertTrue(all(len(b.narration.split())>=25 for b in BEATS))
        self.assertGreater(sum(len(b.narration.split()) for b in BEATS),1600)
    def test_narration_generated(self):
        doc=(ROOT/'narration_COMB02_v2.md').read_text(encoding='utf-8')
        self.assertIn(BEATS[0].narration,doc)
        self.assertIn(BEATS[-1].narration,doc)
    def test_srt_timing(self):
        srt=(ROOT/'subtitles_COMB02_v2.srt').read_text(encoding='utf-8')
        self.assertIn('00:00:00,000',srt)
        self.assertIn('-->',srt)
    def test_manifest(self):
        data=json.loads((ROOT/'voice'/'comb02_voice_manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(data['beats'],len(BEATS))
        self.assertGreaterEqual(data['target_seconds'],750)

class TestCombinatorialCounts(unittest.TestCase):
    A=('A1','A2','A3');Q=('Q1','Q2')
    def test_six_pairs(self):
        pairs=list(itertools.product(self.A,self.Q))
        self.assertEqual(len(pairs),6)
        self.assertEqual(len(set(pairs)),6)
    def test_two_per_shirt(self):
        self.assertEqual([sum(1 for q in self.Q) for a in self.A],[2,2,2])
    def test_grid_count(self):self.assertEqual(sum([2]*3),3*2)
    def test_three_steps(self):
        triples=list(itertools.product(self.A,self.Q,('M1','M2')))
        self.assertEqual(len(set(triples)),12)
    def test_forbidden_one(self):
        pairs={(a,q) for a in self.A for q in self.Q if (a,q)!=('A2','Q2')}
        self.assertEqual(len(pairs),5)
        self.assertEqual([sum((a,q) in pairs for q in self.Q) for a in self.A],[2,1,2])
    def test_forbidden_complement(self):
        pairs=set(itertools.product(self.A,self.Q))
        self.assertEqual(len(pairs-{('A2','Q2')}),len(pairs)-1)
    def test_uneven_branches(self):
        choices={'A1':('Q1','Q2'),'A2':('Q1',),'A3':('Q1','Q2','Q3')}
        outcomes={(a,q) for a,qs in choices.items() for q in qs}
        self.assertEqual(len(outcomes),2+1+3)
    def test_number_formation(self):
        numbers={10*a+b for a,b in itertools.permutations((1,2,3,4),2)}
        self.assertEqual(len(numbers),12)
        self.assertTrue(all(10<=x<100 for x in numbers))
    def test_or_choose_one_item(self):
        self.assertEqual(len({('but',i) for i in range(3)}|{('vo',j) for j in range(2)}),5)
    def test_forbidden_two(self):
        shirts=range(1,5);pants=range(1,4)
        eligible={(a,q) for a in shirts for q in pants if (a,q) not in {(1,2),(1,3)}}
        self.assertEqual(len(eligible),10)
        self.assertEqual([sum((a,q) in eligible for q in pants) for a in shirts],[1,3,3,3])
    def test_general_rule_small(self):
        for m in range(1,7):
            for n in range(1,7):
                self.assertEqual(len(list(itertools.product(range(m),range(n)))),m*n)
    def test_variable_branch_general(self):
        for factor in ((),(0,),(2,),(1,3,2),(0,4,1,0,2)):
            outcomes=[(i,j) for i,k in enumerate(factor) for j in range(k)]
            self.assertEqual(len(outcomes),sum(factor))
    def test_multiplication_special_case(self):
        for m in range(1,5):
            for n in range(1,5):self.assertEqual(sum([n]*m),m*n)
    def test_wrong_mul_when_branch_changes(self):
        self.assertNotEqual(sum([2,1,3]),3*3)
    def test_no_double_count_in_tree(self):
        paths=[(a,q) for a in self.A for q in self.Q]
        self.assertEqual(len(paths),len(set(paths)))

if __name__=='__main__':unittest.main()
