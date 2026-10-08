"""Shared settings for Sang Math combinatorics lessons.

Notation is configurable because the user's example C^(n)_(k) places n
above k, while common Vietnamese textbooks print C_n^k (n below).
"""
import os

# Explicitly follow the example C^(n)_(k) given for this series.
# Switch to "sgk" to use C_n^k and A_n^k instead.
NOTATION = os.getenv('COMB_NOTATION', 'user')
if NOTATION not in {'user', 'sgk'}:
    raise ValueError('COMB_NOTATION must be user or sgk')

PALETTE = {
    'bg': '#0B1120', 'panel': '#101F33', 'panel_alt': '#172A43',
    'text': '#ECF4FF', 'muted': '#A8B9CC', 'cyan': '#22D3EE',
    'gold': '#FBBF24', 'purple': '#A78BFA', 'red': '#EF4444',
    'green': '#22C55E', 'line': '#2E4862', 'inactive': '#475569',
}


def symbol(letter: str, n: str | int, k: str | int) -> str:
    """Return Typst math markup for either index convention."""
    if letter not in {'A', 'C'}:
        raise ValueError('letter must be A or C')
    if NOTATION == 'user':
        return f'{letter}^({n})_({k})'
    return f'{letter}_({n})^({k})'


def combination(n: int, k: int) -> int:
    from math import comb
    return comb(n, k)


def arrangement(n: int, k: int) -> int:
    from math import perm
    return perm(n, k)
