"""COMB22: independent brute-force verification, no Manim dependency."""
import unittest
from itertools import product,permutations
from pathlib import Path
from math import comb
from comb22_lesson_data import (
    BEATS,FORMULAS,CHAPTERS,validate,grid_table,paths_bruteforce,tilings,
    tilings_direct,no11_states,no11_bruteforce,automaton_next,pattern_dp,
    pattern_bruteforce,pattern_rows,bitmask_derangements,bitmask_layers,
    matrix_power,circular_no11,circular_no11_direct)

class TestCOMB22(unittest.TestCase):
    def test_lesson_valid(self):self.assertTrue(validate())
    def test_chapters_beats_formulas(self):self.assertEqual((len(CHAPTERS),len(BEATS),len(FORMULAS)),(8,48,48))
    def test_unique_narration(self):self.assertEqual(len(set(b.narration for b in BEATS)),48)
    def test_words(self):self.assertGreaterEqual(sum(len(b.narration.split()) for b in BEATS),3500)
    def test_duration(self):self.assertGreaterEqual(sum(b.min_seconds for b in BEATS),1250)
    def test_notation(self):self.assertIn('C_3^7',FORMULAS['grid_0'])
    def test_grid_general(self):
        for a in range(6):
            for b in range(5):self.assertEqual(grid_table(a,b)[a][b],comb(a+b,a))
    def test_grid_against_brute(self):
        for a in range(5):
            for b in range(5):self.assertEqual(grid_table(a,b)[a][b],paths_bruteforce(a,b))
    def test_blocked_grid(self):
        for block in ((2,1),(1,2),(3,1)):
            table=grid_table(4,3,{block})
            self.assertEqual(table[4][3],paths_bruteforce(4,3,{block}))
    def test_grid_final(self):self.assertEqual(grid_table(4,3,{(2,1)})[4][3],17)
    def test_tilings(self):
        for n in range(11):self.assertEqual(tilings(n),len(tilings_direct(n)))
    def test_tilings_final(self):self.assertEqual(tilings(6),13)
    def test_no11(self):
        for n in range(12):self.assertEqual(sum(no11_states(n)),no11_bruteforce(n))
    def test_no11_final(self):self.assertEqual(sum(no11_states(6)),21)
    def test_automaton_forbidden_transition(self):self.assertIsNone(automaton_next(2,1))
    def test_automaton_other_transitions(self):
        self.assertEqual([automaton_next(s,b) for s in range(3) for b in (0,1)],[0,1,2,1,0,None])
    def test_automaton_rows(self):self.assertEqual(sum(pattern_rows(6)[-1]),37)
    def test_avoid101_independent(self):
        for n in range(1,12):self.assertEqual(pattern_dp(n),pattern_bruteforce(n))
    def test_avoid_patterns_other(self):
        for pattern in ('00','11','010','001'):
            for n in range(1,9):self.assertEqual(pattern_dp(n,pattern),pattern_bruteforce(n,pattern))
    def test_exact_ones(self):
        for n in range(1,11):
            for k in range(n+1):self.assertEqual(pattern_dp(n,ones=k),pattern_bruteforce(n,ones=k))
    def test_ending_zero(self):
        for n in range(1,11):self.assertEqual(pattern_dp(n,last=0),pattern_bruteforce(n,last=0))
    def test_bitmask_against_brute(self):
        for n in range(1,6):
            brute=sum(all(i!=perm[i] for i in range(n)) for perm in permutations(range(n)))
            self.assertEqual(bitmask_derangements(n),brute)
    def test_bitmask_layers(self):self.assertEqual(bitmask_layers(4),[1,3,7,11,9])
    def test_bitmask_final(self):self.assertEqual(bitmask_derangements(4),9)
    def test_matrix_power_identity(self):self.assertEqual(matrix_power(0),[[1,0],[0,1]])
    def test_circular_independent(self):
        for n in range(1,11):self.assertEqual(circular_no11(n),circular_no11_direct(n))
    def test_circular_final(self):self.assertEqual(circular_no11(8),47)
    def test_circular_reflection_not_quotiented(self):
        self.assertEqual(circular_no11(8),47)
    def test_olympiad_final(self):self.assertEqual(pattern_dp(10,ones=4,last=0),48)
    def test_olympiad_independent(self):
        self.assertEqual(pattern_dp(10,ones=4,last=0),pattern_bruteforce(10,ones=4,last=0))
    def test_invalid_arguments(self):
        for fn,args in ((grid_table,(-1,2)),(tilings,(-1,)),(no11_states,(-1,)),
                         (pattern_dp,(-1,)),(bitmask_derangements,(-1,)),
                         (matrix_power,(-1,)),(circular_no11,(0,))):
            with self.subTest(fn=fn.__name__):
                with self.assertRaises(ValueError):fn(*args)
    def test_workflow(self):
        text=Path('.github/workflows/render-comb22-v2.yml').read_text(encoding='utf8')
        for s in ('prepare_comb22_v2.py','comb22_dynamic_programming.py COMB22',
                  'qa_comb22_v2.py','upload-artifact','voice','fullhd'):
            self.assertIn(s,text)
    def test_previous_episodes(self):
        for n in range(1,22):
            self.assertTrue(any(f.name.startswith(f'comb{n:02}_') for f in Path('episodes').glob('*.py')),n)

if __name__=='__main__':unittest.main()