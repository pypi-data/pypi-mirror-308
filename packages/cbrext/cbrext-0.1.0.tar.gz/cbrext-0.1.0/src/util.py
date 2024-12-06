import os
import glob

def make_dir(dir_path: str):
    os.makedirs(dir_path, exist_ok=True)


def get_files_from_dir(dir_path: str) -> list:
    return glob.glob(f"{dir_path}/*.pcap*")


def hex_to_bin(hex_str: str, delimiter: str = "") -> str:
    hex_to_bin_dict = {
        '0': [0, 0, 0, 0],
        '1': [0, 0, 0, 1],
        '2': [0, 0, 1, 0],
        '3': [0, 0, 1, 1],
        '4': [0, 1, 0, 0],
        '5': [0, 1, 0, 1],
        '6': [0, 0, 1, 1],
        '7': [0, 1, 1, 1],
        '8': [1, 0, 0, 0],
        '9': [1, 0, 0, 1],
        'a': [1, 0, 1, 0],
        'b': [1, 0, 1, 1],
        'c': [1, 1, 0, 0],
        'd': [1, 1, 0, 1],
        'e': [1, 1, 1, 0],
        'f': [1, 1, 1, 1],
        ':': []
    }
    
    bin_list = []
    for char in hex_str:
        bin_list.extend(hex_to_bin_dict[char])

    return delimiter.join(map(str, bin_list))


def save_json(file_path: str, data: dict):
    pass


def save_csv(file_path: str, data: dict):
    pass