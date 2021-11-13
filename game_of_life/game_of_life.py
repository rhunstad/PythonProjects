from tkinter import *
import numpy as np
import time
import sys

width = 1000
height = 850
canvas_buffer = 10
board_dim = height - canvas_buffer*4
ratio = 5
speed = .1
num_rows = 10
num_cols = num_rows
items = []
tiles = []
buttons = {}
buttons_temp = {}
instruction_items = []
is_instructions = False
selecting_tiles = True
paused = True
pause_text = ""
pause_button = ""
base_color = "#87dbff"

root = Tk()
root.title("Conway's Game of Life")
root.geometry('%sx%s' % (width, height))
canvas = Canvas(root, width=width, height=height, highlightthickness=0)
canvas.pack()
matrix = np.zeros(shape=(num_rows, num_cols), dtype='int')
base_tile = board_dim / num_rows
tile_size = max(round(((ratio-1)/ratio)*base_tile), round(((ratio-1)/ratio)*base_tile) - 1)
tile_buffer = max(round(((1)/ratio)*base_tile), 1)
board_dim = round(tile_size*num_rows + tile_buffer*(num_rows+1))
board_x = canvas_buffer
board_y = canvas_buffer


## COLOR PALETTE: ## 
# color = {
#     'big_canvas_fill': ['#a5e6c1', (0, 0, 0), (0, 0, 0)],
#     'big_canvas_out': ['#c7ffdf', (0, 0, 0), (-34, -25, -30)],
#     'control_panel_fill': ['#74c485', (0, 0, 0), (49, 34, 60)],
#     'control_panel_out': ['#74c485', (0, 0, 0), (49, 34, 60)],
#     'title_text_color': ['#007519', (0, 0, 0), (165, 113, 168)],
#     'text_color': ['#ffffff', (0, 0, 0), (-90, -25, -62)],
#     'text_color_active': ['#7affb4', (0, 0, 0), (43, -25, 13)],
#     'button_fill': ['#7affb4', (0, 0, 0), (43, -25, 13)],
#     'button_active': ['#ffffff', (0, 0, 0), (-90, -25, -62)],
#     'button_out': ['#7affb4', (0, 0, 0), (43, -25, 13)],
#     'rectangle_on': ['#74c485', (0, 0, 0), (49, 34, 60)],
#     'rectangle_off': ['#ffffff', (0, 0, 0), (-90, -25, -62)]
# }


color = {
    'big_canvas_fill': ['#a5e6c1', (0, 0, 0), (0, 0, 0)],
    'big_canvas_out': ['#c7ffdf', (0, 0, 0), (-30, -30, -30)],
    'control_panel_fill': ['#74c485', (0, 0, 0), (47, 47, 47)],
    'control_panel_out': ['#74c485', (0, 0, 0), (47, 47, 47)],
    'title_text_color': ['#007519', (0, 0, 0), (100, 100, 100)],
    'text_color': ['#ffffff', (0, 0, 0), (-59, -59, -59)],
    'text_color_active': ['#7affb4', (0, 0, 0), (10, 10, 10)],
    'button_fill': ['#7affb4', (0, 0, 0), (10, 10, 10)],
    'button_active': ['#ffffff', (0, 0, 0), (-59, -59, -59)],
    'button_out': ['#7affb4', (0, 0, 0), (10, 10, 10)],
    'rectangle_on': ['#74c485', (0, 0, 0), (47, 47, 47)],
    'rectangle_off': ['#ffffff', (0, 0, 0), (-59, -59, -59)]
}



def main(): 
    on_load()
    canvas.bind("<Button-1>", event_handler)
    root.protocol("WM_DELETE_WINDOW", exit_game)
    root.mainloop()


def game():
    global matrix
    
    B = np.zeros(shape=(matrix.shape[0], matrix.shape[1]), dtype='int')

    for i in range(1, matrix.shape[0]-1):
        for j in range(1, matrix.shape[1]-1):
            if matrix[i, j] == 1:
                B[i, j] = int(live(i, j))
            else:
                B[i, j] = int(dead(i, j))
                
    if bool(B[:,0].sum() + B[:,B.shape[1]-1].sum() + B[0,:].sum() + B[B.shape[0]-1,:].sum()):
        B = expand(B)
    
    changed = True
    if np.array_equal(matrix, B):
        changed = False
    
    matrix = B
    update_board()
    
    return changed


def dead(i, j):
    total = 0
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            total += matrix[x, y]
    
    if total == 3:
        return True
    else:
        return False

    
