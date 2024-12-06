# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from pathlib import Path

from cmakemake.concepts import ProjectConfiguration, ProjectType
from cmakemake.constants import CURRENT_DIR_STR
from cmakemake.utils import stringify_path


class PublicPredictor(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def predict(self, configuration: ProjectConfiguration, directory: Path) -> bool:
        pass


class DefaultPublicPredictor(PublicPredictor):

    def __init__(self):
        super().__init__()

    def predict(self, configuration: ProjectConfiguration, directory: Path) -> bool:
        if configuration.type() == ProjectType.ConsoleApplication:
            return False
        relative_path = stringify_path(directory.relative_to(configuration.workspace), quotation=False)
        if relative_path == CURRENT_DIR_STR:
            return configuration.type() == ProjectType.StaticLibrary

        parts = relative_path.split('/')
        if len(parts) == 0:
            return False
        root_dir = parts[0].lower()
        if configuration.type() == ProjectType.DynamicLinkLibrary:
            return root_dir == 'public'
        if configuration.type() == ProjectType.StaticLibrary:
            return root_dir != 'private'
