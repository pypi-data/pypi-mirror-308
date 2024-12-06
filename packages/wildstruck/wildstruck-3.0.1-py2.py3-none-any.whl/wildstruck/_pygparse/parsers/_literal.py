# ----------------------------------------------------------------------------------------------
# Copyright (C) Botni.Vision, Inc - Montreal, QC, Canada - All Rights Reserved
# Unauthorized copying, use, or modification to this file via any medium is strictly prohibited.
# This file is private and confidential.
# Contact: dev@botni.vision
# ----------------------------------------------------------------------------------------------

import ast
from typing import Any


def parse_literal(value: str) -> Any:
    """literal"""
    return ast.literal_eval(value)


def parse_plus_literal(value: str) -> Any:
    """+literal"""
    if value[0] == "+":
        return parse_literal(value[1:])
    if value[0] == "\\":
        return value[1:]
    return value
