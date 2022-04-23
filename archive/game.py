# Tetris (*** can't run in Colab ***)

import pygame
import numpy as np

# ----------------------------------------------


def get_score(board):
    col_count = board.shape[1]
    has_block = board > 0
    res = np.sum(has_block, axis=1) == col_count
    return np.sum(res) * 40


def get_time_cap(board, time_caps):
    score_by_time = board.reshape(len(time_caps), -1).sum(axis=1)
    time_caps_array = np.array(time_caps)
    res = time_caps_array[score_by_time > 0]
    return res[0] if res.size > 0 else time_caps[-1]


def rotate_right(shape):
    return shape.T[:, ::-1]


def rotate_left(shape):
    return shape.T[::-1, :]


def animate_drop(board, shape, c):
    time_line = []
    width = shape.shape[1]
    height = shape.shape[0]
    for i in range(board.shape[0]):
        slot = board[i : i + height, c : c + width]
        # is_empty = np.sum()
        if slot.shape != shape.shape:
            break
        is_empty = np.sum(slot[shape > 0]) == 0
        if is_empty:
            new_board = board * 1
            new_board[i : i + height, c : c + width] += shape
            time_line.append(new_board)
        else:
            break
    return time_line


def animate_clear(board):
    cleared_board = board * 1
    is_full = np.sum(board > 0, axis=1) == board.shape[1]
    if np.sum(is_full) == 0:
        return []
    cleared_board[is_full] = np.zeros(board.shape[1])
    floor = cleared_board.shape[0] - 1
    time_line = [cleared_board]
    while floor >= 0:
        is_empty = np.sum(cleared_board[floor] > 0) == 0
        if not is_empty:
            floor -= 1
            continue
        is_empty_above = np.sum(cleared_board[: floor + 1] > 0) == 0
        if is_empty_above:
            break

        new_board = np.zeros(board.shape, int)
        new_board[floor + 1 :] = cleared_board[floor + 1 :]
        new_board[1 : floor + 1] = cleared_board[:floor]
        cleared_board = new_board * 1
        time_line.append(new_board * 1)
        floor = cleared_board.shape[0] - 1

    return time_line


# ----------------------------------------------
def make_shape():
    # shape width >= shape height
    s = [
        [[1, 1, 1], [1, 0, 0]],
        [[2, 2, 2], [0, 0, 2]],
        [[3, 3, 3], [0, 3, 0]],
        [[4, 4, 4, 4]],
        [[5, 5, 0], [0, 5, 5]],
        [[6, 0], [6, 6], [0, 6]],
        [[7, 7], [7, 7]],
    ]
    return np.array(s[np.random.randint(len(s))])


def pgame():
    def draw_rect(e, r, c, dr, dc):
        if e == 0:
            return
        pygame.draw.rect(
            screen, COLORS[e - 1], [30 + (dc + c) * 24, dr + r * 24, 20, 20], 0
        )

    def draw_line(color, c, line_width):
        pygame.draw.line(
            screen,
            color,
            [28 + c * 24, (BOARD_NROWS) * 24 + 96],
            [28 + c * 24, 96],
            line_width,
        )

    def show_text(x, y, size, text):
        font_name = pygame.font.match_font("arial")
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

    BOARD_NCOLS, BOARD_NROWS = 10, 24
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS = 480, 720, 60
    BLACK, GREY, WHITE = (0, 0, 0), (128, 128, 128), (255, 255, 255)
    COLORS = [
        (255, 128, 0),
        (0, 0, 255),
        (255, 0, 255),
        (0, 255, 255),
        (255, 0, 0),
        (0, 255, 0),
        (255, 255, 0),
    ]
    HOW_TO = (
        "Z/X for rotating   "
        + "Right/Left Arrow Key for moving   "
        + "Spacebar for dropping"
    )

    board = np.zeros((BOARD_NROWS, BOARD_NCOLS), dtype=int)
    shape = make_shape()
    column = 3
    score = 0
    time_caps = [3000, 3000, 3000, 3000]
    time = get_time_cap(board, time_caps)

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    end = False
    screen.fill(BLACK)
    while not end:
        frames = [board]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    time = 0  # force the drop
                elif event.key == pygame.K_LEFT:
                    column -= int(column > 0)
                elif event.key == pygame.K_RIGHT:
                    column += int(column < BOARD_NCOLS - len(shape[0]))
                elif event.key == pygame.K_z:
                    shape = rotate_left(shape)
                elif event.key == pygame.K_x:
                    shape = rotate_right(shape)
                column = max(0, min(column, BOARD_NCOLS - len(shape[0])))
        time -= 1
        if time <= 0:
            frames = animate_drop(board, shape, column)
            if frames:
                score += get_score(frames[-1])
                frames += animate_clear(frames[-1])
            else:
                end = True
        for frame in frames:
            screen.fill(BLACK)
            clock.tick(FPS)
            board_row, board_column = board.shape
            shape_row, shape_column = shape.shape
            for r in range(shape_row):
                for c in range(shape_column):
                    draw_rect(shape[r, c], r, c, 20, column)
            for r in range(board_row):
                for c in range(board_column):
                    draw_rect(frame[r, c], r, c, 100, 0)
            for c in range(board_column + 1):
                if column <= c <= column + shape_column:
                    draw_line(WHITE, c, 3)
                else:
                    draw_line(GREY, c, 1)
            show_text(380, 120, 50, "TIME")
            show_text(380, 500, 50, "SCORE")
            show_text(240, 685, 15, HOW_TO)
            show_text(380, 550, 75, str(score))
            show_text(
                380, 180, 150, str(time // FPS) + "." + str((time // (FPS // 10)) % 10)
            )
            pygame.display.flip()
            board = frames[-1]
            if time <= 0:
                shape = make_shape()
                column = max(0, min(column, BOARD_NCOLS - len(shape[0])))
                time = get_time_cap(board, time_caps)

    while True:
        for event in pygame.event.get():
            if (
                event.type == pygame.QUIT
                or event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN
            ):
                pygame.quit()
                return

        screen.fill(BLACK)
        show_text(240, 150, 50, "TOTAL SCORE")
        show_text(240, 250, 200, str(score))
        show_text(240, 550, 25, "press enter to exit the game")
        pygame.display.flip()


pgame()
