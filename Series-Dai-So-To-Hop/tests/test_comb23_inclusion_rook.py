"""COMB23: independent checks of advanced inclusion-exclusion and rook models."""
import unittest
from itertools import permutations,combinations
from math import comb, factorial
from pathlib import Path
from comb23_lesson_data import (
 BEATS,FORMULAS,CHAPTERS,validate,three_sets,
 rook_numbers,rook_numbers_dp,rook_recurrence,derangements,count_exact_fixed,
 forbidden_diagonal,forbidden_asymmetric,forbidden_cycle,
 count_avoiding,brute_avoiding,two_fixed_ban_six)

class TestCOMB23(unittest.TestCase):
    def test_lesson_valid(self):self.assertTrue(validate())
    def test_8_chapters_48_beats(self):self.assertEqual((len(CHAPTERS),len(BEATS),len(FORMULAS)),(8,48,48))
    def test_unique_voice(self):self.assertEqual(len({b.narration for b in BEATS}),48)
    def test_long_lesson(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),1300)
    def test_narration_depth(self):self.assertGreaterEqual(sum(len(b.narration.split()) for b in BEATS),3500)
    def test_vietnamese_notation(self):self.assertIn('C_k^m',FORMULAS['fixed_ban_4'])
    def test_three_sets(self):
        a,b,c=three_sets()
        self.assertEqual((len(a),len(b),len(c)),(15,10,6))
        self.assertEqual((len(a&b),len(a&c),len(b&c),len(a&b&c)),(5,3,2,1))
        self.assertEqual(len(a|b|c),22)
        self.assertEqual(len(a)+len(b)+len(c)-len(a&b)-len(a&c)-len(b&c)+len(a&b&c),22)
    def test_derangements_sequence(self):
        self.assertEqual([derangements(n) for n in range(7)],[1,0,1,2,9,44,265])
    def test_derangements_independent(self):
        for n in range(1,8):
            self.assertEqual(derangements(n),sum(all(i!=p[i] for i in range(n)) for p in permutations(range(n))))
    def test_derangements_recurrence(self):
        for n in range(2,12):self.assertEqual(derangements(n),(n-1)*(derangements(n-1)+derangements(n-2)))
    def test_three_restricted_fixed(self):
        self.assertEqual(two_fixed_ban_six(),426)
        forbidden={(i,i) for i in range(3)}
        self.assertEqual(brute_avoiding(6,forbidden),426)
    def test_diagonal_4_rooks(self):self.assertEqual(rook_numbers(4,forbidden_diagonal(4)),[1,4,6,4,1])
    def test_asymmetric_4_rooks(self):self.assertEqual(rook_numbers(4,forbidden_asymmetric()),[1,5,8,5,1])
    def test_cycle_5_rooks(self):self.assertEqual(rook_numbers(5,forbidden_cycle(5)),[1,10,35,50,25,2])
    def test_diagonal_assignment(self):self.assertEqual(count_avoiding(4,forbidden_diagonal(4)),9)
    def test_asymmetric_assignment(self):self.assertEqual(count_avoiding(4,forbidden_asymmetric()),6)
    def test_cycle_assignment(self):self.assertEqual(count_avoiding(5,forbidden_cycle(5)),13)
    def test_others_legal_permutations(self):
        for n,board in [(4,forbidden_diagonal(4)),(4,forbidden_asymmetric()),(5,forbidden_cycle(5))]:
            self.assertEqual(count_avoiding(n,board),brute_avoiding(n,board))
    def test_rook_row_dp(self):
        for n,board in [(4,forbidden_asymmetric()),(5,forbidden_cycle(5)),(6,forbidden_cycle(6))]:
            self.assertEqual(rook_numbers(n,board),rook_numbers_dp(n,board))
    def test_diagonal_rook_coeff(self):
        for n in range(1,8):self.assertEqual(rook_numbers(n,forbidden_diagonal(n)),[comb(n,k) for k in range(n+1)])
    def test_cycle_small_crosscheck(self):
        for n in range(2,7):self.assertEqual(count_avoiding(n,forbidden_cycle(n)),brute_avoiding(n,forbidden_cycle(n)))
    def test_recurrence_diagonal_and_asymmetric(self):
        for n,board in [(4,forbidden_asymmetric()),(4,forbidden_diagonal(4)),(5,forbidden_cycle(5))]:
            for cell in list(board)[:4]:
                self.assertEqual(rook_recurrence(n,board,cell),rook_numbers(n,board))
    def test_exactly_fixed_sum(self):
        for n in range(0,8):self.assertEqual(sum(count_exact_fixed(n,k) for k in range(n+1)),factorial(n))
    def test_exactly_fixed_two(self):self.assertEqual(count_exact_fixed(5,2),20)
    def test_exactly_fixed_one(self):self.assertEqual(count_exact_fixed(5,1),45)
    def test_exactly_fixed_three(self):self.assertEqual(count_exact_fixed(5,3),10)
    def test_exactly_fixed_four_impossible(self):self.assertEqual(count_exact_fixed(5,4),0)
    def test_fixed_distribution_5(self):self.assertEqual([count_exact_fixed(5,k) for k in range(6)],[44,45,20,10,0,1])
    def test_exactly_fixed_independent(self):
        for n in range(1,7):
            count=[0]*(n+1)
            for p in permutations(range(n)):count[sum(i==p[i] for i in range(n))]+=1
            self.assertEqual(count,[count_exact_fixed(n,k) for k in range(n+1)])
    def test_empty_board(self):
        for n in range(6):self.assertEqual(count_avoiding(n,set()),factorial(n))
    def test_row_full_forbidden(self):
        for n in range(1,6):
            board={(0,j) for j in range(n)}
            self.assertEqual(count_avoiding(n,board),0)
    def test_full_board(self):
        for n in range(1,5):self.assertEqual(count_avoiding(n,{(i,j) for i in range(n) for j in range(n)}),0)
    def test_outside_board(self):
        with self.assertRaises(ValueError):rook_numbers(3,{(3,1)})
    def test_invalid_derangement_n(self):
        with self.assertRaises(ValueError):derangements(-1)
    def test_invalid_cycle_n(self):
        with self.assertRaises(ValueError):forbidden_cycle(1)
    def test_bad_recurrence_cell(self):
        with self.assertRaises(ValueError):rook_recurrence(4,forbidden_asymmetric(),(1,0))
    def test_workflow(self):
        yml=Path('.github/workflows/render-comb23-v2.yml').read_text(encoding='utf8')
        for needle in ['prepare_comb23_v2.py','comb23_inclusion_rook.py COMB23','qa_comb23_v2.py','upload-artifact','voice','fullhd']:
            self.assertIn(needle,yml)
    def test_past_episodes_kept(self):
        for n in range(1,23):self.assertTrue(any(p.name.startswith(f'comb{n:02}_') for p in Path('episodes').glob('*.py')),n)

if __name__=='__main__':unittest.main()
