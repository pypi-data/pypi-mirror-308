"""
Tests for the TreeParser class.
"""

import unittest
from treecraft.core.parser import TreeParser

class TestTreeParser(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.parser = TreeParser()

    def test_simple_structure(self):
        """Test parsing a simple directory structure."""
        content = """
        src/
        ├── main.py
        └── utils/
            └── helpers.py
        """
        expected = {
            'src': {
                'main.py': {},
                'utils': {
                    'helpers.py': {}
                }
            }
        }
        result = self.parser.parse(content)
        self.assertEqual(result, expected)

    def test_empty_input(self):
        """Test parsing empty input."""
        content = ""
        result = self.parser.parse(content)
        self.assertEqual(result, {})

    def test_complex_structure(self):
        """Test parsing a complex directory structure."""
        content = """
        project/
        ├── docs/
        │   └── index.md
        ├── src/
        │   ├── __init__.py
        │   ├── core/
        │   │   ├── __init__.py
        │   │   └── main.py
        │   └── utils/
        │       ├── __init__.py
        │       └── helpers.py
        ├── tests/
        │   └── test_core.py
        └── README.md
        """
        expected = {
            'project': {
                'docs': {
                    'index.md': {}
                },
                'src': {
                    '__init__.py': {},
                    'core': {
                        '__init__.py': {},
                        'main.py': {}
                    },
                    'utils': {
                        '__init__.py': {},
                        'helpers.py': {}
                    }
                },
                'tests': {
                    'test_core.py': {}
                },
                'README.md': {}
            }
        }
        result = self.parser.parse(content)
        self.assertEqual(result, expected)

    def test_invalid_input(self):
        """Test parsing invalid input."""
        content = "Not a valid tree structure"
        result = self.parser.parse(content)
        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()