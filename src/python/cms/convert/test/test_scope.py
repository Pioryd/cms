import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
from convert.file_source import Position
from convert.scope import BlocksOfInstructions
from convert.scope import Header
from convert.scope import Scope


class TestBlocksOfInstructions(unittest.TestCase):

  def test_all(self):
    pass


class TestHeader(unittest.TestCase):

  def test_all(self):
    pass


class TestScope(unittest.TestCase):

  def test_open_and_close(self):
    pass


if __name__ == '__main__':
  unittest.main()