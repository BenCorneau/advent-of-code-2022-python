from typing import Any, List
from util import read_lines
from grid import Grid
from collections import defaultdict

X = 0
Y = 1

MOVEMENT = {
    'U':(Y, -1),
    'D':(Y, +1),
    'L':(X, -1),
    'R':(X, +1)
}

def move_head(direction, head):
    dimension, offset = MOVEMENT[direction]
    head[dimension] += offset



def move_tail(head, tail):
    x_offset = head[X] - tail[X] 
    y_offset = head[Y] - tail[Y] 
 
    if x_offset == 0:
        if y_offset > +1: tail[Y] += 1
        if y_offset < -1: tail[Y] -= 1
    elif y_offset == 0:
        if x_offset > +1: tail[X] += 1
        if x_offset < -1: tail[X] -= 1
    elif abs(x_offset) == 1 and abs(y_offset)==1:
        pass
    else:
        if y_offset > 0: tail[Y] += 1
        if y_offset < 0: tail[Y] -= 1
        if x_offset > 0: tail[X] += 1
        if x_offset < 0: tail[X] -= 1      
        

def parse_line(line: str) -> Any:
    return line[0], int(line[2:])
    
def run()->int:

    visited_all = defaultdict(set)

    knots = []
    for _ in range(10):
        knots.append([20,20])

    for line in read_lines("day_09/input.txt"):
        direction, moves = parse_line(line)
        for _ in range(moves):
            for knot_index, knot in enumerate(knots):
                if knot_index == 0:
                    move_head(direction, knot)
                else:
                    move_tail(prev, knot)
                
                prev = knot
                visited_all[knot_index].add(tuple(knot))
         
    return len(visited_all[9])

    

