# -*- coding: utf-8 -*-

__all__ = ['CMakeMake']

import os
from typing import Optional, Union, MutableSequence
from pathlib import Path

from cmakemake.ConfigurationDetector import ConfigurationDetector
from cmakemake.ConfigurationBuilder import ConfigurationBuilder
from cmakemake.CMakeWriter import ProjectCMakeWriter, SolutionCMakeWriter
from cmakemake.FileFilter import FileFilter
from cmakemake.PublicPredictor import PublicPredictor, DefaultPublicPredictor
from cmakemake.utils import relative_path_to


class CMakeMake:

    def __init__(self, source_dir: Path, build_dir: Path, binary_dir: Path):
        self.source_dir = source_dir
        self.build_dir = build_dir
        self.binary_dir = binary_dir
        self.__file_filter: Union[FileFilter, None] = None
        self.__public_predictor: PublicPredictor = DefaultPublicPredictor()

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

    def run(self, build: Optional[bool] = True, start: Optional[bool] = False):
        self.__create()
        if build:
            self.__build()
            if start:
                self.__start()

    def __create(self):
        configuration_detector = ConfigurationDetector(source_dir=self.source_dir)
        solution_configuration_path, project_configuration_paths = configuration_detector.run()
        if solution_configuration_path is None or project_configuration_paths is None:
            return

        configuration_builder = ConfigurationBuilder(
            file_filter=self.file_filter,
            public_predictor=self.public_predictor
        )
        solution_configuration = configuration_builder.run(solution_configuration_path, project_configuration_paths)
        solution_configuration.output_directory = self.binary_dir

        project_writer = ProjectCMakeWriter()
        for project_configuration in solution_configuration.projects:
            project_writer.write(project_configuration)

        solution_writer = SolutionCMakeWriter()
        solution_writer.write(solution_configuration)

    def __build(self):
        current_dir = self.build_dir
        directories: MutableSequence[str] = []
        while not current_dir.is_dir():
            directories.append(current_dir.name)
            current_dir = current_dir.parent
        while len(directories) > 0:
            current_dir = current_dir.joinpath(directories[-1])
            os.mkdir(current_dir)
            directories.pop(-1)

        os.chdir(self.build_dir)
        relative_path = relative_path_to(self.build_dir, self.source_dir)
        os.popen(f'cmake {relative_path}')

    def __start(self):
        generator = self.build_dir.iterdir()
        for item in generator:
            if item.is_file():
                filename = item.name
                if filename.endswith('.sln'):
                    os.chdir(self.build_dir)
                    os.popen(filename)
