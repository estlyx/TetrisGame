import copy
import pygame
import random


pygame.init()


# init consts
ROWS = 21
COLS = 11
DIS_WIDTH = 250
DIS_HEIGHT = 500
CELL_WIDTH = DIS_WIDTH / (COLS - 1)
CELL_HEIGHT = DIS_HEIGHT / (ROWS - 1)

BLACK = (0, 0, 0)
BLUE = (50, 153, 213)
WHITE = (255, 255, 255)
GRAY = (190, 190, 190)

DIS = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption("Tetris")
CLOCK = pygame.time.Clock()
FPS = 60


def init_grid():
    grid = []

    for i in range(COLS):
        grid.append([])
        for j in range(ROWS):
            grid[i].append([1])

    for i in range(COLS):
        for j in range(ROWS):
            # добавляем ещё два параметра: создаём область прямоугольника и задаём цвет для каждой ячейки
            grid[i][j].append(pygame.Rect(i * CELL_WIDTH, j * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
            grid[i][j].append(pygame.Color(*GRAY, 100))

    return grid


def init_details():
    details = [
        # LINE
        [[-2, 0], [-1, 0], [0, 0], [1, 0]],
        # L
        [[-1, 1], [-1, 0], [0, 0], [1, 0]],
        # reverse L
        [[1, 1], [-1, 0], [0, 0], [1, 0]],
        # SQUARE
        [[-1, 1], [0, 1], [0, 0], [-1, 0]],
        # Z
        [[1, 0], [1, 1], [0, 0], [-1, 0]],
        # reverse Z
        [[0, 1], [-1, 0], [0, 0], [1, 0]],
        # T
        [[-1, 1], [0, 1], [0, 0], [1, 0]],
    ]

    det = [[], [], [], [], [], [], []]
    for i in range(len(details)):
        for j in range(4):
            # создаём прямоугольные области для каждого составного квадрата
            det[i].append(
                pygame.Rect(
                    details[i][j][0] * CELL_WIDTH + CELL_WIDTH * (COLS // 2),
                    details[i][j][1] * CELL_HEIGHT,
                    CELL_WIDTH,
                    CELL_HEIGHT,
                )
            )

    return det


def game_loop():
    grid = init_grid()
    det = init_details()

    detail = pygame.Rect(0, 0, CELL_WIDTH, CELL_HEIGHT)
    det_choice = copy.deepcopy(random.choice(det))
    count = 0
    game = True
    rotate = False

    while game:
        delta_x = 0
        delta_y = 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    delta_x = -1
                elif event.key == pygame.K_RIGHT:
                    delta_x = 1
                elif event.key == pygame.K_UP:
                    rotate = True

        # speed up
        key = pygame.key.get_pressed()
        if key[pygame.K_DOWN]:
            count = 31 * FPS

        DIS.fill(pygame.Color(*BLUE, 100))

        # game field
        for i in range(COLS):
            for j in range(ROWS):
                pygame.draw.rect(DIS, grid[i][j][2], grid[i][j][1], grid[i][j][0])

        for i in range(4):
            if (det_choice[i].x + delta_x * CELL_WIDTH < 0) or (det_choice[i].x + delta_x * CELL_WIDTH >= DIS_WIDTH):
                delta_x = 0

            if ((det_choice[i].y + CELL_HEIGHT >= DIS_HEIGHT) or (
                    grid[int(det_choice[i].x // CELL_WIDTH)][int(det_choice[i].y // CELL_HEIGHT) + 1][0] == 0)):
                delta_y = 0

                for j in range(4):
                    x = int(det_choice[j].x // CELL_WIDTH)
                    y = int(det_choice[j].y // CELL_HEIGHT)
                    grid[x][y][0] = 0
                    # change detail color
                    grid[x][y][2] = pygame.Color(*BLACK, 100)

                detail.x = 0
                detail.y = 0
                det_choice = copy.deepcopy(random.choice(det))

        # move horizontally
        for i in range(4):
            det_choice[i].x += delta_x * CELL_WIDTH

        count += FPS

        # move vertically
        if count > 30 * FPS:
            for i in range(4):
                det_choice[i].y += delta_y * CELL_HEIGHT
            count = 0

        # current
        for i in range(4):
            detail.x = det_choice[i].x
            detail.y = det_choice[i].y
            pygame.draw.rect(DIS, pygame.Color(*WHITE, 100), detail)

        # rotate if needed
        det_middle = det_choice[2]
        if rotate:
            for i in range(4):
                x = det_choice[i].y - det_middle.y
                y = det_choice[i].x - det_middle.x
                det_choice[i].x = det_middle.x - x
                det_choice[i].y = det_middle.y + y
            rotate = False

        # delete full rows
        for j in range(ROWS - 1, -1, -1):
            count_cells = 0
            for i in range(COLS):
                if grid[i][j][0] == 1:
                    break
                count_cells += 1

            if count_cells == (COLS - 1):
                for l in range(COLS):
                    grid[l][0][0] = 1
                for k in range(j, -1, -1):
                    for l in range(COLS):
                        grid[l][k][0] = grid[l][k - 1][0]  # move rows down

        pygame.display.flip()
        CLOCK.tick(FPS)



if __name__ == '__main__':
    game_loop()
