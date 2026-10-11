"""Kiểm tra luật cờ, ký pháp và kịch bản. Chạy offline: CDB_OFFLINE=1."""
import json
import os
import unittest
from pathlib import Path

os.environ.setdefault('CDB_OFFLINE', '1')
ROOT = Path(__file__).resolve().parents[1]

from xq import cdb  # noqa: E402
from xq.board import Position  # noqa: E402
from xq.notation import short_move, vn_move  # noqa: E402
from xq.validate import validate_episode  # noqa: E402
from src.layout import assert_safe_layout  # noqa: E402


class RulesAgainstTablebase(unittest.TestCase):
    def test_legal_moves_match_every_cached_chessdb_position(self):
        checked = 0
        for path in sorted((ROOT / 'data' / 'cdb').glob('*.json')):
            for fen, raw in json.loads(path.read_text(encoding='utf-8')).items():
                res = cdb.parse(raw)
                pos = Position.from_fen(fen)
                if res['status'] == 'mate':
                    self.assertEqual(pos.legal_moves(), [], fen)
                elif res['status'] == 'egtb':
                    self.assertEqual(sorted(m['move'] for m in res['moves']), pos.legal_moves(), fen)
                    checked += 1
        self.assertGreater(checked, 100)

    def test_fen_roundtrip_and_flying_general(self):
        fen = '3k5/9/9/9/9/9/9/9/9/4K4 w'
        self.assertEqual(Position.from_fen(fen).fen(), fen)
        pos = Position.from_fen('4k4/9/9/9/9/9/9/9/9/3K5 w')
        self.assertNotIn('d0e0', pos.legal_moves())  # không được lộ mặt tướng


class Notation(unittest.TestCase):
    def test_vietnamese_notation(self):
        pos = Position.from_fen('3k1a3/9/3N5/9/9/9/9/4K4/9/9 w')
        self.assertEqual(vn_move(pos, 'd7f8'), 'Mã 6 tiến 4')
        self.assertEqual(vn_move(pos, 'e2f2'), 'Tướng 5 bình 4')
        self.assertEqual(vn_move(pos, 'e2e1'), 'Tướng 5 thoái 1')
        self.assertEqual(short_move(pos, 'd7f8'), 'M6.4')
        black = Position.from_fen('3k1a3/9/3N5/9/9/9/9/4K4/9/9 b')
        self.assertEqual(vn_move(black, 'f9e8'), 'Sĩ 6 tiến 5')
        self.assertEqual(vn_move(black, 'd9d8'), 'Tướng 4 tiến 1')

    def test_front_back_rooks(self):
        pos = Position.from_fen('4k4/9/9/9/2R6/9/9/2R6/9/3K5 w')
        self.assertEqual(vn_move(pos, 'c5d5'), 'Xe trước bình 6')
        self.assertEqual(vn_move(pos, 'c2c1'), 'Xe sau thoái 1')


class Episodes(unittest.TestCase):
    def test_all_episodes_valid_and_match_tablebase(self):
        assert_safe_layout()
        for path in sorted((ROOT / 'episodes').glob('ep-*.json')):
            with self.subTest(path.name):
                data = json.loads(path.read_text(encoding='utf-8'))
                validate_episode(data, check_tablebase=True)
                self.assertEqual(data['id'], path.stem)


if __name__ == '__main__':
    unittest.main()
