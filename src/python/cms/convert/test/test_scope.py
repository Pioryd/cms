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
    # test struct
    cpp_header = "struct MyStruct : Parent, OldParent"
    python_header = "class MyStruct(Parent, OldParent):"
    header = Header(0)
    #
    header.set(Header.Type.STRUCT, cpp_header, 0)
    self.assertEqual(header.header_source, python_header)

    # test while
    cpp_header = "while(var == true && is_openon || (test == 5))"
    python_header = "while(var == true and is_openon or (test == 5)):"
    header = Header(0)
    #
    header.set(Header.Type.LOOP_WHILE, cpp_header, 0)
    self.assertEqual(header.header_source, python_header)

    # test if
    cpp_header = "if(var == true && is_openon || (test == 5))"
    python_header = "if(var == true and is_openon or (test == 5)):"
    header = Header(0)
    #
    header.set(Header.Type.IF_STATEMENT, cpp_header, 0)
    self.assertEqual(header.header_source, python_header)

    # test finction
    cpp_header = "void fun(const int a, char* b, const std::string& c)"
    python_header = "def fun(a, b, c):"
    header = Header(0)
    #
    header.set(Header.Type.FUNCTION, cpp_header, 0)
    self.assertEqual(header.header_source, python_header)


class TestScope(unittest.TestCase):
  working_directory = os.path.dirname(os.path.abspath(__file__))
  test_source_path = working_directory + "/source_cms_syntax.cms.txt"

  def test_open_and_close(self):
    source = Source(self.test_source_path)

    root_scope = Scope(None, Position(source))
    # 1# child
    scope = root_scope.process_open(Position(source))
    scope = scope.process_close(Position(source))
    # 2# child
    scope = scope.process_open(Position(source))
    scope = scope.process_close(Position(source))
    # 3# child
    scope = scope.process_open(Position(source))
    scope = scope.process_close(Position(source))
    # 4# child
    scope = scope.process_open(Position(source))
    scope = scope.process_close(Position(source))

    self.assertEqual(len(root_scope.childs), 4)
    if __name__ == '__main__':
      self.assertEqual(root_scope.id, 0)
      self.assertEqual(root_scope.childs[0].id, 1)
      self.assertEqual(root_scope.childs[1].id, 2)
      self.assertEqual(root_scope.childs[2].id, 3)
      self.assertEqual(root_scope.childs[3].id, 4)


if __name__ == '__main__':
  unittest.main()