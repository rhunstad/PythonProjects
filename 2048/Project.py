from tkinter import *
from random import randint
import time
from datetime import datetime, date
import sys

root = Tk()
root.title('2048')
width = 500
height = 800
root.geometry('%sx%s' % (width, height))
canvas = Canvas(root, width=width, height=height, highlightthickness=0)
canvas.pack()
tile_size = 75
tile_buffer = 10
radius = 10
board_dim = (5*tile_buffer) + (4*tile_size)
board_top = 50
board_x = (width-board_dim)/2
board_y = ((height-board_dim)/2)+board_top
big_grey_x = board_x
big_grey_y = board_y
level = 'easy'
score = 0
items = ()
best_x = width - board_x - 80
best_y = big_grey_y - 150
score_x = width - board_x - 160 - 10
score_y = big_grey_y - 150
menu_x = width - board_x - 160 - 10
menu_y = big_grey_y - 50
leader_x = width - board_x - 80
leader_y = big_grey_y - 50
tiles = None
score_text = None
best_score_text = None
game_over = False
real_game_over = False
AI = False
AIMove = False
AIMoveValue = 0
paused = False
graphics = True
user = 'username'


def main():
    global tiles
    setup()
    root.mainloop()


def game(shift):
    global game_over
    global tiles
    badmove = check(shift)
    if not badmove:
        tiles = move(shift, True)
        random()
        game_over = check(0)


def AI_game():
    canvas.unbind('<Key>')
    canvas.unbind('<Button-1>')
    global real_game_over
    global game_over
    global tiles
    global paused
    shifts = ['up', 'down', 'left', 'right']
    delete_menu()
    while not real_game_over & paused:
        shift = shifts[randint(0, 3)]
        badmove = check(shift)
        if not badmove:
            tiles = move(shift, True)
            random()
            game_over = check(0)
            canvas.update()
    global AI
    global AIMove
    end_menu()
    AIMove = False
    canvas.bind('<Key>', keyed)
    canvas.bind("<Button-1>", end_screen)


def AI_assess():
    shift = "up"
    max_move = 0
    global AIMove
    global AIMoveValue
    AIMoveValue = 0
    AIMove = True

    move("up", False)
    up_val = AIMoveValue
    if up_val > max_move:
        shift = 'up'
    AIMoveValue = 0

    move("left", False)
    left_val = AIMoveValue
    AIMoveValue = 0
    if up_val > max_move:
        shift = 'left'
    AIMoveValue = 0

    move("down", False)
    down_val = AIMoveValue
    AIMoveValue = 0
    if up_val > max_move:
        shift = 'down'
    AIMoveValue = 0

    move("right", False)
    right_val = AIMoveValue
    AIMoveValue = 0
    if up_val > max_move:
        shift = 'right'
    AIMoveValue = 0

    AIMove = False
    if max_move == 0:
        shift = 0
    return shift


def keyed(event):
    global tiles
    global game_over
    global paused
    if (not real_game_over) & (not paused):
        paused = True

        r = repr(event.char)
        lett = str("".join(list(r)))
        uparrow = str("".join(["'", '\\', 'u', 'f', '7', '0', '0', "'"]))
        downarrow = str("".join(["'", '\\', 'u', 'f', '7', '0', '1', "'"]))
        leftarrow = str("".join(["'", '\\', 'u', 'f', '7', '0', '2', "'"]))
        rightarrow = str("".join(["'", '\\', 'u', 'f', '7', '0', '3', "'"]))

        print(lett, downarrow, lett==downarrow)
        shift = ""
        if lett == uparrow:
            shift = 'up'
            game(shift)
        elif lett == downarrow:
            shift = 'down'
            print(shift)
            game(shift)
        elif lett == leftarrow:
            shift = 'left'
            game(shift)
        elif lett == rightarrow:
            shift = 'right'
            game(shift)
        else:
             None
        paused = False
    elif real_game_over:
        end_menu()
        canvas.bind("<Button-1>", end_screen)
    else:
        None


