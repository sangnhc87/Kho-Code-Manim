"""Reusable probability props for the vertical Shorts: coin, die, playing card,
urn of balls, top-down probability tree and sample-space grid.

All functions return plain mobjects (no scene needed); text inside props uses
Text only for physical labels (pips, card ranks), never for mathematics.
"""
from __future__ import annotations

import random

import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, Circle, Dot, Line, RoundedRectangle, Square, Text, VGroup,
                   VMobject)

from common.theme import CORAL, CYAN, FONT, GOLD, GREEN, INK, PURPLE, SOFT, STROKE, WHITE

BALL_COLORS = {'R': CORAL, 'B': CYAN, 'Y': GOLD, 'G': GREEN, 'P': PURPLE}
COIN_FACE = {'N': ('#F2C14E', '#A87B12'), 'S': ('#C7D2DE', '#6B7A8C')}  # ngửa vàng, sấp bạc

PIPS = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
        4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
        6: [(-1, 1), (-1, 0), (-1, -1), (1, 1), (1, 0), (1, -1)]}


# ------------------------------------------------------------------ coin
def coin(face='N', r=0.8):
    fill, rim = COIN_FACE[face]
    body = Circle(radius=r, fill_color=fill, fill_opacity=1, stroke_color=rim, stroke_width=7)
    ring = Circle(radius=r * .78, stroke_color=rim, stroke_width=3)
    letter = Text(face, font=FONT, font_size=int(78 * r), color=INK, weight='BOLD')
    g = VGroup(body, ring, letter)
    g.face = face
    return g


# ------------------------------------------------------------------ die
def die(v=1, s=1.1, color=WHITE, pip=INK, stroke='#CBD5E1'):
    body = RoundedRectangle(width=s, height=s, corner_radius=s * .17, fill_color=color, fill_opacity=1,
                            stroke_color=stroke, stroke_width=3)
    pips = VGroup(*[Dot([dx * s * .27, dy * s * .27, 0], radius=s * .085, color=pip) for dx, dy in PIPS[v]])
    g = VGroup(body, pips)
    g.value = v
    return g


def roll_faces(final, n=7, seed=1):
    """Pseudo-random face sequence ending on ``final`` (deterministic)."""
    rnd = random.Random(seed * 31 + final)
    seq = [rnd.randint(1, 6) for _ in range(n - 1)]
    for i in range(1, len(seq)):
        if seq[i] == seq[i - 1]:
            seq[i] = seq[i] % 6 + 1
    if seq and seq[-1] == final:
        seq[-1] = final % 6 + 1
    return seq + [final]


# ------------------------------------------------------------------ playing card
SUITS = {'S': ('♠', INK), 'H': ('♥', '#E5484D'), 'D': ('♦', '#E5484D'), 'C': ('♣', INK)}


def playing_card(rank='A', suit='H', w=1.2):
    h = w * 1.42
    sym, col = SUITS[suit]
    body = RoundedRectangle(width=w, height=h, corner_radius=w * .1, fill_color=WHITE, fill_opacity=1,
                            stroke_color='#CBD5E1', stroke_width=2)
    corner = VGroup(Text(rank, font=FONT, font_size=int(30 * w), color=col, weight='BOLD'),
                    Text(sym, font_size=int(24 * w), color=col)).arrange(DOWN, buff=.03)
    corner.move_to(body.get_corner(UP + LEFT) + np.array([w * .2, -h * .2, 0]))
    big = Text(sym, font_size=int(70 * w), color=col).move_to(body)
    return VGroup(body, corner, big)


def card_back(w=1.2):
    h = w * 1.42
    body = RoundedRectangle(width=w, height=h, corner_radius=w * .1, fill_color='#2B4A7A', fill_opacity=1,
                            stroke_color=WHITE, stroke_width=3)
    inner = RoundedRectangle(width=w * .78, height=h * .82, corner_radius=w * .07, stroke_color=CYAN,
                             stroke_width=2).move_to(body)
    return VGroup(body, inner)


