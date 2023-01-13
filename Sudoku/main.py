import pygame
from pygame import Rect
import time
from solver import solve, valid, find_empty
from json_functions import read_json
from button_text import Button, WHITE, BLACK, RED, GREEN

pygame.font.init()

WIDTH, HEIGHT = (540, 650)
GRID_R, GRID_C = (9, 9)
GRID_W, GRID_H = (WIDTH, WIDTH)
GRAY = (128, 128, 128)
BOARD_DATA = read_json("board_data.json")
FONT = pygame.font.SysFont("arialrounded", 25)
MOVE_KEYS = [
    pygame.K_UP,
    pygame.K_DOWN,
    pygame.K_LEFT,
    pygame.K_RIGHT,
    pygame.K_w,
    pygame.K_s,
    pygame.K_a,
    pygame.K_d
]
BUTTONS = [
    Button(100, 40, 230, HEIGHT - 50, "Solve", FONT, 1, WHITE, shading=False),
    Button(100, 40, 10, HEIGHT - 50, "Load", FONT, 2, WHITE, shading=False),
    Button(100, 40, 120, HEIGHT - 50, "Hint", FONT, 3, WHITE, shading=False)
]
BTN_CLOSE = Button(40, 40, WIDTH - 50, 10, "X", FONT, 0, RED, shading=False)


class Grid:
    def __init__(self, rows, cols, width, height, name):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.name = name
        self.cubes = [[Cube(BOARD_DATA[name][i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected = None
        self.start_time = time.time()
        self.strikes = 0

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for row in range(self.rows + 1):
            if row % 3 == 0 and row != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, BLACK, (0, row * gap),
                             (self.width, row * gap), thick)
            pygame.draw.line(win, BLACK, (row * gap, 0),
                             (row * gap, self.height), thick)

        # Draw Cubes
        for row in range(self.rows):
            for col in range(self.cols):
                self.cubes[row][col].draw(win)

    def select(self, sel_row, sel_col):
        # Reset all other
        for row in range(self.rows):
            for col in range(self.cols):
                self.cubes[row][col].selected = False
        # Select cell
        self.cubes[sel_row][sel_col].selected = True
        self.selected = (sel_row, sel_col)

    def move_selection(self, pos_selection, event):
        row, col = pos_selection
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            if row:
                self.select(row - 1, col)
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            if row < self.rows - 1:
                self.select(row + 1, col)
        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
            if col:
                self.select(row, col - 1)
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            if col < self.cols - 1:
                self.select(row, col + 1)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_completed(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.cubes[row][col].value == 0:
                    return False
        return True

    def solve_gui(self, win):
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find

        for num in range(1, 10):
            if valid(self.model, num, (row, col)):
                self.model[row][col] = num
                self.cubes[row][col].set(num)
                self.cubes[row][col].draw_change(win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_gui(win):
                    return True

                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(win, False)
                pygame.display.update()
                pygame.time.delay(100)

        return False

    def hint_gui(self):
        if self.selected:
            row, col = self.selected
            self.update_model()
            solve(self.model)
            valid_value = self.model[row][col]
            self.cubes[row][col].set(valid_value)
            self.update_model()


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = FONT.render(str(self.temp), 1, GRAY)
            win.blit(text, (x + 5, y + 5))
        elif not(self.value == 0):
            text = FONT.render(str(self.value), 1, BLACK)
            win.blit(text, (x + (gap / 2 - text.get_width() / 2),
                     y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, RED, (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        pygame.draw.rect(win, WHITE, (x, y, gap, gap), 0)

        text = FONT.render(str(self.value), 1, BLACK)
        win.blit(text, (x + (gap / 2 - text.get_width() / 2),
                 y + (gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def draw_window(win, board: Grid, time, buttons):
    win.fill((255, 255, 255))
    # Draw board name
    text = FONT.render(board.name.upper(), 1, BLACK)
    win.blit(text, (WIDTH - text.get_width() - 10, HEIGHT - 95))
    # Draw time
    text = FONT.render("Time:" + format_time(time), 1, BLACK)
    win.blit(text, (WIDTH - 160, HEIGHT - 45))
    # Draw Strikes
    text = FONT.render("X " * board.strikes, 1, RED)
    win.blit(text, (20, HEIGHT - 95))
    # Draw grid and board
    board.draw(win)
    # Draw buttons
    for btn in buttons:
        if btn.draw_button(win):
            if btn.value == 1:
                board.solve_gui(win)
            if btn.value == 2:
                board = load_screen(win, board)
            if btn.value == 3:
                board.hint_gui()
    return board


def load_screen(win, board):
    win.fill(BLACK)
    btn_load = []
    i = 0
    for name in ["easy", "medium", "hard"]:
        btn_load.append(Button(150, 40, WIDTH // 2 - 50, 100 + (50 * i),
                               name.upper(), FONT, name, WHITE, shading=False))
        i += 1

    name = ""
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
        if BTN_CLOSE.draw_button(win):
            return board
        for btn in btn_load:
            if btn.draw_button(win):
                name = btn.value
                run = False
                break
        pygame.display.update()

    return Grid(GRID_R, GRID_C, GRID_W, GRID_H, name)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    time_str = " " + "".join(["0", str(minute)][len(str(minute)) - 1:]) + \
        ":" + "".join(["0", str(sec)][len(str(sec)) - 1:])
    return time_str


def board_completed(win, time):
    text = FONT.render("Completed in" + format_time(time), 1, WHITE)
    width, height = text.get_width() + 20, text.get_height() + 20
    pygame.draw.rect(win, BLACK, Rect(
        WIDTH // 2 - width // 2 - 10, HEIGHT // 2 - height // 2 - height - 10, width, height))
    win.blit(text, (WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2 - height))

    text = FONT.render("Press any key to continue", 1, WHITE)
    width, height = text.get_width() + 20, text.get_height() + 20
    pygame.draw.rect(win, BLACK, Rect(
        WIDTH // 2 - width // 2 - 10, HEIGHT // 2 - height // 2 - 10, width, height))
    win.blit(text, (WIDTH // 2 - width // 2, HEIGHT // 2 - height // 2))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True


def main():
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku")
    board = Grid(GRID_R, GRID_C, GRID_W, GRID_H, "")
    key = None
    run = True
    while run:

        play_time = round(time.time() - board.start_time)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.unicode.isnumeric() and event.unicode != "0":
                    key = int(event.unicode)
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if board.selected:
                        row, col = board.selected
                        if board.cubes[row][col].temp != 0:
                            if board.place(board.cubes[row][col].temp) == False:
                                board.strikes += 1
                            key = None

                if event.key in MOVE_KEYS:
                    board.move_selection(board.selected, event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.is_completed():
            run = board_completed(WIN, play_time)
            board = Grid(GRID_R, GRID_C, GRID_W, GRID_H, "")

        if board.selected and key != None:
            board.sketch(key)

        board = draw_window(WIN, board, play_time, BUTTONS)
        if board == None:
            run = False
        pygame.display.update()


if __name__ == "__main__":
    main()
pygame.quit()
