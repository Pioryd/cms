import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
from convert.file_source import Position


class TestSource(unittest.TestCase):
  WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
  TEST_SOURCE_PATH = WORKING_DIRECTORY + "/source_file_source.txt"

  TEST_SOURCE_DATA = ("This is      string\n"
                      "This is second line\n"
                      "This is third line\n"
                      "\n"
                      "\n"
                      "This is line number 6\n"
                      "This is line number 7\n"
                      "This is l(ne )um)er 8\n"
                      "This (is (line) ((number))) 9\n"
                      "This is line num(e( 10")

  @classmethod
  def setUpClass(self):
    self.source = Source(self.TEST_SOURCE_PATH)

  def setUp(self):
    self.source.restore()

  def test_init(self):
    with self.assertRaises(FileNotFoundError):
      Source("Wrong_path")

    source = Source(self.TEST_SOURCE_PATH)

    self.assertEqual(source.str, source._oryginal)
    self.assertEqual(source.str, self.TEST_SOURCE_DATA)

  def test_reload_source(self):
    self.source.str += "@"
    self.source._oryginal += "@"

    temp_str = self.source.str
    temp_oryginal = self.source._oryginal

    self.source.reload()

    self.assertEqual(self.source.str, self.source._oryginal)
    self.assertNotEqual(self.source.str, temp_str)
    self.assertNotEqual(self.source._oryginal, temp_oryginal)

  def test_restore_source(self):
    self.source.str += "@"
    temp_str = self.source.str

    self.source.restore()

    self.assertEqual(self.source.str, self.source._oryginal)
    self.assertNotEqual(self.source.str, temp_str)


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