def random():
    global tiles
    num = 0
    empty_tiles = ([])
    for r in range(4):
        for c in range(4):
            if tiles[r][c].empty:
                pos = [r, c]
                empty_tiles += [pos]

    if level == 'easy':
        while num == 0:
            num = 2*abs(randint(-1, 2))
    else:
        while num == 0:
            num = 2*randint(-1, 2)

    try:
        t = randint(0, len(empty_tiles)-1)
    except ValueError:
        return
    rand_tile = empty_tiles[t]
    r = rand_tile[0]
    c = rand_tile[1]
    tiles[r][c].newval(num)

    dif = 6
    x = board_x + (tile_buffer * (c + 1)) + (tile_size * c) - dif/2
    y = board_y + (tile_buffer * (r + 1)) + (tile_size * r) - dif/2

    points = get_points(tile_size+dif, tile_size+dif)
    half = (tile_size + dif)/2
    style = Rectangle.rect_style(num)
    text_style = Text.text_style(num)

    time.sleep(.02)
    pop_tile = canvas.create_polygon(points, smooth=True, fill=style[0], outline=style[1])
    canvas.move(pop_tile, x, y)
    pop_text = canvas.create_text(x + half, y + half, fill=text_style[1], font=text_style[0], text=str(num), anchor='center')
    canvas.update()
    time.sleep(.05)
    canvas.delete(pop_tile)
    canvas.delete(pop_text)
    return tiles


def check(n):
    global tiles
    global game_over
    global real_game_over
    game_over = True
    if n == 0:
        move('up', False)
        move('down', False)
        move('left', False)
        move('right', False)
        if game_over:
            real_game_over = True
    elif n == 'left':
        move('left', False)
    elif n == 'right':
        move('right', False)
    elif n == 'up':
        move('up', False)
    elif n == 'down':
        move('down', False)
    return game_over


def move(shift, live):
    global tiles
    start = 0
    inc = 1
    print(shift)
    if (shift == 'down') | (shift == 'right'):
        start = 3
        inc = -1

    if (shift == 'up') | (shift == 'down'):
        # COLUMNS ARE FIXED, ROWS VARIABLE
        for r in range(0, 4, 1):
            columns = ([])
            columns += [tiles[start][r]]
            columns += [tiles[start+inc][r]]
            columns += [tiles[start+2*inc][r]]
            columns += [tiles[start+3*inc][r]]
            tiles = game_engine(columns, live)

    else:
        for c in range(0, 4, 1):
            rows = ([])
            rows += [tiles[c][start]]
            rows += [tiles[c][start+inc]]
            rows += [tiles[c][start+2*inc]]
            rows += [tiles[c][start+3*inc]]
            tiles = game_engine(rows, live)
    return tiles


def game_engine(group, live):
    global tiles
    global AI
    global AIMove
    global graphics
    old_group = group[:]
    global score
    points = 0
    global game_over

    for i in range(len(group)-1):
        for j in range(i+1, len(group)):
            order = True
            if j-1 > i:
                for k in range(i+1, j):
                    if group[k].value != 0:
                        order = False
            if order:
                if abs(group[i].value) == abs(group[j].value):
                    if group[i].value != 0:
                        if group[i].value == old_group[i].value:
                            if not live:
                                game_over = False
                                return tiles
                            points += group[i].value + group[j].value
                            if graphics:
                                Move(group[j], group[i], True)
                            group[i].value = group[i].value+group[j].value
                            group[j].value = 0
                            if i <= len(group)-2:
                                i += 1
    filled = 0
    for i in range(len(group)):
        if group[i].value != 0:
            if live:
                group[filled].value = group[i].value
            if filled != i:
                if not live:
                    game_over = False
                    return tiles
                if graphics:
                    Move(group[i], group[filled], True)
                group[i].value = 0

            filled += 1
    if AI & AIMove:
        global AIMoveValue
        AIMoveValue = score+points
        return tiles
    set_score(score + points)

    for member in group:
        tiles[member.row][member.col].newval(member.value)
    return tiles


