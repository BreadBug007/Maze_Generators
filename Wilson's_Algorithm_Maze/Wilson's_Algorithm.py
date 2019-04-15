import pygame as py
import random

py.init()

width, height = 600, 600
size = 20
screen = py.display.set_mode((width, height))

cols, rows = width//size, height//size

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0, 50)
red = (121, 63, 13)


class Cell:

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True]*4
        self.visited = False

    def show(self, color):
        py.draw.rect(screen, color, (self.i * size, self.j * size, size, size))

    def create_walls(self):
        x = self.i * size
        y = self.j * size
        if self.walls[0]:
            py.draw.line(screen, white, (x, y), (x + size, y))
        if self.walls[1]:
            py.draw.line(screen, white, (x + size, y), (x + size, y + size))
        if self.walls[2]:
            py.draw.line(screen, white, (x + size, y + size), (x, y + size))
        if self.walls[3]:
            py.draw.line(screen, white, (x, y + size), (x, y))
        if self.visited:
            py.draw.rect(screen, (0, 0, 255), (x, y, size, size))

    # def check_neighbours(self):
    #     i = self.i
    #     j = self.j
    #     neighbours = []
    #     top = index(i, j - 1)
    #     right = index(i + 1, j)
    #     bottom = index(i, j + 1)
    #     left = index(i - 1, j)
    #     probability = [25, 20, 25, 30]
    #     if top != 0:
    #         temp = [Cells[top]] * probability[0]
    #         neighbours.extend(temp)
    #     if right != 0:
    #         temp = [Cells[right]] * probability[1]
    #         neighbours.extend(temp)
    #     if bottom != 0:
    #         temp = [Cells[bottom]] * probability[2]
    #         neighbours.extend(temp)
    #     if left != 0:
    #         temp = [Cells[left]] * probability[3]
    #         neighbours.extend(temp)
    #
    #     if len(neighbours) > 0:
    #         return neighbours[random.randint(0, len(neighbours) - 1)]
    #     else:
    #         return 0
    def check_neighbours(self):
        i = self.i
        j = self.j
        neighbour = []
        top = index(i, j - 1)
        right = index(i + 1, j)
        bottom = index(i, j + 1)
        left = index(i - 1, j)

        if top != 0:
            neighbour.append(Cells[top])
        if right != 0:
            neighbour.append(Cells[right])
        if bottom != 0:
            neighbour.append(Cells[bottom])
        if left != 0:
            neighbour.append(Cells[left])

        if len(neighbour) > 0:
            return neighbour[random.randint(0, len(neighbour)-1)]
        else:
            return 0


Cells, Cells_Remaining, Cells_Maze, Branch, New_Branch = [], [], [], [], []

for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        Cells.append(cell)
        Cells_Remaining.append(cell)


target = Cells[(rows//2)*cols + rows//2 - 1]
current = Cells[-3]
Cells_Maze.append(target)


def get_current():
    global Cells_Maze, Cells
    try:
        temp = random.choice(Cells)
        if temp in Cells_Maze:
            return get_current()
        else:
            return temp
    except RecursionError:
        return 0


def branch():
    global current, Cells_Maze, Branch, New_Branch

    if len(Branch) > 0:
        if current in Cells_Maze:
            Cells_Maze.extend(Branch)
            New_Branch = Branch
            New_Branch.append(current)
            remove_walls()
            New_Branch.clear()
            Branch.clear()
            current = get_current()
            if current == 0:
                return 0

    if current in Branch:
        for k, cell in enumerate(Branch):
            if cell == current:
                if k == 0:
                    Branch.clear()
                    break
                else:
                    current = Branch[k-1]
                    Branch = Branch[:k]
                    break

    new = current.check_neighbours()
    if new != 0 and new != current:
        Branch.append(current)
        current = new


def remove_walls():
    global New_Branch

    for cell in range(0, len(New_Branch) - 1):
        first = New_Branch[cell]
        second = New_Branch[cell + 1]

        x = first.i - second.i
        if x == 1:
            first.walls[3] = False
            second.walls[1] = False
        elif x == -1:
            first.walls[1] = False
            second.walls[3] = False

        y = first.j - second.j
        if y == 1:
            second.walls[2] = False
            first.walls[0] = False
        elif y == -1:
            second.walls[0] = False
            first.walls[2] = False


def index(i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return 0
    return i + j * cols


clock = py.time.Clock()
length = 0

game = True

while game:
    for event in py.event.get():
        if event.type == py.QUIT:
            game = False
            py.quit()

    screen.fill(black)

    pause = branch()

    if pause == 0:
        game = False

    for cell in Branch:
        cell.show(green)
    for k, cell in enumerate(Cells_Maze):
        cell.show(red)
        cell.create_walls()

    py.display.update()
    clock.tick(120)
