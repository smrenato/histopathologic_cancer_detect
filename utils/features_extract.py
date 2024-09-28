from pathlib import Path

import torch
from PIL import Image
from torch.nn import Module
from torchvision import transforms


def get_transformers(center_crop: int = 32, resize: int = 448) -> list:
    transfomers = transforms.Compose([
        transforms.CenterCrop(center_crop),
        transforms.Resize(resize),
        transforms.ToTensor(),
    ])
    return transfomers


def get_feature(
    img_path: Path,
    transformers,
    model: Module,
    device: str = 'cuda',
) -> list:
    """
    return: extract feture for each image given
    """
    img = Image.open(img_path)
    img = transformers(img)
    img = img.reshape(1, 3, 448, 448)
    img = img.to(device)

    with torch.no_grad():
        img_feature = model(img)
    return img_feature


# WARNING: it's will take a long time to execute
def get_images_features(
    model: Module,
    files_list: list[Path],
    transformers: list,
    device: str = 'cuda',
) -> list:
    features = []

    for _, file in enumerate(files_list):
        img = Image.open(file)
        img = transformers(img)
        img = img.reshape(1, 3, 448, 448)
        img = img.to(device)

        with torch.no_grad():
            img_feature = model(img)
            features.append(img_feature)

    return features
