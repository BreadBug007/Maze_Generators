import pygame as py
import random


class Cell:

    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True]*4
        self.visited = False

    def show(self, image):

        x = self.i * w
        y = self.j * w
        if self.walls[0]:
            py.draw.line(screen, white, (x, y), (x + w, y))
        if self.walls[1]:
            py.draw.line(screen, white, (x + w, y), (x + w, y + w))
        if self.walls[2]:
            py.draw.line(screen, white, (x + w, y + w), (x, y + w))
        if self.walls[3]:
            py.draw.line(screen, white, (x, y + w), (x, y))
        if self.visited:
            py.draw.rect(image, (0, 0, 255), (x, y, w, w))

    def highlight(self):
        py.draw.rect(screen, (0, 255, 0, 100), (self.i*w, self.j*w, w, w))

    def check_neighbour(self):
        neighbour = []
        top = grid[index(self.i, self.j - 1)]
        right = grid[index(self.i + 1, self.j)]
        bottom = grid[index(self.i, self.j + 1)]
        left = grid[index(self.i - 1, self.j)]

        if top and not top.visited:
            neighbour.append(top)
        if right and not right.visited:
            neighbour.append(right)
        if bottom and not bottom.visited:
            neighbour.append(bottom)
        if left and not left.visited:
            neighbour.append(left)

        if len(neighbour) > 0:
            return neighbour[random.randint(0, len(neighbour)-1)]
        else:
            return 0


def remove_wall(current, new):
    x = current.i - new.i
    y = current.j - new.j

    if x == 1:
        current.walls[3] = False
        new.walls[1] = False
    elif x == -1:
        current.walls[1] = False
        new.walls[3] = False
    if y == 1:
        new.walls[2] = False
        current.walls[0] = False
    elif y == -1:
        new.walls[0] = False
        current.walls[2] = False


def index(i, j):
    if i < 0 or j < 0 or i > cols-1 or j > rows-1:
        return False
    return i + j * cols


def main():
    global current, count
    image = py.Surface((width, height), py.SRCALPHA)
    current.visited = True

    for cell in grid:
        cell.show(image)

    if count != 0:
        current.highlight()

    new = current.check_neighbour()
    count = 0

    if new != 0:
        new.visited = True
        stack.append(current)
        remove_wall(current, new)
        current = new
        count += 1

    elif len(stack) > 0:
        current = stack.pop()
        count += 1

    if count == 0:
        start_cell = grid[0]
        end_cell = grid[-1]
        start_cell.walls[3] = False
        end_cell.walls[1] = False


py.init()

width, height = 1005, 605
w = 20

rows, cols = height//w, width//w

screen = py.display.set_mode((width, height), py.SRCALPHA)

black = (0, 0, 0)
white = (255, 255, 255)

grid, stack = [], []

for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)

current = grid[0]

clock = py.time.Clock()

flag = True
count = 1

while flag:
    for event in py.event.get():
        if event.type == py.QUIT:
            flag = False

    screen.fill(black)
    main()
    py.display.update()
    clock.tick(60)

py.quit()
