import ast
from itertools import permutations, combinations, product
from pathlib import Path
import os
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import series_config as cfg


class TestCombinatorics(unittest.TestCase):
    def test_sum_routes(self):
        buses = [('bus', i) for i in range(2)]
        trains = [('train', i) for i in range(3)]
        self.assertEqual(len(set(buses) | set(trains)), 5)
        self.assertTrue(set(buses).isdisjoint(trains))

    def test_book_choices(self):
        maths = {f'T{i}' for i in range(1,5)}
        physics = {f'L{i}' for i in range(1,4)}
        self.assertEqual(len(maths | physics), 7)

    def test_overlapping_sets(self):
        A = {i for i in range(1,13) if i % 2 == 0}
        B = {i for i in range(1,13) if i % 3 == 0}
        self.assertEqual((len(A), len(B), len(A & B)), (6,4,2))
        self.assertEqual(len(A | B), 8)
        self.assertEqual(len(A)+len(B)-len(A&B), len(A|B))

    def test_exercise(self):
        self.assertEqual(len({f'A{i}' for i in range(5)} | {f'B{i}' for i in range(2)}), 7)

    def test_next_episode_math(self):
        self.assertEqual(len(list(product(range(3), range(2)))), 6)
        self.assertEqual(len([x for x in product(range(3), range(2)) if x != (0,1)]), 5)
        self.assertEqual(len(list(product('NS',repeat=3))),8)
        self.assertEqual(sum('NN' not in ''.join(a) for a in product('NS', repeat=3)),5)

    def test_arrangements_and_combinations(self):
        self.assertEqual(len(list(permutations('ABCD',2))), 12)
        self.assertEqual(len(list(combinations('ABCD',2))), 6)
        self.assertEqual(cfg.arrangement(6,3),120)
        self.assertEqual(cfg.combination(5,3),10)
        self.assertEqual(cfg.arrangement(7,3)-cfg.arrangement(6,2),180)
        self.assertEqual(cfg.combination(6,3)-cfg.combination(4,1),16)
        self.assertEqual(cfg.combination(8,3)*3,168)

    def test_explicit_index_order(self):
        expected = 'C^(n)_(k)' if cfg.NOTATION == 'user' else 'C_(n)^(k)'
        self.assertEqual(cfg.symbol('C','n','k'),expected)

    def test_source_parse(self):
        src = ROOT/'episodes'/'comb01_rule_of_sum.py'
        ast.parse(src.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
