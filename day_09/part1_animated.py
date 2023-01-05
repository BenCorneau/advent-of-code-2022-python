from collections import deque
from typing import Any, List
from util import read_lines


from grid import SparseGrid, RenderGrid
from video_generator import VideoGenerator
import colors

OUTPUT_VIDEO = "day_09/video_part1.mp4"

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
    

#x -118 185
#y -279 67   
import time
grid = RenderGrid(SparseGrid(min_x=-119, max_x=186,min_y=-280,max_y=68))
video_generator = VideoGenerator(OUTPUT_VIDEO, subsample=5, subsample_multiplier=1, live_preview=True)
def render(head, tail):
    grid._canvas.rectangle((0,0, grid.image.width, grid.image.height),fill=(5,5,255,8))
    grid.set_value(tuple(head), "H", colors.WHITE)
    grid.set_value(tuple(tail), "T", colors.WHITE)
    video_generator.append_image(grid.image)
     

def run()->int:

    visited = set()

    head = [0,0]
    tail = [0,0]
    count = 0
    for line in read_lines("day_09/input.txt"):
        direction, moves = parse_line(line)
        
        for _ in range(moves):
            move_head(direction, head)
            move_tail(head, tail)
            visited.add(tuple(tail))
            render(head, tail)
            count += 1
            if count %100==0:
                print("PROGRESS:", int(count*100/11687))


    min_x = min((x for x,_ in visited))
    max_x = max((x for x,_ in visited))
    min_y = min((y for _,y in visited))
    max_y = max((y for _,y in visited))
    print("x", min_x, max_x)
    print("y", min_y, max_y)
       
    print("TOTAL STEPS", count)  
    video_generator.close() 
    return len(visited)

