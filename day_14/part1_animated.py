from collections import defaultdict
from typing import Any, List,Iterable, NamedTuple
from PIL import Image, ImageDraw, ImageFont
from  subprocess import Popen, PIPE
import time
from io import BytesIO
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


def drop_sand(grid, save_grid_func)->bool:
    sand = Point(x=500,y=0)

    path = []

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
            save_grid_func(grid)

            for p in path:
                grid[p] = ' ' 
            path = []
            grid[sand] = 'o'
            
            return True

        grid[sand] = '*'
        path.append(sand)
        #save_grid_func(grid)

X_OFFSET = 350
X_PADDING = 30
def run()->int:
       
    segments = get_input()
    grid = build_grid(segments)
    grid[(500,0)] = "+"

    count = 0
    index = 0

    image = Image.new('RGB', ((grid.width-X_OFFSET+X_PADDING)*CHAR_WIDTH, grid.height*CHAR_HEIGHT), (10,10,10))
    draw = ImageDraw.Draw(image)

    video_generator = VideoGenerator2(image.width, image.height, "day_14/video.mp4", temp_path="day_14/animation")
    def save_grid_func(grid):
        draw_grid(grid, draw)
        video_generator.append_image(image)
            
    more = True
    while more:
        more = drop_sand(grid, save_grid_func)
        if more:
            count += 1

    video_generator.close()
    return count


CHAR_WIDTH = 11
CHAR_HEIGHT = 25
FONT = ImageFont.truetype('sourcecodepro.ttf', size=20)
#[b'ExtraLight', b'Light', b'Regular', b'Medium', b'SemiBold', b'Bold', b'ExtraBold', b'Black']
FONT.set_variation_by_name("Bold")

char_color = {
    '#' : (190,190,190),
    'o' : (250,250,250),
    '+' : (100,100,200),
    '*' : (100,100,100),
}


def draw_grid(grid, draw):

    for point in grid.points():
        ch = grid[point]
        if ch == " ":
            continue

        x,y = point
        draw_x = (x-X_OFFSET)*CHAR_WIDTH
        draw_y = y*CHAR_HEIGHT

        color = char_color[ch]
        draw.text((draw_x, draw_y), ch, font=FONT, fill=color)


class VideoGenerator2:
    
    def __init__(self, width, height, output_file, temp_path):
        self._frame_index = 0
        self._temp_dir = temp_path
        self._output_file = output_file

    
    def append_image(self, image):
        img_path = f"{self._temp_dir}/frame_{self._frame_index:04}.bmp"
        print(f"save frame {img_path}...")  
        image.save(img_path, format="bmp")
        self._frame_index += 1

          

    def close(self):
        print("closing video...")

       # ffmpeg -r 1/5 -start_number 2 -i img%03d.png -c:v libx264 -r 30 -pix_fmt yuv420p out.mp
        command = ["ffmpeg",
                '-i', f"{self._temp_dir}/frame_%04d.bmp",
                '-r', '30',
                '-pix_fmt', 'yuv420p',
                '-y',    # overwrite
                self._output_file ]

        self._proc = Popen(command, text=False)
        self._proc.wait()
        print("done")

class VideoGenerator:
    
    def __init__(self, width, height, output_file):

        #this did work
        command = ["ffmpeg",
                '-y',
                '-f', 'rawvideo',
                '-vcodec','rawvideo',
                '-s', f'{width}x{height}',
                '-pix_fmt', 'rgb444le',
                '-r', '30',
                '-i', '-',
                '-an',
                '-vcodec', 'mpeg4',
                '-b:v', '5000k',
                output_file ]


        #NOT WORKING
        # #-f image2pipe -framerate 1 -i - -c:v libx264 
        # #-vf format=yuv420p -r 25 -movflags +faststart out.mp4
        # command = ["ffmpeg",
        #         '-probesize', '16M',
        #         '-y',
        #         '-f', 'image2pipe',
        #         '-framerate',  '30',
        #  '-s', f'{width}x{height}',
        #  '-pix_fmt', 'rgb24',
        #         '-r', '30',
        #         '-i', '-',
        #         '-an',
        #          '-vcodec', 'mpeg4',
        #          '-b:v', '5000k',
        #         output_file ]


        # command = ['ffmpeg',
        #     '-y',
        #    '-f', 'image2pipe',
        #     '-framerate', '5',
        #    '-r', '5',  # FPS 
        #    '-i', '-',  # Indicated input comes from pipe 
        #    '-qscale', '0',
        #    output_file]
        
        self._proc = Popen(command, stdin=PIPE, stderr=PIPE, stdout=PIPE, text=False)
        print("a")
        #print(self._proc.stdout.read(10))
        print("b")

    def append_frame(self, frame):
        try:
            self._proc.stdin.write(frame)
        except Exception as e:
            print(e)
            print(self._proc)
            print(self._proc.stdout.read(10))
            print(self._proc.stderr.read())

    def append_image(self, image):
        print("save frame...")
        try:
            image.save(self._proc.stdin, format="bmp")
        except Exception as e:
            print(e)
            print(self._proc)
            print(self._proc.stdout.read())
            print(self._proc.stderr.read().decode().replace("\\n", "\n"))
            

    def close(self):
        print("closing video...")
        self._proc.stdin.close()
        self._proc.stderr.close()
        self._proc.wait()
