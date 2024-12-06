# -*- coding: utf-8 -*-

import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Sequence, MutableSet

from cmakemake.concepts import ProjectConfiguration


class FileFilter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def filter(self, configuration: ProjectConfiguration, file_path: Path) -> bool:
        pass


class ExtensionFilter(FileFilter):

    def __init__(self, ignored_extensions: Sequence[str]):
        super().__init__()
        self.__ignored_extensions: MutableSet[str] = set()

        for ignored_extension in ignored_extensions:
            self.add_extension(ignored_extension)

    def add_extension(self, extension: str):
        if not isinstance(extension, str) or len(extension) == 0:
            return
        self.__ignored_extensions.add(extension.lower())

    def filter(self, configuration: ProjectConfiguration, file_path: Path) -> bool:
        if not file_path.is_file():
            return False
        _, extension = os.path.splitext(file_path.name)
        return extension.lower() not in self.__ignored_extensions
