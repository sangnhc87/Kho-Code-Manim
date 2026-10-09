"""Stable landscape frame geometry, independent of Manim for CI validation."""
FRAME_HALF_WIDTH = 64.0 / 9.0  # Manim default 16:9 frame about 14.222 x 8
FRAME_HALF_HEIGHT = 4.0
BOARD_GRID_STEP = 0.61
BOARD_CENTER_X = -3.27
BOARD_CENTER_Y = -0.10
BOARD_ART_BORDER_X = 0.57 / 2
BOARD_ART_BORDER_Y = 0.52 / 2
HEADER_LINE_Y = 3.24
FOOTER_TOP_Y = -3.60
RIGHT_PANEL_LEFT_X = 3.21 - 6.02/2

def board_bbox():
    return (
        BOARD_CENTER_X - 4*BOARD_GRID_STEP - BOARD_ART_BORDER_X,
        BOARD_CENTER_Y - 4.5*BOARD_GRID_STEP - BOARD_ART_BORDER_Y,
        BOARD_CENTER_X + 4*BOARD_GRID_STEP + BOARD_ART_BORDER_X,
        BOARD_CENTER_Y + 4.5*BOARD_GRID_STEP + BOARD_ART_BORDER_Y,
    )

def assert_safe_layout():
    left,bottom,right,top=board_bbox()
    assert left>=-FRAME_HALF_WIDTH+0.35, 'Left side of board clipped'
    assert top < HEADER_LINE_Y-0.15, 'Upper ranks clipped by header'
    assert bottom > FOOTER_TOP_Y+0.15, 'Bottom ranks clipped by footer'
    assert right < RIGHT_PANEL_LEFT_X-0.20, 'Board overlaps text panel'
    assert top<FRAME_HALF_HEIGHT-0.30 and bottom>-FRAME_HALF_HEIGHT+0.30
    return True
