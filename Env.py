from Tkinter import *
master = Tk()
from random import randint

cell_score_min = -0.2
cell_score_max = 0.2
Width = 50
(x, y) = (23, 13)
actions = ["up", "down", "left", "right"]

board = Canvas(master, width=x*Width, height=y*Width)
player = (0, y-1)
score = 1
restart = False
walk_reward = -0.03

walls = []

def buildWalls(i, j, i1, j1, doors):
    global walls
    if i == i1:
        while( j <= j1):
            if ((i,j) not in doors):
                walls.append((i, j))
            j += 1
    if j == j1:
        while(i <= i1):
            if ((i, j) not in doors):
                walls.append((i, j))
            i += 1

def buildRoom(i, j, i1, j1, doors):
    global walls
    a,b = i,j
    while(a <= i1):
        buildWalls(a, j, i1, j, doors)
        a += 1
    while(b <= j1):
        buildWalls(i, b, i, j1, doors)
        b += 1
    newA, newB = a-1, b-1
    a, b = i, j
    while(a <= i1):
        buildWalls(a, newB, i1, newB, doors)
        a += 1
    while(b <= j1):
        buildWalls(newA, b, newA, j1, doors)
        b += 1

#living room
livingRoomDoors = [(2, 7), (4, 3)]
buildRoom(0, 0, 4, 7, livingRoomDoors)

#lobby
lobbyDoors = [(2, 7), (3, 10), (2, 10), (4, 8)]
buildRoom(0, 7, 4, 10, lobbyDoors)

#kitchen
kitchenDoors = [(5, 2)]
buildRoom(4, 0, 13, 2, kitchenDoors)

#storage
storageDoors = [(5, 4)]
buildRoom(4, 4, 9, 7, storageDoors)

#studio
studioDoors = [(4, 8)]
buildRoom(4, 7, 9, 10, studioDoors)

#bedroom1
bedroom1Doors = [(11, 4)]
buildRoom(9, 4, 13, 7, bedroom1Doors)

#bedroom2
bedroom2Doors = [(15, 4)]
buildRoom(13, 4, 17, 7, bedroom2Doors)

#bathroom1
bathroom1Doors = [(14, 2)]
buildRoom(13, 0, 15, 2, bathroom1Doors)

#bathroom2
bathroom2Doors = [(16, 2)]
buildRoom(15, 0, 17, 2, bathroom2Doors)

#garage
garageDoors = [(17, 3), (19, 7), (20, 7)]
buildRoom(17, 0, 21, 7, garageDoors)

specials = [(16, 5, "green", 1)]
cell_scores = {}

def render_grid():
    global specials, walls, Width, x, y, player
    for i in range(x):
        for j in range(y):
            board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="white", width=1)
            temp = {}
            cell_scores[(i,j)] = temp
    for (i, j, c, w) in specials:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill=c, width=1)
    for (i, j) in walls:
        board.create_rectangle(i*Width, j*Width, (i+1)*Width, (j+1)*Width, fill="black", width=1)

render_grid()

def try_move(dx, dy):
    global player, restart, x, y, walk_reward, me, specials, score
    if restart == True:
        restart_game()
    new_x = player[0] + dx
    new_y = player[1] + dy
    score += walk_reward
    if (new_x >= 0) and (new_x < x) and (new_y >= 0) and (new_y < y) and not ((new_x, new_y) in walls):
        board.coords(me, new_x*Width+Width*2/10, new_y*Width+Width*2/10, new_x*Width+Width*8/10, new_y*Width+Width*8/10)
        player = (new_x, new_y)
    for (i, j, c, w) in specials:
        if new_x == i and new_y == j:
            score -= walk_reward
            score += w
            specials.remove((i, j, c, w))
            if score > 0:
                print "Success! score: ", score
            else:
                print "Fail! score: ", score
            restart = True
            return


def call_up(event):
    try_move(0, -1)


def call_down(event):
    try_move(0, 1)


def call_left(event):
    try_move(-1, 0)


def call_right(event):
    try_move(1, 0)


def restart_game():
    global player, score, me, restart, specials
    specials = [(16, 5, "green", 1)]
    player = (0, y-1)
    score = 1
    restart = False
    board.coords(me, player[0]*Width+Width*2/10, player[1]*Width+Width*2/10, player[0]*Width+Width*8/10, player[1]*Width+Width*8/10)

def has_restarted():
    return restart

master.bind("<Up>", call_up)
master.bind("<Down>", call_down)
master.bind("<Right>", call_right)
master.bind("<Left>", call_left)

me = board.create_rectangle(player[0]*Width+Width*2/10, player[1]*Width+Width*2/10,
                            player[0]*Width+Width*8/10, player[1]*Width+Width*8/10, fill="orange", width=1, tag="me")

board.grid(row=0, column=0)


def start_game():
    master.mainloop()