def live(i, j):
    total = 0
    for x in range(i-1, i+2):
        for y in range(j-1, j+2):
            total += matrix[x, y]
    
    if (total == 3) or (total == 4):
        return True
    else:
        return False
    

def expand(M):
    M = np.insert(M, 0, 0, axis=1)
    M = np.insert(M, M.shape[1], 0, axis=1)
    M = np.insert(M, 0, 0, axis=0)
    M = np.insert(M, M.shape[0], 0, axis=0)
    return M


def update_board():
    global num_cols
    global num_rows
    global tile_size
    global tile_buffer
    global tiles
    
    for i in range(num_rows):
        for j in range(num_cols):
            tiles[i][j].rect.destroy()
    
    tiles = []
    
    num_rows = matrix.shape[0]
    num_cols = matrix.shape[1]
    
    tile_size = max(round(board_dim/num_rows * (ratio-1)/ratio), round(board_dim/num_rows - 5))
    tile_buffer = min(round(board_dim/num_rows/ratio), 5)
    
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            row.append(Tile(bool(matrix[i,j]), i, j))
        tiles.append(row)
    

def on_load():
    global tiles
    global buttons
    global items
    tiles = []
    buttons = {}
    items = []
    get_color_palette(base_color)
    big_canvas()
    control_panel()
    board_setup()


def big_canvas():
    x_pos = board_x - 5
    y_pos = board_y - 5
    x = x_pos + board_dim + 5
    y = y_pos + board_dim + 5
    r = 10
    Shape(x=x, y=y, r=r, x_pos=x_pos, y_pos=y_pos, fill=color['big_canvas_fill'][0], outline=color['big_canvas_out'][0])


def control_panel():
    global pause_text
    global pause_button
    global buttons
    
    x = 128
    y = 600
    x_pos = board_dim + canvas_buffer*3
    y_pos = (height - y)/2 + canvas_buffer
    r = 10
    Shape(x=x, y=y, r=r, x_pos=x_pos, y_pos=y_pos, fill=color['control_panel_fill'][0], outline=color['control_panel_out'][0])

    font = ("Helvetica", 24)
    fill = color['title_text_color'][0]
    text = "Conway's \nGame of \nLife"
    x_text = round(x_pos + x/2)
    y_text = round(canvas_buffer + (board_dim - y)/4)
    Text(text, x_text, y_text, font=font, fill=fill)
    buttons['change_color'] = [[x_text - 40, 80], [y_text - 20, 40]]
    
    inside_buffer = 10
    side = 108
    
    y_pos=y_pos + inside_buffer
    x_pos = x_pos + inside_buffer 
    pause_button = Shape(x=side, y=side, r=r, x_pos=x_pos, y_pos=y_pos, fill=color['button_fill'][0], outline=color['button_out'][0])
    pause_button = [pause_button, side, x_pos, y_pos]
    
    pause_text = Text('Play', x_pos+side/2, y_pos+side/2, fill=color['text_color'][0])
    pause_text = [pause_text, x_pos+side/2, y_pos+side/2]
    buttons['play_pause'] = [[x_pos, side], [y_pos, side]]
    
    y_pos = y_pos + inside_buffer + side
    sh = Shape(x=side, y=side, r=r, x_pos=x_pos, y_pos=y_pos, fill=color['button_fill'][0], outline=color['button_out'][0])
    Text('+', x_pos+side/2, y_pos+side/2, fill=color['text_color'][0], font="Arial 60")
    buttons['inc_speed'] = [[x_pos, side], [y_pos, side], sh.square]
    
    y_pos = y_pos + inside_buffer + side
    sh = Shape(x=side, y=side, r=r, x_pos=x_pos, y_pos=y_pos, fill=color['button_fill'][0], outline=color['button_out'][0])
    Text('-', x_pos+side/2, y_pos+side/2, fill=color['text_color'][0], font="Arial 60")
    buttons['dec_speed'] = [[x_pos, side], [y_pos, side], sh.square]
    
    y_pos = y_pos + inside_buffer + side
    sh = Shape(x=side, y=side, r=r, x_pos=x_pos, y_pos=y_pos, fill=color['button_fill'][0], outline=color['button_out'][0])
    Text('X', x_pos+side/2, y_pos+side/2, fill=color['text_color'][0])
    buttons['stop_reset'] = [[x_pos, side], [y_pos, side], sh.square]
    
    y_pos = y_pos + inside_buffer + side
    sh = Shape(x=side, y=side, r=r, x_pos=x_pos, y_pos=y_pos, fill=color['button_fill'][0], outline=color['button_out'][0])
    Text('?', x_pos+side/2, y_pos+side/2, fill=color['text_color'][0])
    buttons['instructions'] = [[x_pos, side], [y_pos, side], sh.square]
    

