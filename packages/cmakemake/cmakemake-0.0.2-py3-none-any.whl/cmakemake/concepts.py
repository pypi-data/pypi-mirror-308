# -*- coding: utf-8 -*-

import abc
from abc import ABC
from pathlib import Path
from enum import StrEnum, IntEnum
from typing import MutableSequence, Sequence, Optional, Union, Mapping, MutableSet, Iterable

from cmakemake.keywords import *
from cmakemake.constants import CMAKE_FILENAME


class ProjectType(StrEnum):

    Solution = 'solution'
    ConsoleApplication = 'console-application'
    DynamicLinkLibrary = 'dynamic-link-library'
    StaticLibrary = 'static-library'


class CxxStandard(IntEnum):

    Cxx_11 = 11
    Cxx_14 = 14
    Cxx_17 = 17
    Cxx_20 = 20
    Cxx_23 = 23
    Cxx_26 = 26


CXX_STANDARD_MAPPING: Mapping[int, CxxStandard] = {
    11: CxxStandard.Cxx_11,
    14: CxxStandard.Cxx_14,
    17: CxxStandard.Cxx_17,
    20: CxxStandard.Cxx_20,
    23: CxxStandard.Cxx_23,
    26: CxxStandard.Cxx_26
}


def int_to_cxx_standard(value: int, default: Optional[CxxStandard] = CxxStandard.Cxx_14) -> CxxStandard:
    return default if value not in CXX_STANDARD_MAPPING else CXX_STANDARD_MAPPING[value]


class Configuration(ABC):

    def __init__(self, configuration_path: Path, **kwargs):
        self.__name: str = ''
        self.__workspace_dir: Path = configuration_path.parent
        self.__disable_warnings: MutableSet[str] = set()

        self.name = kwargs.get(NAME)
        self.add_disable_warnings(kwargs.get(DISABLE_WARNINGS))

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @abc.abstractmethod
    def type(self):
        pass

    @property
    def workspace(self) -> Path:
        return self.__workspace_dir

    def disable_warnings(self) -> Sequence[str]:
        result = list(self.__disable_warnings)
        return result

    def add_disable_warning(self, warning: str):
        if isinstance(warning, str) and len(warning) != 0:
            self.__disable_warnings.add(warning)

    def add_disable_warnings(self, warnings: Sequence[str]):
        if isinstance(warnings, Iterable):
            for warning in warnings:
                self.add_disable_warning(warning)

    def __bool__(self):
        return True


class ProjectConfiguration(Configuration, ABC):

    def __init__(self, configuration_path: Path, **kwargs):
        super().__init__(configuration_path, **kwargs)
        self.__solution_configuration: Union[Configuration, None] = None
        self.__files: MutableSequence[Path] = [
            self.workspace.joinpath(CMAKE_FILENAME)
        ]
        self.__public_directories: MutableSequence[Path] = []
        self.__target_name: Union[str, None] = None
        self.__definitions: MutableSet[str] = set()

        self.__include_directories: MutableSet[str] = set()
        self.__link_directories: MutableSet[str] = set()
        self.__link_libraries: MutableSet[str] = set()

        self.__internal_includes: MutableSet[str] = set()       # project names
        self.__internal_libraries: MutableSet[str] = set()      # project names

        self.target_name = kwargs.get(TARGET_NAME)
        self.add_definitions(kwargs.get(DEFINITIONS))
        self.add_include_directories(kwargs.get(INCLUDE_DIRECTORIES))
        self.add_link_directories(kwargs.get(LINK_DIRECTORIES))
        self.add_link_libraries(kwargs.get(LINK_LIBRARIES))
        self.add_internal_includes(kwargs.get(INTERNAL_INCLUDES))
        self.add_internal_libraries(kwargs.get(INTERNAL_LIBRARIES))

    @property
    def solution_configuration(self) -> Union[Configuration, None]:
        return self.__solution_configuration

    @solution_configuration.setter
    def solution_configuration(self, solution_configuration: Configuration):
        if isinstance(solution_configuration, Configuration):
            self.__solution_configuration = solution_configuration

    def __contains__(self, item):
        if not isinstance(item, Path):
            return False
        for file in self.__files:
            if file == item:
                return True
        return False

    def add_file(self, file: Path):
        if file not in self:
            self.__files.append(file)

    def add_files(self, files: Sequence[Path]):
        for file in files:
            self.add_file(file)

    @property
    def files(self) -> MutableSequence[Path]:
        return self.__files

    @property
    def public_directories(self) -> Sequence[Path]:
        return self.__public_directories

    def add_public_directory(self, value: Path):
        if value not in self.__public_directories:
            self.__public_directories.append(value)

    def add_public_directories(self, values: Sequence[Path]):
        for value in values:
            self.add_public_directory(value)

    @property
    def target_name(self) -> str:
        return self.name if self.__target_name is None else self.__target_name

    @target_name.setter
    def target_name(self, value: str):
        if isinstance(value, str) and len(value) > 0:
            self.__target_name = value

    @property
    def definitions(self) -> Sequence[str]:
        definitions: MutableSequence[str] = []
        for definition in self.__definitions:
            definitions.append(definition)
        return definitions

    def add_definition(self, definition: str):
        if isinstance(definition, str) and len(definition) > 0:
            self.__definitions.add(definition)

    def add_definitions(self, definitions: Sequence[str]):
        if definitions is None:
            return
        for definition in definitions:
            self.add_definition(definition)

    def disable_warnings(self) -> Sequence[str]:
        result: MutableSequence[str] = []
        for item in super().disable_warnings():
            result.append(item)
        if isinstance(self.solution_configuration, SolutionConfiguration):
            for item in self.solution_configuration.disable_warnings():
                result.append(item)
        return result

    @property
    def include_directories(self) -> Sequence[str]:
        return list(self.__include_directories)

    def add_include_directory(self, value: str):
        if isinstance(value, str) and len(value) != 0:
            self.__include_directories.add(value)

    def add_include_directories(self, values: Sequence[str]):
        if isinstance(values, Iterable):
            for value in values:
                self.add_include_directory(value)

    @property
    def link_directories(self) -> Sequence[str]:
        return list(self.__link_directories)

    def add_link_directory(self, value: str):
        if isinstance(value, str) and len(value) != 0:
            self.__link_directories.add(value)

    def add_link_directories(self, values: Sequence[str]):
        if isinstance(values, Iterable):
            for value in values:
                self.add_link_directory(value)

    @property
    def link_libraries(self) -> Sequence[str]:
        return list(self.__link_libraries)

    def add_link_library(self, value: str):
        if isinstance(value, str) and len(value) != 0:
            self.__link_libraries.add(value)

    def add_link_libraries(self, values: Sequence[str]):
        if isinstance(values, Iterable):
            for value in values:
                self.add_link_library(value)

    @property
    def internal_includes(self) -> Sequence[str]:
        result: MutableSequence[str] = []
        for item in self.__internal_includes:
            result.append(item)
        return result

    def add_internal_include(self, value: str):
        if isinstance(value, str) and len(value) != 0:
            self.__internal_includes.add(value)

    def add_internal_includes(self, values: Sequence[str]):
        if not isinstance(values, Iterable):
            return
        for value in values:
            self.add_internal_include(value)

    @property
    def internal_libraries(self) -> Sequence[str]:
        result: MutableSequence[str] = []
        for item in self.__internal_libraries:
            result.append(item)
        return result

    def add_internal_library(self, value: str):
        if isinstance(value, str) and len(value) != 0:
            self.add_internal_include(value)
            self.__internal_libraries.add(value)

    def add_internal_libraries(self, values: Sequence[str]):
        if not isinstance(values, Iterable):
            return
        for value in values:
            self.add_internal_library(value)


