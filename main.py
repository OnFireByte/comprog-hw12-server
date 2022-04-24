from fastapi import FastAPI, Response
from fastapi.responses import FileResponse, RedirectResponse

import numpy as np
import random

from utils.func_randomizer import *


TEST_COUNT = 10
API_VERSION = "1.0.0"


app = FastAPI()
favicon_path = "favicon.ico"


@app.get("/")
def go_to_random_seed():
    random_seed = random.randint(0, 2 ** 32 - 1)
    return RedirectResponse(url=f"/{random_seed}")


@app.get("/test_file")
def serve_test_file():
    return FileResponse("public/test.py")


@app.get("/favicon.ico")
async def serve_favicon():
    return FileResponse(favicon_path)


@app.get("/{seed}")
def get_random_test_by_seed(seed: int, response: Response):
    response.headers["api-version"] = API_VERSION

    if seed >= 2 ** 32 - 1:
        return {"error": "seed is too large, maximum is 2**32 -1"}

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
