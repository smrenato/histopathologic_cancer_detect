import tomllib
from pathlib import Path


def get_conf(conf_path: Path) -> dict:

    with open(conf_path, 'rb') as f:
        data = tomllib.load(f)
    return data
