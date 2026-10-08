"""Independent mathematical and production tests for COMB01 v2."""
import ast
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from comb01_lesson_data import BEATS, CHAPTER_LABELS, FORMULAS, spoken_text


class TestCOMB01V2(unittest.TestCase):
    def test_route_disjoint_and_total(self):
        bus={('bus',1),('bus',2)}
        train={('train',1),('train',2),('train',3)}
        self.assertFalse(bus&train)
        self.assertEqual(len(bus|train),5)

    def test_books(self):
        math_books={f'T{i}' for i in range(1,5)}
        science_books={f'L{i}' for i in range(1,4)}
        self.assertEqual(len(math_books|science_books),7)
        self.assertFalse(math_books&science_books)

    def test_overlap_1_12(self):
        evens={i for i in range(1,13) if i%2==0}
        threes={i for i in range(1,13) if i%3==0}
        self.assertEqual(len(evens),6)
        self.assertEqual(len(threes),4)
        self.assertEqual(evens&threes,{6,12})
        self.assertEqual(len(evens|threes),8)

    def test_disjoint_1_20(self):
        odds={i for i in range(1,21) if i%2}
        fours={i for i in range(1,21) if i%4==0}
        self.assertEqual((len(odds),len(fours)),(10,5))
        self.assertFalse(odds&fours)
        self.assertEqual(len(odds|fours),15)

    def test_or_vs_and(self):
        clothes={'A1','A2','A3'}
        hats={'M1','M2'}
        self.assertEqual(len(clothes|hats),5)
        self.assertEqual(len({(a,b) for a in clothes for b in hats}),6)

    def test_quiz(self):
        a={f'A{i}' for i in range(5)}
        b={f'B{i}' for i in range(2)}
        self.assertEqual(len(a|b),7)
        A={i for i in range(1,16) if i%3==0}
        B={i for i in range(1,16) if i%5==0}
        self.assertEqual((len(A),len(B),A&B,len(A|B)),(5,3,{15},7))

    def test_source_parse(self):
        for relative in ['episodes/comb01_rule_of_sum.py','scripts/prepare_comb01_v2.py',
                         'scripts/qa_comb01_v2.py','comb01_lesson_data.py']:
            with self.subTest(path=relative):
                ast.parse((ROOT/relative).read_text(encoding='utf-8'))

    def test_chapters_and_order(self):
        self.assertEqual(len(BEATS),42)
        sections=list(dict.fromkeys(b.section for b in BEATS))
        self.assertEqual(sections,list(CHAPTER_LABELS))
        for section in sections:
            steps=[b.step for b in BEATS if b.section==section]
            self.assertEqual(steps,list(range(len(steps))))

    def test_forms_available(self):
        self.assertTrue(all(not b.formula or b.formula in FORMULAS for b in BEATS))
        self.assertEqual(len(FORMULAS),10)

    def test_substantial_synchronized_narration(self):
        words=sum(len(spoken_text(b).split()) for b in BEATS)
        self.assertGreaterEqual(words,2000)
        self.assertLessEqual(words,2450)
        self.assertTrue(all(len(spoken_text(b).split())>=30 for b in BEATS))

    def test_target_duration(self):
        silent=sum(b.min_seconds for b in BEATS)+5
        self.assertGreaterEqual(silent,660)
        self.assertLessEqual(silent,840)

    def test_panel_text_fits_expected_count(self):
        self.assertTrue(all(len(b.lines)==3 for b in BEATS))
        self.assertTrue(all(len(b.heading)<54 for b in BEATS))
        self.assertTrue(all(len(b.takeaway)<85 for b in BEATS))


if __name__=='__main__':unittest.main()
