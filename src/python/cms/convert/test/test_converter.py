import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.converter import Converter


class TestConverter(unittest.TestCase):
  working_directory = os.path.dirname(os.path.abspath(__file__))
  test_cpp_source_path = working_directory + "/source_converter.cms.txt"
  test_py_source_path = working_directory + "/source_converter.py.txt"

  def test_all(self):
    self.converter = Converter(self.test_cpp_source_path)
    self.converter.convert()

    self.maxDiff = None
    with open(self.test_py_source_path) as file:
      self.assertEqual(self.converter.python_source.as_text, file.read())


if __name__ == '__main__':
  unittest.main()