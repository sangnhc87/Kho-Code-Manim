"""Kiểm tra một kịch bản tập trước khi tạo âm thanh/video."""
from __future__ import annotations

from .board import Position

KINDS = {'intro', 'theory', 'puzzle', 'candidates', 'line', 'trap', 'mate', 'summary'}


def validate_episode(data, check_tablebase=False):
    for key in ('id', 'number', 'title', 'category', 'fen', 'verdict', 'beats', 'youtube'):
        if key not in data:
            raise ValueError(f'Thiếu trường {key}')
    state = Position.from_fen(data['fen'])
    for i, beat in enumerate(data['beats'], 1):
        where = f'phân đoạn {i} ({beat.get("kind")})'
        if beat.get('kind') not in KINDS:
            raise ValueError(f'{where}: loại không hợp lệ')
        for key in ('label', 'headline', 'steps'):
            if not beat.get(key):
                raise ValueError(f'{where}: thiếu {key}')
        if beat['kind'] == 'trap':
            pos = Position.from_fen(beat['fen'])
            if not beat.get('rewind') and pos.fen() != state.fen():
                raise ValueError(f'{where}: biến phụ không xuất phát từ thế hiện tại')
        elif beat.get('fen'):
            state = Position.from_fen(beat['fen'])
            pos = state
        else:
            pos = state
        for j, step in enumerate(beat['steps'], 1):
            if not step.get('say', '').strip():
                raise ValueError(f'{where}, câu {j}: thiếu lời đọc')
            if step.get('move'):
                pos = pos.play(step['move'])  # báo lỗi nếu nước sai luật
        if beat['kind'] == 'trap':
            if Position.from_fen(beat['return_fen']).fen() != state.fen():
                raise ValueError(f'{where}: không quay về đúng thế biến chính')
        else:
            state = pos
    if check_tablebase and data.get('kind') != 'game':
        from . import cdb
        wdl, dtm = cdb.value(data['fen'])
        if (wdl, dtm) != (data['verdict']['wdl'], data['verdict']['dtm']):
            raise ValueError(f'Kết luận {data["verdict"]} lệch bảng tra ({wdl}, {dtm})')
    if data.get('kind') != 'game' and data['verdict']['wdl'] == 'W' and not state.is_mate():
        raise ValueError('Biến chính của thế thắng phải kết thúc bằng thế bí')
    return True
