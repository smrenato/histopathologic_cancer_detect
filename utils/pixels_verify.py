from math import ceil, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def get_samples(sample_size: int, files_list: Path) -> tuple[list, int]:
    samples = np.random.choice(files_list, sample_size)

    return samples


dim_y = dim_x = lambda sample_size: ceil(sqrt(sample_size))


def _get_rgb_pixels(image: Image) -> dict[str, list]:  # noqa: PLR6301
    pixels = image.histogram()  # A list of pixel concateneted
    p_r = pixels[:256]
    p_g = pixels[256:512]
    p_b = pixels[512:]

    return {
        'R': p_r,
        'G': p_g,
        'B': p_b,
    }


def plot_histogram(sample_size: int) -> None:
    samples = get_samples(sample_size)

    # FIXME: get names id and labels on a easy form
    # name_ids = [
    #     str(sample_path).split('/')[-1].split('.')[0]
    #     for sample_path in samples
    # ]

    # labels = self.labels_train_df[self.labels_train_df['id'].isin(name_ids)][
    #     'label'
    # ].tolist()

    plt.figure(figsize=(10, 10))
    plt.suptitle('Histogram from random samples')
    for i, file in enumerate(samples):
        img = Image.open(file)
        pixels = _get_rgb_pixels(img)

        plt.subplot(dim_x(sample_size), dim_y(sample_size), i + 1)
        plt.plot(list(range(0, 256)), pixels['R'], color='red')
        plt.plot(list(range(0, 256)), pixels['G'], color='green')
        plt.plot(list(range(0, 256)), pixels['B'], color='blue')

        # plt.title('{} - {}'.format(i, labels[i]))

    plt.tight_layout()
    plt.show()
