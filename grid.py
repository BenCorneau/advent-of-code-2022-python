
from typing import Iterable, List, NamedTuple, Protocol, TypeVar
from PIL import Image, ImageDraw, ImageFont

from colors import Color

Point = NamedTuple("Point", [('x', int), ('y', int)])

T = TypeVar('T')

class Grid(Protocol[T]):
 
    @property
    def height(self) -> int: pass

    @property 
    def width(self) -> int: pass

    @property
    def min_x(self) -> int: pass

    @property
    def max_x(self) -> int: pass

    @property
    def min_y(self) -> int: pass

    @property
    def max_y(self) -> int: pass

    def __getitem__(self, point:Point) -> T: pass
    def __setitem__(self, point:Point, value:T) -> None: pass
    def points(self) -> Iterable[Point]: pass
    def valid_point(self, point:Point) -> bool: pass
    def adjacent_points(self, point:Point)-> Iterable[Point]: pass


class BaseGrid(Grid[T]):
    @property
    def height(self)->int: return self.max_y - self.min_y + 1

    @property
    def width(self)->int: return self.max_x - self.min_x + 1

    @property
    def min_x(self) -> int: return self._min_x

    @property
    def max_x(self) -> int: return self._max_x

    @property
    def min_y(self) -> int: return self._min_y

    @property
    def max_y(self) -> int: return self._max_y

    
    def valid_point(self, point:Point) -> bool:
        x,y = point
        if x < self.min_x or x > self.max_x: return False
        if y < self.min_y or y > self.max_y: return False
        return True


    def adjacent_points(self, point:Point)-> Iterable[Point]:
        x,y = point
        neighboors = [
            (x, y-1),
            (x, y+1),
            (x-1,y),
            (x+1,y)]

        return set([p for p in neighboors if self.valid_point(p)])

    def __str__(self)->str:
        rows = []
        for y in range(self.min_y, self.max_y+1):
            row = []
            for x in range(self.min_x, self.max_x+1):
                row.append(str(self[(x,y)]))    
            rows.append("".join(row))
        return "\n".join(rows)


    def print(self, x_start=None, x_end=None, y_start=None, y_end=None)->None:
        if x_start == None: x_start = self.min_x
        if x_end   == None: x_end   = self.max_x + 1
        if y_start == None: y_start = self.min_y
        if y_end   == None: y_end   = self.max_y + 1

        wide = x_end-x_start
        print('┏' + "-"*wide + '┓' )
        for y in range(y_start, y_end):
            row = []
            for x in range(x_start, x_end):
                row.append(self[(x,y)])    
            print("|" + "".join([str(v) for v in row]) + "|" )
        print('┗' + "-"*wide + '┛' )


class ArrayGrid(BaseGrid[T]):

    def __init__(self, data:List[List[T]], start_x=0, start_y=0):
        self.data = data
        self._min_x = start_x
        self._min_y = start_y

        width = len(data[0])
        height = len(data)
        self._max_x = (width + start_x) - 1
        self._max_y = (height + start_y) - 1  

    def __getitem__(self, point:Point)->T:
        x,y = self._offset_point(point)
        return self.data[y][x]

    def __setitem__(self, point:Point, value:T):
        x,y = self._offset_point(point)
        self.data[y][x] = value

    def _offset_point(self, point:Point)->Point:
        x,y = point
        assert self.min_x<=x<=self.max_x, f"x index out of range. point(x={x}, y={y}) x range[{self.min_x}:{self.max_x}]"
        assert self.min_y<=y<=self.max_y, f"y index out of range. point(x={x}, y={y}) y range[{self.min_y}:{self.max_y}]"
        return x-self.min_x, y-self.min_y
  
    def points(self) -> Iterable[Point]:
        for x in range(self.min_x, self.max_x+1):
            for y in range(self.min_y, self.max_y+1):
                yield (x,y)
    

class SparseGrid(BaseGrid[T]):

    def __init__(self, max_x:int, max_y:int,  min_x:int=0, min_y:int=0, default_value = None):
        self._min_x = min_x
        self._max_x = max_x
        self._min_y = min_y
        self._max_y = max_y
        self._default_value = default_value

        self._data = {}
       
    def __getitem__(self, point:Point)->T:
        self._assert_valid_point(point)
        return self._data.get(point, self._default_value)

    def __setitem__(self, point:Point, value:T):
        self._assert_valid_point(point)
        self._data[point] = value

    def _assert_valid_point(self, point:Point)->None:
        x,y = point
        assert self.min_x <= x <= self.max_x, f"x[{x}] must be in range {self.min_x} {self.max_x}"
        assert self.min_y <= y <= self.max_y, f"y[{y}] must be in range {self.min_y} {self.max_y}"
   
    def points(self) -> Iterable[Point]:
        for p in self._data.keys():
            yield p
              

class FontConfig(NamedTuple):
    font_name: str 
    font_size: int
    char_width: int
    char_height: int
    x_offset: int
    y_offset: int

