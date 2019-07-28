import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
from convert.file_source import Position


class TestSource(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    pass

  def setUp(self):
    pass

  def test_init(self):
    pass

  def test_reload_source(self):
    pass

  def test_restore_source(self):
    pass


class TestPosition(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    pass

  def setUp(self):
    pass

  def test_init(self):
    pass

  def test_move_and_rmove(self):
    pass

  def test_set_positions(self):
    pass

  def test_to_string(self):
    pass


if __name__ == '__main__':
  unittest.main()
