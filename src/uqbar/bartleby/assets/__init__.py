# SPDX-License-Identifier: MIT
# uqbar/bartleby/assets/__init__.py
"""
Bartleby
====

Overview
--------
Placeholder.

Metadata
--------
- Project: Bartleby
- License: MIT
"""

from pathlib import Path

__this__: Path = Path(__file__).parent.resolve()
STACK_FILE: Path = __this__ / "stack.yaml"

__all__ = [
    "__this__",
    "STACK_FILE",
]
