from tkinter import *
from tkinter import ttk
import random

game_ended = False

def startGame():
    global options
    global minefield
    global cells
    global bombs
    global seen_cells
    global flagged_cells
    global game_ended

    game_ended = False
    options = {
        'bombs': int(qtd_bombs.get()),
        'width': int(width.get()),
        'height': int(height.get()),
    }

    minefield = Frame(root, bg='black')
    minefield.grid(column=0, row=2, ipadx=1, ipady=1, sticky=(N, W, E, S))
    minefield.columnconfigure(0, weight=1)
    minefield.columnconfigure(options['width'] + 1, weight=1)
    minefield.rowconfigure(0, weight=1)
    minefield.rowconfigure(options['height'] + 1, weight=1)

    cells = {}
    bombs = []
    seen_cells = []
    flagged_cells = []

    if options['bombs'] > options['width'] * options['height']:
        print('more bombs than cells, stopping execution')
        return

    while len(bombs) < options['bombs']:
        bombX = random.randint(0, options['width'] - 1)
        bombY = random.randint(0, options['height'] - 1)
        pos = {
            'x': bombX,
            'y': bombY
        }
        if pos not in bombs:
            bombs.append(pos)
    for x in range(0, options['width']):
        cells[x] = {}
        for y in range(0, options['height']):
            pos = {
                'x': x,
                'y': y
            }
            cell = Label(minefield, bg='grey', width=2, height=1, font=('​Helvetica', 12, 'bold'))
            cell.grid(column=x+1, row=y+1, padx=1, pady=1)
            cell.bind("<Button-1>", lambda event, pos=pos: viewCell(pos))
            cell.bind("<Button-2>", lambda event, pos=pos: toogleFlag(pos))
            cell.bind("<Button-3>", lambda event, pos=pos: toogleFlag(pos))
            cells[x][y] = cell

    startButton['text'] = 'Restart'


def getCellText(pos):
    if pos in bombs:
        btnText = 'B'
    else:
        bombsAround = getBombsAround(pos)
        btnText = bombsAround if bombsAround > 0 else ''
    return btnText


def viewCell(pos):
    global game_ended
    if game_ended:
        return

    colors = [
        'white',
        'green',
        'blue',
        'orange',
        'purple',
        'gold',
        'cyan',
        'browm',
        'black'
    ]
    cellText = getCellText(pos)
    if cellText == 'B':
        Label(root, text='You lost!', font=('​Helvetica', 18, 'bold'), bg='black', fg='red').grid(column=0, row=2)
        game_ended = True
    elif 0 <= pos['x'] < int(width.get()) and 0 <= pos['y'] < int(height.get()) and pos not in seen_cells:
        cells[pos['x']][pos['y']]['text'] = cellText
        cells[pos['x']][pos['y']]['bg'] = 'white'
        cells[pos['x']][pos['y']]['fg'] = 'red' if getCellText(pos) == 'B' else colors[getBombsAround(pos)]

        seen_cells.append(pos)
        if not hasBomb(pos) and getBombsAround(pos) == 0:
            for xNeighbor in range(pos['x'] - 1, pos['x'] + 2):
                for yNeighbor in range(pos['y'] - 1, pos['y'] + 2):
                    if xNeighbor != pos['x'] or yNeighbor != pos['y']:
                        neighborPos = {
                            'x': xNeighbor,
                            'y': yNeighbor
                        }
                        viewCell(neighborPos)
    elif len(seen_cells) == options['width'] * options['height'] - options['bombs']:
        Label(root, text='You won!', font=('​Helvetica', 18, 'bold'), bg='black', fg='green').grid(column=0, row=2)
        game_ended = True


def toogleFlag(pos):
    global game_ended
    if game_ended:
        return

    if pos not in seen_cells:
        cells[pos['x']][pos['y']]['fg'] = 'white'
        if cells[pos['x']][pos['y']]['text'] == '':
            cells[pos['x']][pos['y']]['text'] = 'F'
            flagged_cells.append(pos)
        else:
            cells[pos['x']][pos['y']]['text'] = ''
            flagged_cells.pop(flagged_cells.index(pos))


def hasBomb(pos):
    return pos in bombs


def getBombsAround(pos):
    bombsAround = 0
    for xNeighbor in range(pos['x'] - 1, pos['x'] + 2):
        for yNeighbor in range(pos['y'] - 1, pos['y'] + 2):
            if {'x': xNeighbor, 'y': yNeighbor} in bombs:
                bombsAround += 1
    return bombsAround

root = Tk()

root.title('Minesweeper')
root.resizable(False, False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe = ttk.Frame(root, padding="5 5 5 5")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

width = StringVar()
width.set(10)
width_entry = ttk.Entry(mainframe, width=7, textvariable=width)
width_entry.grid(column=0, row=1, sticky=(N, S, W, E), padx=2)
ttk.Label(mainframe, text="Width").grid(column=0, row=0, sticky=W)

height = StringVar()
height.set(10)
height_entry = ttk.Entry(mainframe, width=7, textvariable=height)
height_entry.grid(column=1, row=1, sticky=(N, S, W, E), padx=2)
ttk.Label(mainframe, text="Height").grid(column=1, row=0, sticky=W)

qtd_bombs = StringVar()
qtd_bombs.set(10)
qtd_bombs_entry = ttk.Entry(mainframe, width=7, textvariable=qtd_bombs)
qtd_bombs_entry.grid(column=2, row=1, sticky=(N, S, W, E), padx=2)
ttk.Label(mainframe, text="Bombs").grid(column=2, row=0, sticky=W)

startButton = ttk.Button(mainframe, text="Start", command=startGame)
startButton.grid(column=3, row=1, sticky=(N, S, W, E))

root.mainloop()
