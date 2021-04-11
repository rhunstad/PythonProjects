from tkinter import *


player = {
    True: ['#B1D3BB', 'X', 1],
    False: ['#E4B6B3', 'O', 2]}

tiles = {}
exes = {}

root = Tk()
root.title('Tic-Tac-Toe ')
width = 1000
height = 900
root.geometry('%sx%s' % (width, height))
canvas = Canvas(root, width=width, height=height, highlightthickness=0)
header = canvas.create_text(225, 30, fill='#13B2E9', font='Calibri 30', text="Player 1's turn",
                       anchor='center')
ones_turn = True
lost_trigger = 0

tile_size = 180
tile_buffer = 25
radius = 10


def main():
    setup()
    canvas.pack()
    root.mainloop()


def game(event):
    x = event.x
    y = event.y
    global tiles
    if (720 <= x <= 900) & (120 <= y <= 180):
        setup()
    for key, value in tiles.items():
        btn_x = value[0]
        btn_y = value[1]
        if (btn_x <= x <= (btn_x+tile_size)) & (btn_y <= y <= (btn_y+tile_size)):
            if exes.get(key) == 0:
                global lost_trigger
                if lost_trigger == 0:
                    choose(key, value)
                    is_lost()
                    if lost_trigger == 1:
                        global header
                        global ones_turn
                        canvas.delete(header)
                        player_num = player.get(not ones_turn)[2]
                        header = canvas.create_text(750/2, 30, fill='#000000', font='Calibri 40',
                            text="Player %s wins!" % player_num, anchor='center')


def is_lost():
    global exes
    global lost_trigger
    lost = False
    open_spot = False
    for r in range(3):
        for c in range(3):
            if exes.get((r, c)) == 0:
                open_spot = True

    if not open_spot:
        global header
        canvas.delete(header)
        header = canvas.create_text(750 / 2, 30, fill='#000000', font='Calibri 40',
                                    text="Cat's game!", anchor='center')
        lost_trigger = 2

    for i in range(3):
        if exes.get((i, 0)) == exes.get((i, 1)) == exes.get((i, 2)):
            if exes.get((i, 0)) != 0:
                lost = True
        if exes.get((0, i)) == exes.get((1, i)) == exes.get((2, i)):
            if exes.get((0, i)) != 0:
                lost = True

    if exes.get((0, 0)) == exes.get((1, 1)) == exes.get((2, 2)):
        if exes.get((1, 1)) != 0:
            lost = True
    elif exes.get((2, 0)) == exes.get((1, 1)) == exes.get((0, 2)):
        if exes.get((1, 1)) != 0:
            lost = True

    if lost:
        lost_trigger += 1



def setup():
    global tiles, exes, header, lost_trigger, ones_turn
    lost_trigger = 0
    ones_turn = True
    tiles = {}
    exes = {}
    canvas.delete(header)
    header = canvas.create_text(750/2, 30, fill='#13B2E9', font='Calibri 40', text="Player 1's turn:",
                           anchor='center')
    x = 60
    y = 60
    big_grey = rectangle(width=640, length=640, fill='#B1D3BB', x=x, y=y)
    restart = rectangle(length=60, width=180, fill='#CEC0B5', x=720, y=120)
    canvas.create_text(720+180/2, 120+60/2, fill='#FAFFFF', font='Calibri 40', text='Restart',
                       anchor='center')

    canvas.create_text(720, 250, fill='#776E65', font='Calibri 25', text="First to complete 3 X's\nin-a-row wins!",
                       anchor='w')

    for r in range(3):
        for c in range(3):
            y = 60 + tile_size*r + (tile_buffer*(r+1))
            x = 60 + tile_size*c + (tile_buffer*(c+1))
            tiles[(r, c)] = (x, y)
            exes[(r, c)] = 0
            rectangle(x=x, y=y)


def choose(key, value):
    x, y = value[0], value[1]
    global header
    global ones_turn
    fill, text, num = player.get(ones_turn)[0], player.get(ones_turn)[1], player.get(ones_turn)[2]
    canvas.create_text(x+(tile_size/2), y+(tile_size/2), fill=fill, font='Calibri 100', text=text,
                       anchor='center')
    canvas.delete(header)
    color = '#FF3F3F'
    text = "Player 2's turn:"
    if not ones_turn:
        color = '#13B2E9'
        text = "Player 1's turn"
    header = canvas.create_text(750/2, 30, fill=color, font='Calibri 40', text=text,
                           anchor='center')
    exes[key] = num
    ones_turn = not ones_turn



def rectangle(**kwargs):
    x1, y1 = 0, 0
    x2, y2 = tile_size, tile_size
    fill, outline = '#FCF8F8', '#B6A699'
    x, y = 0, 0

    for key, value in kwargs.items():
        if key == 'radius':
            global radius
            radius = value
        elif key == 'width':
            x2 = value
        elif key == 'length':
            y2 = value
        elif key == 'fill':
            fill = value
        elif key == 'outline':
            outline = value
        elif key == 'x':
            x = value
        elif key == 'y':
            y = value

    points = [x1 + radius, y1, x1 + radius, y1, x2 - radius, y1, x2 - radius, y1, x2, y1, x2, y1 + radius,
        x2, y1 + radius, x2, y2 - radius, x2, y2 - radius, x2, y2, x2 - radius, y2, x2 - radius, y2, x1 + radius,
        y2, x1 + radius, y2, x1, y2, x1, y2 - radius, x1, y2 - radius, x1, y1 + radius,x1, y1 + radius, x1, y1]

    square = canvas.create_polygon(points, smooth=True, fill=fill, outline=outline)
    canvas.move(square, x, y)
    canvas.bind("<Button-1>", game)
    return square


if __name__ == '__main__':
    main()