# ------------------------------------------------------------------ urn
def ball(color='R', r=0.26):
    c = BALL_COLORS.get(color, color)
    shine = Circle(radius=r * .28, fill_color=WHITE, fill_opacity=.55, stroke_width=0) \
        .move_to([-r * .35, r * .35, 0])
    return VGroup(Circle(radius=r, fill_color=c, fill_opacity=1, stroke_color=INK, stroke_width=2), shine)


def urn(colors, cols=4, r=0.26, width=None):
    """Open jar holding balls (``colors`` like 'RRRBB'); balls fill from the bottom row."""
    rows = -(-len(colors) // cols)
    w = width or cols * 2.3 * r + .5
    h = rows * 2.3 * r + .7
    jar = VMobject(stroke_color=SOFT, stroke_width=6)
    jar.set_points_smoothly([[-w / 2 - .12, h / 2, 0], [-w / 2, -h / 2 + .25, 0], [-w / 2 + .3, -h / 2, 0],
                             [w / 2 - .3, -h / 2, 0], [w / 2, -h / 2 + .25, 0], [w / 2 + .12, h / 2, 0]])
    balls = VGroup()
    for i, c in enumerate(colors):
        row, col = divmod(i, cols)
        in_row = min(cols, len(colors) - row * cols)
        x = (col - (in_row - 1) / 2) * 2.3 * r
        y = -h / 2 + .32 + r + row * 2.15 * r
        balls.add(ball(c, r).move_to([x, y, 0]))
    g = VGroup(jar, balls)
    g.balls = balls
    return g


# ------------------------------------------------------------------ probability tree (top-down)
def tree(spec, top=(0, 3.0), dy=1.45, width=6.4, edge_color=STROKE):
    """``spec`` = {'m': mob, 'e': edge-label mob or None, 'kids': [spec, ...]} (root has no edge).

    Returns (group, levels) where levels[d] = VGroup(edges + edge labels + nodes) at depth d,
    so a scene can grow the tree one generation at a time.
    """
    def leaves(node):
        return 1 if not node.get('kids') else sum(leaves(k) for k in node['kids'])

    levels = []

    def place(node, x0, x1, depth, parent_pt):
        x = (x0 + x1) / 2
        y = top[1] - depth * dy
        while len(levels) <= depth:
            levels.append(VGroup())
        node['m'].move_to([top[0] + x, y, 0])
        if parent_pt is not None:
            start = parent_pt
            end = node['m'].get_top() + UP * .06
            ln = Line(start, end, color=edge_color, stroke_width=4)
            node['line'] = ln
            levels[depth].add(ln)
            if node.get('e') is not None:
                mid = (start + end) / 2
                side = LEFT if end[0] < start[0] else RIGHT
                node['e'].next_to(mid, side, buff=.08)
                levels[depth].add(node['e'])
        levels[depth].add(node['m'])
        kids = node.get('kids') or []
        total = sum(leaves(k) for k in kids)
        a = x0
        for k in kids:
            b = a + (x1 - x0) * leaves(k) / total
            place(k, a, b, depth + 1, node['m'].get_bottom() + DOWN * .06)
            a = b

    place(spec, -width / 2, width / 2, 0, None)
    return VGroup(*levels), levels


# ------------------------------------------------------------------ sample-space grid
def grid(rows, cols, cell=0.78, stroke=STROKE, fill='#14233B'):
    """rows × cols squares; ``g.cells[i][j]`` is row i (top) column j (left)."""
    g = VGroup()
    cells = []
    for i in range(rows):
        line = []
        for j in range(cols):
            sq = Square(side_length=cell, stroke_color=stroke, stroke_width=2, fill_color=fill, fill_opacity=1)
            sq.move_to([(j - (cols - 1) / 2) * cell, ((rows - 1) / 2 - i) * cell, 0])
            line.append(sq)
            g.add(sq)
        cells.append(line)
    g.cells = cells
    return g
