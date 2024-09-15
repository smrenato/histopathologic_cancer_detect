from math import ceil, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image


class PixelsVerify:
    def __init__(self, path: Path, labels_path: Path) -> None:
        self.train_path = path
        self.labels_train_df = pd.read_csv(labels_path)
        self.files = self.__get_path_list()
        self.samples = []
        # TODO: fix this later
        self.dimensions = None

    def __get_path_list(self) -> list[Path]:
        files_path_gen = self.train_path.glob('*.*')
        return [file for file in files_path_gen]

    def __set_samples_and_dim(self, sample_size: int) -> None:
        self.samples = np.random.choice(self.files, sample_size)
        self.dimensions = ceil(sqrt(sample_size))

    def __get_rgb_pixels(self, image) -> dict[str, list]:
        pixels = image.histogram()
        p_r = pixels[:256]
        p_g = pixels[256:512]
        p_b = pixels[512:]
        return {
            'R': p_r,
            'G': p_g,
            'B': p_b,
        }

    def plot_histogram(self, sample_size: int) -> None:
        self.__set_samples_and_dim(sample_size)  # set dimensions

        name_ids = [
            str(sample_path).split('/')[-1].split('.')[0]
            for sample_path in self.samples
        ]

        labels = self.labels_train_df[
            self.labels_train_df['id'].isin(name_ids)
        ]['label'].tolist()

        plt.figure(figsize=(10, 10))
        plt.suptitle('Histogram from random samples')

        for i, file in enumerate(self.samples):
            img = Image.open(file)
            pixels = self.__get_rgb_pixels(img)

            plt.subplot(self.dimensions, self.dimensions, i + 1)
            plt.plot(list(range(0, 256)), pixels['R'], color='red')
            plt.plot(list(range(0, 256)), pixels['G'], color='green')
            plt.plot(list(range(0, 256)), pixels['B'], color='blue')

            plt.title('{} - {}'.format(i, labels[i]))

        plt.tight_layout()
        plt.show()

    def plot_images_from_histogram(self) -> None:
        plt.figure(figsize=(10, 10))
        plt.suptitle('Images from radom samples')
        for i, file in enumerate(self.samples):
            img = Image.open(file)
            plt.subplot(self.dimensions, self.dimensions,i + 1)
            plt.imshow(img)
            plt.title(f'{i}')
            plt.axis('off')

        plt.tight_layout()
        plt.show()
