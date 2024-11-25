from tkinter import Tk, Canvas
from random import choice

def graphic_window(xdim, ydim, size):
    """ Init de la fenêtre Tkinter. """

    w = (xdim + 1) * size # Calculs des coords.
    h = (ydim + 1) * size

    window = Tk() # Init de la fenêtre.
    window.title("Projet 6 - Labyrinthe")
    window.geometry(str(w) + "x" + str(h))
    window.resizable(0, 0)

    canvas = Canvas(window, bg="white", width=w, height=h) # Init du Canvas.
    canvas.place(x=0, y=0)

    return window, canvas

def celltowalls(x, y, xdim, ydim):
    """ Permet de convertir les coords d'une cellule pour un mur. """

    # Calcul des coords.
    north = y * xdim + x
    south = north + xdim
    west = Nh + y * (xdim + 1) + x
    east = west + 1

    return (north, west, south, east)

def draw_maze(canvas, walls, xdim, ydim, size):
    """ Trace les segments pour chaque mur fermé. """

    for y in range(ydim + 1):
        for x in range(xdim):
            if walls[y * xdim + x]:
                canvas.create_line(x * size + size // 2, y * size + size // 2,
                                   (x + 1) * size + size // 2, y * size + size // 2)
    for y in range(ydim):
        for x in range(xdim + 1):
            if walls[Nh + y * (xdim + 1) + x]:
                canvas.create_line(x * size + size // 2, y * size + size // 2,
                                   x * size + size // 2, (y + 1) * size + size // 2)

def walltocells(w, xdim, Nh):
    """ Permet de convertir les coords d'un mur pour une cellule. """

    if w < Nh:
        x = w % xdim
        y = w // xdim

        return (x, y - 1, x, y)
    else:
        w -= Nh
        x = w % (xdim + 1)
        y = w // (xdim + 1)
        
        return (x - 1, y, x, y)

def pick_wall(closed, cells, xdim, ydim, Nh):
    """ Tire aléatoire grâce à Closed un mur fermé. """

    while True:
        w = choice(closed)
        x1, y1, x2, y2 = walltocells(w, xdim, Nh)

        if 0 <= x1 < xdim and 0 <= y1 < ydim and 0 <= x2 < xdim and 0 <= y2 < ydim:
            if cells[x1][y1] != cells[x2][y2]:
                return w

def merge(cells, x1, y1, x2, y2):
    """ Modifie les valeurs de Cells. """

    temp = cells[x2][y2]
    valeur = cells[x1][y1]

    for y in range(len(cells[0])):
        for x in range(len(cells)):
            if cells[x][y] == temp:
                cells[x][y] = valeur

def generate_maze(walls, xdim, ydim):
    """ Génère le labyrinthe. """

    cells = [[x + y * xdim for x in range(xdim)] for y in range(ydim)]
    closed = list(range(Nh + Nv))

    for k in range(xdim * ydim - 1):
        w = pick_wall(closed, cells, xdim, ydim, Nh)
        closed.remove(w)
        walls[w] = False
        x1, y1, x2, y2 = walltocells(w, xdim, Nh)
        merge(cells, x1, y1, x2, y2)


def reset(canvas, xdim, ydim, size):
    """ Efface et redessine un labyrinthe. """

    global Nh, Nv, walls

    canvas.delete("all")

    Nh = xdim * (ydim + 1)
    Nv = (xdim + 1) * ydim
    walls = [True] * (Nh + Nv)

    generate_maze(walls, xdim, ydim)
    draw_maze(canvas, walls, xdim, ydim, size)

def solve(canvas, walls, xdim, ydim, size):
    Nh = xdim * (ydim + 1)
    start = (0, 0)
    end = (xdim - 1, ydim - 1)
    pile_temp = [start]
    venant = {start: None}

    while pile_temp:
        temp = pile_temp.pop()
        if temp == end:
            break
        x, y = temp
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < xdim and 0 <= ny < ydim:
                index = None
                if dx == -1:
                    index = Nh + y * (xdim + 1) + x
                elif dx == 1:
                    index = Nh + y * (xdim + 1) + x + 1
                elif dy == -1:
                    index = y * xdim + x
                elif dy == 1:
                    index = (y + 1) * xdim + x
                if index is not None and not walls[index]:
                    suivant = (nx, ny)
                    if suivant not in venant:
                        pile_temp.append(suivant)
                        venant[suivant] = temp

    lst_wall = []
    temp = end
    while temp:
        lst_wall.append(temp)
        temp = venant[temp]
    lst_wall.reverse()

    for (x, y) in lst_wall:
        x1, y1 = (x * size + size, y * size + size)
        canvas.create_oval(x1 - size // 4, y1 - size // 4, x1 + size // 4, y1 + size // 4, fill="blue")

def maze_generator(xdim, ydim, size):
    global Nh, Nv, walls

    Nh = xdim * (ydim + 1)
    Nv = (xdim + 1) * ydim
    walls = [True] * (Nh + Nv)
    
    window, canvas = graphic_window(xdim, ydim, size)
    generate_maze(walls, xdim, ydim)
    draw_maze(canvas, walls, xdim, ydim, size)
    
    # Assignation des touches.
    window.bind("r", lambda event: reset(canvas, xdim, ydim, size))
    window.bind("s", lambda event: solve(canvas, walls, xdim, ydim, size))
    
    window.mainloop()

xdim = int(input("Largeur souhaité du labyrinthe : "))
ydim = int(input("Hauteur souhaité du labyrinthe : "))
size = int(input("Taille de chaque cellule souhaitée : "))
maze_generator(xdim, ydim, size)
