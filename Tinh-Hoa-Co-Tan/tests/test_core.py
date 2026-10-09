import unittest
import hashlib
import json
from pathlib import Path
from src.core import Board, read_episode
from src.layout import assert_safe_layout, board_bbox
from scripts.solve_masi import solve, fen_of, legal_moves

ROOT=Path(__file__).resolve().parents[1]

class CoreTests(unittest.TestCase):
    def test_pikafish_evidence_matches_episode(self):
        path=ROOT/'episodes'/'tap-0036.json'
        report=json.loads((ROOT/'verification'/'tap-0036-pikafish.json').read_text())
        self.assertEqual(report['episode_sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
        ep=read_episode(path)
        expected=[(i,j,m) for i,beat in enumerate(ep['beats'],1)
                  for j,m in enumerate(beat.get('moves',[]),1)]
        actual=[(c['beat'],c['move_index'],c['display_move']) for c in report['checks']]
        self.assertEqual(actual,expected)
        self.assertEqual(report['verified_moves'],len(expected))
        for check in report['checks']:
            self.assertIn(check['uci_move'],check['legal_uci_moves'])

    def test_001_all_variations_legally_play(self):
        ep=read_episode(ROOT/'episodes'/'tap-0001.json')
        self.assertEqual(ep['category'],'Tàn Binh')
        self.assertEqual(ep['analysis_status'],'three_piece_pawn_retrograde')
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b=Board.fen(beat['fen'])
            for uci in beat.get('moves',[]):
                b.play(uci[:2],uci[2:])

    def test_002_all_variations_legally_play(self):
        ep=read_episode(ROOT/'episodes'/'tap-0002.json')
        self.assertEqual(ep['category'],'Tàn Binh')
        self.assertEqual(ep['analysis_status'],'four_piece_pawn_advisor_retrograde')
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b=Board.fen(beat['fen'])
            for uci in beat.get('moves',[]):
                b.play(uci[:2],uci[2:])

    def test_003_all_variations_legally_play(self):
        ep=read_episode(ROOT/'episodes'/'tap-0003.json')
        self.assertEqual(ep['category'],'Tàn Binh')
        self.assertEqual(ep['analysis_status'],'four_piece_pawn_elephant_retrograde')
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b=Board.fen(beat['fen'])
            for uci in beat.get('moves',[]):
                b.play(uci[:2],uci[2:])

    def test_004_all_variations_legally_play(self):
        ep=read_episode(ROOT/'episodes'/'tap-0004.json')
        self.assertEqual(ep['category'],'Tàn Binh')
        self.assertEqual(ep['analysis_status'],'four_piece_pawn_advisor_retrograde')
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b=Board.fen(beat['fen'])
            for uci in beat.get('moves',[]):
                b.play(uci[:2],uci[2:])

    def test_036_all_variations_legally_play(self):
        ep=read_episode(ROOT/'episodes'/'tap-0036.json')
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

    def test_retrograde_036_choices(self):
        ep=read_episode(ROOT/'episodes'/'tap-0036.json')
        ss,index,res,depth=solve()
        root=next(s for s in ss if fen_of(*s)==ep['fen'])
        self.assertEqual((res[index[root]],depth[index[root]]),(1,13))
        options={mv:next for mv,next in legal_moves(root)}
        self.assertEqual((res[index[options['d2f1']]],depth[index[options['d2f1']]]),(-1,12))
        self.assertEqual((res[index[options['d2c4']]],depth[index[options['d2c4']]]),(-1,12))
        self.assertEqual((res[index[options['d2e0']]],depth[index[options['d2e0']]]),(-1,20))
        self.assertEqual(res[index[options['e7d7']]],0)

    def test_final_capture_in_each_pv(self):
        ep=read_episode(ROOT/'episodes'/'tap-0036.json')
        for idx in (4,5,6,7,8,10,14):
            beat=ep['beats'][idx]
            b=Board.fen(beat['fen'])
            last_capture=None
            for move in beat['moves']:
                last_capture=b.play(move[:2],move[2:])
            self.assertEqual(last_capture,'a',f'Beat {idx+1} did not capture black advisor')

    def test_037_all_variations_legally_play(self):
        ep=read_episode(ROOT/'episodes'/'tap-0037.json')
        self.assertEqual(len(ep['beats']),12)
        self.assertEqual(ep['analysis_status'],'four_piece_elephant_retrograde')
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        moves=0
        for beat in ep['beats']:
            b=Board.fen(beat['fen'])
            for uci in beat.get('moves',[]):
                b.play(uci[:2],uci[2:])
                moves+=1
        self.assertGreaterEqual(moves,25)

if __name__=='__main__':unittest.main()
