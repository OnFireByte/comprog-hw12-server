import random
import numpy as np
from utils.func import *


def create_board(board_width, board_height, p=None):
    return np.random.choice(
        6,
        size=(board_height, board_width),
        p=p,
    )


def random_get_score():

    board_width = random.randint(4, 8)
    board_height = random.randint(6, 10)
    board = np.random.randint(
        6,
        size=(board_height, board_width),
    )
    return {"input": [board.tolist()], "expect": int(get_score(board))}


def divisor(n):
    return [i for i in range(2, n + 1) if n % i == 0]


def random_get_time_cap():
    not_zero_prob = 0.5
    board_width = random.randint(4, 8)
    board_height = random.randint(6, 10)
    board = create_board(
        board_width, board_height, p=[1 - not_zero_prob] + [not_zero_prob / 5] * 5
    )

    if random.randint(0, 10):
        board[: random.randint(0, board_height - 1), :] = 0

    time_cap = sorted(
        [random.randint(100, 1000) for _ in range(random.choice(divisor(board_height)))]
    )

    return {
        "input": [board.tolist(), time_cap],
        "expect": int(get_time_cap(board, time_cap)),
    }


def random_rotate_right():
    board_width = random.randint(4, 8)
    board_height = random.randint(6, 10)
    board = create_board(board_width, board_height)
    return {
        "input": [board.tolist()],
        "expect": rotate_right(board).tolist(),
    }


def random_rotate_left():
    board_width = random.randint(4, 8)
    board_height = random.randint(6, 10)
    board = create_board(board_width, board_height)
    return {
        "input": [board.tolist()],
        "expect": rotate_left(board).tolist(),
    }


def random_animate_drop():
    not_zero_prob = random.uniform(0.25, 0.5)
    shapes = [
        [[1, 1, 1], [1, 0, 0]],
        [[2, 2, 2], [0, 0, 2]],
        [[3, 3, 3], [0, 3, 0]],
        [[4, 4, 4, 4]],
        [[5, 5, 0], [0, 5, 5]],
        [[6, 0], [6, 6], [0, 6]],
        [[7, 7], [7, 7]],
    ]
    shape = np.array(random.choice(shapes))
    for _ in range(random.randint(0, 3)):
        shape = rotate_right(shape)

    board_width = random.randint(4, 8)
    board_height = random.randint(6, 10)
    board = create_board(
        board_width, board_height, p=[1 - not_zero_prob] + [not_zero_prob / 5] * 5
    )

    if random.randint(0, 4):
        board[: random.randint(0, board_height - 1), :] = 0
    c = random.randint(0, board_width - shape.shape[1])
    return {
        "input": [board.tolist(), shape.tolist(), c],
        "expect": [i.tolist() for i in animate_drop(board, shape, c)],
    }


def random_animate_clear():
    board_width = random.randint(4, 8)
    board_height = random.randint(6, 10)
    board = create_board(board_width, board_height)
    full_floors = [
        random.randint(0, board_height - 1) for _ in range(random.randint(0, 3))
    ]
    for floor in full_floors:
        board[floor] = np.random.randint(1, 6, size=board_width)

    return {
        "input": [board.tolist()],
        "expect": [i.tolist() for i in animate_clear(board)],
    }
