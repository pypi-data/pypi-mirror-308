"""
TreeParser: Converts text-based tree representations into structured data.
"""

from typing import Dict, List, Optional
import re
from treecraft.utils.helpers import clean_line, validate_line

class TreeParser:
    """Parser for converting text-based tree structures into a dictionary representation."""

    def __init__(self):
        # Regex pattern for matching tree symbols and indentation
        self.indent_pattern = re.compile(r'^[│├└─\s]+')
        self.tree_symbols = {'├', '│', '└', '─'}

    def parse(self, content: str) -> Dict[str, any]:
        """
        Parse tree structure text into a nested dictionary.

        Args:
            content (str): Input text containing the tree structure

        Returns:
            Dict[str, any]: Nested dictionary representing the file/directory structure

        Example:
            >>> parser = TreeParser()
            >>> content = '''
            ... src/
            ... ├── utils/
            ... │   └── helpers.py
            ... └── main.py
            ... '''
            >>> parser.parse(content)
            {'src': {'utils': {'helpers.py': {}}, 'main.py': {}}}
        """
        lines = content.strip().split('\n')
        structure = {}
        path_stack = []
        indent_stack = [-1]

        for line in lines:
            if not line.strip():
                continue

            # Clean and validate the line
            line = clean_line(line)
            if not validate_line(line):
                continue

            # Calculate indent level
            indent = self._get_indent_level(line)
            name = self._extract_name(line)

            # Adjust path stack based on indentation
            while indent_stack[-1] >= indent:
                indent_stack.pop()
                path_stack.pop()

            # Update stacks
            path_stack.append(name)
            indent_stack.append(indent)

            # Update structure
            self._update_structure(structure, path_stack)

        return structure

    def _get_indent_level(self, line: str) -> int:
        """Calculate the indentation level of a line."""
        match = self.indent_pattern.match(line)
        return len(match.group(0)) if match else 0

    def _extract_name(self, line: str) -> str:
        """Extract the name from a line, removing tree symbols and trailing slashes."""
        # Remove tree symbols and whitespace
        for symbol in self.tree_symbols:
            line = line.replace(symbol, '')
        return line.strip().rstrip('/')

    def _update_structure(self, structure: Dict, path: List[str]):
        """
        Update the structure dictionary with the given path.

        Args:
            structure (Dict): Current structure dictionary
            path (List[str]): Path to add to the structure
        """
        current = structure
        for item in path[:-1]:
            if item not in current:
                current[item] = {}
            current = current[item]
        current[path[-1]] = {}