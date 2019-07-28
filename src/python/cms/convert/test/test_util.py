import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

import convert.util as util


class TestUtil(unittest.TestCase):

  def test_insert(self):
    string = "This is a string"
    add = "[some new data]"

    # add string at the end
    self.assertEqual(util.insert(string, len(string), add), string + add)
    self.assertEqual(util.insert(string, len(string) + 100, add), string + add)

    # add string at the begin
    self.assertEqual(util.insert(string, 0, add), add + string)
    self.assertEqual(util.insert(string, 0 - 100, add), add + string)

  def test_replace(self):
    string = "This is a string"
    replace = "c"

    # When sub-string in center of string
    self.assertEqual(util.replace(string, 5, 4, 10, replace),
                     "This cccccccccc string")
    # When sub-string in begin of string
    self.assertEqual(util.replace(string, 0, 4, 5, replace),
                     "ccccc is a string")
    # When sub-string in end of string
    self.assertEqual(util.replace(string, 10, 6, 7, replace),
                     "This is a ccccccc")

    # When index out of range
    with self.assertRaises(IndexError):
      util.replace(string, 50, 4, 10, replace)
    with self.assertRaises(IndexError):
      util.replace(string, -100, 4, 10, replace)
    #
    with self.assertRaises(IndexError):
      util.replace(string, 4, 50, 10, replace)
    with self.assertRaises(IndexError):
      util.replace(string, 4, -100, 10, replace)

  def test_erase(self):
    string = "This is a string"

    # When sub-string in center of string
    self.assertEqual(util.erase(string, 4, 6), "Thisstring")
    self.assertEqual(util.erase(string, 4, 0), string)
    # When sub-string in begin of string
    self.assertEqual(util.erase(string, 0, 5), "is a string")
    # When sub-string in end of string
    self.assertEqual(util.erase(string, 9, 7), "This is a")

    # Default value
    self.assertEqual(util.erase(string, 4), "This")

    # When index of sub-string or part of sub-string is out of range
    with self.assertRaises(IndexError):
      util.erase(string, 4, 50)
    with self.assertRaises(IndexError):
      util.erase(string, -10, 2)
    with self.assertRaises(IndexError):
      util.erase(string, 4, -20)

  def test_substr(self):
    string = "This is a string"

    # When sub-string in center of string
    self.assertEqual(util.substr(string, 4, 6), " is a ")
    self.assertEqual(util.substr(string, 4, 0), string)
    self.assertEqual(util.substr(string, 4, -20), " is a string")
    # When sub-string in begin of string
    self.assertEqual(util.substr(string, 0, 5), "This ")
    # When sub-string in end of string
    self.assertEqual(util.substr(string, 9, 7), " string")

    # Default value
    self.assertEqual(util.substr(string, 4), " is a string")

    # When index of sub-string or part of sub-string is out of range
    with self.assertRaises(IndexError):
      util.substr(string, 4, 50)
    with self.assertRaises(IndexError):
      util.substr(string, -10, 2)

  def test_remove_double_spaces(self):
    string = "   This      is     a     string   "

    self.assertEqual(util.remove_double_spaces(string), " This is a string ")
    self.assertEqual(util.remove_double_spaces(""), "")
    self.assertEqual(util.remove_double_spaces(" "), " ")

  def test_find(self):
    string = "This is a string"

    # Seach in cetner of string
    self.assertEqual(util.find(string, "is", 3), 5)
    self.assertEqual(util.find(string, "is"), 2)

    # Seach in begin of string
    self.assertEqual(util.find(string, "T", 0), 0)
    self.assertEqual(util.find(string, "T"), 0)

    # Seach in end of string
    self.assertEqual(util.find(string, "i", 10), 13)
    self.assertEqual(util.find(string, "i"), 2)

    # Search for last element
    self.assertEqual(util.find(string, "g", 15), 15)
    self.assertEqual(util.find(string, "g"), 15)

    # Search in out of range
    self.assertEqual(util.find(string, "a", 16), -1)
    self.assertEqual(util.find(string, "a", -10), -1)

  def test_rfind(self):
    string = "This is a string"

    # Seach in cetner of string
    self.assertEqual(util.rfind(string, "is", 4), 2)
    self.assertEqual(util.rfind(string, "is"), 5)

    # Seach in begin of string
    self.assertEqual(util.rfind(string, "T", 0), 0)
    self.assertEqual(util.rfind(string, "T", 15), 0)
    self.assertEqual(util.rfind(string, "T"), 0)

    # Seach in end of string
    self.assertEqual(util.rfind(string, "i", 14), 13)
    self.assertEqual(util.rfind(string, "i"), 13)

    # Search for last element
    self.assertEqual(util.rfind(string, "g", 15), 15)
    self.assertEqual(util.rfind(string, "g"), 15)

    # Search in out of range
    self.assertEqual(util.rfind(string, "a", 16), -1)
    self.assertEqual(util.rfind(string, "a", -10), -1)


if __name__ == '__main__':
  unittest.main()