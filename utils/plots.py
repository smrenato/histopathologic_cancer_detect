from math import ceil, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def plot_images_on_grid(path: Path, sample_size: int):
    files_path = path.glob('*.*')
    files_list = [file for file in files_path]

    sample = np.random.choice(files_list, sample_size)

    # adaptable grid
    plot_dim = ceil(sqrt(sample_size))
    plt.figure(figsize=(10, 10))
    plt.suptitle('Database images')
    for i, file in enumerate(sample):
        img = Image.open(file)
        plt.subplot(plot_dim, plot_dim, i + 1)
        plt.imshow(img)
        plt.axis('off')

    plt.tight_layout()
    plt.show()
