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


if __name__ == '__main__':
  unittest.main()