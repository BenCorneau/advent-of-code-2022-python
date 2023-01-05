from typing import List, Iterable, Tuple, NamedTuple
from util import read_lines

from grid import Grid, SparseGrid, RenderGrid, Point
from video_generator import VideoGenerator
from colors import Color

#types
Line = NamedTuple("Line", [('a', Point), ('b', Point)])
Segment = List[Line]


OUTPUT_VIDEO = "day_14/video_part2.mp4"

CHAR_COLOR = {
    '#' : Color(220,220,100),
    'o' : Color(250,250,250),
    '+' : Color(100,100,200),
    '*' : Color(100,100,100),
}
def color_map(_:Point, value:str)->Tuple[Color|None, Color|None]:
    return CHAR_COLOR.get(value), None


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


def build_grid(segments:List[Segment])->RenderGrid[str]:

    max_y = 0
    for segment in segments:
        for line in segment:
            for point in line:
                max_y = max(point.y, max_y)

    #  the floor is two plus the highest y coordinate of any point in your scan 
    height = max_y + 2
    min_x=500-height
    max_x=500+height

    grid = SparseGrid(min_x=min_x, max_x=max_x, max_y=height+1, default_value=' ')
    render_grid = RenderGrid(grid, cell_color_func=color_map)

    # add a floor
    for x in range(min_x, max_x+1):
        render_grid[(x,height)] = "#"

    # add each segment to the empty grid
    for segment in segments:
        for line in segment:
            for point in points_in_line(line):
                render_grid[point] = "#"

    return render_grid


def drop_sand(grid:Grid, fall_path):
    sand = fall_path[-1]   
    next_down  = Point(sand.x,   sand.y+1)
    next_left  = Point(sand.x-1, sand.y+1)
    next_right = Point(sand.x+1, sand.y+1)

    if grid[next_down] == ' ':
        fall_path.append(next_down)
    elif grid[next_left] == ' ':
        fall_path.append(next_left)
    elif grid[next_right] == ' ':
        fall_path.append(next_right)
    else:
        grid[sand] = 'o'
        fall_path.pop()
        return sand    

    grid[fall_path[-1]] = "*"
    return None


def run()->int:
    segments = get_input()
    grid = build_grid(segments)
    grid[(500,0)] = "+"  # marker for sand source

    with VideoGenerator(OUTPUT_VIDEO, subsample_multiplier=1.01, live_preview=True) as video_generator:
        count = 0
        fall_path = [Point(500,0)] 
        while fall_path:
            if drop_sand(grid, fall_path):    
                video_generator.append_image(grid.image)
                count+=1
                  
        video_generator.append_image(grid.image, force=True)

    return count
