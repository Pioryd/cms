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
    blocks_of_instructions = BlocksOfInstructions()
    source_of_block_of_instructions = ("int a = 1;\n"
                                       "cms::string b = \"hello\";\n"
                                       "int c = a + 10;")
    block_of_instructions = ['a = 1', 'b = \"hello\"', 'c = a + 10']

    blocks_of_instructions.add(12, source_of_block_of_instructions)
    for position, block in blocks_of_instructions.blocks.items():
      self.assertEqual(len(block), len(block_of_instructions))
      i = 0
      while i < len(block):
        self.assertEqual(block[i], block_of_instructions[i])
        i += 1


class TestHeader(unittest.TestCase):

  def test_all(self):
    pass


class TestScope(unittest.TestCase):

  def test_open_and_close(self):
    pass


if __name__ == '__main__':
  unittest.main()