def main_screen(event):
    global paused
    x = event.x
    y = event.y
    # Menu button:
    if (menu_x < x < (menu_x+80)) & (menu_y < y < (menu_y+30)):
        canvas.bind("<Button-1>", side_screen)
        side_menu()
    # Leader-board button (put coordinates):
    elif (leader_x < x < (leader_x+80)) & (leader_y < y < (leader_y+30)):
        canvas.bind("<Button-1>", leader_screen)
        leader_menu()
    
    
def side_screen(event):
    global tiles
    global paused

    x = event.x
    y = event.y
    x1 = width/2 - 60
    y1 = 150
    y2 = 250
    y3 = 350
    y4 = 450
    y5 = 550
    if (x1 < x < (x1+120)) & (y1 < y < (y1+40)):
        delete_menu()
        paused = False
        canvas.bind("<Button-1>", main_screen)
    elif (x1 < x < (x1 + 120)) & (y2 < y < (y2 + 40)):
        tiles = new_game_board()
        delete_menu()
        paused = False
        canvas.bind("<Button-1>", main_screen)
    elif (x1 < x < (x1 + 120)) & (y3 < y < (y3 + 40)):
        global level
        if level == 'easy':
            level = 'hard'
        else:
            level = 'easy'
        delete_menu()
        paused = False
        canvas.bind("<Button-1>", main_screen)
    elif (x1 < x < (x1 + 120)) & (y4 < y < (y4 + 40)):
        global AI
        global real_game_over
        AI = True
        delete_menu()
        paused = True
        canvas.bind("<Button-1>", main_screen)
        AI_game()
    elif (x1 < x < (x1 + 120)) & (y5 < y < (y5 + 40)):
        global graphics
        if graphics:
            graphics = False
        else:
            graphics = True
        delete_menu()
        paused = False
        canvas.bind("<Button-1>", main_screen)


def side_menu():
    global paused
    paused = True
    global items
    global level
    white = canvas.create_rectangle(0, 0, 1000, 1000, fill='white', outline='white')
    points = get_points(120, 40)
    x = width/2 - 60
    y = 150
    a_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(a_tile, x, y)
    a_text = canvas.create_text(x + 60, y + 20, fill='#FAFFFF', font='Arial 15', text='KEEP GOING', anchor='center')

    b_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(b_tile, x, y+100)
    b_text = canvas.create_text(x + 60, y + 120, fill='#FAFFFF', font='Arial 15', text='NEW GAME', anchor='center')
    items = (white, a_tile, a_text, b_tile, b_text)

    level_text = 'HARD'
    if level != 'easy':
        level_text = 'EASY'

    c_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(c_tile, x, y+200)
    c_text = canvas.create_text(x + 60, y + 220, fill='#FAFFFF', font='Arial 15', text='%s MODE' % level_text,
                                anchor='center')

    d_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(d_tile, x, y+300)
    d_text = canvas.create_text(x + 60, y + 320, fill='#FAFFFF', font='Arial 15', text='PLAY AS AI',
                                anchor='center')
    global graphics
    graphics_text = 'HIGH'
    if graphics:
        graphics_text = 'LOW'

    e_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(e_tile, x, y+400)
    e_text = canvas.create_text(x + 60, y + 420, fill='#FAFFFF', font='Arial 15', text='%s GRAPHICS' % graphics_text,
                                anchor='center')

    items = (white, a_tile, a_text, b_tile, b_text, c_text, c_tile, d_text, d_tile, e_tile, e_text)


def delete_menu():
    global items
    for item in items:
        canvas.delete(item)
    items = ()


def leader_screen(event):
    global paused
    x = event.x
    y = event.y
    x1 = width/2 - 60
    y1 = 200
    if (x1 < x < (x1+120)) & (y1 < y < (y1+40)):
        delete_menu()
        paused = False
        canvas.bind("<Button-1>", main_screen)


def leader_menu():
    global paused
    global items
    paused = True
    white = canvas.create_rectangle(0, 0, 1000, 1000, fill='white', outline='white')
    points = get_points(120, 40)
    x = width/2 - 60
    y = 200
    a_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(a_tile, x, y)
    a_text = canvas.create_text(x + 60, y + 20, fill='#FAFFFF', font='Arial 15', text='KEEP GOING', anchor='center')

    leaders = get_best(False)
    b_text = canvas.create_text(x-100, y + 20+60, fill='#776E65', font='Arial 18', text=leaders, anchor='nw')
    items = (white, a_tile, a_text, b_text)


