import unittest
from pathlib import Path
from src.core import Board, read_episode
from src.layout import assert_safe_layout, board_bbox
from scripts.solve_masi import solve, fen_of, legal_moves

ROOT=Path(__file__).resolve().parents[1]

class CoreTests(unittest.TestCase):
    def test_001_all_variations_legally_play(self):
        ep=read_episode(ROOT/'episodes'/'tap-0001.json')
        self.assertEqual(len(ep['beats']),18)
        self.assertEqual(ep['analysis_status'],'four_piece_retrograde_ordinary_moves')
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        moves=0
        for beat in ep['beats']:
            b=Board.fen(beat['fen'])
            for uci in beat.get('moves',[]):
                b.play(uci[:2],uci[2:])
                moves+=1
        self.assertGreaterEqual(moves,60)

    def test_layout_board_fits_9_by_10(self):
        self.assertTrue(assert_safe_layout())
        left,bottom,right,top=board_bbox()
        self.assertLess(top,3.24)
        self.assertGreater(bottom,-3.60)
        self.assertGreater(right,left)

    def test_horse_leg_blocked(self):
        b=Board.fen('4k4/3a5/9/9/5PN2/9/9/9/9/3K5 w')
        with self.assertRaisesRegex(ValueError,'Illegal move'):
            b.play('g4','e3')

    def test_generals_facing_rejected(self):
        with self.assertRaisesRegex(ValueError,'facing generals'):
            Board.fen('4k4/9/9/9/9/9/9/9/9/4K4 w')

    def test_retrograde_001_choices(self):
        ep=read_episode(ROOT/'episodes'/'tap-0001.json')
        ss,index,res,depth=solve()
        root=next(s for s in ss if fen_of(*s)==ep['fen'])
        self.assertEqual((res[index[root]],depth[index[root]]),(1,13))
        options={mv:next for mv,next in legal_moves(root)}
        self.assertEqual((res[index[options['d2f1']]],depth[index[options['d2f1']]]),(-1,12))
        self.assertEqual((res[index[options['d2c4']]],depth[index[options['d2c4']]]),(-1,12))
        self.assertEqual((res[index[options['d2e0']]],depth[index[options['d2e0']]]),(-1,20))
        self.assertEqual(res[index[options['e7d7']]],0)

    def test_final_capture_in_each_pv(self):
        ep=read_episode(ROOT/'episodes'/'tap-0001.json')
        for idx in (4,5,6,7,8,10,14):
            beat=ep['beats'][idx]
            b=Board.fen(beat['fen'])
            last_capture=None
            for move in beat['moves']:
                last_capture=b.play(move[:2],move[2:])
            self.assertEqual(last_capture,'a',f'Beat {idx+1} did not capture black advisor')

if __name__=='__main__':unittest.main()
