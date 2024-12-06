"""
Tests for the Generator class.
"""

import unittest
import os
import shutil
import tempfile
from treecraft.core.generator import Generator

class TestGenerator(unittest.TestCase):
    def setUp(self):
        """Set up test cases."""
        self.generator = Generator()
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up after tests."""
        # Remove the temporary directory
        shutil.rmtree(self.test_dir)

    def test_generate_simple_structure(self):
        """Test generating a simple directory structure."""
        structure = {
            'src': {
                'main.py': {},
                'utils': {
                    'helpers.py': {}
                }
            }
        }
        self.generator.generate(structure, self.test_dir)
        
        # Verify the structure was created correctly
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'src')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'src', 'main.py')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'src', 'utils')))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'src', 'utils', 'helpers.py')))

    def test_generate_empty_structure(self):
        """Test generating an empty structure."""
        structure = {}
        self.generator.generate(structure, self.test_dir)
        # Directory should exist but be empty
        self.assertTrue(os.path.exists(self.test_dir))
        self.assertEqual(os.listdir(self.test_dir), [])

    def test_python_file_generation(self):
        """Test that Python files are generated with docstrings."""
        structure = {
            'test.py': {}
        }
        self.generator.generate(structure, self.test_dir)
        
        file_path = os.path.join(self.test_dir, 'test.py')
        self.assertTrue(os.path.exists(file_path))
        
        with open(file_path, 'r') as f:
            content = f.read()
            self.assertIn('"""', content)
            self.assertIn('test.py', content)

    def test_invalid_path(self):
        """Test generating structure with invalid path."""
        structure = {'test': {}}
        with self.assertRaises(ValueError):
            self.generator.generate(structure, '/invalid/path/that/doesnt/exist')

if __name__ == '__main__':
    unittest.main()