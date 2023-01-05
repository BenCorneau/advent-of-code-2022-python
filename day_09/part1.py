from collections import defaultdict
from typing import Any, List
from util import read_lines

X = 0
Y = 1

MOVEMENT = {
    'U':(Y, +1),
    'D':(Y, -1),
    'L':(X, -1),
    'R':(X, +1)
}

def move_head(direction, head):
    dimension, offset = MOVEMENT[direction]
    head[dimension] += offset


TAIL_MOVEMENT = {
    (0,+2) : (0,+1), # →
    (0,-2) : (0,-1), # ←

    (+2,0) : (+1,0), # ↑
    (-2,0) : (-1,0), # ⬇

    (+1,+2) : (+1,+1), # ↗
    (+2,+1) : (+1,+1),

    (+1,-2) : (+1,-1), # ↘
    (+2,-1) : (+1,-1),

    (-1,-2) : (-1,-1), # ↙
    (-2,-1) : (-1,-1),

    (-1,+2) : (-1,+1), # ↖
    (-2,+1) : (-1,+1),
}
def move_tail(head, tail):
    x_offset = head[X] - tail[X] 
    y_offset = head[Y] - tail[Y] 

    (dx, dy) = TAIL_MOVEMENT.get((x_offset, y_offset), (0,0))

    tail[X] += dx
    tail[Y] += dy
        

def parse_line(line: str) -> Any:
    return line[0], int(line[2:])
    
def run()->int:

    visited = set()

    head = [0,0]
    tail = [0,0]
    
    for line in read_lines("day_09/input.txt"):
        direction, moves = parse_line(line)
        for i in range(moves):
            move_head(direction, head)
            move_tail(head, tail)
            visited.add(tuple(tail))
            
    return len(visited)

