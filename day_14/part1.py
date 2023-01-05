
from typing import List, Iterable, NamedTuple

from util import read_lines
from grid import Grid, Point


Line = NamedTuple("Line", [('a', Point), ('b', Point)])
Segment = List[Line]


def get_input() -> List[Segment]:
    segments = []
    for line in read_lines("day_14/input.txt"):
        points = []
        for point in line.split(" -> "):
            x,y = point.split(",")
            points.append(Point(x=int(x), y=int(y)))

        segment = []
        for i in range(1,len(points)):
            segment.append(Line(a=points[i-1], b=points[i]))
        segments.append(segment)
    return segments


def line_points(line:Line)->Iterable[Point]:
    next_point = line.a
    yield next_point
    while next_point != line.b:
        x,y = next_point
        dx,dy = 0, 0
        if x < line.b.x: dx = 1
        elif x > line.b.x: dx = -1
        elif y < line.b.y: dy = 1
        elif y > line.b.y: dy = -1
        next_point = Point(x=x+dx, y=y+dy)
        yield next_point


def build_grid(segments:List[Segment])->Grid:
    max_x = 0
    max_y = 0
    for segment in segments:
        for line in segment:
            for point in line:
                max_x = max(point.x, max_x)
                max_y = max(point.y, max_y)
    
    data = []
    for y in range(max_y+1):
        data.append([' ']*(max_x+1))

    grid = Grid(data)
    for segment in segments:
        for line in segment:
            for point in line_points(line):
                grid[point] = "#"
            
    return grid


def drop_sand(grid)->bool:
    sand = Point(x=500,y=0)

    while True:
        if sand.y + 1 == grid.height:
            return False
            
        next_down = Point(sand.x,sand.y+1)
        next_left = Point(sand.x-1,sand.y+1)
        next_right = Point(sand.x+1,sand.y+1)
        if grid[next_down] == ' ':
            sand = next_down
        elif grid[next_left] == ' ':
            sand = next_left
        elif grid[next_right] == ' ':
            sand = next_right
        else:
            grid[sand] = 'o'
            return True

        
def run()->int:
       
    segments = get_input()
    grid = build_grid(segments)
    grid[(500,0)] = "+"

    grid.print(x_start=420)
    
    count = 0
    while drop_sand(grid):
        count += 1
    
    print("="*50)
    grid.print(x_start=420)
    
    return count