class ConsoleApplicationConfiguration(ProjectConfiguration):

    def __init__(self, configuration_path: Path, **kwargs):
        super().__init__(configuration_path, **kwargs)

    def type(self):
        return ProjectType.ConsoleApplication


class DynamicLinkLibraryConfiguration(ProjectConfiguration):

    def __init__(self, configuration_path: Path, **kwargs):
        super().__init__(configuration_path, **kwargs)

    def type(self):
        return ProjectType.DynamicLinkLibrary


class StaticLibraryConfiguration(ProjectConfiguration):

    def __init__(self, configuration_path: Path, **kwargs):
        super().__init__(configuration_path, **kwargs)

    def type(self):
        return ProjectType.StaticLibrary


class SolutionConfiguration(Configuration):

    def __init__(self, configuration_path: Path, **kwargs):
        super().__init__(configuration_path, **kwargs)
        self.__projects: MutableSequence[ProjectConfiguration] = []
        self.__cxx_standard: CxxStandard = CxxStandard.Cxx_11
        self.__startup_project: Union[str, None] = None
        self.__output_directory: Union[Path, None] = None

        self.cxx_standard = kwargs.get(CXX_STANDARD)
        self.startup_project = kwargs.get(STARTUP_PROJECT)

    def type(self):
        return ProjectType.Solution

    def __contains__(self, item):
        if not isinstance(item, ProjectConfiguration):
            return False
        for project in self.__projects:
            if project.name.lower() == item.name.lower():
                return True
        return False

    def __getitem__(self, item) -> Union[ProjectConfiguration, None]:
        if not isinstance(item, str):
            return
        for project in self.__projects:
            if project.name == item:
                return project

    def add_project(self, project: ProjectConfiguration):
        if project not in self:
            project.solution_configuration = self
            self.__projects.append(project)

    @property
    def projects(self) -> MutableSequence[ProjectConfiguration]:
        return self.__projects

    @property
    def cxx_standard(self) -> CxxStandard:
        return self.__cxx_standard

    @cxx_standard.setter
    def cxx_standard(self, value: int):
        self.__cxx_standard = int_to_cxx_standard(value, CxxStandard.Cxx_14)

    @property
    def startup_project(self) -> Union[str, None]:
        if self.__startup_project is not None and len(self.__startup_project) > 0:
            return self.__startup_project
        for project in self.projects:
            if ProjectType.ConsoleApplication == project.type():
                return project.name

    @startup_project.setter
    def startup_project(self, value: Union[str, None]):
        if value is None:
            self.__startup_project = value
        if isinstance(value, str) and len(value) > 0:
            self.__startup_project = value

    @property
    def output_directory(self) -> Union[Path, None]:
        return self.__output_directory

    @output_directory.setter
    def output_directory(self, value: Union[Path, None]):
        if value is None or isinstance(value, Path):
            self.__output_directory = value
