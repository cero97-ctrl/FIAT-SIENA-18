import check_dependencies
import unittest
from unittest.mock import patch, mock_open
import sys
import os

# Add execution dir to path to import the module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class TestCheckDependencies(unittest.TestCase):

    @patch('os.path.exists')
    def test_requirements_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(SystemExit) as cm:
            check_dependencies.main()
        self.assertEqual(cm.exception.code, 1)

    @patch('os.path.exists')
    @patch('builtins.open', new_callable=mock_open, read_data="package-a==1.0.0\npackage-b>=2.0")
    @patch('importlib.metadata.distributions')
    def test_dependencies_missing(self, mock_dists, mock_file, mock_exists):
        mock_exists.return_value = True

        # Mock installed packages: only package-a is installed
        mock_dist_a = unittest.mock.Mock()
        mock_dist_a.metadata = {"Name": "package-a"}
        mock_dists.return_value = [mock_dist_a]

        with self.assertRaises(SystemExit) as cm:
            check_dependencies.main()
        self.assertEqual(cm.exception.code, 1)


if __name__ == '__main__':
    unittest.main()
