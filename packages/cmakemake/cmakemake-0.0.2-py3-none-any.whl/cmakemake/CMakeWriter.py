# -*- coding: utf-8 -*-

__all__ = ['CMakeWriter', 'ProjectCMakeWriter', 'SolutionCMakeWriter']

import abc
from abc import ABC
from pathlib import Path
from typing import Sequence, MutableSequence, MutableSet, MutableMapping, Union, Any, Final, Tuple

from cmakemake.concepts import (
    Configuration,
    SolutionConfiguration,
    ProjectConfiguration,
    ConsoleApplicationConfiguration,
    StaticLibraryConfiguration,
    DynamicLinkLibraryConfiguration
)
from cmakemake.constants import (
    CMAKE_MINIMUM_REQUIRED,
    CMAKE_FILENAME,
    TEXT_FILE_ENCODING,
    CURRENT_DIR_STR_WITH_QUOTATION,
    CURRENT_DIR_STR
)
from cmakemake.utils import stringify_path, relative_path_to


VAR_FILES: Final[str] = 'files'
VAR_NAME: Final[str] = 'var_name'


class _Variable:

    def __init__(self, name: str):
        self.__name: str = name
        self.__values: MutableSequence[Any] = []

    @property
    def name(self) -> str:
        return self.__name

    @property
    def values(self) -> Sequence[Any]:
        return self.__values

    def __bool__(self):
        return len(self.name) > 0 and len(self.values) > 0

    def __str__(self):
        return f'${{{self.name}}}'

    def add_value(self, value: Any):
        self.__values.append(value)

    def to_lines(self, lines: MutableSequence[str]):
        if len(self.values) == 1:
            lines.append(f'set({self.name} {self.values[0]})')
        elif len(self.values) > 1:
            lines.append(f'set({self.name}')
            for item in self.values:
                lines.append(f'    {item}')
            lines.append(f')')


class _Variables:

    def __init__(self):
        self.__variables: MutableMapping[str, _Variable] = {}

    def add_variable(self, variable: _Variable):
        if not variable:
            return
        if variable in self.__variables:
            return
        self.__variables[variable.name] = variable

    def __contains__(self, item):
        if not isinstance(item, str):
            return False
        return item in self.__variables

    def __getitem__(self, item) -> Union[_Variable, None]:
        return None if item not in self.__variables else self.__variables[item]


class CMakeWriter(ABC):

    def __init__(self):
        pass

    def write(self, configuration: Configuration):
        if not isinstance(configuration, Configuration):
            return

        variables = _Variables()

        lines: MutableSequence[str] = [
            f'cmake_minimum_required(VERSION {CMAKE_MINIMUM_REQUIRED})',
            f'project({configuration.name} LANGUAGES CXX)'
        ]
        self.generate_cmake_lines(configuration, variables, lines)

        filename = configuration.workspace.joinpath(CMAKE_FILENAME)
        with open(filename, 'w', encoding=TEXT_FILE_ENCODING) as fp:
            fp.write('\n'.join(lines))

    @abc.abstractmethod
    def generate_cmake_lines(self, configuration: Configuration, variables: _Variables, lines: MutableSequence[str]):
        pass


