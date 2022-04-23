import numpy as np


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


# board = np.array(
#     [[3, 3, 0, 0], [2, 2, 2, 6], [0, 5, 5, 4], [7, 7, 7, 6], [0, 0, 0, 0], [4, 0, 1, 1]]
# )

# for time in animate_clear(board):
#     print(time)
