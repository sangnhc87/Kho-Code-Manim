"""Checks that every presented count and 48-beat lesson contract are sound."""
from __future__ import annotations
import ast,sys,json,unittest
from pathlib import Path
from itertools import combinations, permutations
from math import comb,perm,factorial
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb04_lesson_data import *

class Combinatorics(unittest.TestCase):
    def test_12_ordered_pairs(self):self.assertEqual(len(ORDERED4),12)
    def test_no_repeats_among_ordered(self):self.assertEqual(len(set(ORDERED4)),12)
    def test_ordered_pair_distinct_roles(self):self.assertTrue(all(a!=b for a,b in ORDERED4))
    def test_order_swap_distinct(self):self.assertIn('AB',ORDERED4);self.assertIn('BA',ORDERED4);self.assertNotEqual('AB','BA')
    def test_six_unordered_groups(self):self.assertEqual(len(UNORDERED4),6)
    def test_undirected_two_orientations(self):
        for canonical,choices in group_ordered_pairs().items():
            self.assertEqual(len(choices),2)
            self.assertEqual(set(choices),{canonical,canonical[::-1]})
    def test_classes_are_disjoint(self):
        groups=list(group_ordered_pairs().values())
        self.assertEqual(len(set(x for g in groups for x in g)),12)
    def test_bijection_all_pairs_to_groups(self):
        f=lambda pair:''.join(sorted(pair))
        counts=Counter(f(pair) for pair in ORDERED4)
        self.assertEqual(set(counts),set(UNORDERED4))
        self.assertEqual(set(counts.values()),{2})
    def test_5_choose_3(self):self.assertEqual(len(UNORDERED5_3),comb(5,3))
    def test_5_perm_3(self):self.assertEqual(perm(5,3),60)
    def test_abc_six(self):self.assertEqual(set(ORDERS_ABC),{''.join(x) for x in permutations('ABC')})
    def test_three_factorial_classes(self):
        reps=[''.join(x) for x in permutations('ABCDE',3)]
        classes=Counter(''.join(sorted(x)) for x in reps)
        self.assertEqual(len(classes),10)
        self.assertTrue(all(v==6 for v in classes.values()))
    def test_choose6(self):self.assertEqual(len(UNORDERED6_2),15)
    def test_roles6(self):self.assertEqual(perm(6,2),30)
    def test_group6_factor(self):self.assertEqual(perm(6,2)//2,comb(6,2))
    def test_five_awards(self):self.assertEqual(perm(5,2),20)
    def test_three_8_teams(self):self.assertEqual(comb(8,3),56)
    def test_captain_first(self):self.assertEqual(8*comb(7,2),168)
    def test_team_first(self):self.assertEqual(comb(8,3)*3,168)
    def test_both_168_enumerations_identical(self):self.assertEqual(team_with_captain(),team_with_captain_by_captain())
    def test_168_no_duplicates(self):self.assertEqual(len(team_with_captain()),168)
    def test_336_double_count(self):self.assertEqual(8*7*6//2,168)
    def test_captain_member_of_team(self):self.assertTrue(all(cap in team for team,cap in team_with_captain()))

class Production(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_8_chapters(self):self.assertEqual(len(CHAPTER_IDS),8)
    def test_48_beats(self):self.assertEqual(len(BEATS),48)
    def test_each_chapter_six(self):self.assertEqual(Counter(b.section for b in BEATS),dict.fromkeys(CHAPTER_IDS,6))
    def test_distinct_headers(self):self.assertEqual(len({b.heading for b in BEATS}),48)
    def test_narration_word_count(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),2200)
    def test_not_short(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),810)
    def test_formulas_exist(self):self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
    def test_manifest_exists(self):self.assertTrue((ROOT/'voice/comb04_voice_manifest.json').is_file())
    def test_manifest_contract(self):
        d=json.loads((ROOT/'voice/comb04_voice_manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['clips']),len(BEATS))
        self.assertEqual(d['beats'],48)
        self.assertGreaterEqual(d['target_seconds'],810)
    def test_srt_cues(self):
        s=(ROOT/'subtitles_COMB04_v2.srt').read_text(encoding='utf-8')
        self.assertGreater(s.count('-->'),120)
    def test_episode_python_syntax(self):ast.parse((ROOT/'episodes/comb04_order_matters.py').read_text(encoding='utf-8'))
    def test_prepare_python_syntax(self):ast.parse((ROOT/'scripts/prepare_comb04_v2.py').read_text(encoding='utf-8'))
    def test_qa_python_syntax(self):ast.parse((ROOT/'scripts/qa_comb04_v2.py').read_text(encoding='utf-8'))
    def test_workflow_and_scene(self):
        w=(ROOT.parent/'.github/workflows/render-comb04-v2.yml').read_text()
        self.assertIn('episodes/comb04_order_matters.py COMB04',w)
        self.assertIn('scripts/prepare_comb04_v2.py',w)
        self.assertIn('scripts/qa_comb04_v2.py',w)
    def test_previous_scenes_preserved(self):
        for path in ('episodes/comb01_rule_of_sum.py','episodes/comb02_rule_of_product.py','episodes/comb03_tree_sample_space.py','episodes/geo01_point_inside_triangle.py'):
            self.assertTrue((ROOT/path).is_file())

if __name__=='__main__':unittest.main()
