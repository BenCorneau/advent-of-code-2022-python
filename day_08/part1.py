from collections import defaultdict
from typing import Any, List
from util import read_lines
from grid import Grid


def get_input() -> Grid:
    rows = []
    for line in read_lines("day_08/input.txt"):
        rows.append([int(t) for t in line])
    return Grid(rows)

def visible(tree, forest):
    tree_height = forest[tree]
    for dx, dy in ((0,1), (0,-1), (1,0), (-1,0)):
        x,y = tree
        next_height = -1
        while tree_height > next_height:
            x,y = x+dx, y+dy
            if not forest.valid_point((x,y)): #hit the edge of the forest
                return True
            next_height = forest[(x,y)]
    return False
            
            
        
def run()->int:
    forest = get_input()
    visible_count = 0
    for tree in forest.points():
        if visible(tree, forest):
            visible_count += 1
        
    return visible_count
