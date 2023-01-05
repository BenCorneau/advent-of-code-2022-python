from typing import Iterable
import os
import shutil


def read_lines(file:str, strip=True)->Iterable[str]:
    with open(file, encoding="utf8") as f:
        for line in f.readlines():
            if strip:
                yield line.strip()
            else:
                yield line.rstrip("\n")


def clean_dir(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
