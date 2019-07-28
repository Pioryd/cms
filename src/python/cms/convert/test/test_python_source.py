import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
from convert.file_source import Position
from convert.scope import Scope
from convert.python_source import PythonSource


class TestPythonSource(unittest.TestCase):
  working_directory = os.path.dirname(os.path.abspath(__file__))
  test_source_path = working_directory + "/source_cms_syntax.cms.txt"

  def test_all(self):
    source = Source(self.test_source_path)
    root_scope = Scope(None, Position(source))
    python_source = PythonSource(root_scope)
    # TODO
    # Missing test


if __name__ == '__main__':
  unittest.main()
