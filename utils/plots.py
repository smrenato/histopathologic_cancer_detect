from math import ceil, sqrt
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer, SilhouetteVisualizer

from .func import _get_rgb_pixels


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


dim_y = dim_x = lambda sample_size: ceil(sqrt(sample_size))


def plot_histogram(
    labels_train_path: Path, samples: list[Path], title: str
) -> None:
    sample_size = len(samples)
    name_ids = [
        str(sample_path).split('/')[-1].split('.')[0]
        for sample_path in samples
    ]

    labels_train_df = pd.read_csv(labels_train_path)

    labels = labels_train_df[labels_train_df['id'].isin(name_ids)][
        'label'
    ].tolist()

    plt.figure(figsize=(10, 10))
    plt.suptitle(title)
    for i, file in enumerate(samples):
        img = Image.open(file)
        pixels = _get_rgb_pixels(img)
        plt.subplot(dim_x(sample_size), dim_y(sample_size), i + 1)
        plt.plot(list(range(0, 256)), pixels['R'], color='red')
        plt.plot(list(range(0, 256)), pixels['G'], color='green')
        plt.plot(list(range(0, 256)), pixels['B'], color='blue')
        plt.title('{} - {}'.format(i, labels[i]))

    plt.tight_layout()
    plt.show()


def plot_imgs_from_histograms(samples: list[Path], title: str):
    sample_size = len(samples)

    plt.figure(figsize=(10, 10))
    plt.suptitle(title)
    for i, file in enumerate(samples):
        img = Image.open(file)
        plt.subplot(dim_x(sample_size), dim_y(sample_size), i + 1)
        plt.imshow(img)
        plt.title(f'{i}')
        plt.axis('off')

    plt.tight_layout()
    plt.show()


def plot_silhouette(
    clusters: list | np.ndarray,
    feature_matrix: pd.DataFrame,
) -> None:
    plt.figure(figsize=(8, 12))
    plt.suptitle('Silhouette Plot')
    for i, cluster in enumerate(clusters, start=1):
        km = KMeans(
            n_clusters=cluster,
            init='k-means++',
            n_init=10,
            max_iter=100,
            random_state=42,
        )
        plt.subplot(5, 2, i)
        visualizer = SilhouetteVisualizer(km, colors='yellowbrick')
        visualizer.fit(feature_matrix)
        plt.title(f'Clusters: {cluster}')

    plt.tight_layout()
    plt.show()


def plot_elbow(
    clusters: list | np.ndarray,
    feature_matrix: pd.DataFrame,
) -> None:
    km = KMeans(init='k-means++', n_init=10, max_iter=100, random_state=42)
    visualizer = KElbowVisualizer(km, k=clusters)
    visualizer.fit(feature_matrix)
    plt.title('Elbow Plot')
