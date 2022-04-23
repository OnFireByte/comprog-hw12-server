import numpy as np
import random

TEST_COUNT = 10
API_VERSION = "1.0.0"


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


from fastapi import FastAPI, Response


app = FastAPI()


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
    not_zero_prob = 0.2
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

    if random.randint(0, 10):
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


@app.get("/")
def default():
    return {"message": "You forgot to add a seed!"}


@app.get("/{seed}")
def read_item(seed, response: Response):
    response.headers["api-version"] = API_VERSION

    try:
        seed = int(seed)
    except ValueError:
        return {"error": "seed must be an integer"}

    random.seed(seed)
    np.random.seed(seed)
    return {
        "get_score": [random_get_score() for _ in range(TEST_COUNT)],
        "get_time_cap": [random_get_time_cap() for _ in range(TEST_COUNT)],
        "rotate_right": [random_rotate_right() for _ in range(TEST_COUNT)],
        "rotate_left": [random_rotate_left() for _ in range(TEST_COUNT)],
        "animate_drop": [random_animate_drop() for _ in range(TEST_COUNT)],
        "animate_clear": [random_animate_clear() for _ in range(TEST_COUNT)],
    }
