# -*- coding: utf-8 -*-

import sys
from typing import Union, Final, Sequence, Optional
from pathlib import Path
from argparse import ArgumentParser

from cmakemake import CMakeMake


_SOURCE_DIR: Final[str] = 'source_dir'
_BUILD_DIR: Final[str] = 'build_dir'
_BINARY_DIR: Final[str] = 'binary_dir'
_BUILD: Final[str] = 'build'
_START: Final[str] = 'start'


class CMakeMakeInput:

    def __init__(self, source_dir: Path, build_dir: Path, binary_dir: Path, will_build: Optional[bool] = True,
                 will_start: Optional[bool] = False):
        self.source_dir: Path = source_dir
        self.build_dir: Path = build_dir
        self.binary_dir: Path = binary_dir
        self.will_build: bool = will_build
        self.will_start: bool = will_start

    def __bool__(self):
        return self.source_dir is not None and self.build_dir is not None and self.binary_dir is not None

    def __str__(self):
        return f'''source_dir: {self.source_dir}
build_dir : {self.build_dir}
binary_dir: {self.binary_dir}'''


def parse_path(literal: str) -> Union[Path, None]:
    parsed = Path(literal)
    return parsed


def parse_input(args: Sequence[str]) -> Union[CMakeMakeInput, None]:
    parser = ArgumentParser()
    parser.add_argument('--source_dir', type=parse_path)
    parser.add_argument('--build_dir', type=parse_path)
    parser.add_argument('--binary_dir', type=parse_path)
    parser.add_argument('--build', type=bool, default=True)
    parser.add_argument('--start', type=bool, default=False)
    namespace, _ = parser.parse_known_args(args)
    if _SOURCE_DIR in namespace and _BUILD_DIR in namespace and _BINARY_DIR in namespace:
        return CMakeMakeInput(
            source_dir=getattr(namespace, _SOURCE_DIR),
            build_dir=getattr(namespace, _BUILD_DIR),
            binary_dir=getattr(namespace, _BINARY_DIR),
            will_build=getattr(namespace, _BUILD),
            will_start=getattr(namespace, _START)
        )


def main_impl(args: Sequence[str]):
    cmakemake_input = parse_input(args)
    if cmakemake_input is None:
        return
    cmakemake_task = CMakeMake(
        source_dir=cmakemake_input.source_dir,
        build_dir=cmakemake_input.build_dir,
        binary_dir=cmakemake_input.binary_dir
    )
    cmakemake_task.run(build=cmakemake_input.will_build, start=cmakemake_input.will_start)


def main():
    main_impl(sys.argv)


if __name__ == '__main__':
    main()
