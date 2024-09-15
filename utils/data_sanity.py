""" """

from pathlib import Path

from PIL import Image, UnidentifiedImageError


class SanityCheck:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.files_list = self.__get_path__list()
        self.modes_types = []
        self.width = []
        self.height = []

    def __get_path__list(self) -> list[Path]:
        files_path_gen = self.path.glob('*.*')
        return [file for file in files_path_gen]

    def check_corruption(self) -> dict[str, int]:
        error = []
        for file in self.files_list:
            try:
                img = Image.open(file)
                self.modes_types.append(img.mode)
                self.width.append(img.width)
                self.height.append(img.height)

            except UnidentifiedImageError:
                error.append(file)
                print(f'error found on:{file}')

        return {'error': len(error), 'file_error': error}

    def check_typing(self) -> dict[str, list]:
        ext = [str(file).split('.')[-1] for file in self.files_list]
        return {'ext': list(set(ext))}

    def check_dimensions(self) -> dict[str, list]:
        return {
            'width': list(set(self.width)),
            'height': list(set(self.height)),
        }

    def check_mode(self) -> dict[str, list]:
        return {'modes': list(set(self.modes_types))}
