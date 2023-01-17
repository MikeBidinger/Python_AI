import queue
import pygame
from pygame.locals import Rect
from maze.constants import *
from maze.json_functions import read_json
from os.path import join


class Maze():
    def __init__(self, maze_data):
        self.data = maze_data
        self.blocks = []
        self.blocks = [[Block(self.data[y][x], x, y)
                        for x in range(len(self.data[0]))]
                       for y in range(len(self.data))]

    def draw(self, surface, width, height):
        # Draw blocks
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                self.blocks[y][x].draw(surface)
        # Draw gridlines
        for y in range(1, len(self.data)):
            pygame.draw.line(surface, GRAY, (0, y * BLOCK_H),
                             (width, y * BLOCK_H))
            for x in range(1, len(self.data[0])):
                pygame.draw.line(
                    surface, GRAY, (x * BLOCK_W, 0), (x * BLOCK_W, height))


class Block():
    def __init__(self, value, x, y):
        if value == 0:
            self.color = BLACK
        elif value == 1:
            self.color = WHITE
        elif value == 2:
            self.color = GREEN
        elif value == 3:
            self.color = RED
        elif value == 4:
            self.color = BLUE
        self.rect = Rect(x * BLOCK_W, y * BLOCK_H, BLOCK_W, BLOCK_H)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


def printMaze(maze, path=""):
    for x, pos in enumerate(maze.data[0]):
        if pos == 2:
            start = x
    i = start
    j = 0
    pos = set()
    for move in path:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
        pos.add((j, i))
    for j, row in enumerate(maze.data):
        for i, col in enumerate(row):
            if (j, i) in pos:
                print("+ ", end="")
            else:
                print(str(col) + " ", end="")
        print()


def valid(maze, moves):
    for x, pos in enumerate(maze.data[0]):
        if pos == 2:
            start = x
    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
        if not(0 <= i < len(maze.data[0]) and 0 <= j < len(maze.data)):
            return False
        elif (maze.data[j][i] == 0):
            return False
    return True


def find_end(maze, moves):
    for x, pos in enumerate(maze.data[0]):
        if pos == 2:
            start = x
    i = start
    j = 0
    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
    if maze.data[j][i] == 3:
        print("Found: " + moves)
        # printMaze(maze, moves)
        return moves
    return None


def display_text(surface, text):
    text_img = FONT.render(text, 1, WHITE)
    rect = text_img.get_rect()
    pos = (surface.get_width() // 2 - rect.centerx,
           surface.get_height() // 2 - rect.centery)
    pygame.draw.rect(surface, BLACK, Rect(pos, (rect.width, rect.height)))
    surface.blit(text_img, pos)
    pygame.display.update()


def find_path(maze, surface):
    display_text(surface, "Searching path...")
    nums = queue.Queue()
    nums.put("")
    add = ""
    while True:
        moves = find_end(maze, add)
        if moves != None:
            return moves
        add = nums.get()
        # print(add)
        for j in ["L", "R", "U", "D"]:
            put = add + j
            if valid(maze, put):
                nums.put(put)


def draw_path(maze, moves):
    for x, pos in enumerate(maze.data[0]):
        if pos == 2:
            start = x
    i = start
    j = 0
    pos = set()
    for move in moves:
        if move == "L":
            i -= 1
        elif move == "R":
            i += 1
        elif move == "U":
            j -= 1
        elif move == "D":
            j += 1
        pos.add((j, i))
    for j, row in enumerate(maze.data):
        for i, col in enumerate(row):
            if (j, i) in pos:
                maze.data[j][i] = 4


def main():
    maze = Maze(read_json(join("maze", "maze_data.json"))["maze_2"])

    WIDTH, HEIGHT = (len(maze.data[0]) * BLOCK_W, len(maze.data) * BLOCK_H)
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze")

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    moves = find_path(maze, WIN)
                    draw_path(maze, moves)
                    maze = Maze(maze.data)

        maze.draw(WIN, WIDTH, HEIGHT)

        pygame.display.update()


if __name__ == "__main__":
    main()
pygame.quit()
