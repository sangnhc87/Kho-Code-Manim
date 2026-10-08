"""Mathematical, production and packaging checks for COMB07."""
import ast,json,sys,unittest
from itertools import combinations,permutations
from math import comb,factorial,perm
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from comb07_lesson_data import BEATS,FORMULAS,CHAPTER_IDS,groups,ordered_groups,restricted_teams,teams_with_captain,validate
from series_config import symbol

class Combinatorics(unittest.TestCase):
    def test_5_choose_3(self):self.assertEqual(len(groups(5,3)),10)
    def test_5_arrange_3(self):self.assertEqual(len(ordered_groups(5,3)),60)
    def test_single_team_six_orders(self):self.assertEqual(len(tuple(permutations('ABC',3))),6)
    def test_single_team_six_same_group(self):self.assertEqual({frozenset(p) for p in permutations('ABC',3)},{frozenset('ABC')})
    def test_five_groups_are_unique(self):self.assertEqual(len({frozenset(g) for g in groups(5,3)}),10)
    def test_list_ten_exact(self):self.assertEqual([''.join(x) for x in groups(5,3)],['ABC','ABD','ABE','ACD','ACE','ADE','BCD','BCE','BDE','CDE'])
    def test_six_teams_with_a(self):self.assertEqual(sum('A' in q for q in groups(5,3)),6)
    def test_four_without_a(self):self.assertEqual(sum('A' not in q for q in groups(5,3)),4)
    def test_empty(self):self.assertEqual(comb(5,0),1)
    def test_all(self):self.assertEqual(comb(5,5),1)
    def test_choose_one(self):self.assertEqual(comb(7,1),7)
    def test_symmetry(self):
        for n in range(1,9):
            for k in range(n+1):self.assertEqual(comb(n,k),comb(n,n-k))
    def test_relation(self):
        for n in range(1,9):
            for k in range(n+1):self.assertEqual(comb(n,k)*factorial(k),perm(n,k))
    def test_pascal(self):
        for n in range(2,9):
            for k in range(1,n):self.assertEqual(comb(n,k),comb(n-1,k-1)+comb(n-1,k))
    def test_pascal_six(self):self.assertEqual(comb(6,3),comb(5,2)+comb(5,3))
    def test_7choose2(self):self.assertEqual(comb(7,2),21)
    def test_no_ab_both(self):self.assertEqual(len(restricted_teams()),16)
    def test_forbidden_ab(self):self.assertEqual(sum('A' in g and 'B' in g for g in groups(6,3)),4)
    def test_direct_count_alternative(self):self.assertEqual(comb(4,3)+2*comb(4,2),16)
    def test_no_both_ab(self):self.assertTrue(all(not {'A','B'}<=set(g) for g in restricted_teams()))
    def test_one_required_one_banned(self):self.assertEqual(sum('A' in t and 'B' not in t for t in groups(7,3)),10)
    def test_eight_choose_three(self):self.assertEqual(comb(8,3),56)
    def test_captains_total(self):self.assertEqual(len(teams_with_captain()),168)
    def test_each_team_three_captains(self):self.assertEqual(set(Counter(t for t,_ in teams_with_captain()).values()),{3})
    def test_each_captain_21_teams(self):self.assertEqual(set(Counter(c for _,c in teams_with_captain()).values()),{21})
    def test_six_choose_two(self):self.assertEqual(comb(6,2),15)
    def test_at_least_one_female(self):
        teams=combinations('MMMMFFF',3)
        # Differentiate the four men and three women by their indices.
        count=sum(any(j>=4 for j in t) for t in combinations(range(7),3))
        self.assertEqual(count,31)
    def test_exact_two_males_one_female(self):self.assertEqual(sum(sum(j<4 for j in t)==2 for t in combinations(range(7),3)),18)
    def test_sum_of_subsets(self):self.assertEqual(sum(comb(5,k) for k in range(6)),32)

class Production(unittest.TestCase):
    def test_validate(self):self.assertTrue(validate())
    def test_48_beats(self):self.assertEqual(len(BEATS),48)
    def test_8_chapters(self):self.assertEqual(len(CHAPTER_IDS),8)
    def test_6_per_chapter(self):self.assertEqual(Counter(b.section for b in BEATS),{k:6 for k in CHAPTER_IDS})
    def test_narration_over_3000_words(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),3000)
    def test_base_over_15_min(self):self.assertGreater(sum(b.min_seconds for b in BEATS),900)
    def test_unique_headings(self):self.assertEqual(len({b.heading for b in BEATS}),48)
    def test_formula_keys(self):self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
    def test_user_notation(self):self.assertEqual(symbol('C',5,3),'C^(5)_(3)')
    def test_tex_order(self):self.assertIn('C^(n)_(k)',FORMULAS['general'])
    def test_all_srt(self):self.assertGreater((ROOT/'subtitles_COMB07_v2.srt').read_text().count('-->'),140)
    def test_audio_manifest(self):
        m=json.loads((ROOT/'voice/comb07_voice_manifest.json').read_text())
        self.assertEqual(m['beats'],48)
        self.assertGreater(m['target_seconds'],900)
    def test_ast(self):
        for name in ('episodes/comb07_combinations.py','comb07_lesson_data.py','scripts/prepare_comb07_v2.py','scripts/qa_comb07_v2.py'):
            with self.subTest(path=name):ast.parse((ROOT/name).read_text())
    def test_workflow(self):
        x=(ROOT/'.github/workflows/render-comb07-v2.yml').read_text()
        for s in ('workflow_dispatch','comb07_combinations.py','prepare_comb07_v2.py','qa_comb07_v2.py','COMB07'):
            self.assertIn(s,x)
    def test_prior_episodes_preserved(self):
        for name in ('comb01_rule_of_sum.py','comb02_rule_of_product.py','comb03_tree_sample_space.py','comb04_order_matters.py','comb05_permutations.py','comb06_arrangements.py','geo01_point_inside_triangle.py'):
            self.assertTrue((ROOT/'episodes'/name).is_file())

if __name__=='__main__':unittest.main()
