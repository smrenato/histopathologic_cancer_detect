from math import ceil, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def plot_img(path: Path, figure_size: tuple[int, int], title: str) -> None:
    """
    Plot a single image
    """
    plt.figure(figsize=figure_size)
    plt.suptitle(title)
    img = Image.open(path)
    plt.imshow(img)
    plt.axis('off')


def plot_images_on_grid(
    path: Path, sample_size: int, title: str = 'Images plot'
) -> None:
    """
    @param path:Path -> take a path to image dir
    @param sample_size -> size of rando sample from the image set
    """
    sample = np.random.choice(path, sample_size)

    # adaptable grid
    plot_dim = ceil(sqrt(sample_size))
    plt.figure(figsize=(10, 10))
    plt.suptitle(title)
    for i, file in enumerate(sample):
        img = Image.open(file)
        plt.subplot(plot_dim, plot_dim, i + 1)
        plt.imshow(img)
        plt.axis('off')

    plt.tight_layout()
    plt.show()