def end_screen(event):
    global paused
    global user
    global AI
    global items
    global real_game_over
    global game_over
    x = event.x
    y = event.y
    x1 = width/2 - 60
    y1 = 200
    if (x1 < x < (x1+120)) & (y1 < y < (y1+40)):
        if AI:
            user = 'AI'
            AI = False
        else:
            user = str(items[0])
        f = open('scores.txt', 'a')
        f.write('%s#%s#%s\n' % (score, str(date.today()), user))
        f.close()
        best_score_num_text(get_best(True))
        paused = False
        real_game_over = False
        game_over = False
        delete_menu()
        new_game_board()
        canvas.focus_set()
        canvas.bind("<Button-1>", main_screen)


def end_menu():
    global paused
    global items
    global real_game_over
    global AI
    global user
    paused = True
    real_game_over = False
    white = canvas.create_rectangle(0, 0, 1000, 1000, fill='white', outline='white')
    points = get_points(120, 40)
    x = width/2 - 60
    y = 200
    a_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(a_tile, x, y)
    a_text = canvas.create_text(x + 60, y + 20, fill='#FAFFFF', font='Arial 15', text='NEW GAME', anchor='center')

    b_text = canvas.create_text(x, y - 100, fill='#776E65', font='Arial 20', text="Good game! Score: " + str(score),
                                anchor='w')
    user = 'username'
    if AI:
        user = 'AI'
    else:
        e = Entry(canvas)
        w = canvas.create_window(200, 200, window=e)
        canvas.move(w, x-105, y-50)
        e_text = canvas.create_text(x, y + 100, fill='#776E65', font='Arial 20', text="Enter username to save score: ",
                                    anchor='w')

    if AI:
        items = (white, a_tile, a_text, b_text)
    else:
        items = (e, w, white, e_text, a_tile, a_text, b_text)


def on_exit():
    global real_game_over
    out = "0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0"
    if not real_game_over:
        out = ""
        global tiles
        for r in range(4):
            for c in range(4):
                out += str(tiles[r][c].value) + ','
        global score
        out += str(score)
    f = open('resumegame.txt', 'w')
    f.write(out)
    f.close()
    sys.exit(0)


def resume_game():
    global paused
    e = open('resumegame.txt', 'r')
    f = e.read().rsplit(',')
    e.close()

    global score
    set_score(int(f[len(f)-1]))
    global best_score
    best_score = get_best(True)
    best_score_num_text(best_score)
    global tiles

    tiles = None
    a1 = Tile(value=int(f[0]), row=0, col=0)
    a2 = Tile(value=int(f[1]), row=0, col=1)
    a3 = Tile(value=int(f[2]), row=0, col=2)
    a4 = Tile(value=int(f[3]), row=0, col=3)
    b1 = Tile(value=int(f[4]), row=1, col=0)
    b2 = Tile(value=int(f[5]), row=1, col=1)
    b3 = Tile(value=int(f[6]), row=1, col=2)
    b4 = Tile(value=int(f[7]), row=1, col=3)
    c1 = Tile(value=int(f[8]), row=2, col=0)
    c2 = Tile(value=int(f[9]), row=2, col=1)
    c3 = Tile(value=int(f[10]), row=2, col=2)
    c4 = Tile(value=int(f[11]), row=2, col=3)
    d1 = Tile(value=int(f[12]), row=3, col=0)
    d2 = Tile(value=int(f[13]), row=3, col=1)
    d3 = Tile(value=int(f[14]), row=3, col=2)
    d4 = Tile(value=int(f[15]), row=3, col=3)
    tiles = ((a1, a2, a3, a4), (b1, b2, b3, b4), (c1, c2, c3, c4), (d1, d2, d3, d4))
    zero = True
    for r in range(4):
        for c in range(4):
            if tiles[r][c].value != 0:
                zero = False
            tiles[r][c].newval(tiles[r][c].value)
    if zero:
        random()


