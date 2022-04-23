from main import *


class test:
    def __init__(self):
        self.kept = []

    def keep(self, e):
        self.kept.append(e)

    def test_get_score(self):
        board = array(
            [
                [0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0],
                [0, 2, 0, 1, 0],
                [0, 2, 0, 1, 1],
                [4, 2, 2, 5, 5],
                [4, 4, 2, 5, 5],
                [1, 4, 2, 0, 3],
                [1, 1, 2, 3, 3],
            ]
        )
        self.keep(get_score(board))

        board = array(
            [
                [0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0],
                [0, 2, 0, 0, 2],
                [0, 2, 0, 0, 2],
                [3, 2, 2, 0, 2],
                [3, 3, 2, 0, 2],
                [1, 0, 2, 3, 3],
                [1, 1, 2, 3, 0],
            ]
        )
        self.keep(get_score(board))

    def test_get_time_cap(self):
        board = array(
            [
                [0, 0, 0, 0, 0],
                [0, 2, 0, 0, 0],
                [0, 2, 0, 0, 0],
                [0, 2, 0, 0, 2],
                [0, 2, 0, 0, 2],
                [3, 3, 2, 0, 2],
                [3, 3, 2, 0, 2],
                [1, 1, 2, 3, 0],
            ]
        )
        time_caps = [120, 180, 240, 300]
        self.keep(get_time_cap(board, time_caps))

        board = array(
            [
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 1, 0, 0, 2],
                [3, 1, 2, 0, 2],
                [3, 3, 2, 0, 2],
                [1, 1, 2, 0, 2],
            ]
        )
        time_caps = [120, 180, 240, 300]
        self.keep(get_time_cap(board, time_caps))

        board = array(
            [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        )
        time_caps = [120, 180]
        self.keep(get_time_cap(board, time_caps))

    def test_rotate_right_1(self):
        shape = array([[1, 1, 1], [0, 0, 1]])
        self.keep(rotate_right(shape))

    def test_rotate_right_2(self):
        shape = array([[1, 2, 3, 4]])
        self.keep(rotate_right(shape))

    def test_rotate_left_1(self):
        shape = array([[1, 1, 1], [0, 0, 1]])
        self.keep(rotate_left(shape))

    def test_rotate_left_2(self):
        shape = array([[1, 2, 3, 4]])
        self.keep(rotate_left(shape))

    def test_animate_drop_1(self):
        board = array([[4, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0]])
        shape = array([[2, 2, 2]])
        c = 1
        self.keep(animate_drop(board, shape, c))

    def test_animate_drop_2(self):
        board = array([[4, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0]])

        shape = array([[2, 2, 2]])
        c = 0
        self.keep(animate_drop(board, shape, c))

    def test_animate_clear_1(self):
        board = array(
            [
                [3, 3, 0, 0],
                [2, 2, 2, 6],
                [0, 5, 5, 4],
                [7, 7, 7, 6],
                [0, 0, 0, 0],
                [4, 0, 1, 1],
            ]
        )
        self.keep(animate_clear(board))

    def test_animate_clear_2(self):
        board = array([[0, 0, 0, 0, 0], [2, 0, 0, 0, 0], [2, 3, 3, 4, 4]])
        self.keep(animate_clear(board))

    def test_animate_clear_3(self):
        board = array([[3, 0, 0, 0, 2], [3, 0, 4, 0, 2], [4, 4, 4, 0, 2]])
        self.keep(animate_clear(board))


from io import StringIO
from contextlib import redirect_stdout
from numpy import array, ndarray, array_equal
from pprint import pformat


def eq(sol, stu):
    if isinstance(sol, ndarray) and isinstance(stu, ndarray):
        return array_equal(sol, stu)
    if isinstance(sol, ndarray) or isinstance(stu, ndarray):
        return False
    if isinstance(sol, (tuple, list)) and isinstance(stu, (tuple, list)):
        if type(sol) != type(stu) or len(sol) != len(stu):
            return False
        for a, b in zip(sol, stu):
            if not eq(a, b):
                return False
        return True
    return sol == stu


def pp(label, s):
    ps = pformat(s, width=20)[1:-1].splitlines(True)
    for n, e in enumerate(ps[0], 1):
        if e != "[":
            break
    t = ps[0]
    for line in ps[1:]:
        k = 0 if "array" in line else n
        t += " " * (k + len(label)) + line
    print(label, t)


def check(testfunc_name, solution_output, stdin_txt="", show_detail=False):
    err = ""
    try:
        buf = StringIO()
        ts = test()
        with redirect_stdout(buf):
            getattr(ts, testfunc_name)()
        _, sol_kept = solution_output
        stu_stdout = buf.getvalue()
        status = "❌" if not eq(sol_kept, ts.kept) else "✅"
        if buf.getvalue():
            raise Exception("Function spec. does not allow any prints")
    except Exception as e:
        status = "❌"
        err = str(e)
    print(status, testfunc_name)
    if "❌" in status and show_detail:
        if err:
            print("    " + err)
        if not eq(sol_kept, ts.kept):
            pp("    solution:", sol_kept)
            pp("    your ans:", ts.kept)


solutions = {
    "test_get_score": ("", [120, 0]),
    "test_get_time_cap": ("", [120, 240, 180]),
    "test_rotate_right_1": ("", [array([[0, 1], [0, 1], [1, 1]])]),
    "test_rotate_right_2": ("", [array([[1], [2], [3], [4]])]),
    "test_rotate_left_1": ("", [array([[1, 1], [1, 0], [1, 0]])]),
    "test_rotate_left_2": ("", [array([[4], [3], [2], [1]])]),
    "test_animate_drop_1": (
        "",
        [
            [
                array([[4, 2, 2, 2], [1, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0]]),
                array([[4, 0, 0, 0], [1, 2, 2, 2], [1, 0, 0, 0], [1, 1, 0, 0]]),
                array([[4, 0, 0, 0], [1, 0, 0, 0], [1, 2, 2, 2], [1, 1, 0, 0]]),
            ]
        ],
    ),
    "test_animate_drop_2": ("", [[]]),
    "test_animate_clear_1": (
        "",
        [
            [
                array(
                    [
                        [3, 3, 0, 0],
                        [0, 0, 0, 0],
                        [0, 5, 5, 4],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [4, 0, 1, 1],
                    ]
                ),
                array(
                    [
                        [0, 0, 0, 0],
                        [3, 3, 0, 0],
                        [0, 0, 0, 0],
                        [0, 5, 5, 4],
                        [0, 0, 0, 0],
                        [4, 0, 1, 1],
                    ]
                ),
                array(
                    [
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [3, 3, 0, 0],
                        [0, 0, 0, 0],
                        [0, 5, 5, 4],
                        [4, 0, 1, 1],
                    ]
                ),
                array(
                    [
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [3, 3, 0, 0],
                        [0, 5, 5, 4],
                        [4, 0, 1, 1],
                    ]
                ),
            ]
        ],
    ),
    "test_animate_clear_2": (
        "",
        [
            [
                array([[0, 0, 0, 0, 0], [2, 0, 0, 0, 0], [0, 0, 0, 0, 0]]),
                array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [2, 0, 0, 0, 0]]),
            ]
        ],
    ),
    "test_animate_clear_3": ("", [[]]),
}
stdin_texts = {}
try:
    for testfunc_name in solutions:
        check(
            testfunc_name,
            solutions[testfunc_name],
            stdin_texts.get(testfunc_name, ""),
            show_detail=True,
        )
    print("WARNING: These are only preliminary tests.")
except Exception as err:
    print(err)
