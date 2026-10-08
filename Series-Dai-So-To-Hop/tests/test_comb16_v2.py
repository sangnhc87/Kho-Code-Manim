"""Tests of group partitioning formulas and COMB16 GitHub deliverables."""
from collections import Counter
from math import comb, factorial
from pathlib import Path
import sys,unittest,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb16_lesson_data import (CHAPTERS,BEATS,FORMULAS,validate,
    math_counts,partitions_of_size,three_triplets)

class GroupCountingTests(unittest.TestCase):
    def test_validation(self):self.assertTrue(validate())
    def test_equal_partition_enumeration(self):
        p=partitions_of_size('ABCDEFGH',(4,4))
        self.assertEqual(len(p),35)
        self.assertEqual(len({tuple(sorted(part)) for part in p}),35)
    def test_unequal(self):
        self.assertEqual(comb(8,3),56)
        self.assertEqual(factorial(9)//(factorial(2)*factorial(3)*factorial(4)),1260)
    def test_labeled_three_teams(self):
        self.assertEqual(comb(9,3)*comb(6,3),1680)
        self.assertEqual(comb(9,3)*comb(6,3)//factorial(3),280)
    def test_pairings_six(self):
        pairs=partitions_of_size('ABCDEF',(2,2,2))
        self.assertEqual(len(pairs),15)
        self.assertEqual(factorial(6)//((factorial(2)**3)*factorial(3)),15)
    def test_pairings_eight(self):
        pairs=partitions_of_size('ABCDEFGH',(2,2,2,2))
        self.assertEqual(len(pairs),105)
        self.assertEqual(factorial(8)//((factorial(2)**4)*factorial(4)),105)
    def test_chosen_six_then_paired(self):self.assertEqual(comb(9,6)*15,1260)
    def test_captains(self):
        self.assertEqual(comb(8,3)*3,168)
        self.assertEqual(280*3**3,7560)
    def test_four_four_same(self):
        p=partitions_of_size('ABCDEFGH',(4,4))
        same=sum(any({'A','B'}<=set(g) for g in x) for x in p)
        self.assertEqual(same,15)
    def test_four_four_different(self):
        p=partitions_of_size('ABCDEFGH',(4,4))
        separate=sum(not any({'A','B'}<=set(g) for g in x) for x in p)
        self.assertEqual(separate,20)
        self.assertEqual(separate,comb(6,3))
    def test_three_three_three(self):
        groups=three_triplets()
        self.assertEqual(len(groups),280)
        same=sum(any('A' in g and 'B' in g for g in pp) for pp in groups)
        different=len(groups)-same
        self.assertEqual((same,different),(70,210))
        self.assertEqual(same,7*comb(6,3)//2)
        self.assertEqual(different,comb(7,2)*comb(5,2))
    def test_capstone_two_methods(self):
        p=three_triplets()
        good=[q for q in p if all(not ('A' in group and 'B' in group) for group in q)]
        self.assertEqual(len(good),210)
        self.assertEqual(len(good)*27,5670)
        self.assertEqual((280-70)*27,comb(7,2)*comb(5,2)*27)
    def test_exhaustive_model(self):
        c=math_counts()
        self.assertEqual(c['capstone'],5670)
        self.assertEqual(c['pairs_eight'],105)

class VideoDataTests(unittest.TestCase):
    def test_beat_count(self):self.assertEqual((len(CHAPTERS),len(BEATS),len(FORMULAS)),(8,48,48))
    def test_six_beats_each(self):self.assertEqual(Counter(x.section for x in BEATS),{x[0]:6 for x in CHAPTERS})
    def test_formulas_exist(self):self.assertTrue(all(b.formula in FORMULAS for b in BEATS))
    def test_typst_notation_style(self):
        text=' '.join(FORMULAS.values())
        self.assertIn('C_(3)^(8)',text)
        self.assertIn('C_(2)^(7)',text)
        self.assertNotIn('binom',text)
    def test_minimum_narration(self):
        self.assertGreaterEqual(sum(len(x.narration.split()) for x in BEATS),3400)
        self.assertGreaterEqual(min(len(x.narration.split()) for x in BEATS),45)
    def test_timing(self):self.assertGreaterEqual(sum(x.min_seconds for x in BEATS),1100)
    def test_scene_import_target(self):
        src=(ROOT/'episodes/comb16_group_division.py').read_text(encoding='utf-8')
        self.assertIn('class COMB16(Scene)',src)
        self.assertIn('def model(section,state)',src)
    def test_action_workflow(self):
        wf=(ROOT/'.github/workflows/render-comb16-v2.yml').read_text(encoding='utf-8')
        for q in ('COMB16','comb16_group_division.py','prepare_comb16_v2.py','qa_comb16_v2.py','upload-artifact'):
            self.assertIn(q,wf)
    def test_preparer_exists(self):self.assertTrue((ROOT/'scripts/prepare_comb16_v2.py').is_file())
    def test_expected_assets(self):self.assertTrue((ROOT/'comb16_beats.json').is_file())
    def test_chapter_order(self):self.assertEqual([x.state for x in BEATS],list(range(6))*8)

if __name__=='__main__':unittest.main()
