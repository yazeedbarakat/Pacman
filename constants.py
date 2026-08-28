"""Filesystem path helpers.

Centralizes the path logic needed so asset loading and highscore
saving keep working both when running from source and when frozen
into a standalone build (e.g. PyInstaller).
"""

import os
import sys


def resource_path(relative_path: str) -> str:
    """Resolve a path to a bundled, read-only file (assets, config.json).

    Args:
        relative_path: Path relative to the project root, e.g.
            'assets/menu/heart.png'.

    Returns:
        The path resolved against the source tree when running from
        source, or against PyInstaller's extracted bundle directory
        (`sys._MEIPASS`) when running from a frozen build.
    """
    base_dir = getattr(
        sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, relative_path)


def writable_path(filename: str) -> str:
    """Resolve a path for a file the game needs to write at runtime.

    Bundled builds are read-only, so files like the highscore save
    need to live next to the executable (or script) instead of inside
    the bundle.

    Args:
        filename: Name of the file to resolve, e.g. 'pc.json'.

    Returns:
        The path next to the running executable when frozen, or next
        to this file when running from source.
    """
    if getattr(sys, 'frozen', False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)
