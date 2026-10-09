"""Exercise Manim's actual removal/restructuring across every episode branch."""
import unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
try:
    from manim import Circle, Scene, tempconfig
    from manimpango import list_fonts
    import src.scene as display
    HAS_MANIM = True
except ImportError:
    HAS_MANIM = False

from src.core import Board, read_episode
from src.engine_coords import board_fen, flip_move

ROOT = Path(__file__).resolve().parents[1]


class DisplayTests(unittest.TestCase):
    def test_engine_coordinate_conversion(self):
        self.assertEqual(flip_move('d2f1'), 'd7f8')
        self.assertEqual(flip_move('e7d7'), 'e2d2')
        for move in ('d2f1', 'a0i9', 'f0e1'):
            self.assertEqual(flip_move(flip_move(move)), move)
        with self.assertRaises(ValueError):
            flip_move('j0a1')
        fen = '3k1a3/9/3N5/9/9/9/9/4K4/9/9 w'
        self.assertEqual(board_fen(Board.fen(fen)), fen+' - - 0 1')

    @unittest.skipUnless(HAS_MANIM, "manim is required for visual scene tests")
    def test_no_ghost_or_missing_pieces_after_moves_captures_and_resets(self):
        episode = read_episode(ROOT/'episodes'/'tap-0001.json')
        fonts = list_fonts()
        font = 'Noto Sans' if 'Noto Sans' in fonts else 'Arial'
        cjk = 'Noto Sans CJK SC' if 'Noto Sans CJK SC' in fonts else 'PingFang SC'
        with patch.object(display, 'FONT', font), patch.object(display, 'CJK', cjk), tempconfig({
            'dry_run': True, 'frame_rate': 1, 'pixel_width': 160,
            'pixel_height': 90, 'verbosity': 'ERROR', 'progress_bar': 'none',
        }):
            scene = Scene()
            scene.renderer.skip_animations = True
            board = display.XiangqiDisplay(Board.fen(episode['fen']))
            artwork = board.submobjects[0]
            scene.add(board)
            self.assertGreater(board.get_bottom()[1], -3.45)
            self.assertLess(board.get_top()[1], 3.09)
            self.assertLess(board.get_right()[0], 0)
            def assert_visible():
                family = scene.get_mobject_family_members()
                bodies = [m for m in family if isinstance(m, Circle)
                          and abs(m.width-.47) < .001 and m.get_fill_opacity() > .9]
                self.assertIn(artwork, family)
                self.assertEqual(len(bodies), len(board.state.cells))
                self.assertEqual(set(board.pieces), set(board.state.cells))
                for square, mob in board.pieces.items():
                    self.assertIn(mob, family)
                    np.testing.assert_allclose(mob.get_center(), board.xy(square), atol=1e-6)
            assert_visible()
            for index, beat in enumerate(episode['beats'], 1):
                with self.subTest(beat=index):
                    board.reset_position(beat['fen'], scene)
                    assert_visible()
                    for move in beat.get('moves', []):
                        board.move_piece(move, scene)
                        assert_visible()


if __name__ == '__main__':
    unittest.main()
