# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Optional


def stringify_path(path: Path, quotation: Optional[bool] = True) -> str:
    left_quotation = ''
    right_quotation = ''
    if quotation:
        left_quotation = '"'
        right_quotation = '"'
    text = f'{left_quotation}{str(path)}{right_quotation}'
    return text.replace('\\', '/')


def relative_path_to(from_path: Path, to_path: Path) -> str:
    from_path_parts = from_path.parts
    to_path_parts = to_path.parts
    index = 0
    while index < len(from_path_parts) and index < len(to_path_parts):
        if from_path_parts[index] != to_path_parts[index]:
            break
        index += 1

    from_path_diff_parts = from_path_parts[index:]
    to_path_diff_parts = to_path_parts[index:]

    if len(from_path_diff_parts) == 0 and len(to_path_diff_parts) == 0:
        return '.'

    parts = ['..' for _ in from_path_diff_parts]
    for item in to_path_diff_parts:
        parts.append(item)
    return '/'.join(parts)
