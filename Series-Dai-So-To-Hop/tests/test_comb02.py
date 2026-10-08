"""Math and source contract for COMB02, independent of rendering packages."""
from itertools import product
from pathlib import Path
import ast
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]


class TestCOMB02(unittest.TestCase):
    def test_all_outfits_distinct(self):
        outfits = list(product(range(1,4), range(1,3)))
        self.assertEqual(len(outfits), 6)
        self.assertEqual(len(set(outfits)), 6)

    def test_each_shirt_has_two_ways(self):
        outfits = list(product(range(1,4), range(1,3)))
        self.assertEqual([sum(x == i for x, y in outfits) for i in range(1,4)], [2, 2, 2])

    def test_shirts_pants_hats(self):
        self.assertEqual(len(list(product(range(3), range(2), range(2)))), 12)

    def test_forbidden_pair(self):
        outfits = set(product(range(1,4), range(1,3)))
        valid = outfits - {(1,2)}
        self.assertEqual(len(valid),5)
        self.assertNotIn((1,2), valid)
        self.assertEqual([sum(s == i for s,p in valid) for i in range(1,4)], [1,2,2])

    def test_or_different_from_and(self):
        choose_one = {('shirt', i) for i in range(3)} | {('pants', j) for j in range(2)}
        choose_both = set(product(range(3), range(2)))
        self.assertEqual((len(choose_one),len(choose_both)), (5,6))

    def test_quiz(self):
        self.assertEqual(len(set(product(range(2),range(3),range(2)))),12)

    def test_syntax_scene_and_asset_keys(self):
        source = (ROOT/'episodes'/'comb02_rule_of_product.py').read_text('utf8')
        tree = ast.parse(source)
        classes = [n for n in tree.body if isinstance(n,ast.ClassDef)]
        self.assertIn('COMB02',[c.name for c in classes])
        lesson=(ROOT/'comb02_lesson_data.py').read_text('utf8')
        prepare=(ROOT/'scripts'/'prepare_comb02_v2.py').read_text('utf8')
        self.assertIn('FORMULAS = {',lesson)
        self.assertIn('formula_sources()',prepare)
        self.assertIn('formula_png(beat.formula)',source)

    def test_manifest_and_workflow(self):
        manifest = json.loads((ROOT/'season_manifest.json').read_text('utf8'))
        ep = next(e for e in manifest['episodes'] if e['id'] == 'COMB02')
        self.assertEqual(ep['scene'],'COMB02')
        self.assertTrue((ROOT/ep['source']).is_file())
        self.assertTrue((ROOT.parent/ep['workflow']).is_file())


if __name__ == '__main__':
    unittest.main()
