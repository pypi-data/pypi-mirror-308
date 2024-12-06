# -*- coding: utf-8 -*-

__all__ = ['ConfigurationDetector']

from typing import Tuple, Sequence, MutableSequence, Union
from pathlib import Path

from cmakemake.constants import CONFIGURATION_FILENAME


class ConfigurationDetector:

    def __init__(self, source_dir: Path):
        self.__source_dir: Path = source_dir

    @property
    def source_dir(self) -> Path:
        return self.__source_dir

    def run(self) -> Tuple[Union[Path, None], Union[Sequence[Path], None]]:
        solution_configuration_path = self.source_dir.joinpath(CONFIGURATION_FILENAME)
        if not solution_configuration_path.is_file():
            return None, None

        project_configuration_paths: MutableSequence[Path] = []
        generator = self.source_dir.iterdir()
        for child in generator:
            if child.is_dir():
                self.__detect(child, project_configuration_paths)

        return solution_configuration_path, project_configuration_paths

    def __detect(self, directory: Path, project_configuration_paths: MutableSequence[Path]):
        if not directory.is_dir():
            return
        generator = directory.iterdir()
        for child in generator:
            if child.name == CONFIGURATION_FILENAME:
                project_configuration_paths.append(child)
                return

            if child.is_dir():
                self.__detect(child, project_configuration_paths)
