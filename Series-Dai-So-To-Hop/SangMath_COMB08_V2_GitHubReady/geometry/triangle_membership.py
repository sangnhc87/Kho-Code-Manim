"""Exact oriented-area tests for a 2D triangle (no Manim dependency).

cross(U,V) is a determinant. `interior` excludes the boundary.
"""
from __future__ import annotations


def cross(ax, ay, bx, by):
    return ax * by - ay * bx


def orient(a, b, p):
    return cross(b[0]-a[0], b[1]-a[1], p[0]-a[0], p[1]-a[1])


def nondegenerate(a,b,c):
    return orient(a,b,c) != 0


def membership(a,b,c,p):
    """Return 'inside', 'boundary' or 'outside' for a non-degenerate triangle.

    Input numbers can be Fraction for exact equality on the edges.
    """
    delta = orient(a,b,c)
    if delta == 0:
        raise ValueError('Three vertices must not be collinear')
    tests=[delta*orient(a,b,p),delta*orient(b,c,p),delta*orient(c,a,p)]
    if all(t>0 for t in tests):
        return 'inside'
    if all(t>=0 for t in tests):
        return 'boundary'
    return 'outside'


def barycentric(a,b,c,p):
    delta=orient(a,b,c)
    if delta == 0:
        raise ValueError('Degenerate triangle')
    return (orient(b,c,p)/delta, orient(c,a,p)/delta, orient(a,b,p)/delta)