def board_setup():
    global tiles
    global matrix
    
    resume_game()
    if matrix.shape[0] != num_rows or matrix.shape[1] != num_cols:
        matrix = np.zeros(shape=(num_rows, num_cols), dtype='int')
    
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            row.append(Tile(bool(matrix[i,j]), i, j))
        tiles.append(row)


def play_pause():
    if not paused:
        pause()
    else:
        play()


def play():
    global paused
    global selecting_tiles
    global pause_text
    global pause_button
    
    paused = False
    selecting_tiles = False
    x_pos = pause_text[1]
    y_pos = pause_text[2]
    
    canvas.delete(pause_button[0].square)
    pause_button[0] = Shape(x=pause_button[1], y=pause_button[1], r=10, x_pos=pause_button[2], y_pos=pause_button[3], fill=color['button_active'][0], outline=color['button_out'][0])
    
    pause_text[0].destroy()
    pause_text = Text('Pause', x_pos, y_pos, fill=color['text_color_active'][0])
    pause_text = [pause_text, x_pos, y_pos]
    changed = True
    
    while not paused and changed:
        changed = game()
        canvas.update()
        time.sleep(speed)

    canvas.delete(pause_button[0].square)
    pause_button[0] = Shape(x=pause_button[1], y=pause_button[1], r=10, x_pos=pause_button[2], y_pos=pause_button[3], fill=color['button_fill'][0], outline=color['button_out'][0])
    
    pause_text[0].destroy()
    pause_text = Text('Play', x_pos, y_pos, fill=color['text_color'][0])
    pause_text = [pause_text, x_pos, y_pos]
    paused = True
    selecting_tiles = True


def pause():
    global paused
    global selecting_tiles
    global pause_text
    paused = True
    selecting_tiles = True
    x_pos = pause_text[1]
    y_pos = pause_text[2]
    pause_text[0].destroy()
    pause_text = Text('Play', x_pos, y_pos, fill=color['text_color'][0])
    pause_text = [pause_text, x_pos, y_pos]


def inc_speed():
    global speed
    speed -= .01
    speed = max(0, speed)


def dec_speed():
    global speed
    speed += .01


def stop_reset():
    global tiles
    global matrix
    
    pause()
    matrix = np.zeros(shape=(num_rows, num_cols), dtype='int')
    for i in range(num_rows):
        row = []
        for j in range(num_cols):
            tiles[i][j].rect.destroy()
            row.append(Tile(bool(matrix[i,j]), i, j))
        tiles.append(row)
    canvas.update()
    
    
def change_color():
    global buttons_temp
    global instruction_items
    global is_instructions
    
    is_instructions = True
    
    box_width = 500
    box_height = 700
    x_pos = (width - box_width)/2
    y_pos = (height - box_height)/2
    item = Shape(x=box_width, y=box_height, r=10, x_pos=x_pos, y_pos=y_pos, fill=color['control_panel_fill'][0], outline=color['big_canvas_out'][0])
    instruction_items.append(item.square)
    
    button_height = 50
    button_width = 200
    button_y = y_pos + box_height - 20 - button_height
    button_x = x_pos + (box_width - button_width)/2
    item = Shape(x=button_width, y=button_height, r=10, x_pos=button_x, y_pos=button_y, fill=color['button_fill'][0], outline=color['button_out'][0])
    buttons_temp['exit_instructions'] = [[button_x, button_width], [button_y, button_height]]
    instruction_items.append(item.square)
    
    x = x_pos + box_width/2
    y = y_pos + 50
    string = "Instructions"
    item = canvas.create_text(x, y, fill=color['text_color'][0], font="Arial 40", text=string, anchor='center')
    instruction_items.append(item)
    
    x = button_x + button_width/2
    y = button_y + button_height/2
    string = "Cool!"
    item = canvas.create_text(x, y, fill=color['text_color'][0], font="Arial 40", text=string, anchor='center')
    instruction_items.append(item)
    
    x = x_pos + 10
    y = y_pos + 75
    string = """
    Conway's world lives by only a few 
    simple rules. If an 'alive' cell 
    has 2 or 3 neighbors, it lives on 
    to the next day. If fewer, it dies 
    by malnourishment. If more, it dies 
    by overpopulation. If a 'dead' cell 
    has exactly 2 neighbors, it becomes 
    'alive' by reproduction. 
    
    To play, click any sqaures in the 
    grid to bring them to life, to 
    create your starting conditions. Then, 
    click the 'Play' button to simulate 
    50 nights in the world. Click + to
    speed it up, - to slow it down, and X
    to clear the board. 
    
    See what cool patterns you can make!"""
    item = canvas.create_text(x, y, fill=color['text_color'][0], font="Arial 24", text=string, anchor='nw')
    instruction_items.append(item)
        