def set_score(new_score):
    global score
    score = new_score
    score_num_text()
  
    
def get_best(best):
    def func(line):
        val = int(line.rsplit('#')[0])
        return val

    f = open("scores.txt", 'r')
    scores = f.readlines()
    f.close()
    scores = sorted(scores, key=func, reverse=True)
    if best:
        return int(scores[0].rsplit('#')[0])
    else:
        out = ""
        records = 10
        if len(scores) < 10:
            records = len(scores)
        for i in range(records):
            ln = scores[i].rsplit('#')
            out += "%s\t%s\t%s\n" % (ln[0], ln[1], ln[2])
        return out


def setup():
    global best_score
    global tiles
    # Big grey:
    points = get_points(board_dim, board_dim)
    style = ('#BBADA0', '#B6A699')
    big_grey = canvas.create_polygon(points, smooth=True, fill='%s' % style[0], outline='%s' % style[1])
    canvas.move(big_grey, big_grey_x, big_grey_y)

    # Small Grey:
    points = get_points(tile_size, tile_size)
    style = ('#CEC0B5', '#BDAFA2')
    for c in range(4):
        for r in range(4):
            x_pos = board_x + (tile_buffer * (c + 1)) + (tile_size * c)
            y_pos = board_y + (tile_buffer * (r + 1)) + (tile_size * r)
            small_grey = canvas.create_polygon(points, smooth=True, fill='%s' % style[0], outline='%s' % style[1])
            canvas.move(small_grey, x_pos, y_pos)

    # 2048 logo tile:
    points = get_points(100, 100)
    x_2048 = big_grey_x
    y_2048 = big_grey_y - 150
    tile_2048 = canvas.create_polygon(points, smooth=True, fill='#EFC32C', outline='#D7BA64')
    canvas.move(tile_2048, x_2048, y_2048)
    # 2048 logo text:
    x = x_2048 + 50
    y = y_2048 + 50
    canvas.create_text(x, y, fill='#FAFFFF', font='Arial 36', text='2048', anchor='center')

    # Best Score Tile:
    points = get_points(80, 80)
    global best_x
    global best_y
    best_score_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(best_score_tile, best_x, best_y)
    best_score_num_text(best_score)

    # Score Tile:
    points = get_points(80, 80)
    global score_x
    global score_y
    score_tile = canvas.create_polygon(points, smooth=True, fill='#CEC0B5', outline='#BDAFA2')
    canvas.move(score_tile, score_x, score_y)
    score_num_text()

    # Menu tile:
    points = get_points(80, 30)
    global menu_y
    global menu_x
    score_tile = canvas.create_polygon(points, smooth=True, fill='#F57C5F', outline='#EA856B')
    canvas.move(score_tile, menu_x, menu_y)
    canvas.create_text(menu_x + 40, menu_y + 15, fill='#FAFFFF', font='Arial 15', text='MENU', anchor='center')

    # Leader-board tile:
    points = get_points(80, 30)
    global leader_y
    global leader_x
    score_tile = canvas.create_polygon(points, smooth=True, fill='#F57C5F', outline='#EA856B')
    canvas.move(score_tile, leader_x, leader_y)
    canvas.create_text(leader_x + 40, leader_y + 15, fill='#FAFFFF', font='Arial 9', text='LEADERBOARD',
                       anchor='center')

    canvas.create_text(best_x+40, best_y+80/4, fill='#EEE4D4', font='Arial 15', text='BEST',
                       anchor='center')
    canvas.create_text(score_x+40, score_y+80/4, fill='#EEE4D4', font='Arial 15', text='SCORE',
                       anchor='center')
    canvas.create_text(x_2048, y_2048 + 100 + 20, fill='#776E65', font='Arial 20',
                       text='Join the numbers!', anchor='w')
    resume_game()


def get_points(x, y):
    x1, y1 = 0, 0
    x2, y2 = x, y
    points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
              x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius,
              y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius, x1, y1 + radius, x1, y1]
    return points