def _include_directories(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    def _include_directory(current_path: Path, path_set: MutableSet[str]):
        _ = relative_path_to(config.workspace, current_path)
        if _ != CURRENT_DIR_STR:
            path_set.add(_)

    include_directories: MutableSet[str] = set()
    for file in config.files:
        _include_directory(file.parent, include_directories)

    for project in config.internal_includes:
        solution_configuration = config.solution_configuration
        if not isinstance(solution_configuration, SolutionConfiguration):
            continue
        depended = solution_configuration[project]
        if not isinstance(depended, ProjectConfiguration):
            continue
        public_directories = depended.public_directories
        for public_directory in public_directories:
            _include_directory(public_directory, include_directories)

    for include_directory in config.include_directories:
        include_directories.add(include_directory)

    include_directory_list: MutableSequence[str] = list(include_directories)
    include_directory_list = sorted(include_directory_list)
    for include_directory in include_directory_list:
        lines.append(f'include_directories("{include_directory}")')


def _source_group(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    files: MutableSequence[Tuple[str, str]] = []
    for file in config.files:
        relative_path = file.relative_to(config.workspace)
        source_group = stringify_path(relative_path.parent)
        if source_group == CURRENT_DIR_STR_WITH_QUOTATION:
            source_group = '""'
        files.append((source_group, stringify_path(relative_path)))
    files = sorted(files, key=lambda item: item[1])

    for file in files:
        lines.append(f'source_group({file[0]} FILES {file[1]})')


def _link_directories(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    solution_configuration = config.solution_configuration
    if not isinstance(solution_configuration, SolutionConfiguration):
        return
    output_dir = solution_configuration.output_directory
    if not isinstance(output_dir, Path):
        return
    link_directories = [
        relative_path_to(config.workspace, output_dir)
    ]
    for link_directory in config.link_directories:
        link_directories.append(link_directory)

    libs = config.internal_libraries
    if len(libs) == 0 and len(link_directories) == 1:
        return

    link_directories = sorted(link_directories)
    if len(link_directories) == 1:
        lines.append(f'link_directories("{link_directories[0]}")')
    elif len(link_directories) > 1:
        lines.append(f'link_directories(')
        for link_directory in link_directories:
            lines.append(f'    "{link_directory}"')
        lines.append(f')')


def _add_definitions(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    definitions = config.definitions
    for definition in definitions:
        lines.append(f'add_definitions(/D {definition})')


def _add_compile_options(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    warnings = config.disable_warnings()
    if len(warnings) == 0:
        return
    warnings = sorted(warnings)
    lines.append(f'if(WIN32)')
    for warning in warnings:
        lines.append(f'    add_compile_options(/wd{warning})')
    lines.append(f'endif(WIN32)')


def _link_libraries(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    libs = config.internal_libraries
    solution_configuration = config.solution_configuration
    if not isinstance(solution_configuration, SolutionConfiguration):
        return
    libs = sorted(libs)
    for lib in libs:
        depended = solution_configuration[lib]
        if isinstance(depended, ProjectConfiguration):
            lines.append(f'link_libraries("{depended.target_name}.lib")')

    libs = config.link_libraries
    libs = sorted(libs)
    for lib in libs:
        lines.append(f'link_libraries("{lib}")')


def _output_name(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    if config.name != config.target_name:
        lines.append(f'set_target_properties({config.name} PROPERTIES OUTPUT_NAME "{config.target_name}")')


def _vs_debugger_environment(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str]):
    link_directories = config.link_directories
    if len(link_directories) == 0:
        return
    link_directories = sorted(link_directories)
    all_link_directories: MutableSequence[str] = ['$(PATH)']
    for link_directory in link_directories:
        all_link_directories.append(f'${{PROJECT_SOURCE_DIR}}/{link_directory}')
        all_link_directories.append(f'${{PROJECT_SOURCE_DIR}}/{link_directory}/$(Configuration)')
    env = ';'.join(all_link_directories)
    lines.append(f'set_property(TARGET {config.name} PROPERTY VS_DEBUGGER_ENVIRONMENT "PATH={env}")')


def _add_executable_or_library(config: ProjectConfiguration, vars: _Variables, lines: MutableSequence[str], **kwargs):
    var_name = kwargs.get(VAR_NAME)
    if var_name is None:
        return
    var = vars[var_name]
    if var is None:
        return
    if isinstance(config, ConsoleApplicationConfiguration):
        lines.append(f'add_executable({config.name} {str(var)})')
    elif isinstance(config, StaticLibraryConfiguration):
        lines.append(f'add_library({config.name} STATIC {str(var)})')
    elif isinstance(config, DynamicLinkLibraryConfiguration):
        lines.append(f'add_library({config.name} SHARED {str(var)})')


def _set_variable_value(var_name: str, values: Sequence[str], vars: _Variables, lines: MutableSequence[str]):
    var = _Variable(var_name)
    for value in values:
        var.add_value(value)
    var.to_lines(lines)
    vars.add_variable(var)


class ProjectCMakeWriter(CMakeWriter):

    def __init__(self):
        super().__init__()

    def generate_cmake_lines(self, configuration: Configuration, variables: _Variables, lines: MutableSequence[str]):
        if not isinstance(configuration, ProjectConfiguration):
            return
        solution_configuration = configuration.solution_configuration
        if solution_configuration is not None and not isinstance(solution_configuration, SolutionConfiguration):
            return

        files: MutableSet[str] = set()
        for file in configuration.files:
            files.add(stringify_path(file.relative_to(configuration.workspace)))
        file_list: MutableSequence[str] = list(files)
        file_list = sorted(file_list)

        lines.append(f'set(CMAKE_CXX_STANDARD {solution_configuration.cxx_standard})')
        lines.append(f'set(CMAKE_INCLUDE_CURRENT_DIR ON)')
        _include_directories(configuration, variables, lines)
        _set_variable_value(var_name=VAR_FILES, values=file_list, vars=variables, lines=lines)
        _source_group(configuration, variables, lines)
        _add_definitions(configuration, variables, lines)
        _add_compile_options(configuration, variables, lines)
        _link_directories(configuration, variables, lines)
        _link_libraries(configuration, variables, lines)
        _add_executable_or_library(configuration, variables, lines, **{VAR_NAME: VAR_FILES})
        _output_name(configuration, variables, lines)
        _vs_debugger_environment(configuration, variables, lines)


def _output_directories(config: SolutionConfiguration, vars: _Variables, lines: MutableSequence[str]):
    output_dir = config.output_directory
    if output_dir is None:
        return

    relative_path = relative_path_to(config.workspace, output_dir)
    relative_path = f'${{CMAKE_SOURCE_DIR}}/{relative_path}'
    lines.append(f'set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY {relative_path})')
    lines.append(f'set(CMAKE_LIBRARY_OUTPUT_DIRECTORY {relative_path})')
    lines.append(f'set(CMAKE_RUNTIME_OUTPUT_DIRECTORY {relative_path})')


def _add_subdirectories(config: SolutionConfiguration, vars: _Variables, lines: MutableSequence[str]):
    subdirectories: MutableSequence[str] = []
    solution_dir = config.workspace
    for project in config.projects:
        project_dir = project.workspace
        relative_path = project_dir.relative_to(solution_dir)
        subdirectories.append(stringify_path(relative_path))

    subdirectories = sorted(subdirectories)
    for subdirectory in subdirectories:
        lines.append(f'add_subdirectory({subdirectory})')


def _vs_startup_project(config: SolutionConfiguration, variables: _Variables, lines: MutableSequence[str]):
    startup_project = config.startup_project
    if startup_project is not None:
        lines.append(f'set_property(DIRECTORY PROPERTY VS_STARTUP_PROJECT {startup_project})')


def _vs_debugger_working_directory(config: SolutionConfiguration, variables: _Variables, lines: MutableSequence[str]):
    output_dir = config.output_directory
    if output_dir is None:
        return

    projects: MutableSequence[str] = []
    for project in config.projects:
        projects.append(project.name)
    sorted(projects)

    relative_path = relative_path_to(config.workspace, output_dir)
    relative_path = f'${{CMAKE_SOURCE_DIR}}/{relative_path}/$(Configuration)'
    for project in projects:
        lines.append(f'set_target_properties({project} PROPERTIES VS_DEBUGGER_WORKING_DIRECTORY {relative_path})')


def _add_dependencies(config: SolutionConfiguration, variables: _Variables, lines: MutableSequence[str]):
    projects: MutableSequence[MutableSequence[str]] = []
    for project in config.projects:
        libraries = project.internal_libraries
        if len(libraries) == 0:
            continue
        libraries = sorted(libraries)
        projects.append([project.name])
        for library in libraries:
            projects[-1].append(library)

    projects = sorted(projects, key=lambda item: item[0])
    space: str = ' '
    for project in projects:
        lines.append(f'add_dependencies({space.join(project)})')


class SolutionCMakeWriter(CMakeWriter):

    def __init__(self):
        super().__init__()

    def generate_cmake_lines(self, configuration: Configuration, variables: _Variables, lines: MutableSequence[str]):
        if not isinstance(configuration, SolutionConfiguration):
            return

        _output_directories(configuration, variables, lines)
        _add_subdirectories(configuration, variables, lines)
        _vs_startup_project(configuration, variables, lines)
        _vs_debugger_working_directory(configuration, variables, lines)
        _add_dependencies(configuration, variables, lines)
