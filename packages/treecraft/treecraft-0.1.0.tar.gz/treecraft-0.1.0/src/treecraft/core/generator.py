"""
Generator: Creates directory structures from parsed tree representations.
"""

import os
from typing import Dict, Optional
from treecraft.utils.helpers import validate_path, is_python_file

class Generator:
    """Generates file system structures from parsed tree representations."""

    def __init__(self, dry_run: bool = False):
        """
        Initialize the Generator.

        Args:
            dry_run (bool): If True, only print what would be done without creating files
        """
        self.dry_run = dry_run

    def generate(self, structure: Dict[str, any], base_path: str) -> None:
        """
        Generate the directory structure from the parsed representation.

        Args:
            structure (Dict[str, any]): Nested dictionary representing the structure
            base_path (str): Base directory where the structure will be created

        Raises:
            ValueError: If the base path is invalid
            OSError: If there's an error creating directories or files
        """
        if not validate_path(base_path):
            raise ValueError(f"Invalid base path: {base_path}")

        self._create_structure(structure, base_path)

    def _create_structure(self, structure: Dict[str, any], current_path: str) -> None:
        """
        Recursively create the directory structure.

        Args:
            structure (Dict[str, any]): Current level of the structure
            current_path (str): Current path being processed
        """
        for name, contents in structure.items():
            path = os.path.join(current_path, name)

            if self._is_file(name):
                self._create_file(path)
            else:
                self._create_directory(path)
                self._create_structure(contents, path)

    def _create_directory(self, path: str) -> None:
        """
        Create a directory if it doesn't exist.

        Args:
            path (str): Path where to create the directory
        """
        if self.dry_run:
            print(f"Would create directory: {path}")
            return

        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Created directory: {path}")

    def _create_file(self, path: str) -> None:
        """
        Create an empty file with optional template content.

        Args:
            path (str): Path where to create the file
        """
        if self.dry_run:
            print(f"Would create file: {path}")
            return

        if not os.path.exists(path):
            with open(path, 'w') as f:
                if is_python_file(path):
                    # Add docstring template for Python files
                    filename = os.path.basename(path)
                    f.write(f'"""\n{filename}\n"""\n\n')
            print(f"Created file: {path}")

    def _is_file(self, name: str) -> bool:
        """Check if the name represents a file (contains an extension)."""
        return '.' in name