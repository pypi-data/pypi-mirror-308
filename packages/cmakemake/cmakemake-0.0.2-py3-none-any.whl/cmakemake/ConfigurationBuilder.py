# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Sequence, MutableSequence, Union, Optional

from cmakemake.keywords import *
from cmakemake.concepts import (
    SolutionConfiguration,
    ProjectConfiguration,
    ConsoleApplicationConfiguration,
    DynamicLinkLibraryConfiguration,
    StaticLibraryConfiguration,
    ProjectType
)
from cmakemake.FileFilter import FileFilter
from cmakemake.PublicPredictor import PublicPredictor, DefaultPublicPredictor
from cmakemake.constants import TEXT_FILE_ENCODING


class ConfigurationBuilder:

    def __init__(self, file_filter: Optional[FileFilter] = None, public_predictor: Optional[PublicPredictor] = None):
        self.__file_filter: Union[FileFilter, None] = None
        self.__public_predictor: PublicPredictor = DefaultPublicPredictor()

        self.file_filter = file_filter
        self.public_predictor = public_predictor

    @property
    def file_filter(self) -> Union[FileFilter, None]:
        return self.__file_filter

    @file_filter.setter
    def file_filter(self, f: Union[FileFilter, None]):
        if f is None or isinstance(f, FileFilter):
            self.__file_filter = f

    @property
    def public_predictor(self) -> PublicPredictor:
        return self.__public_predictor

    @public_predictor.setter
    def public_predictor(self, value: PublicPredictor):
        if isinstance(value, PublicPredictor):
            self.__public_predictor = value

    def run(self, solution_configuration_path: Path, project_configuration_paths: Sequence[Path],
            ) -> Union[SolutionConfiguration, None]:
        if not solution_configuration_path.is_file():
            return

        with open(solution_configuration_path, 'r', encoding=TEXT_FILE_ENCODING) as fp:
            configuration = json.load(fp)
            solution_configuration = SolutionConfiguration(solution_configuration_path, **configuration)

        for project_configuration_path in project_configuration_paths:
            with open(project_configuration_path, 'r', encoding=TEXT_FILE_ENCODING) as fp:
                configuration = json.load(fp)
                if not isinstance(configuration, dict):
                    continue
                project_type = configuration.get(TYPE)
                if not isinstance(project_type, str):
                    continue

                project_configuration: Union[ProjectConfiguration, None] = None
                if project_type == ProjectType.ConsoleApplication:
                    project_configuration = ConsoleApplicationConfiguration(project_configuration_path, **configuration)
                elif project_type == ProjectType.StaticLibrary:
                    project_configuration = StaticLibraryConfiguration(project_configuration_path, **configuration)
                elif project_type == ProjectType.DynamicLinkLibrary:
                    project_configuration = DynamicLinkLibraryConfiguration(project_configuration_path, **configuration)
                if project_configuration is None:
                    continue

                self.__build_project_configuration(project_configuration)
                solution_configuration.add_project(project_configuration)

        return solution_configuration

    def __search_files(self, project_configuration: ProjectConfiguration) -> Sequence[Path]:
        def search_files_impl(directory: Path, files: MutableSequence[Path], file_filter: Optional[FileFilter] = None):
            generator = directory.iterdir()
            for child in generator:
                if child.is_file():
                    if file_filter is None or file_filter.filter(project_configuration, child):
                        files.append(child)
                elif child.is_dir():
                    search_files_impl(child, files)

        result: MutableSequence[Path] = []
        search_files_impl(project_configuration.workspace, result, self.file_filter)
        return result

    def __build_project_configuration(self, project_configuration: ProjectConfiguration):
        files: Sequence[Path] = self.__search_files(project_configuration)
        project_configuration.add_files(files)

        for file in files:
            directory = file.parent
            if self.public_predictor.predict(project_configuration, directory):
                project_configuration.add_public_directory(directory)

    def __build_solution_configuration(self, solution_configuration: SolutionConfiguration):
        pass
