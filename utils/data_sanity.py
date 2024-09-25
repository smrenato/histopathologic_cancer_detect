"""
Refactoring this shit code that was made
"""

from pathlib import Path
from types import FunctionType
from typing import Any

import imagehash
from PIL import Image, UnidentifiedImageError

# Sanity check


def get_path_list(path: Path) -> list[Path]:
    """
    @param
    """
    files_path_gen = path.glob('*.*')
    return [file for file in files_path_gen]


def check_imgs(files_list: list[Path]) -> dict[str, Any]:
    img_error = []
    img_modes = []
    img_width = []
    img_height = []
    img_format = []

    for file in files_list:
        try:
            with Image.open(file) as img:
                img_modes.append(img.mode)
                img_width.append(img.width)
                img_height.append(img.height)
                img_format.append(img.format)

        except UnidentifiedImageError:
            img_error.append(file)
    return {
        'img_error': img_error,
        'img_modes': img_modes,
        'img_width': img_width,
        'img_height': img_height,
        'img_format': img_format,
    }


# No use
def get_img_extensions(img_list: list[Path]) -> dict[str, list]:
    ext = [str(file).split('.')[-1] for file in img_list]
    ext = list(set(ext))

    return {'extensions': ext}


# REVIEW: maybe improve this with hamming approach, but not today!
def find_similar_images(
    path_img_list: Path, hash_func: FunctionType = imagehash.average_hash
) -> dict[str, Path]:
    """
    Find similar images based on hash
    """
    hashed_img_dict = {}
    for path_img in path_img_list:
        try:
            img = Image.open(path_img)
            hashed_img = hash_func(img)
            key = str(hashed_img)
            # If the keys doesn't exist, create a new one and add a new list
            hashed_img_dict[key] = hashed_img_dict.get(key, []) + [path_img]

        except UnidentifiedImageError as e:
            raise e

        return hashed_img_dict
