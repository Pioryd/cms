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
  WORKING_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
  TEST_SOURCE_PATH = WORKING_DIRECTORY + "/source_file_source.txt"

  @classmethod
  def setUpClass(self):
    self.source = Source(self.TEST_SOURCE_PATH)

  def setUp(self):
    self.source.restore()

  def test_init(self):
    with self.assertRaises(Exception):
      Position(None)
    with self.assertRaises(Exception):
      Position(None, None)

    position = Position(self.source)

    self.assertEqual(position.get_index(), position._index)
    self.assertEqual(position.get_line_number(), position._line_number)
    self.assertEqual(position.get_line_position(), position._line_position)

    self.assertEqual(position.get_index(), 0)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 1)

    self.assertTrue(position.move(5))
    position_2 = Position(position=position)
    self.assertEqual(position.get_index(), position_2.get_index())
    self.assertEqual(position.get_line_number(), position_2.get_line_number())
    self.assertEqual(position.get_line_position(),
                     position_2.get_line_position())

  def test_move_and_rmove(self):
    position = Position(self.source)

    first_line_data = "This is test string\n"
    first_line_lenght = len(first_line_data)

    # Move with default parameter
    self.assertTrue(position.move())
    self.assertEqual(position.get_index(), 1)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 2)

    # Move with given parameter
    self.assertTrue(position.move(2))
    self.assertEqual(position.get_index(), 3)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 4)

    # Move throught new line
    self.assertTrue(position.move(first_line_lenght))
    self.assertEqual(position.get_index(), first_line_lenght + 3)
    self.assertEqual(position.get_line_number(), 2)
    self.assertEqual(position.get_line_position(), 4)

    # Rmove throught new line
    self.assertTrue(position.rmove(first_line_lenght))
    self.assertEqual(position.get_index(), 3)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 4)

    # Rmove with given parameter
    self.assertTrue(position.rmove(2))
    self.assertEqual(position.get_index(), 1)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 2)

    # Rmove with default parameter
    self.assertTrue(position.rmove())
    self.assertEqual(position.get_index(), 0)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 1)

    # Test move throught many new lines
    self.assertTrue(position.move(61))
    self.assertEqual(position.get_index(), 61)
    self.assertEqual(position.get_line_number(), 6)
    self.assertEqual(position.get_line_position(), 1)

    # Test rmove throught many new lines
    self.assertTrue(position.rmove())
    self.assertEqual(position.get_line_number(), 5)
    self.assertEqual(position.get_line_position(), 1)
    #
    self.assertTrue(position.rmove())
    self.assertEqual(position.get_line_number(), 4)
    self.assertEqual(position.get_line_position(), 1)
    #
    self.assertTrue(position.rmove())
    self.assertEqual(position.get_line_number(), 3)
    self.assertEqual(position.get_line_position(), 19)
    #
    self.assertTrue(position.rmove(58))
    self.assertEqual(position.get_index(), 0)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 1)

    # Test move outside source range
    position = Position(self.source)
    self.assertFalse(position.rmove())
    self.assertEqual(position.get_index(), 0)
    self.assertEqual(position.get_line_number(), 1)
    self.assertEqual(position.get_line_position(), 1)
    self.assertTrue(position.go_to_end_of_line(10))
    #
    self.assertFalse(position.move())
    self.assertEqual(position.get_index(), 178)
    self.assertEqual(position.get_line_number(), 10)
    self.assertEqual(position.get_line_position(), 22)

  def test_set_positions(self):
    pass

  def test_to_string(self):
    pass


if __name__ == '__main__':
  unittest.main()
