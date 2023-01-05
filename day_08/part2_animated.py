from typing import Any, List
from util import read_lines
from grid import ArrayGrid, RenderGrid
from video_generator import VideoGenerator
import colors
from colors import Color

OUTPUT_VIDEO = "day_08/video_part2.mp4"

GREEN_HIGHLIGHT = Color( 10,100, 10)
DARK_GREEN      = Color(  0, 50,  0)
LIGHT_GREEN     = Color( 30,250,130)

def background_color_gradiant(_, value):

    level_9_color = DARK_GREEN
    level_8_color = colors.offset(level_9_color, 25)
    
    if value == 9: return colors.offset(level_9_color, 100), level_9_color
    if value == 8: return colors.offset(level_8_color, 100), level_8_color
    
    c = colors.offset(colors.WHITE, value*-10)
    return colors.offset(c, -50), c
  

def get_input() -> RenderGrid:
    rows = []
    for line in read_lines("day_08/input.txt"):
        rows.append([int(t) for t in line])
    return RenderGrid(data_grid=ArrayGrid(rows), cell_color_func=background_color_gradiant)
    

def scenic_score(tree, forest, background_color=None):

    forest.set_color(tree, fg=GREEN_HIGHLIGHT, bg=LIGHT_GREEN)
    tree_height = forest[tree]
    distances = []
    for dx, dy in ((0,1), (0,-1), (1,0), (-1,0)):
        x,y = tree
        visible_trees = 0
        blocked = False
        while not blocked:
            x,y = x+dx, y+dy
            if not forest.base_grid.valid_point((x,y)):
                blocked = True
            else:
                visible_trees += 1
                next_height = forest[(x,y)]
                blocked = next_height >= tree_height

                if blocked:
                    forest.set_color((x,y), fg=colors.RED, bg=colors.DARK_RED)
                else:
                    forest.set_color((x,y), fg=LIGHT_GREEN, bg=background_color)
                      
        distances.append(visible_trees)

    return distances[0] * distances[1] * distances[2] * distances[3]
                          
def run()->int:
    forest_grid = get_input()
    with VideoGenerator(OUTPUT_VIDEO, live_preview=True, subsample=10) as video_generator:
        video_generator.append_image(forest_grid.image)

        best_score = 0
        for tree in forest_grid.points():
            with forest_grid.image_state():
                score = scenic_score(tree, forest_grid)
                video_generator.append_image(forest_grid.image)
    
            if score > best_score:  
                if best_score > 0:
                    forest_grid.pop_image_state()

                # update the state of the grid to show the new best view
                forest_grid.push_image_state()
                scenic_score(tree, forest_grid, background_color=GREEN_HIGHLIGHT)
                video_generator.append_image(forest_grid.image)
        
                best_score = score

    return best_score
