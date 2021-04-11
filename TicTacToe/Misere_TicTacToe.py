from tkinter import *
import time


player = {
    0: '#EEE4D4',
    1: '#13B2E9',
    2: '#FF3F3F',
    3: '#3FFF7A',
    4: '#FFCF3F',
    5: '#FF3FF0'}

tiles = {}

exes = {}

root = Tk()
root.title('Misere Tic-Tac-Toe')
width = 500
height = 500
root.geometry('%sx%s' % (width, height))
canvas = Canvas(root, width=width, height=height, highlightthickness=0)
e = canvas.create_text(225, 30, fill='#13B2E9', font='Arial 30', text="Player 1's turn",
                       anchor='center')
one = True
lost = 0

tile_size = 75
tile_buffer = 10
radius = 10


def main():
    setup()
    canvas.pack()
    root.mainloop()


def game(event):
    x = event.x
    y = event.y
    global tiles
    if (185 <= x <= 275) & (420 <= y <= 450):
        setup()
    for key, value in tiles.items():
        btn_x = value[0]
        btn_y = value[1]
        if (btn_x <= x <= (btn_x+tile_size)) & (btn_y <= y <= (btn_y+tile_size)):
            if not exes.get(key):
                global e, one, lost
                p = 2
                exes[key] = True
                if one:
                    p = 1
                    if win():
                        lost += 1
                    if lost == 1:
                        ex(p, btn_x, btn_y)
                        ex(p, btn_x, btn_y)
                        canvas.delete(e)
                        e = canvas.create_text(225, 30, fill='#FF3F3F', font='Arial 30', text="Player 2 wins!",
                           anchor='center')
                    one = False
                else:
                    if win():
                        lost += 1
                    if lost == 1:
                        one = True
                        p = 1
                        ex(p, btn_x, btn_y)
                        ex(p, btn_x, btn_y)
                        canvas.delete(e)
                        e = canvas.create_text(225, 30, fill='#13B2E9', font='Arial 30', text="Player 1 wins!",
                           anchor='center')
                    one = True
                if not win():
                    ex(p, btn_x, btn_y)
                    ex(p, btn_x, btn_y)


def win():
    num = False
    if (exes.get((0, 0))) & (exes.get((1, 1))) & (exes.get((2, 2))):
        num = True
    elif (exes.get((1, 1))) & (exes.get((2, 2))) & (exes.get((3, 3))):
        num = True
    elif (exes.get((0, 3))) & (exes.get((1, 2))) & (exes.get((2, 1))):
        num = True
    elif (exes.get((1, 2))) & (exes.get((2, 1))) & (exes.get((3, 0))):
        num = True
    elif (exes.get((0, 0))) & (exes.get((0, 1))) & (exes.get((0, 2))):
        num = True
    elif (exes.get((0, 1))) & (exes.get((0, 2))) & (exes.get((0, 3))):
        num = True
    elif (exes.get((1, 0))) & (exes.get((1, 1))) & (exes.get((1, 2))):
        num = True
    elif (exes.get((1, 1))) & (exes.get((1, 2))) & (exes.get((1, 3))):
        num = True
    elif (exes.get((2, 0))) & (exes.get((2, 1))) & (exes.get((2, 2))):
        num = True
    elif (exes.get((2, 1))) & (exes.get((2, 2))) & (exes.get((2, 3))):
        num = True
    elif (exes.get((3, 0))) & (exes.get((3, 1))) & (exes.get((3, 2))):
        num = True
    elif (exes.get((3, 1))) & (exes.get((3, 2))) & (exes.get((3, 3))):
        num = True
    elif (exes.get((0, 0))) & (exes.get((1, 0))) & (exes.get((2, 0))):
        num = True
    elif (exes.get((1, 0))) & (exes.get((2, 0))) & (exes.get((3, 0))):
        num = True
    elif (exes.get((0, 1))) & (exes.get((1, 1))) & (exes.get((2, 1))):
        num = True
    elif (exes.get((1, 1))) & (exes.get((2, 1))) & (exes.get((3, 1))):
        num = True
    elif (exes.get((0, 2))) & (exes.get((1, 2))) & (exes.get((2, 2))):
        num = True
    elif (exes.get((1, 2))) & (exes.get((2, 2))) & (exes.get((3, 2))):
        num = True
    elif (exes.get((0, 3))) & (exes.get((1, 3))) & (exes.get((2, 3))):
        num = True
    elif (exes.get((1, 3))) & (exes.get((2, 3))) & (exes.get((3, 3))):
        num = True
    elif (exes.get((0, 2))) & (exes.get((1, 1))) & (exes.get((2, 0))):
        num = True
    elif (exes.get((1, 0))) & (exes.get((2, 1))) & (exes.get((3, 2))):
        num = True
    elif (exes.get((0, 1))) & (exes.get((1, 2))) & (exes.get((2, 3))):
        num = True
    elif (exes.get((3, 1))) & (exes.get((2, 2))) & (exes.get((1, 3))):
        num = True
    return num


def setup():
    global tiles, exes, e, lost, one
    lost = 0
    tiles = {}
    exes = {}
    canvas.delete(e)
    e = canvas.create_text(225, 30, fill='#13B2E9', font='Arial 30', text="Player 1's turn",
                           anchor='center')
    x = 50
    y = 50
    big_grey = rectangle(width=350, length=350, fill='#BBADA0', x=x, y=y)
    restart = rectangle(length=30, width=90, fill='#CEC0B5', x=200-15, y=420)
    canvas.create_text(200-15 + 90/2, 420 + 30/2, fill='#FAFFFF', font='Arial 18', text='RESTART',
                       anchor='center')

    canvas.create_text(232, 475, fill='#776E65', font='Arial 16', text="First to complete 3 X's in-a-row loses",
                       anchor='center')

    for r in range(4):
        for c in range(4):
            y = 50 + tile_size*r + (tile_buffer*(r+1))
            x = 50 + tile_size*c + (tile_buffer*(c+1))
            tiles[(r, c)] = (x, y)
            exes[(r, c)] = False
            rectangle(x=x, y=y)


def ex(num, x, y):
    global e
    fill = player.get(num)
    canvas.create_text(x+(tile_size/2), y+(tile_size/2), fill=fill, font='Arial 45', text='X',
                       anchor='center')
    canvas.delete(e)
    color = '#FF3F3F'
    text = "Player 2's turn"
    if one:
        color = '#13B2E9'
        text = "Player 1's turn"
    e = canvas.create_text(225, 30, fill=color, font='Arial 30', text=text,
                           anchor='center')



def rectangle(**kwargs):
    x1, y1 = 0, 0
    x2, y2 = tile_size, tile_size
    fill, outline = '#CEC0B5', '#B6A699'
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

