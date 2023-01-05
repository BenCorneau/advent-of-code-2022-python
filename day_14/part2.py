
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


def points_in_line(line:Line)->Iterable[Point]:
    '''
    Given two points return each point between those points and the points themeself.
    Assume that the line is either perfectly horizontal or perfectly vertical.
    '''
    next_point = line.a
    end_point = line.b
    yield next_point
    while next_point != end_point:
        x,y = next_point
        if   x < end_point.x: x+=1
        elif x > end_point.x: x-=1
        elif y < end_point.y: y+=1
        elif y > end_point.y: y-=1
        next_point = Point(x,y)
        yield next_point


def build_grid(segments:List[Segment])->Grid:

    max_y = 0
    for segment in segments:
        for line in segment:
            for point in line:
                max_y = max(point.y, max_y)

    #  the floor is two plus the highest y coordinate of any point in your scan 
    height = max_y + 2
         
    # sand can fall one space left for each space down
    width = 500 + height + 1

    # build an empty grid
    data = []
    for y in range(height): data.append([' ']*(width))

    # add a floor
    data.append(['#']*(width))

    # add each segment to the empty grid
    grid = Grid(data)
    for segment in segments:
        for line in segment:
            for point in points_in_line(line):
                grid[point] = "#"

    return grid


def drop_sand(grid)->bool:
    sand = Point(x=500,y=0)

    while True:
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
    grid[(500,0)] = "+"  # marker for sand source

    grid.print(x_start=420)
    count = 0
    while grid[(500,0)] != "o":
        drop_sand(grid)
        count += 1      
    grid.print(x_start=420)
    
    return count

