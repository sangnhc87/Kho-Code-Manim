import unittest
import hashlib
import json
from pathlib import Path
from src.core import Board, read_episode
from src.layout import assert_safe_layout, board_bbox

ROOT = Path(__file__).resolve().parents[1]

class CoreTests(unittest.TestCase):
    def test_all_existing_episodes_legally_play(self):
        episodes = sorted((ROOT/'episodes').glob('tap-*.json'))
        self.assertGreater(len(episodes), 0, "No episode files found")
        for path in episodes:
            with self.subTest(episode=path.name):
                ep = read_episode(path)
                self.assertTrue(all('fen' in beat for beat in ep['beats']))
                for beat in ep['beats']:
                    b = Board.fen(beat['fen'])
                    for uci in beat.get('moves', []):
                        b.play(uci[:2], uci[2:])

    def test_pikafish_evidence_matches_episode(self):
        path = ROOT/'episodes'/'tap-0036.json'
        ver = ROOT/'verification'/'tap-0036-pikafish.json'
        if not path.exists() or not ver.exists():
            self.skipTest('tap-0036 fixture not present')
        report = json.loads(ver.read_text())
        self.assertEqual(report['episode_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        ep = read_episode(path)
        expected = [(i,j,m) for i,beat in enumerate(ep['beats'],1)
                    for j,m in enumerate(beat.get('moves',[]),1)]
        actual = [(c['beat'],c['move_index'],c['display_move']) for c in report['checks']]
        self.assertEqual(actual, expected)
        self.assertEqual(report['verified_moves'], len(expected))
        for check in report['checks']:
            self.assertIn(check['uci_move'], check['legal_uci_moves'])

    def test_001_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0001.json'
        if not path.exists():
            self.skipTest('tap-0001.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_002_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0002.json'
        if not path.exists():
            self.skipTest('tap-0002.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_003_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0003.json'
        if not path.exists():
            self.skipTest('tap-0003.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_004_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0004.json'
        if not path.exists():
            self.skipTest('tap-0004.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_005_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0005.json'
        if not path.exists():
            self.skipTest('tap-0005.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_006_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0006.json'
        if not path.exists():
            self.skipTest('tap-0006.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_007_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0007.json'
        if not path.exists():
            self.skipTest('tap-0007.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_036_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0036.json'
        if not path.exists():
            self.skipTest('tap-036.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

    def test_layout_board_fits_9_by_10(self):
        self.assertTrue(assert_safe_layout())
        left, bottom, right, top = board_bbox()
        self.assertLess(top, 3.24)
        self.assertGreater(bottom, -3.60)
        self.assertGreater(right, left)

    def test_horse_leg_blocked(self):
        b = Board.fen('4k4/3a5/9/9/5PN2/9/9/9/9/3K5 w')
        with self.assertRaisesRegex(ValueError, 'Illegal move'):
            b.play('g4', 'e3')

    def test_generals_facing_rejected(self):
        with self.assertRaisesRegex(ValueError, 'facing generals'):
            Board.fen('4k4/9/9/9/9/9/9/9/9/4K4 w')

    def test_retrograde_036_choices(self):
        path = ROOT/'episodes'/'tap-0036.json'
        if not path.exists():
            self.skipTest('tap-0036.json not found')
        from scripts.solve_masi import solve, fen_of, legal_moves
        ep = read_episode(path)
        ss, index, res, depth = solve()
        root = next(s for s in ss if fen_of(*s) == ep['fen'])
        self.assertEqual((res[index[root]], depth[index[root]]), (1, 13))
        options = {mv: next for mv, next in legal_moves(root)}
        self.assertEqual((res[index[options['d2f1']]], depth[index[options['d2f1']]]), (-1, 12))
        self.assertEqual((res[index[options['d2c4']]], depth[index[options['d2c4']]]), (-1, 12))
        self.assertEqual((res[index[options['d2e0']]], depth[index[options['d2e0']]]), (-1, 20))
        self.assertEqual(res[index[options['e7d7']]], 0)

    def test_final_capture_in_each_pv(self):
        path = ROOT/'episodes'/'tap-0036.json'
        if not path.exists():
            self.skipTest('tap-0036.json not found')
        ep = read_episode(path)
        for idx in (4, 5, 6, 7, 8, 10, 14):
            beat = ep['beats'][idx]
            b = Board.fen(beat['fen'])
            last_capture = None
            for move in beat['moves']:
                last_capture = b.play(move[:2], move[2:])
            self.assertEqual(last_capture, 'a', f'Beat {idx+1} did not capture black advisor')

    def test_037_all_variations_legally_play(self):
        path = ROOT/'episodes'/'tap-0037.json'
        if not path.exists():
            self.skipTest('tap-0037.json not found')
        ep = read_episode(path)
        self.assertTrue(all('fen' in beat for beat in ep['beats']))
        for beat in ep['beats']:
            b = Board.fen(beat['fen'])
            for uci in beat.get('moves', []):
                b.play(uci[:2], uci[2:])

if __name__ == '__main__':
    unittest.main()