def score_num_text():
    global score
    global best_score
    global score_text
    canvas.delete(score_text)
    style = Text.text_style(score)
    score_text = canvas.create_text(score_x + 40, score_y + 50, fill='#FAFFFF', font=style[0], text=str(score),
                                    anchor='center')
    if score >= best_score:
        best_score_num_text(score)


def best_score_num_text(num):
    global best_score_text
    canvas.delete(best_score_text)
    style = Text.text_style(num)
    best_score_text = canvas.create_text(best_x + 40, best_y + 50, fill='#FAFFFF', font=style[0], text=str(num),
                                    anchor='center')


def new_game_board():
    global level
    global score
    level = 'easy'
    score = 0
    score_num_text()
    global tiles
    if tiles:
        for r in range(4):
            for c in range(4):
                tiles[r][c].newval(0)
    tiles = None
    a1 = Tile(value=0, row=0, col=0)
    a2 = Tile(value=0, row=0, col=1)
    a3 = Tile(value=0, row=0, col=2)
    a4 = Tile(value=0, row=0, col=3)
    b1 = Tile(value=0, row=1, col=0)
    b2 = Tile(value=0, row=1, col=1)
    b3 = Tile(value=0, row=1, col=2)
    b4 = Tile(value=0, row=1, col=3)
    c1 = Tile(value=0, row=2, col=0)
    c2 = Tile(value=0, row=2, col=1)
    c3 = Tile(value=0, row=2, col=2)
    c4 = Tile(value=0, row=2, col=3)
    d1 = Tile(value=0, row=3, col=0)
    d2 = Tile(value=0, row=3, col=1)
    d3 = Tile(value=0, row=3, col=2)
    d4 = Tile(value=0, row=3, col=3)
    tiles = ((a1, a2, a3, a4), (b1, b2, b3, b4), (c1, c2, c3, c4), (d1, d2, d3, d4))
    out = "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"
    f = open('resumegame.txt', 'w')
    f.write(out)
    f.close()
    random()
    return tiles


class Tile(object):
    def __init__(self, value, row, col):
        self.empty = True
        self.row = row
        self.col = col
        self.value = value
        self.move = None
        self.rect = Rectangle(tile=self)
        self.text = Text(tile=self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, val):
        self.__value = val
        if self.__value != 0:
            self.empty = False
        else:
            self.empty = True

    def newval(self, val):
        self.value = val
        if val == 0:
            self.rect.destroy()
            self.text.destroy()
        else:
            self.rect.destroy()
            self.text.destroy()
            self.rect = Rectangle(tile=self)
            self.text = Text(tile=self)


class Move(object):
    def __init__(self, tile, dest, type):
        x1 = board_x + (tile_buffer*(tile.col+1)) + (tile_size*tile.col)
        y1 = board_y + (tile_buffer*(tile.row+1)) + (tile_size*tile.row)
        x2 = board_x + (tile_buffer*(dest.col+1)) + (tile_size*dest.col)
        y2 = board_y + (tile_buffer*(dest.row+1)) + (tile_size*dest.row)
        inc = 12
        x_dist = x2-x1
        y_dist = y2-y1
        x_step = x_dist/inc
        y_step = y_dist/inc

        canvas.lift(tile.rect.square)
        canvas.lift(tile.text.text)
        if x_dist > 0:
            while x_dist != 0:
                canvas.move(tile.rect.square, x_step, 0)
                canvas.move(tile.text.text, x_step, 0)
                canvas.update()
                x_dist -= x_step
                if x_dist < x_step:
                    x_step = x_dist
        elif y_dist > 0:
            while y_dist != 0:
                canvas.move(tile.rect.square, 0, y_step)
                canvas.move(tile.text.text, 0, y_step)
                canvas.update()
                y_dist -= y_step
                if y_dist < y_step:
                    y_step = y_dist
        elif x_dist < 0:
            x_dist = abs(x_dist)
            x_step = abs(x_step)
            while x_dist != 0:
                canvas.move(tile.rect.square, -x_step, 0)
                canvas.move(tile.text.text, -x_step, 0)
                canvas.update()
                x_dist -= x_step
                if x_dist < x_step:
                    x_step = x_dist
        elif y_dist < 0:
            y_dist = abs(y_dist)
            y_step = abs(y_step)
            while y_dist != 0:
                canvas.move(tile.rect.square, 0, -y_step)
                canvas.move(tile.text.text, 0, -y_step)
                canvas.update()
                y_dist -= y_step
                if y_dist < y_step:
                    y_step = y_dist


