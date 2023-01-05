from typing import Any, List
from util import read_lines
from grid import Grid


def get_input() -> Grid:
    rows = []
    for line in read_lines("day_08/input.txt"):
        rows.append([int(t) for t in line])
    return Grid(rows)

def scenic_score(tree, forest):
    tree_height = forest[tree]
    distances = []
    for dx, dy in ((0,1), (0,-1), (1,0), (-1,0)):
        x,y = tree
        visible_trees = 0
        blocked = False
        while not blocked:
            x,y = x+dx, y+dy
            if not forest.valid_point((x,y)):
                blocked = True
            else:
                visible_trees += 1
                next_height = forest[(x,y)]
                blocked = next_height >= tree_height
        distances.append(visible_trees)
       
    return distances[0] * distances[1] * distances[2] * distances[3]
            
                 
def run()->int:
    forest = get_input()
    best_score = 0
    for tree in forest.points():
        score = scenic_score(tree, forest)
        best_score = max(best_score, score)
     
    return best_score
