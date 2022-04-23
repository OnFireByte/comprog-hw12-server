from fastapi import FastAPI, Response
from fastapi.responses import FileResponse

import numpy as np
import random

from utils.func_randomizer import *


TEST_COUNT = 10
API_VERSION = "1.0.0"


app = FastAPI()


@app.get("/")
def default():
    return {"message": "You forgot to add a seed!"}


@app.get("/test_file")
def get_test_file():
    return FileResponse("public/test.py")


@app.get("/{seed}")
def get_random_test_by_seed(seed, response: Response):
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