FONT_10_NUMERIC = FontConfig('sourcecodepro.ttf', font_size=10, char_width= 6, char_height= 9, x_offset=0, y_offset=-2)
FONT_20_NUMERIC = FontConfig('sourcecodepro.ttf', font_size=20, char_width=12, char_height=16, x_offset=0, y_offset=-6)

FONT_10_ALPHA = FontConfig('sourcecodepro.ttf', font_size=10, char_width= 8, char_height= 11, x_offset=1, y_offset=-1)
FONT_20_ALPHA = FontConfig('sourcecodepro.ttf', font_size=20, char_width=14, char_height=21, x_offset=1,  y_offset=-4)

DEFAULT_FG_COLOR = (250,250,250)
DEFAULT_BG_COLOR = (10,10,10)


class RenderGridStateContext():
    def __init__(self, rednder_grid, state_name=None):
        self._render_grid = rednder_grid
        self._state_name = state_name

    def __enter__(self):
        self._render_grid.push_image_state(self._state_name)

    def __exit__(self, exc_type, exc_value, traceback):
        self._render_grid.pop_image_state() 


class RenderGrid(BaseGrid[T]):

    def __init__(self, data_grid, fg_color=None, bg_color=None, cell_color_func=None, font_config=FONT_10_NUMERIC) -> None:
        self.base_grid = data_grid
        self._min_x = data_grid.min_x
        self._max_x = data_grid.max_x
        self._min_y = data_grid.min_y
        self._max_y = data_grid.max_y

        self.fg_color = fg_color or DEFAULT_FG_COLOR
        self.bg_color = bg_color or DEFAULT_BG_COLOR
        self._cell_color_func = cell_color_func or (lambda _1,_2:(None, None))

        self._font_config = font_config
        self._font = ImageFont.truetype(font_config.font_name, size=font_config.font_size)
        self._font.set_variation_by_name("Bold")

        img_width = data_grid.width * font_config.char_width
        img_height = data_grid.height * font_config.char_height
        self.image = Image.new('RGB', (img_width, img_height), color=self.bg_color)
        self._canvas = ImageDraw.Draw(self.image, mode='RGBA') # use RGBA draw mode to use colors with alpha 

        self._save_state_stack = []
        self._color_override = {}

        # load the current state of the grid into the image
        for p in data_grid.points():
            self.set_value(p, data_grid[p])

    def __getitem__(self, point:Point)->T:
        return self.base_grid[point]

    def __setitem__(self, point:Point, value:T): 
        self.set_value(point, value)

    def points(self) -> Iterable[Point]:
        return self.base_grid.points()
    
    def push_image_state(self, name:str = None):
        self._save_state_stack.append(([],name))

    def pop_image_state(self)->str|None:
        restore_state, state_name = self._save_state_stack.pop()

        while restore_state:
            point, value, color_settings = restore_state.pop()
            fg_color, bg_color = None, None
            if color_settings:
                fg_color, bg_color = color_settings
            self._set_value_direct(point, value, fg_color, bg_color)
        return state_name

    def image_state(self, name = None) -> RenderGridStateContext:
        return RenderGridStateContext(self, name)

    def set_color(self, point, fg=None, bg=None):
        self.set_value(point, self.base_grid[point], fg, bg)

    def set_value(self, point, value, fg_color=None, bg_color=None):

        if self._save_state_stack:
            old_value = self.base_grid[point]
            color_settings = self._color_override.get(point)
            self._save_state_stack[-1][0].append((point, old_value, color_settings))
  
        self._set_value_direct(point, value, fg_color, bg_color)

    def _get_cell_colors(self, point, value):
        fg_color, bg_color = self._cell_color_func(point, value)
        return (fg_color or self.fg_color, bg_color or self.bg_color)
        

    def _set_value_direct(self, point, value, fg_color, bg_color):
        default_fg_color, default_bg_color = self._get_cell_colors(point, value)
        
        fg_color = fg_color or default_fg_color
        bg_color = bg_color or default_bg_color
        
        if fg_color != default_fg_color or bg_color != default_bg_color:
            self._color_override[point] = (fg_color, bg_color)
        elif point in self._color_override:
            del self._color_override[point]

        self._fill_background(point, bg_color)
        self._draw_value(point, value, fg_color)
    
        self.base_grid[point] = value


    def _fill_background(self, point, color):
        x,y = point

        x1 = (x-self.base_grid.min_x) * self._font_config.char_width
        y1 = (y-self.base_grid.min_y) * self._font_config.char_height
        p1 = (x1,y1)

        x2 = x1 + self._font_config.char_width - 1
        y2 = y1 + self._font_config.char_height - 1
        p2 = (x2,y2)
    
        self._canvas.rectangle((p1,p2), fill=color)
    

    def _draw_value(self, point, value, color):
        if value == None:
            value = ""

        x,y = point
        draw_x = (x-self.base_grid.min_x) * self._font_config.char_width  + self._font_config.x_offset
        draw_y = (y-self.base_grid.min_y) * self._font_config.char_height + self._font_config.y_offset
        self._canvas.text((draw_x, draw_y), str(value), font=self._font, fill=color)

  