def instructions():
    global buttons_temp
    global instruction_items
    global is_instructions
    
    is_instructions = True
    
    box_width = 500
    box_height = 700
    x_pos = (width - box_width)/2
    y_pos = (height - box_height)/2
    item = Shape(x=box_width, y=box_height, r=10, x_pos=x_pos, y_pos=y_pos, fill=color['control_panel_fill'][0], outline=color['big_canvas_out'][0])
    instruction_items.append(item.square)
    
    button_height = 50
    button_width = 200
    button_y = y_pos + box_height - 20 - button_height
    button_x = x_pos + (box_width - button_width)/2
    item = Shape(x=button_width, y=button_height, r=10, x_pos=button_x, y_pos=button_y, fill=color['button_fill'][0], outline=color['button_out'][0])
    buttons_temp['exit_instructions'] = [[button_x, button_width], [button_y, button_height]]
    instruction_items.append(item.square)
    
    x = x_pos + box_width/2
    y = y_pos + 50
    string = "Instructions"
    item = canvas.create_text(x, y, fill=color['text_color'][0], font="Arial 40", text=string, anchor='center')
    instruction_items.append(item)
    
    x = button_x + button_width/2
    y = button_y + button_height/2
    string = "Cool!"
    item = canvas.create_text(x, y, fill=color['text_color'][0], font="Arial 40", text=string, anchor='center')
    instruction_items.append(item)
    
    x = x_pos + 10
    y = y_pos + 75
    string = """
    Conway's world lives by only a few 
    simple rules. If an 'alive' cell 
    has 2 or 3 neighbors, it lives on 
    to the next day. If fewer, it dies 
    by malnourishment. If more, it dies 
    by overpopulation. If a 'dead' cell 
    has exactly 2 neighbors, it becomes 
    'alive' by reproduction. 
    
    To play, click any sqaures in the 
    grid to bring them to life, to 
    create your starting conditions. Then, 
    click the 'Play' button to simulate 
    50 nights in the world. Click + to
    speed it up, - to slow it down, and X
    to clear the board. 
    
    See what cool patterns you can make!"""
    item = canvas.create_text(x, y, fill=color['text_color'][0], font="Arial 24", text=string, anchor='nw')
    instruction_items.append(item)


def exit_instructions():
    global is_instructions
    is_instructions = False
    
    for item in instruction_items:
        canvas.delete(item)


def exit_game():
    f = open('/Users/rylandhunstad/Desktop/Projects/python/game_of_life/game.npy', 'wb')
    np.save(f, matrix, allow_pickle=False)
    f.close()
    root.destroy()
    sys.exit()
    pass


def resume_game():
    global matrix
    f = open('/Users/rylandhunstad/Desktop/Projects/python/game_of_life/game.npy', 'rb')
    matrix = np.load(f, allow_pickle=False)
    f.close()


def event_handler(event):
    
    x = event.x
    y = event.y
    if not is_instructions: 
           
        for func, coords in buttons.items(): 
            if (coords[0][0] <= x <= coords[0][0] + coords[0][1]) & (coords[1][0] <= y <= coords[1][0] + coords[1][1]):
                eval(func + '()')
        
        if selecting_tiles:
            for i in range(num_rows):
                for j in range(num_cols):
                    x_pos = board_x + (tile_buffer*(j+1)) + (tile_size*j)
                    y_pos = board_y + (tile_buffer*(i+1)) + (tile_size*i)
                    if (x_pos <= x <= x_pos+tile_size) & (y_pos <= y <= y_pos+tile_size):
                        val = not tiles[i][j].value
                        tiles[i][j].rect.destroy()
                        tiles[i][j] = Tile(val, i, j)
                        matrix[i, j] = int(val)
    else:
        for func, coords in buttons_temp.items(): 
            if (coords[0][0] <= x <= coords[0][0] + coords[0][1]) & (coords[1][0] <= y <= coords[1][0] + coords[1][1]):
                eval(func + '()')


def minus(t1, t2):
    t = [0,0,0]
    for i in range(3):
        t[i] = min(max(t1[i] - t2[i], 0), 255)
    return tuple(t)


