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
    block_of_instructions = self.blocks[position]

    cms_include_statement = "#include"
    python_import_statement = "import"
    for i, instruction in enumerate(block_of_instructions):
      instruction = instruction.strip()
      if instruction and instruction[0] == '#':
        instruction = instruction.replace(cms_include_statement,
                                          python_import_statement)
        instruction = instruction.replace('.h', "")
        instruction = instruction.replace('"', ".")
        instruction = instruction.replace('/', ".")
        instruction = instruction.replace('<', "")
        instruction = instruction.replace('>', "")

        block_of_instructions[i] = instruction

  def _convert_comments(self, position: int):
    block_of_instructions = self.blocks[position]

    for i, instruction in enumerate(block_of_instructions):
      instruction = block_of_instructions[i]
      instruction = instruction.strip()
      if instruction and instruction[0] == '/' and instruction[1] == '/':
        instruction = instruction.replace('//', "#", 1)
        block_of_instructions[i] = instruction

  def _convert_initializer_list(self, position: int):
    init_list_syntax = "INITIALIZER_LIST"  # lenght = 16
    init_list_syntax_hash = "#(!&$%!)*$&%^@*%"  # lenght = 16

    block_of_instructions = self.blocks[position]

    for i, instruction in enumerate(block_of_instructions):
      # Encrypt strings to be sure that strings wont break search algorithm.
      instruction, string_dict = (cms_syntax.encrypt_strings(instruction))

      found = instruction.find(init_list_syntax, 0)
      if found != -1:
        # Replace '(' with '['
        found = instruction.find('(', found)
        if found == -1:
          raise Exception("Not found '(' for: " + init_list_syntax)
        instruction = util.replace(instruction, found, 1, 1, "[")

        # Replace ')' with ']'
        found = instruction.find(')', found)
        if found == -1:
          raise Exception("Not found ')' for: " + init_list_syntax)
        instruction = util.replace(instruction, found, 1, 1, "]")

        # Hash initializer list syntax. It's important to distinguish
        # initializer list in string and comments from initializer as cms
        # syntax after we decrypt instruction.
        # NOTE: We cant remove initializer when instruction is encrypted,
        # becouse to decrypt we need string with same size and not changed
        # positions of encrypted strings.
        instruction = instruction.replace(init_list_syntax,
                                          init_list_syntax_hash)
        # no more need decrypted instruction
        instruction = cms_syntax.decrypt_strings(instruction, string_dict)

        # Now we can remove cms initializer syntax
        instruction = instruction.replace(init_list_syntax_hash, "")

        block_of_instructions[i] = instruction

  def _convert_inicializations(self, position: int):
    reserved_cpp_type_qualifiers = ["const", "auto"]
    reserved_cpp_types = [
        "void", "bool", "char", "signed char", "unsigned char", "wchar_t",
        "char16_t", "char32_t", "short", "short int", "signed short",
        "signed short int", "unsigned short", "unsigned short int", "int",
        "signed", "signed int", "unsigned", "unsigned int", "long", "long int",
        "signed long", "signed long int", "unsigned long", "unsigned long int",
        "long long", "long long int", "signed long long",
        "signed long long int", "unsigned long long", "unsigned long long int",
        "float", "double", "long double"
    ]
    additional_cpp_types = [
        "int8_t", "int16_t", "int32_t", "int64_t", "uint8_t", "uint16_t",
        "uint32_t", "uint64_t"
    ]

    block_of_instructions = self.blocks[position]

    for i, instruction in enumerate(block_of_instructions):
      splited_instruction = instruction.split(' ')

      # Minimum ["int", "a", "=",  "123"]
      if len(splited_instruction) < 4: continue

      index_of_type = 0
      if splited_instruction[index_of_type] in reserved_cpp_type_qualifiers:
        index_of_type += 1

        # Minimum ["const", int", "a", "=",  "123"]
        if len(splited_instruction) < 5:
          raise Exception(" Wrong inicialization format: " + instruction)

      # Possible "const auto", "auto const", "const int", "const int32_t"
      # So we must check second time [reserved_cpp_type_qualifiers]
      if (splited_instruction[index_of_type] in reserved_cpp_type_qualifiers or
          (splited_instruction[index_of_type] in reserved_cpp_types) or
          (splited_instruction[index_of_type] in additional_cpp_types) or
          (util.find(splited_instruction[index_of_type], "cms::") != -1)):
        if util.find(instruction, "=") == -1:
          raise Exception(
              "Type must be inicialized by operator '=' in instruction: " +
              instruction)

        found = util.find(instruction, splited_instruction[index_of_type])
        instruction = util.substr(
            instruction, found + len(splited_instruction[index_of_type]))
        instruction = instruction.strip()
      else:
        if index_of_type > 0:
          raise Exception(
              "Type qualifiers found, but not fund the type in instruction: " +
              instruction)

      block_of_instructions[i] = instruction

    # Remove only last empty instruction. Others empty instructions are like new
    # lines. So new lines will more simililar to the original source.a
    if block_of_instructions:
      if not block_of_instructions[len(block_of_instructions) - 1]:
        block_of_instructions = block_of_instructions[:-1]

    self.blocks[position] = block_of_instructions


class Header(object):
  pass


class Scope(object):
  pass