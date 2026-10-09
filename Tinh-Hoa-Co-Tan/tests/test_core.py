import unittest
from pathlib import Path
from src.core import Board, read_episode

ROOT=Path(__file__).resolve().parents[1]

class CoreTests(unittest.TestCase):
    def test_pilot_full_moves(self):
        ep=read_episode(ROOT/'episodes'/'tap-0001.json')
        self.assertEqual(len(ep['beats']),10)
        self.assertEqual(ep['analysis_status'],'illustrative_not_engine_verified')

    def test_horse_leg_blocked(self):
        board=Board.fen('4k4/3a5/9/9/5PN2/9/9/9/9/3K5 w')
        with self.assertRaisesRegex(ValueError,'Illegal move'):
            board.play('g4','e3')

    def test_generals_facing_rejected(self):
        with self.assertRaisesRegex(ValueError,'facing generals'):
            Board.fen('4k4/9/9/9/9/9/9/9/9/4K4 w')

    def test_pilot_is_legal_and_has_kings(self):
        ep=read_episode(ROOT/'episodes'/'tap-0001.json')
        board=Board.fen(ep['fen'])
        count=0
        for beat in ep['beats']:
            for move in beat.get('moves',[]):
                board.play(move[:2],move[2:]); count+=1
        self.assertEqual(count,12)
        self.assertEqual(sum(1 for p in board.cells.values() if p.upper()=='K'),2)

if __name__=='__main__': unittest.main()
