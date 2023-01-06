
from typing import NamedTuple

class Color(NamedTuple):
    r: int
    g: int
    b: int
    
PURE_BLACK = Color(  0,   0,   0)
BLACK      = Color(  5,   5,   5)
WHITE      = Color(250, 250, 250)
PURE_WHITE = Color(255, 255, 255)

PURE_RED   = Color(255,   0,   0)
DARK_RED   = Color(100,   5,   5)
RED        = Color(250, 150, 150)

GREEN      = Color(  0, 255,   0)
BLUE       = Color(  0,   0, 255)


def _clamp(v:int)->int:
    if v < 0: return 0
    if v > 255: return 255
    return int(v)

def offset(c:Color, offset:int)->Color:
    r,g,b = c
    return Color(_clamp(r+offset), _clamp(g+offset), _clamp(b+offset))