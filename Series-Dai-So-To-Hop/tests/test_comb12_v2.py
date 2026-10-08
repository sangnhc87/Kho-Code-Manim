"""Independent combinatorial checks and GitHub production package guards."""
import ast, json, math, pathlib, sys, unittest
from itertools import permutations
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb12_lesson_data import BEATS,CHAPTER_LABELS,FORMULAS,adjacent,consecutive_group,validate

class TestCOMB12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p5=list(permutations(range(5)))
        cls.p6=list(permutations(range(6)))
        cls.p7=list(permutations(range(7)))
        cls.ab=staticmethod(lambda p:adjacent(p,0,1))
        cls.cd=staticmethod(lambda p:adjacent(p,2,3))
        cls.ef=staticmethod(lambda p:adjacent(p,4,5))

    def test_validate(self):self.assertTrue(validate())
    def test_48_beats(self):self.assertEqual(len(BEATS),48)
    def test_eight_chapters(self):self.assertEqual(len(CHAPTER_LABELS),8)
    def test_chapter_state_order(self):
        for key in CHAPTER_LABELS:self.assertEqual([x.state for x in BEATS if x.section==key],list(range(6)))
    def test_word_count(self):self.assertGreater(sum(len(b.narration.split()) for b in BEATS),3000)
    def test_minimum_beat_narration(self):self.assertTrue(all(len(b.narration.split())>=38 for b in BEATS))
    def test_base_duration(self):self.assertGreater(sum(b.min_seconds for b in BEATS),1080)
    def test_formula_names(self):self.assertTrue(all(b.formula in FORMULAS for b in BEATS))
    def test_each_formula_unique(self):self.assertEqual(len(FORMULAS),48)
    def test_five_pair_total(self):self.assertEqual(sum(self.ab(p) for p in self.p5),48)
    def test_five_pair_direct(self):self.assertEqual(4*2*math.factorial(3),48)
    def test_six_total(self):self.assertEqual(len(self.p6),720)
    def test_six_pair_total(self):self.assertEqual(sum(self.ab(p) for p in self.p6),240)
    def test_six_group_three(self):self.assertEqual(sum(consecutive_group(p,(0,1,2)) for p in self.p6),144)
    def test_six_group_three_order(self):
        self.assertEqual(sum(consecutive_group(p,(0,1,2)) and p.index(0)<p.index(1)<p.index(2) for p in self.p6),24)
    def test_six_b_middle(self):
        self.assertEqual(sum(self.ab(p) and adjacent(p,1,2) for p in self.p6),48)
    def test_six_a_middle(self):
        self.assertEqual(sum(self.ab(p) and adjacent(p,0,2) for p in self.p6),48)
    def test_all_three_pairs_impossible(self):
        self.assertEqual(sum(self.ab(p) and adjacent(p,1,2) and adjacent(p,0,2) for p in self.p6),0)
    def test_two_blocks(self):self.assertEqual(sum(self.ab(p) and self.cd(p) for p in self.p6),96)
    def test_two_blocks_fixed_direction(self):
        self.assertEqual(sum(self.ab(p) and self.cd(p) and p.index(0)<p.index(1) and p.index(2)<p.index(3) for p in self.p6),24)
    def test_three_blocks(self):self.assertEqual(sum(self.ab(p) and self.cd(p) and self.ef(p) for p in self.p6),48)
    def test_union(self):self.assertEqual(sum(self.ab(p) or self.cd(p) for p in self.p6),384)
    def test_neither(self):self.assertEqual(sum(not self.ab(p) and not self.cd(p) for p in self.p6),336)
    def test_partition(self):self.assertEqual(384+336,720)
    def test_exactly_one(self):self.assertEqual(sum(self.ab(p)!=self.cd(p) for p in self.p6),288)
    def test_ab_only(self):self.assertEqual(sum(self.ab(p) and not self.cd(p) for p in self.p6),144)
    def test_cd_only(self):self.assertEqual(sum(self.cd(p) and not self.ab(p) for p in self.p6),144)
    def test_both_and_ef_order(self):
        self.assertEqual(sum(self.ab(p) and self.cd(p) and p.index(4)<p.index(5) for p in self.p6),48)
    def test_seven_total(self):self.assertEqual(len(self.p7),5040)
    def test_seven_one_event(self):self.assertEqual(sum(self.ab(p) for p in self.p7),1440)
    def test_seven_two_events(self):self.assertEqual(sum(self.ab(p) and self.cd(p) for p in self.p7),480)
    def test_seven_three_events(self):self.assertEqual(sum(self.ab(p) and self.cd(p) and self.ef(p) for p in self.p7),192)
    def test_seven_three_pairs_none(self):
        self.assertEqual(sum(not self.ab(p) and not self.cd(p) and not self.ef(p) for p in self.p7),1968)
    def test_seven_inclusion_exclusion(self):self.assertEqual(5040-3*1440+3*480-192,1968)
    def test_seven_parts(self):
        self.assertEqual(sum(self.ab(p) or self.cd(p) or self.ef(p) for p in self.p7),5040-1968)
    def test_math_typst_source_files(self):
        self.assertEqual(len(list((ROOT/'assets/comb12v2').glob('*.typ'))),len(FORMULAS))
    def test_voice_manifest(self):
        m=json.loads((ROOT/'voice/comb12_voice_manifest.json').read_text(encoding='utf8'))
        self.assertEqual(m['beats'],48)
        self.assertGreater(m['target_seconds'],1000)
    def test_script_syntax(self):
        import py_compile
        for filename in ('comb12_lesson_data.py','episodes/comb12_block_method.py',
                         'scripts/prepare_comb12_v2.py','scripts/qa_comb12_v2.py'):
            py_compile.compile(str(ROOT/filename),doraise=True)
    def test_scene_class(self):
        tree=ast.parse((ROOT/'episodes/comb12_block_method.py').read_text(encoding='utf8'))
        self.assertIn('COMB12',[x.name for x in tree.body if isinstance(x,ast.ClassDef)])
    def test_workflow(self):
        w=(ROOT.parent/'.github/workflows/render-comb12-v2.yml').read_text(encoding='utf8')
        for item in ('workflow_dispatch:', 'COMB12','comb12_block_method.py','qa_comb12_v2.py','quality:','voice:','upload-artifact'):
            self.assertIn(item,w)
    def test_preserve_episodes(self):
        for n in range(1,12):self.assertTrue(list((ROOT/'episodes').glob(f'comb{n:02}*.py')))
    def test_docs(self):
        for filename in ('HUONG_DAN_RENDER_COMB12_V2.md','storyboard_COMB12_v2.md','narration_COMB12_v2.md'):
            self.assertTrue((ROOT/filename).exists())

if __name__=='__main__':unittest.main()
