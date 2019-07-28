import sys
import itertools
from enum import Enum
from typing import Dict

import convert.util as util
import convert.cms_syntax as cms_syntax
from convert.cms_syntax import EncryptedString
from convert.file_source import Position


class BlocksOfInstructions(object):

  def __init__(self):
    self.blocks = {}

  def add(self, position: int, source_of_block_of_instructions: str):
    self._split_block_of_instructions(position, source_of_block_of_instructions)
    self._convert_includes(position)
    self._convert_comments(position)
    self._convert_initializer_list(position)
    self._convert_inicializations(position)

  def _split_block_of_instructions(self, position: int,
                                   source_of_block_of_instructions: str):
    # Split instructions by character ';'. To do that, we have have to first add
    # ';' to comments and includes'.

    # Encrypt all strings to be sure that any part of any string wont break
    # search algorithm
    source_of_block_of_instructions, string_dict = (
        cms_syntax.encrypt_strings(source_of_block_of_instructions))

    # Get positions of ';' and "#include"'.
    positions_of_semicolon = []
    positions_of_include = []
    for i, character in enumerate(source_of_block_of_instructions):
      if character == ';': positions_of_semicolon.append(i)
      elif character == '#': positions_of_include.append(i)

    # No more need encrypted source
    source_of_block_of_instructions = cms_syntax.decrypt_strings(
        source_of_block_of_instructions, string_dict)

    # Encrypt only strings(apostrophe and quotation) to be sure that strings
    # wont break search algorithm for positions of comments
    source_of_block_of_instructions, string_dict = cms_syntax.encrypt_strings(
        source_of_block_of_instructions, [
            EncryptedString.Type.STRING_APOSTROPHE,
            EncryptedString.Type.STRING_QUOTATION
        ])

    # Get position of '//'
    positions_of_comment = []
    i = 0
    while i < len(source_of_block_of_instructions):
      found = util.find(source_of_block_of_instructions, "//", i)
      if found == -1:
        break
      else:
        positions_of_comment.append(i)
        found = util.find(source_of_block_of_instructions, "\n", found)
        if found == -1: break
        else: i = found
      i += 1

    # No more need encrypted strings
    source_of_block_of_instructions = cms_syntax.decrypt_strings(
        source_of_block_of_instructions, string_dict)

    # Find close statements '\n' and repleace them with ';'.
    # If close statement not found then add ';' to the end of the string.
    #
    # For includes
    for position_of_include in positions_of_include:
      found = util.find(source_of_block_of_instructions, "\n",
                        position_of_include)
      if found == -1:
        source_of_block_of_instructions += ';'
        positions_of_semicolon.append(i + 1)
        break
      else:
        source_of_block_of_instructions = util.replace(
            source_of_block_of_instructions, found, 1, 1, ';')
        positions_of_semicolon.append(i)
    #
    # For comments
    for position_of_include in positions_of_comment:
      found = util.find(source_of_block_of_instructions, "\n",
                        position_of_include)
      if found == -1:
        source_of_block_of_instructions += ';'
        positions_of_semicolon.append(i + 1)
        break
      else:
        source_of_block_of_instructions = util.replace(
            source_of_block_of_instructions, found, 1, 1, ';')
        positions_of_semicolon.append(i)

    # Split source
    block_of_instructions = source_of_block_of_instructions.split(';')

    # Add block of instructions to our blocks dict
    self.blocks[position] = block_of_instructions

    # Remove end line charactes from instructions.
    i = 0
    while i < len(block_of_instructions):
      block_of_instructions[i] = block_of_instructions[i].replace("\n", "")
      block_of_instructions[i] = util.remove_double_spaces(
          block_of_instructions[i])
      block_of_instructions[i] = block_of_instructions[i].strip()
      i += 1

    # At this point there are some empty instructions. These are new emtpy lines
    # from cms source. We are not removing them to make python code more
    # same looking to cms source

    # Remove only last empty instruction. Others empty instructions are like new
    # lines. So new lines will more simililar to cms source
    if block_of_instructions:
      if not block_of_instructions[len(block_of_instructions) - 1]:
        block_of_instructions = block_of_instructions[:-1]

  def _convert_includes(self, position: int):
    pass

  def _convert_comments(self, position: int):
    pass

  def _convert_initializer_list(self, position: int):
    pass

  def _convert_inicializations(self, position: int):
    pass


class Header(object):
  pass


class Scope(object):
  pass