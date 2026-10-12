"""Seats, people and train cars for the seating Shorts (XSS345+)."""
from __future__ import annotations

from manim import Circle, RoundedRectangle, VGroup

from common.theme import PANEL, SOFT, STROKE
from common.visuals import token


def seat_row(n, y=1.0, w=.82, gap=.16):
    g = VGroup(*[RoundedRectangle(width=w, height=w * .7, corner_radius=.1, stroke_color=STROKE, stroke_width=3,
                                  fill_color=PANEL, fill_opacity=1) for _ in range(n)])
    return g.arrange(buff=gap).move_to([0, y, 0])


def seat(people, seats, r=.3):
    """Tokens ``people`` = [(label, colour), …] placed on the seats in order."""
    return VGroup(*[token(lab, col, r).move_to(s) for (lab, col), s in zip(people, seats)])


def train(k, y=1.0, w=1.9, h=1.1, gap=.22, labels=True, scene=None):
    cars = VGroup()
    for i in range(k):
        body = RoundedRectangle(width=w, height=h, corner_radius=.15, stroke_color=SOFT, stroke_width=4, fill_color=PANEL, fill_opacity=1)
        wheels = VGroup(*[Circle(radius=.13, stroke_color=SOFT, stroke_width=3, fill_color=STROKE, fill_opacity=1)
                          .move_to(body.get_bottom() + [dx, -.05, 0]) for dx in (-w / 3, w / 3)])
        car = VGroup(body, wheels)
        if labels and scene is not None:
            car.add(scene.TM(f'$T_{i + 1}$', 24, SOFT).next_to(body, [0, 1, 0], buff=.08))
        cars.add(car)
    cars.arrange(buff=gap)
    if cars.width > 7.4:
        cars.scale_to_fit_width(7.4)
    return cars.move_to([0, y, 0])


def ride(cars, counts, color=None, r=.17):
    """Passenger dots inside each car: ``counts[i]`` people in car i."""
    from manim import Dot
    from common.theme import CYAN
    g = VGroup()
    for car, c in zip(cars, counts):
        dots = VGroup(*[Dot(radius=r, color=color or CYAN) for _ in range(c)])
        if c:
            dots.arrange_in_grid(rows=2 if c > 3 else 1, buff=.08).move_to(car[0].get_center())
        g.add(dots)
    return g
