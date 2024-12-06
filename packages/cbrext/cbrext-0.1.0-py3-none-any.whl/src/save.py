import json
import pandas as pd
from src.util import hex_to_bin


def save_json(save_path, values, binary=False):
    if binary:
        tmp = []
        for value in values:
            tmp.append(hex_to_bin(value, ","))
        values = tmp

    with open(save_path, "w") as f:
        json.dump(values, f, indent=4)


def save_csv(save_path, values, binary=False):
    if binary:
        tmp = []
        for value in values:
            tmp.append(hex_to_bin(value, ","))
        values = tmp
    df = pd.DataFrame(values)
    df.to_csv(save_path, index=False)