class Rectangle(object):
    def __init__(self, tile):
        x1, y1 = 0, 0
        x2, y2 = tile_size, tile_size
        self.points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
            x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius,
            y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius,x1, y1 + radius, x1, y1]

        style = Rectangle.rect_style(tile.value)
        x_pos = board_x + (tile_buffer*(tile.col+1)) + (tile_size*tile.col)
        y_pos = board_y + (tile_buffer*(tile.row+1)) + (tile_size*tile.row)
        self.square = \
            canvas.create_polygon(self.points, smooth=True, fill=style[0], outline=style[1])
        canvas.move(self.square, x_pos, y_pos)

    def destroy(self):
        canvas.delete(self.square)

    @staticmethod
    def rect_style(val):
        val = abs(val)
        if val == 0:
            return '#CEC0B5', '#BDAFA2'
        elif val == 2:
            return "#EDE4DA", "#D8CCC1"
        elif val == 4:
            return "#ECDFC8", "#D7C9B6"
        elif val == 8:
            return "#F3B178", "#DEAF89"
        elif val == 16:
            return "#F49663", "#CBA791"
        elif val == 32:
            return "#F57C5F", "#EA856B"
        elif val == 64:
            return "#F75D3B", "#D17D63"
        elif val == 128:
            return "#EDCF6D", "#DEC78D"
        elif val == 256:
            return "#EDCC63", "#EBCD75"
        elif val == 512:
            return "#ECC955", "#EBCF7B"
        elif val == 1024:
            return "#EEC440", "#E0BA61"
        elif val == 2048:
            return "#EFC32C", "#D7BA64"
        elif val == 4096:
            return "#ED666D", "#C87674"
        elif val == 8192:
            return "#ED4E59", "#C76365"
        elif val == 16384:
            return "#F04342", "#E69C91"
        elif val == 32768:
            return "#72B2D5", "#8FAFBB"
        elif val == 65536:
            return "#5D9BDF", "#87A4B5"
        elif val == 131072:
            return "#1781CB", "#3577A0"


class Text(object):
    def __init__(self, tile):
        style = Text.text_style(tile.value)
        self.font = style[0]
        self.fill = style[1]
        x = board_x + (tile_buffer*(tile.col+1)) + (tile_size*tile.col) + (tile_size/2)
        y = board_y + (tile_buffer*(tile.row+1)) + (tile_size*tile.row) + (tile_size/2)
        tiletext = tile.value
        if tile.value == 0:
            tiletext = ""
        self.text = canvas.create_text(x, y, fill=self.fill, font=self.font, text=tiletext, anchor='center')

    def destroy(self):
        canvas.delete(self.text)

    @staticmethod
    def text_style(val):
        # returns font&size, text_fill_color
        #     Dark Text hex-code: #776E65
        #     Light Text hex-code: #FAFFFF
        val = abs(val)
        if val < 5:
            return 'Arial 36', '#776E65'
        elif 5 <= val < 100:
            return 'Arial 36', '#FAFFFF'
        elif 100 <= val < 1000:
            return 'Arial 34', '#FAFFFF'
        elif 1000 <= val < 10000:
            return 'Arial 30', '#FAFFFF'
        elif 10000 <= val < 100000:
            return 'Arial 25', '#FAFFFF'
        else:
            return 'Arial 20', '#FAFFFF'


best_score = get_best(True)
canvas.focus_set()
canvas.bind("<Key>", keyed)
canvas.bind("<Button-1>", main_screen)
root.protocol("WM_DELETE_WINDOW", on_exit)


if __name__ == "__main__":
    main()
