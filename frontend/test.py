import requests, json
import numpy as np
import random
from myfunc import *

# ---- Option -----

# ใส่ seed ที่เป็น int เพื่อล็อค seed
custom_seed = None

# ปรับเป็น True ถ้าอยากเห็นว่า Test ที่ผิดมันมี input และ expect ยังไง
# ปรับเป็น False ถ้าไม่อยากเห็น
verbose = True

# -----------------

seed = random.randint(0, 100000000) if custom_seed is None else custom_seed


url = f"https://onfirebyte.tk/{seed}"

print(f"The seed is {seed}")
print(f"Fetching data from {url}")
response = requests.get(url)
data = json.loads(response.text)
print("-------")


# ----------------------------------
# REMOVE THIS SECTION IF YOU DON'T RUN ON COLAB


def get_codecell(firstline_text):
    from google.colab import _message

    nb = _message.blocking_request("get_ipynb", request="", timeout_sec=5)
    for cell in nb["ipynb"]["cells"]:
        if cell["cell_type"] == "code" and firstline_text in cell["source"][0]:
            return "\n".join(e.rstrip() for e in cell["source"])
    return None


def setup_user_srccode(codecell_firstline):
    from types import CodeType
    from inspect import getsource

    user_srcfile = "$$tmp$$.py"
    src = get_codecell(codecell_firstline)
    if src is None:
        raise Exception("No code found: see the first line of your code.")
    with open(user_srcfile, "w", encoding="utf-8") as f:
        f.write(src)
    try:
        c = compile(src, user_srcfile, mode="exec")
    except:
        raise Exception("Compilation Error: see your code.")
    funcs = [getsource(e) for e in c.co_consts if isinstance(e, CodeType)]
    for f in funcs:
        src = src.replace(f, "")
    tls = ["", ""]
    for line in src.splitlines(True):
        tls[line.startswith("import ") or line.startswith("from ")] += line
    s = tls[1] + "\n" + "\n".join(funcs) + "\n"
    exec(s, globals())


try:
    setup_user_srccode("HW12_NUMPY")
except Exception as err:
    print(err)

# ----------------------------------


def print_test(param, expect):
    if not verbose:
        return
    for i, e in enumerate(param, 1):
        if type(e) == list and type(e[0]) == list:
            print(f"Input {i}:")
            print(np.array(e))
        else:
            print(f"Input {i}: {e}")
    print("\nExpect:")
    if type(expect) == list:
        print(np.array(expect))
    else:
        print(expect)
    print("-------------")


print("get_score's Test:")

for i, test in enumerate(data["get_score"], 1):
    raw_board = test["input"][0]
    try:
        res = get_score(np.array(raw_board))
        if res == np.array(test["expect"]):
            print(f"get_score({i}) passed ✅")
        else:
            print(f"get_score({i}) failed ❌")

    except Exception as e:
        print(f"get_score({i}) failed ❌ with error,", repr(e))
        print_test(test["input"], test["expect"])


print("\nget_time_cap's Test:")

for i, test in enumerate(data["get_time_cap"], 1):
    raw_board, time_cap = test["input"]
    try:
        res = get_time_cap(np.array(raw_board), time_cap)
        if res == test["expect"]:
            print(f"get_time_cap({i}) passed ✅")
        else:
            print(f"get_time_cap({i}) failed ❌")

    except Exception as e:
        print(f"get_time_cap({i}) failed ❌ with error,", repr(e))
        print_test(test["input"], test["expect"])


print("\nrotate_right's Test:")
func = "rotate_right"
for i, test in enumerate(data[func], 1):
    raw_board = test["input"][0]
    try:
        res = eval(func)(np.array(raw_board))
        if [x.tolist() for x in res] == test["expect"]:
            print(f"{func}({i}) passed ✅")
        else:
            print(f"{func}({i}) failed ❌")
            print_test(test["input"], test["expect"])

    except Exception as e:
        print(f"{func}({i}) failed ❌ with error,", repr(e))
        print_test(test["input"], test["expect"])

print("\nrotate_left's Test:")
func = "rotate_left"
for i, test in enumerate(data[func], 1):
    raw_board = test["input"][0]
    try:
        res = eval(func)(np.array(raw_board))
        if [x.tolist() for x in res] == test["expect"]:
            print(f"{func}({i}) passed ✅")
        else:
            print(f"{func}({i}) failed ❌")
            print_test(test["input"], test["expect"])

    except Exception as e:
        print(f"{func}({i}) failed ❌ with error,", repr(e))
        print_test(test["input"], test["expect"])


print("\nanimate_drop's Test:")
func = "animate_drop"
for i, test in enumerate(data[func], 1):
    raw_board, raw_shape, c = test["input"]
    try:
        res = eval(func)(np.array(raw_board), np.array(raw_shape), c)
        if [x.tolist() for x in res] == test["expect"]:
            print(f"{func}({i}) passed ✅")
        else:
            print(f"{func}({i}) failed ❌")
            print_test(test["input"], test["expect"])

    except Exception as e:
        print(f"{func}({i}) failed ❌ with error,", repr(e))
        print_test(test["input"], test["expect"])


print("\nanimate_clear's Test:")
func = "animate_clear"
for i, test in enumerate(data[func], 1):
    raw_board = test["input"][0]
    try:
        res = eval(func)(np.array(raw_board))
        if [x.tolist() for x in res] == test["expect"]:
            print(f"{func}({i}) passed ✅")
        else:
            print(f"{func}({i}) failed ❌")
            print_test(test["input"], test["expect"])

    except Exception as e:
        print(f"{func}({i}) failed ❌ with error,", repr(e))
        print_test(test["input"], test["expect"])
