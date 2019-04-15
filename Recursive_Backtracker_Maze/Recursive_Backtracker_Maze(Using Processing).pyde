class Cell:

    def  __init__(self, i, j):
        self.i = i
        self.j = j
        self.walls = [True, True, True, True]
        self.visited = False
        
    def show(self):
        x = self.i * w
        y = self.j * w
        stroke(255)
        if self.walls[0]: line(x, y, x+w, y)
        if self.walls[1]: line(x+w, y, x+w, y+w)
        if self.walls[2]: line(x+w, y+w, x, y+w)
        if self.walls[3]: line(x, y+w, x, y)
        
        if self.visited:
            noStroke()
            fill(200, 0, 200, 50)
            rect(x, y, w, w)
            
    def highlight(self):
        x = self.i * w
        y = self.j * w
        noStroke()
        fill(0, 255, 0)
        rect(x, y, w, w)
        
    def checkNeighbour(self):
        
        neighbour = []
        top = grid[index(self.i, self.j-1)]
        right = grid[index(self.i+1, self.j)]
        bottom = grid[index(self.i, self.j+1)]
        left = grid[index(self.i-1, self.j)]
        
        if top and not top.visited:
            neighbour.append(top)
        if right and not right.visited:
            neighbour.append(right)
        if bottom and not bottom.visited:
            neighbour.append(bottom)
        if left and not left.visited:
            neighbour.append(left)
        
        if len(neighbour) > 0:
            r = int(random(0, len(neighbour)))
            return neighbour[r]
        else: return None


def removeWall(a, b):
    hor = a.i - b.i
    ver = a.j - b.j
    
    if hor == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif hor == -1:
        a.walls[1] = False
        b.walls[3] = False
    if ver == 1:
        b.walls[2] = False
        a.walls[0] = False
    elif ver == -1:
        b.walls[0] = False
        a.walls[2] = False
                
            
def index(i, j):
    if i < 0 or j < 0 or i > cols-1 or j > rows-1:
        return False
    return i + j * cols


grid = []
current = 0
stack = []
count = 1
        
    
def setup():
    global w, rows, cols, grid, current
    size(910, 910)
    
    w = 30
    cols = width/w 
    rows = height/w

    for j in range(rows):
        for i in range(cols):
            cell = Cell(i, j)
            grid.append(cell)
    current = grid[0]

    
    
def draw():
    translate(5, 5)
    global  count, current
    background(50)

    strokeWeight(3)
    for i in range(len(grid)):
        grid[i].show()
    
    current.visited = True
    
    if count != 0:
        current.highlight()
        
    next = current.checkNeighbour()
    count = 0
    
    if next is not None:
        next.visited = True
        stack.append(current)
        removeWall(current, next)
        current = next
        count += 1

    elif len(stack) > 0:
        current = stack.pop()
        count += 1
    
    if count == 0:
        startCell = grid[0]
        endCell = grid[-1]
        startCell.walls[3] = False
        endCell.walls[1] = False

    save("Maze.jpg")
        
    
