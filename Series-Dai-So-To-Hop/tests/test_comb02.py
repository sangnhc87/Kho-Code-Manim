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
        formula_names = [node.args[0].value for node in ast.walk(tree)
                         if isinstance(node,ast.Call) and isinstance(node.func,ast.Name)
                         and node.func.id == 'formula_asset' and node.args
                         and isinstance(node.args[0],ast.Constant) and isinstance(node.args[0].value,str)]
        # Assets are also passed through explanation(... formula=(...), ...)
        script = (ROOT/'scripts'/'build_formulas.py').read_text('utf8')
        for key in ['comb02_product6','comb02_productgeneral','comb02_product12',
                    'comb02_forbidden5','comb02_branch5','comb02_quiz12']:
            self.assertIn(key,source)
            self.assertIn(f"'{key}':",script)

    def test_manifest_and_workflow(self):
        manifest = json.loads((ROOT/'season_manifest.json').read_text('utf8'))
        ep = next(e for e in manifest['episodes'] if e['id'] == 'COMB02')
        self.assertEqual(ep['scene'],'COMB02')
        self.assertTrue((ROOT/ep['source']).is_file())
        self.assertTrue((ROOT/ep['workflow']).is_file())


if __name__ == '__main__':
    unittest.main()
