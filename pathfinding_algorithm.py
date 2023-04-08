import tkinter as tk
import pygame
from random import choices, randint, choice
import queue
import heapq
from math import sqrt
import os

SETTINGS = {}
FPS = 60
WIDTH, HEIGHT = 700, 700
TILE_WIDTH, TILE_HEIGHT = None, None

COLORS = {
    "BG_COLOR": (255, 255, 255),
    "TILE_COLOR": (210, 210, 210),
    "WALL_TILE_COLOR": (128, 128, 128),
    "TEXT_BG_COLOR": (150, 150, 150),
    "TEXT_COLOR": (0, 0, 0),
    "GREEN": (0, 255, 0),
    "ORANGE": (255, 165, 0),
    "RED": (255, 0, 0)
}

pygame.init()


class DijkstraVertex:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.dist = float('inf')
        self.visited = False
        self.parent = None
        self.edges = []

    def __lt__(self, other):
        return self.dist < other.dist
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class AstarVertex:
    def __init__(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.edges = []
        self.distance = float('inf')
        self.heuristic = 0
        self.visited = False
        self.parent = None
        
    def set_heuristic(self, goal):
        self.heuristic = sqrt((self.x - goal.x) ** 2 + (self.y - goal.y) ** 2)

    def __lt__(self, other):
        return self.distance + self.heuristic < other.distance + other.heuristic
    
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


def settings():
    def start_algorithm(root, width, height, showProcess, chooseAlgorithm, drawMaze):
        try:
            width = int(width)
            height = int(height)
        except ValueError:
            return
        else:
            if width < 2 or height < 2:
                return
        
        SETTINGS["width"] = width
        SETTINGS["height"] = height
        SETTINGS["showProcess"] = showProcess
        SETTINGS["chooseAlgorithm"] = chooseAlgorithm
        SETTINGS["drawMaze"] = drawMaze
        
        root.destroy()
        
    root = tk.Tk()
    root.title("Settings")
    root.geometry("+200+10")

    main_font = ("Arial", 14)
    smaller_font = ("Arial", 12, "italic")

    tk.Label(text="Enter width:", font=main_font).grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
    widthEntry = tk.Entry(root, font=main_font)
    widthEntry.grid(row=0, column=1, padx=10, pady=10, ipady=2, sticky=tk.W)

    tk.Label(text="Enter height:", font=main_font).grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
    heightEntry = tk.Entry(root, font=main_font)
    heightEntry.grid(row=1, column=1, padx=10, pady=10, ipady=2, sticky=tk.W)

    tk.Label(text="").grid(row=2, column=0)

    tk.Label(text="Choose an algorithm:", font=main_font).grid(row=3, column=0, padx=10, pady=10, columnspan=2, sticky=tk.W)
    chooseAlgorithmVar = tk.StringVar(value="breadth first")
    tk.Radiobutton(root, text="Breadth first search", variable=chooseAlgorithmVar, value="breadth first", font=smaller_font).grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Radiobutton(root, text="Depth first search", variable=chooseAlgorithmVar, value="depth first", font=smaller_font).grid(row=5, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Radiobutton(root, text="Dijkstra's algorithm", variable=chooseAlgorithmVar, value="dijkstra", font=smaller_font).grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Radiobutton(root, text="A* algorithm", variable=chooseAlgorithmVar, value="a*", font=smaller_font).grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)
    
    tk.Label(text="Would you like to see the algorithm or just the end result?", font=main_font).grid(row=8, column=0, padx=10, pady=10, columnspan=2, sticky=tk.W)
    showProcessVar = tk.BooleanVar(value=True) # True - show alorythm, False - show end result
    tk.Radiobutton(root, text="Show me the algorithm", variable=showProcessVar, value=True, font=smaller_font).grid(row=9, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Radiobutton(root, text="Just show me end result", variable=showProcessVar, value=False, font=smaller_font).grid(row=10, column=0, padx=10, pady=10, sticky=tk.W)
    
    tk.Label(text="Would you like to draw your own maze?", font=main_font).grid(row=11, column=0, padx=10, pady=10, columnspan=2, sticky=tk.W)
    drawMazeVar = tk.StringVar(value="randomize") # randomize - random maze, draw - user draws the maze, file - random maze from a file
    tk.Radiobutton(root, text="Randomize the maze", variable=drawMazeVar, value="randomize", font=smaller_font).grid(row=12, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Radiobutton(root, text="Let me draw the maze", variable=drawMazeVar, value="draw", font=smaller_font).grid(row=13, column=0, padx=10, pady=10, sticky=tk.W)
    tk.Radiobutton(root, text="Choose a random maze from file", variable=drawMazeVar, value="file", font=smaller_font).grid(row=14, column=0, padx=10, pady=10, sticky=tk.W)

    tk.Button(text="Start", font=main_font, command=lambda: start_algorithm(root, widthEntry.get(), heightEntry.get(), showProcessVar.get(), chooseAlgorithmVar.get(), drawMazeVar.get())).grid(row=15, column=0, columnspan=2, padx=10, pady=10, ipadx=30, ipady=10)

    root.mainloop()


def draw_at_the_start(board, WIN):
    font = pygame.font.SysFont(None, int(min(TILE_WIDTH, TILE_HEIGHT)))
    textWidth, textHeight = font.size('O')
    alignX = TILE_WIDTH // 2 - textWidth // 2
    alignY = TILE_HEIGHT // 2 - textHeight // 2
    
    WIN.fill(COLORS["BG_COLOR"])
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col == '#': # wall tile
                pygame.draw.rect(WIN, COLORS["WALL_TILE_COLOR"], (j*TILE_WIDTH, i*TILE_HEIGHT, TILE_WIDTH-2, TILE_HEIGHT-2))
            else: # any other tile
                pygame.draw.rect(WIN, COLORS["TILE_COLOR"], (j*TILE_WIDTH, i*TILE_HEIGHT, TILE_WIDTH-2, TILE_HEIGHT-2))
            
            if col == 'O':
                WIN.blit(font.render('O', True, COLORS["TEXT_COLOR"]), (j*TILE_WIDTH + alignX, i*TILE_HEIGHT + alignY))
            elif col == 'X':
                WIN.blit(font.render('X', True, COLORS["TEXT_COLOR"]), (j*TILE_WIDTH + alignX, i*TILE_HEIGHT + alignY))


def load_maze_from_file():
    fileList = os.listdir("maze")
    file = choice(fileList)
    
    with open(f"maze/{file}", "r") as f:
        board = f.readlines()
    
    start_pos, end_pos = None, None
    for i, row in enumerate(board):
        row = row.rstrip('\n')
        board[i] = row
        for j, col in enumerate(row):
            if col == 'O':
                start_pos = (j, i)
            elif col == 'X':
                end_pos = (j, i)
    
    return (board, start_pos, end_pos)


def mouse_pressed(pos, board, value):
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if j*TILE_WIDTH < pos[0] < (j+1) * TILE_WIDTH - 2 and i * TILE_HEIGHT < pos[1] < (i+1) * TILE_HEIGHT - 2:
                if board[i][j] == ' ':
                    board[i][j] = value
                    return (j, i)


def select_pos_text(WIN, text):
    font = pygame.font.SysFont(None, 40)
    textWidth, textHeight = font.size(text)
    
    pygame.draw.rect(WIN, COLORS["TEXT_BG_COLOR"], (WIDTH / 2 - textWidth / 2 - 10, 0, textWidth + 20 ,textHeight + 20))
    WIN.blit(font.render(text, True, COLORS["TEXT_COLOR"]), (WIDTH / 2 - textWidth / 2, 10))


def start_button(WIN):
    font = pygame.font.SysFont(None, 60)
    textWidth, textHeight = font.size("Ready")
    
    pygame.draw.rect(WIN, COLORS["TEXT_BG_COLOR"], (WIDTH / 2 - textWidth / 2 - 10, 0, textWidth + 20, textHeight + 20))
    WIN.blit(font.render("Ready", True, COLORS["TEXT_COLOR"]), (WIDTH / 2 - textWidth / 2, 10))
    
    return (WIDTH / 2 - textWidth / 2 - 10, 0, WIDTH / 2 + textWidth / 2 + 10, textHeight + 20) # x1 y1 x2 y2


def main_draw(WIN, board, path, was_here):
    font = pygame.font.SysFont(None, int(min(TILE_WIDTH, TILE_HEIGHT)))
    textWidth, textHeight = font.size('X')
    alignX = TILE_WIDTH // 2 - textWidth // 2
    alignY = TILE_HEIGHT // 2 - textHeight // 2
    
    WIN.fill(COLORS["BG_COLOR"])
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if (j, i) in path:
                color = COLORS["GREEN"]
            elif (j, i) in was_here:
                color = COLORS["ORANGE"]
            elif col == '#':
                color = COLORS["WALL_TILE_COLOR"]
            elif col == 'X':
                color = COLORS["RED"]
            elif col == 'O':
                color = COLORS["GREEN"]
            else:
                color = COLORS["TILE_COLOR"]
            
            pygame.draw.rect(WIN, color, (j*TILE_WIDTH, i*TILE_HEIGHT, TILE_WIDTH-2, TILE_HEIGHT-2))
            
            if col == 'O':
                WIN.blit(font.render('O', True, COLORS["TEXT_COLOR"]), (j*TILE_WIDTH + alignX, i*TILE_HEIGHT + alignY))
            elif col == 'X':
                WIN.blit(font.render('X', True, COLORS["TEXT_COLOR"]), (j*TILE_WIDTH + alignX, i*TILE_HEIGHT + alignY))
    pygame.display.update()


def find_neighbors(board, x, y):
    neighbors = []
    
    possibleMoves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    for dx, dy in possibleMoves:
        newX = x + dx
        newY = y + dy
        if board[newY][newX] != '#':
            neighbors.append((newX, newY))
    
    return neighbors


def breadth_first_search(WIN, clock, board, start_pos, end_pos, showProcess):
    was_here = []
    visited = []
    q = queue.Queue()
    q.put((start_pos, [start_pos]))
    
    while not q.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_pos, path = q.get()
        x, y = current_pos
        
        if current_pos not in was_here:
            was_here.append(current_pos)
        
        if showProcess:
            main_draw(WIN, board, path, was_here)
            clock.tick(FPS)
        
        if (x, y) == end_pos:
            break
        
        neighbors = find_neighbors(board, x, y)
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            new_path = path + [neighbor]
            q.put((neighbor, new_path))
            visited.append(neighbor)
    
    main_draw(WIN, board, path, was_here)


def depth_first_search(WIN, clock, board, start_pos, end_pos, showProcess):
    was_here = []
    visited = []
    q = []
    q.append((start_pos, [start_pos]))
    
    while len(q) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current_pos, path = q[-1]
        q.pop()
        x, y = current_pos
        
        if current_pos not in was_here:
            was_here.append(current_pos)
        
        if showProcess:
            main_draw(WIN, board, path, was_here)
            clock.tick(FPS)
        
        if (x, y) == end_pos:
            break
        
        neighbors = find_neighbors(board, x, y)
        try:
            neighbors.reverse()
        except:
            pass
        
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            new_path = path + [neighbor]
            q.append((neighbor, new_path))
            visited.append(neighbor)
    main_draw(WIN, board, path, was_here)


def find_edges(board, vertices, vertex):
    edges = []
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        x = vertex.x + dx
        y = vertex.y + dy
        if 0 <= x < len(board[0]) and 0 <= y < len(board) and board[y][x] != '#':
            edges.append((x, y))
    return [vertices[y][x] for x, y in edges]


def dijkstra_search(WIN, clock, board, start_pos, end_pos, showProcess):
    rows, cols = len(board), len(board[0])
    vertices = [[DijkstraVertex((x, y)) for x in range(cols)] for y in range(rows)]
    
    for row in vertices:
        for col in row:
            col.edges = find_edges(board, vertices, col)
    
    start_vertex = vertices[start_pos[1]][start_pos[0]]
    start_vertex.dist = 0
    end_vertex = vertices[end_pos[1]][end_pos[0]]
    
    pq = queue.PriorityQueue()
    pq.put(start_vertex)
    
    path = [start_pos]
    was_here = [start_pos]
    while not pq.empty():
        current = pq.get()
        
        if current.visited:
            continue
        current.visited = True
        
        was_here.append((current.x, current.y))
        
        if current == end_vertex:
            while current.parent:
                path.append((current.x, current.y))
                current = current.parent
            path.append((current.x, current.y))
            break
        
        for neighbor in current.edges:
            new_dist = current.dist + 1
            if new_dist < neighbor.dist:
                neighbor.dist = new_dist
                neighbor.parent = current
                pq.put(neighbor)
        
        if showProcess:
            main_draw(WIN, board, [], was_here)
            clock.tick(FPS)
    main_draw(WIN, board, path, was_here)


def a_star_search(WIN, clock, board, start_pos, end_pos, showProcess):
    rows, cols = len(board), len(board[0])
    vertices = [[AstarVertex((x, y)) for x in range(cols)] for y in range(rows)]
    
    startVertex = vertices[start_pos[1]][start_pos[0]]
    startVertex.distance = 0
    endVertex = vertices[end_pos[1]][end_pos[0]]
    
    for row in vertices:
        for col in row:
            col.edges = find_edges(board, vertices, col)
            col.set_heuristic(endVertex)
    
    heap = []
    heapq.heappush(heap, startVertex)
    path = []
    was_here = []
    
    while heap:
        current = heapq.heappop(heap)
        
        if current.visited:
            continue
        current.visited = True
        
        was_here.append((current.x, current.y))
        
        if current == endVertex:
            while current:
                path.append((current.x, current.y))
                current = current.parent
            break
        
        for edge in current.edges:
            cost = current.distance + 1
            heuristic = edge.heuristic
            if cost < edge.distance:
                edge.distance = cost
                edge.parent = current
                edge.heuristic = heuristic
                heapq.heappush(heap, edge)
        
        if showProcess:
            clock.tick(FPS)
            main_draw(WIN, board, [], was_here)
    main_draw(WIN, board, path, was_here)


def main():
    # set board width and height / +2 because I add borders around the board
    boardWidth, boardHeight = SETTINGS["width"]+2, SETTINGS["height"]+2
    board = [[" " for j in range(boardWidth)] for i in range(boardHeight)]
    
    # variable to select the start and end position
    drawMaze = SETTINGS["drawMaze"]
    showProcess = SETTINGS["showProcess"]
    
    global TILE_WIDTH
    global TILE_HEIGHT
    TILE_WIDTH, TILE_HEIGHT = WIDTH / boardWidth, HEIGHT / boardHeight
    
    # set board borders as walls
    for i in range(boardHeight):
        for j in range(boardWidth):
            if i == 0 or i == boardHeight - 1 or j == 0 or j == boardWidth - 1:
                board[i][j] = '#'
    
    # pygame essentials
    clock = pygame.time.Clock()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("PATHFINDING ALGORITHM")
    
    start_pos, end_pos = None, None
    
    # if drawMaze is set to "randomize" the random tiles are set as walls
    if drawMaze == "randomize":
        for i in range(1, boardHeight - 1):
            for j in range(1, boardHeight - 1):
                board[i][j] = choices((' ', '#'), weights=(2, 1))[0]
        
        # set random start and end pos
        start_pos = (randint(1, boardWidth - 2), randint(1, boardHeight - 2))
        end_pos = (randint(1, boardWidth - 2), randint(1, boardHeight - 2))
        
        while start_pos == end_pos:
            end_pos = (randint(1, boardWidth - 2), randint(1, boardHeight - 2))
        
        board[start_pos[1]][start_pos[0]] = 'O'
        board[end_pos[1]][end_pos[0]] = 'X'
    
    # if drawMaze is set to "draw" the user chooses start -> end -> walls
    elif drawMaze == "draw":
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            draw_at_the_start(board, WIN)
            # print texts on screen
            if start_pos == None:
                select_pos_text(WIN, "Select a start tile (O)")
            elif end_pos == None:
                select_pos_text(WIN, "Select an end tile (X)")
            else:
                button_pos = start_button(WIN)
            
            # check where mouse was clicked
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                
                if start_pos == None:
                    start_pos = mouse_pressed(pos, board, 'O')
                elif end_pos == None:
                    end_pos = mouse_pressed(pos, board, 'X')
                else:
                    if button_pos[0] < pos[0] < button_pos[2] and button_pos[1] < pos[1] < button_pos[3]:
                        break
                    mouse_pressed(pos, board, '#')
            pygame.display.update()
            clock.tick(60)
    
    # if drawMaze is set to "file" program chooses a random file to load the maze from
    elif drawMaze == "file":
        board, start_pos, end_pos = load_maze_from_file()
        boardWidth, boardHeight = len(board[0]), len(board)
        TILE_WIDTH, TILE_HEIGHT = WIDTH / boardWidth, HEIGHT / boardHeight
    
    # print the board before algorithms
    main_draw(WIN, board, [], [])
    
    # First In Last Out / breadth first search
    if SETTINGS["chooseAlgorithm"] == "breadth first":
        breadth_first_search(WIN, clock, board, start_pos, end_pos, showProcess)
    
    # First In First Out / depth first search
    elif SETTINGS["chooseAlgorithm"] == "depth first":
        depth_first_search(WIN, clock, board, start_pos, end_pos, showProcess)
    
    # dijkstra search
    elif SETTINGS["chooseAlgorithm"] == "dijkstra":
        dijkstra_search(WIN, clock, board, start_pos, end_pos, showProcess)
    
    # A* search
    elif SETTINGS["chooseAlgorithm"] == "a*":
        a_star_search(WIN, clock, board, start_pos, end_pos, showProcess)
    
    # to stop the program from exiting after the algorithm
    while True:
        event = pygame.event.wait()
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            break
    pygame.quit()


if __name__ == "__main__":
    settings()
    main()