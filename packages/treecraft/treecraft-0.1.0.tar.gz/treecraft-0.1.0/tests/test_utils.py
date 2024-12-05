"""
Tests for utility functions.
"""

import unittest
import os
from treecraft.utils.helpers import (
    clean_line,
    validate_line,
    validate_path,
    is_python_file
)

class TestHelpers(unittest.TestCase):
    def test_clean_line(self):
        """Test cleaning lines with various formats."""
        # Test ANSI color codes
        self.assertEqual(clean_line('\x1B[31mtest\x1B[0m'), 'test')
        # Test normal line
        self.assertEqual(clean_line('├── test.py'), '├── test.py')
        # Test whitespace
        self.assertEqual(clean_line('  test  '), '  test  ')

    def test_validate_line(self):
        """Test line validation."""
        # Valid lines
        self.assertTrue(validate_line('├── test.py'))
        self.assertTrue(validate_line('test.py'))
        
        # Invalid lines
        self.assertFalse(validate_line(''))
        self.assertFalse(validate_line('    '))
        self.assertFalse(validate_line('│'))

    def test_validate_path(self):
        """Test path validation."""
        # Valid paths
        self.assertTrue(validate_path('test_dir'))
        self.assertTrue(validate_path('./test_dir'))
        
        # Invalid paths
        self.assertFalse(validate_path('../test_dir'))
        self.assertFalse(validate_path('/root/test_dir'))

    def test_is_python_file(self):
        """Test Python file detection."""
        # Python files
        self.assertTrue(is_python_file('test.py'))
        self.assertTrue(is_python_file('path/to/test.py'))
        
        # Non-Python files
        self.assertFalse(is_python_file('test.txt'))
        self.assertFalse(is_python_file('test'))
        self.assertFalse(is_python_file('test.py.txt'))

class TestPathOperations(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.test_dir = os.path.join(os.path.dirname(__file__), 'test_dir')
        os.makedirs(self.test_dir, exist_ok=True)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)

    def test_path_operations(self):
        """Test various path operations."""
        test_path = os.path.join(self.test_dir, 'test.py')
        
        # Test path validation
        self.assertTrue(validate_path(test_path))
        
        # Test relative paths
        self.assertTrue(validate_path('./test.py'))

if __name__ == '__main__':
    unittest.main()