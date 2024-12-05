"""
Helper functions for the treecraft package.
"""

import os
import re
from typing import Optional

def clean_line(line: str) -> str:
    """
    Clean a line from the tree structure.

    Args:
        line (str): Input line to clean

    Returns:
        str: Cleaned line
    """
    # Remove ANSI color codes if present
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', line)

def validate_line(line: str) -> bool:
    """
    Validate if a line from the tree structure is valid.

    Args:
        line (str): Line to validate

    Returns:
        bool: True if line is valid, False otherwise
    """
    # Skip empty lines or lines with only tree symbols
    stripped = line.strip('│├└─ \t')
    return bool(stripped)

def validate_path(path: str) -> bool:
    """
    Validate if a path is safe to create.

    Args:
        path (str): Path to validate

    Returns:
        bool: True if path is safe, False otherwise
    """
    # Convert to absolute path
    abs_path = os.path.abspath(path)

    # Check for parent directory traversal
    if '..' in path.split(os.sep):
        return False

    # Check if path is too long
    try:
        if len(abs_path) > os.pathconf('/', 'PC_PATH_MAX'):
            return False
    except (AttributeError, OSError):
        # Skip this check on systems where pathconf is not available
        pass

    return True

def is_python_file(path: str) -> bool:
    """
    Check if a file is a Python file.

    Args:
        path (str): Path to check

    Returns:
        bool: True if file is a Python file, False otherwise
    """
    return path.endswith('.py')

def get_relative_path(path: str, base: str) -> str:
    """
    Get the relative path from a base directory.

    Args:
        path (str): Path to convert
        base (str): Base directory

    Returns:
        str: Relative path
    """
    return os.path.relpath(path, base)

def normalize_path(path: str) -> str:
    """
    Normalize a path for the current operating system.

    Args:
        path (str): Path to normalize

    Returns:
        str: Normalized path
    """
    return os.path.normpath(path)