def get_color_palette(base):
    global color
    base = to_rgb(base)

    for item, value in color.items():
        rgb_col = minus(base, value[2])
        hex_col = to_hex(rgb_col)
        value[0] = hex_col
        value[1] = rgb_col
        color[item] = value

        
def to_rgb(hex_color):
    hex_color = hex_color.replace("#", "")
    return tuple([int(hex_color[i:i+2], 16) for i in range(0, len(hex_color), 2)])


def to_hex(rgb_color):
    return "#" + "".join([hex(j).replace("0x", "") + "0"*(2-len(hex(j).replace("0x", ""))) for j in rgb_color])


class Tile(object):
    def __init__(self, value, row, col):
        self.row = row
        self.col = col
        self.value = value
        self.rect = Rectangle(tile=self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
    
    def change(self):
        self.__value = not self.__value
        
        if self.__value:
            self.rect.square.fill, self.rect.square.outline = color['rectangle_on'][0], color['rectangle_on'][0]
        else:
            self.rect.square.fill, self.rect.square.outline = color['rectangle_off'][0], color['rectangle_off'][0]




class Shape(object):
    def __init__(self, x, y, r, x_pos, y_pos, fill, outline):
        global items
        self.x = x
        self.y = y
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.r = r
        self.fill = fill
        self.outline = outline
        
        self.points = self.get_points()
        
        self.square = canvas.create_polygon(self.points, smooth=True, fill=self.fill, outline=self.outline)
        canvas.move(self.square, x_pos, y_pos)
        items.append(self.square)


    def get_points(self):
        x1, y1 = 0, 0
        x2, y2 = self.x, self.y
        radius = self.r
        points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
                  x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius,
                  y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
        return points
    
    
    def destroy(self):
        global items
        # items.pop(items.index(self.square))
        canvas.delete(self.square)
    
    def recreate(self):
        global items
        self.square = canvas.create_polygon(self.points, smooth=True, fill=self.fill, outline=self.outline)
        canvas.move(self.square, self.x_pos, self.y_pos)
        items.append(self.square)
        



class Rectangle(object):
    def __init__(self, tile):
        global items
        self.tile = tile
        
        x1, y1 = 0, 0
        x2, y2 = tile_size, tile_size

        x_pos = board_x + (tile_buffer*(self.tile.col+1)) + (tile_size*self.tile.col)
        y_pos = board_y + (tile_buffer*(self.tile.row+1)) + (tile_size*self.tile.row)
        
        if self.tile.value:
            self.fill = color['rectangle_on'][0]
        else:
            self.fill = color['rectangle_off'][0]
        
        self.square = canvas.create_rectangle(x1, y1, x2, y2, fill=self.fill, outline=self.fill)
        canvas.move(self.square, x_pos, y_pos)
        items.append(self.square)


    def destroy(self):
        global canvas
        global items
        # items.pop(items.index(self.square))
        canvas.delete(self.square)
    
    
    def recreate(self):
        global items
        
        x1, y1 = 0, 0
        x2, y2 = tile_size, tile_size

        x_pos = board_x + (tile_buffer*(self.tile.col+1)) + (self.tile_size*self.tile.col)
        y_pos = board_y + (tile_buffer*(self.tile.row+1)) + (self.tile_size*self.tile.row)
        
        if self.tile.value:
            self.fill = color['rectangle_on'][0]
        else:
            self.fill = color['rectangle_off'][0]
        
        self.square = canvas.create_rectangle(x1, y1, x2, y2, fill=self.fill, outline=self.fill)
        canvas.move(self.square, x_pos, y_pos)
        items.append(self.square)



class Text(object):
    def __init__(self, string, x, y, **kwargs):
        global items
        
        self.font = 'Arial 36'
        self.fill = '#FAFFFF'
        self.x = x
        self.y = y
        self.string = string
        self.anchor = 'center'
        
        if 'font' in kwargs.keys(): 
            self.font = kwargs['font']
    
        if 'fill' in kwargs.keys(): 
            self.fill = kwargs['fill']
            
        if 'anchor' in kwargs.keys(): 
            self.anchor = kwargs['anchor']

        
        self.text = canvas.create_text(self.x, self.y, fill=self.fill, font=self.font, text=self.string, anchor=self.anchor)
        items.append(self.text)
        

    def destroy(self):
        global items
        # items.pop(items.index(self.text))
        canvas.delete(self.text)
    
    
    def recreate(self):
        self.text = canvas.create_text(self.x, self.y, fill=self.fill, font=self.font, text=self.string, anchor=self.anchor)
        items.append(self.text)


main()