"""Mathematical and production-contract tests for COMB03 V2."""
import ast
import json
import sys
import unittest
from collections import Counter
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb03_lesson_data import (BEATS, CHAPTER_IDS, CHAPTER_LABELS, FORMULAS,
    OMEGA_3, OMEGA_4, EXACTLY_TWO_N, NO_ADJACENT_N, BAD_ADJACENT_N,
    NO_ADJACENT_4, TREE_PREFIXES, BRANCH_DEGREES, validate)


class Combinatorics(unittest.TestCase):
    def test_space_complete(self):
        self.assertEqual(len(OMEGA_3),8)
        self.assertEqual(len(set(OMEGA_3)),8)

    def test_each_leaf_three_steps(self):
        self.assertTrue(all(len(x)==3 for x in OMEGA_3))
        self.assertTrue(all(set(x)<=set('NS') for x in OMEGA_3))

    def test_prefix_tree_count(self):
        for depth in (1,2,3):
            self.assertEqual(len(TREE_PREFIXES[depth]),2**depth)

    def test_full_binary_tree_reconstructs_every_sequence(self):
        for leaf in OMEGA_3:
            self.assertEqual([leaf[:k] for k in (1,2,3)][-1],leaf)
            self.assertTrue(all(leaf[:k] in TREE_PREFIXES[k] for k in (1,2,3)))

    def test_exactly_two_heads(self):
        self.assertEqual(EXACTLY_TWO_N,('NNS','NSN','SNN'))

    def test_exactly_one_head(self):
        self.assertEqual({v for v in OMEGA_3 if v.count('N')==1}, {'NSS','SNS','SSN'})

    def test_first_tails(self):
        self.assertEqual({v for v in OMEGA_3 if v.startswith('S')}, {'SNN','SNS','SSN','SSS'})

    def test_no_consecutive_heads(self):
        self.assertEqual(set(NO_ADJACENT_N),{'NSN','NSS','SNS','SSN','SSS'})

    def test_bad_consecutive_heads(self):
        self.assertEqual(set(BAD_ADJACENT_N),{'NNN','NNS','SNN'})

    def test_event_complement_partitions_sample_space(self):
        self.assertFalse(set(NO_ADJACENT_N)&set(BAD_ADJACENT_N))
        self.assertEqual(set(NO_ADJACENT_N)|set(BAD_ADJACENT_N),set(OMEGA_3))

    def test_four_coin_sequences(self):
        self.assertEqual(len(OMEGA_4),16)
        self.assertEqual(len(NO_ADJACENT_4),8)

    def test_four_coin_partition(self):
        good=set(NO_ADJACENT_4)
        end_s={v for v in good if v.endswith('S')}
        end_sn={v for v in good if v.endswith('SN')}
        self.assertEqual((len(end_s),len(end_sn)),(5,3))
        self.assertEqual(end_s|end_sn,good)
        self.assertFalse(end_s&end_sn)

    def test_fibonacci_initial_conditions(self):
        f=lambda n:sum('NN' not in ''.join(x) for x in product('NS',repeat=n))
        self.assertEqual([f(k) for k in range(5)],[1,2,3,5,8])
        self.assertEqual(f(4),f(3)+f(2))

    def test_unequal_branches(self):
        self.assertEqual(BRANCH_DEGREES,(2,1,3))
        self.assertEqual(sum(BRANCH_DEGREES),6)

    def test_probabilities_if_fair(self):
        from fractions import Fraction
        self.assertEqual(Fraction(len(EXACTLY_TWO_N),len(OMEGA_3)),Fraction(3,8))
        self.assertEqual(Fraction(len(NO_ADJACENT_N),len(OMEGA_3)),Fraction(5,8))


class Production(unittest.TestCase):
    def test_beats_validate(self):
        self.assertTrue(validate())

    def test_eight_chapters_six_beats_each(self):
        self.assertEqual(len(CHAPTER_IDS),8)
        self.assertEqual(Counter(b.section for b in BEATS),dict.fromkeys(CHAPTER_IDS,6))

    def test_beat_order(self):
        for chapter in CHAPTER_IDS:
            self.assertEqual([x.state for x in BEATS if x.section==chapter],list(range(6)))

    def test_script_has_substance(self):
        self.assertGreater(sum(len(b.narration.split()) for b in BEATS),2000)
        self.assertTrue(all(len(b.narration.split())>=27 for b in BEATS))

    def test_timing_minimum(self):
        self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),780)

    def test_every_formula_defined(self):
        self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))

    def test_python_source_valid(self):
        for f in ['episodes/comb03_tree_sample_space.py','scripts/prepare_comb03_v2.py','scripts/qa_comb03_v2.py']:
            ast.parse((ROOT/f).read_text(encoding='utf-8'),filename=f)

    def test_manifest_scene(self):
        manifest=json.loads((ROOT/'season_manifest.json').read_text(encoding='utf-8'))
        record=next(e for e in manifest['episodes'] if e['id']=='COMB03')
        self.assertEqual(record['scene'],'COMB03')
        self.assertTrue((ROOT/record['source']).is_file())
        self.assertTrue((ROOT.parent/record['workflow']).is_file())

    def test_manifest_clip_coverage_if_prepared(self):
        p=ROOT/'voice/comb03_voice_manifest.json'
        if not p.exists():self.skipTest('Run preparation script first')
        data=json.loads(p.read_text(encoding='utf-8'))
        self.assertEqual(data['beats'],48)
        self.assertEqual(len(data['clips']),48)
        self.assertGreaterEqual(data['target_seconds'],780)


if __name__=='__main__':unittest.main()
