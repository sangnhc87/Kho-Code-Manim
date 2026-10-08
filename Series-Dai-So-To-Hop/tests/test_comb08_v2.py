"""Mathematical and structural checks for Season One finale COMB08."""
from __future__ import annotations
import ast,json,sys,unittest
from collections import Counter
from itertools import combinations,permutations
from math import comb,perm,factorial
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from series_config import symbol
from comb08_lesson_data import (BEATS,FORMULAS,CHAPTER_IDS,CHAPTER_LABELS,
  all_captain_teams,advanced_teams,even_numbers,constrained_roles,gender_teams,validate)

class Mathematics(unittest.TestCase):
    def test_6_factorial(self):self.assertEqual(factorial(6),720)
    def test_6_ordered_pairs(self):self.assertEqual(perm(6,2),30)
    def test_6_unordered_pairs(self):self.assertEqual(comb(6,2),15)
    def test_two_orders_per_pair(self):
        for p in combinations('ABCDEF',2):
            self.assertEqual(len(tuple(permutations(p))),2)
    def test_relation_for_n_to_8(self):
        for n in range(9):
            for k in range(n+1):
                self.assertEqual(perm(n,k),comb(n,k)*factorial(k))
    def test_8_captain(self):self.assertEqual(len(all_captain_teams()),168)
    def test_8_captain_each_team(self):
        self.assertEqual(set(Counter(t for t,leader in all_captain_teams()).values()),{3})
    def test_8_captain_each_leader(self):
        self.assertEqual(set(Counter(leader for t,leader in all_captain_teams()).values()),{21})
    def test_8_captain_alternate(self):self.assertEqual(8*comb(7,2),168)
    def test_forbidden_roles(self):self.assertEqual(len(constrained_roles()),180)
    def test_forbidden_roles_all(self):self.assertEqual(perm(7,3),210)
    def test_forbidden_roles_bad(self):
        self.assertEqual(sum(x[0]=='A' for x in permutations('ABCDEFG',3)),30)
    def test_forbidden_roles_no_A_leader(self):
        self.assertTrue(all(t[0]!='A' for t in constrained_roles()))
    def test_gender_total(self):self.assertEqual(comb(7,3),35)
    def test_gender_31(self):self.assertEqual(len(gender_teams()),31)
    def test_gender_all_men(self):
        self.assertEqual(sum(all(j<4 for j in t) for t in combinations(range(7),3)),4)
    def test_gender_2men_1woman(self):
        self.assertEqual(sum(sum(j<4 for j in t)==2 for t in gender_teams()),18)
    def test_gender_case_breakdown(self):
        c=Counter(sum(j>=4 for j in t) for t in gender_teams())
        self.assertEqual(dict(c),{1:18,2:12,3:1})
    def test_digit_all(self):
        nums={100*a+10*b+c for a,b,c in permutations(range(5),3) if a!=0}
        self.assertEqual(len(nums),48)
    def test_digit_even(self):self.assertEqual(len(even_numbers()),30)
    def test_digit_even_distinct(self):self.assertEqual(len(set(even_numbers())),30)
    def test_digit_even_valid(self):
        self.assertTrue(all(100<=q<1000 and q%2==0 and len(set(str(q)))==3 for q in even_numbers()))
    def test_digit_last0(self):self.assertEqual(sum(q%10==0 for q in even_numbers()),12)
    def test_digit_last2or4(self):self.assertEqual(sum(q%10 in (2,4) for q in even_numbers()),18)
    def test_digit_even_odd_partition(self):self.assertEqual(48-30,18)
    def test_capstone_87(self):self.assertEqual(len(advanced_teams()),87)
    def test_capstone_unique(self):self.assertEqual(len(set(advanced_teams())),87)
    def test_capstone_leader_not_A(self):self.assertTrue(all(leader!='A' for _,leader in advanced_teams()))
    def test_capstone_has_A_or_B(self):self.assertTrue(all('A' in t or 'B' in t for t,_ in advanced_teams()))
    def test_capstone_bad_no_AB(self):
        self.assertEqual(sum(not ('A' in t or 'B' in t) for t,leader in all_captain_teams()),60)
    def test_capstone_bad_A_leader(self):
        self.assertEqual(sum(leader=='A' for t,leader in all_captain_teams()),21)
    def test_capstone_bad_disjoint(self):
        self.assertEqual(sum(leader=='A' and 'A' not in t and 'B' not in t for t,leader in all_captain_teams()),0)
    def test_capstone_case_A(self):
        self.assertEqual(sum('A' in t for t,leader in advanced_teams()),42)
    def test_capstone_case_not_A_has_B(self):
        self.assertEqual(sum('A' not in t and 'B' in t for t,leader in advanced_teams()),45)
    def test_capstone_direct_and_complement(self):
        self.assertEqual(168-60-21,42+45)
    def test_capstone_third_method(self):
        self.assertEqual(comb(7,2)+6*(comb(7,2)-comb(5,2)),87)

class Production(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_48_beats(self):self.assertEqual(len(BEATS),48)
    def test_8_chapters(self):self.assertEqual(len(CHAPTER_IDS),8)
    def test_6_beats_per_chapter(self):
        self.assertEqual(Counter(b.section for b in BEATS),{c:6 for c in CHAPTER_IDS})
    def test_beat_names_unique(self):self.assertEqual(len({b.heading for b in BEATS}),48)
    def test_narration_full(self):self.assertGreaterEqual(sum(len(b.narration.split()) for b in BEATS),3500)
    def test_duration(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),960)
    def test_formula_keys(self):self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
    def test_user_notation(self):self.assertEqual(symbol('C',8,3),'C^(8)_(3)')
    def test_formula_user_notation(self):self.assertIn('C^(n)_(k)',FORMULAS['genericchoose'])
    def test_full_srt(self):self.assertGreater((ROOT/'subtitles_COMB08_v2.srt').read_text().count('-->'),150)
    def test_manifest(self):
        obj=json.loads((ROOT/'voice/comb08_voice_manifest.json').read_text())
        self.assertEqual(obj['beats'],48)
        self.assertGreater(obj['target_seconds'],1000)
    def test_scripts_compile(self):
        for f in ('episodes/comb08_synthesis.py','comb08_lesson_data.py',
                 'scripts/prepare_comb08_v2.py','scripts/qa_comb08_v2.py'):
            with self.subTest(f=f):ast.parse((ROOT/f).read_text(encoding='utf-8'))
    def test_workflow(self):
        text=(ROOT.parent/'.github/workflows/render-comb08-v2.yml').read_text()
        for v in ('workflow_dispatch','COMB08','prepare_comb08_v2.py','qa_comb08_v2.py','comb08_synthesis.py'):
            self.assertIn(v,text)
    def test_retained_prior_episodes(self):
        for name in ('comb01_rule_of_sum.py','comb02_rule_of_product.py','comb03_tree_sample_space.py',
                     'comb04_order_matters.py','comb05_permutations.py','comb06_arrangements.py',
                     'comb07_combinations.py','geo01_point_inside_triangle.py'):
            self.assertTrue((ROOT/'episodes'/name).is_file())

if __name__=='__main__':unittest.main()
