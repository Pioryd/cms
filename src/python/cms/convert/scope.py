import sys
import itertools
from enum import Enum
from typing import Dict

import convert.util as util
import convert.cms_syntax as cms_syntax
from convert.cms_syntax import EncryptedString
from convert.file_source import Position


class BlocksOfInstructions(object):
  """ Constains converted blocks of instructions from cms to python syntax.
  
  Attributes:
    blocks: dict[position: int, block_of_instructions: list[instruction: str]]
      position: index position between scope childs (next_child_index - 1)
      block_of_instructions: list of instructions as python syntax
  """

  def __init__(self):
    self.blocks = {}

  def add(self, position: int, source_of_block_of_instructions: str):
    """ Collect block of instrunctions and convert them.
    
    Convert instructions from cms to python syntax.

    Args:
      position: index position between scope childs (next_child_index - 1)
      source_of_block_of_instructions: source of blocks of instruction in
        cms syntax
    """
    self._split_block_of_instructions(position, source_of_block_of_instructions)
    self._convert_includes(position)
    self._convert_comments(position)
    self._convert_initializer_list(position)
    self._convert_inicializations(position)

  def _split_block_of_instructions(self, position: int,
                                   source_of_block_of_instructions: str):
    """ Split block of instructions to single instructions.
    
    Args:
      position: index position between scope childs (next_child_index - 1)
      source_of_block_of_instructions: source of blocks of instruction in
        cms syntax.
    """
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
    """ Convert includes.

    Example:
      ["#include <cms>"] -> ["import cms"]
    
    Args:
      position: index position between scope childs (next_child_index - 1)
    """
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
    """ Convert comments.

    Example:
      ["//"] -> ["#"]
    
    Args:
      position: index position between scope childs (next_child_index - 1)
    """
    block_of_instructions = self.blocks[position]

    for i, instruction in enumerate(block_of_instructions):
      instruction = block_of_instructions[i]
      instruction = instruction.strip()
      if instruction and instruction[0] == '/' and instruction[1] == '/':
        instruction = instruction.replace('//', "#", 1)
        block_of_instructions[i] = instruction

  def _convert_initializer_list(self, position: int):
    """ Convert inicializer list to python syntax.

    Example:
      "INITIALIZER_LIST(1, 4, 7,...n)" -> "[1, 4, 7,...n]"
    
    Args:
      position: index position between scope childs (next_child_index - 1)
    """
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
    """ Convert inicializations to python syntax.

    Example:
      "int a = 5" -> "a = 5"
    
    Args:
      position: index position between scope childs (next_child_index - 1)
    """
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

  class Type(Enum):
    UNKNOWN = 1
    ROOT = 2
    STRUCT = 3
    FUNCTION = 4
    LOOP_WHILE = 5
    IF_STATEMENT = 6

  def __init__(self, index_at_main_source: int, type=Type.UNKNOWN):
    self.index_at_main_source = index_at_main_source
    self.type = type
    self.header_source = ""

  def set(self, type: Type, header_body_source: str, index_at_main_source: int):
    self.type = type
    self.index_at_main_source = index_at_main_source

    if type == Header.Type.STRUCT:
      self._convert_struct(header_body_source)
    if type == Header.Type.LOOP_WHILE or type == Header.Type.IF_STATEMENT:
      self._convert_while_or_if(header_body_source)
    if type == Header.Type.FUNCTION:
      self._convert_function(header_body_source)

  def _convert_struct(self, header_body_source: str):
    header_body_source = header_body_source.replace(',', ' ')
    header_body_source = header_body_source.replace(':', ' ')
    header_body_source = util.remove_double_spaces(header_body_source)
    header_body_source = header_body_source.strip()

    splited_header = header_body_source.split(" ")

    for i, header_part in enumerate(splited_header):
      if i == 0:
        self.header_source += "class "
        continue

      if len(splited_header) == 2:
        self.header_source += header_part
        self.header_source += "(object):"
        break

      if i > 0: self.header_source += header_part
      if i == 1: self.header_source += "("
      if (i > 1) and (i < (len(splited_header) - 1)): self.header_source += ", "
      if i == len(splited_header) - 1: self.header_source += "):"

  def _convert_while_or_if(self, header_body_source: str):
    header_body_source = header_body_source.replace('->', '.')
    header_body_source = header_body_source.replace('cms::', 'convert.')
    header_body_source = util.remove_double_spaces(header_body_source)
    header_body_source = header_body_source.strip()

    header_body_source += ":"

    header_body_source = header_body_source.replace(" || ", " or ")
    header_body_source = header_body_source.replace(" && ", " and ")

    self.header_source = header_body_source

  def _convert_function(self, header_body_source: str):
    index_of_close_statement = header_body_source.find('(')

    # "void  fun  (args..)" -> "void  fun  "
    function_name = util.substr(header_body_source, 0, index_of_close_statement)
    # "void  fun  " -> "void  fun"
    function_name = function_name.strip()
    # "void  fun" -> " fun"
    function_name = util.substr(function_name, function_name.rfind(' '))
    # " fun" -> "fun"
    function_name = function_name.strip()

    header_body_source = header_body_source[index_of_close_statement:]

    header_body_source = header_body_source.replace('(', ',')
    header_body_source = header_body_source.replace(')', ',')
    header_body_source = header_body_source.replace('::', '.')
    header_body_source = header_body_source.replace('\n', ' ')
    header_body_source = util.remove_double_spaces(header_body_source)

    header_body_source = header_body_source.replace('const,', ',')
    header_body_source = header_body_source.replace(',const', ',')
    header_body_source = header_body_source.replace('const ', ' ')
    header_body_source = header_body_source.replace(' const,', ' ')
    header_body_source = header_body_source.replace('*,', '')
    header_body_source = header_body_source.replace('&,', '')

    header_body_source = header_body_source.strip()

    function_arguments = header_body_source.split(",")

    # Remove types from arguments. "int a" -> "a"
    i = 0
    while i < len(function_arguments):
      if not function_arguments[i]:
        del function_arguments[i]
        continue
      else:
        index_of_open_statement = function_arguments[i].rfind(" ")
        if index_of_open_statement == -1:
          raise Exception("Argument without type: %s." %
                          (function_arguments[i]))
        function_arguments[i] = function_arguments[i][index_of_open_statement:]
        function_arguments[i] = function_arguments[i].strip()
      i += 1

    # Create python syntax "def fun(args...):"
    self.header_source += "def " + function_name + "("
    for i, argument in enumerate(function_arguments):
      self.header_source += argument
      if i < (len(function_arguments) - 1): self.header_source += ", "
    self.header_source += "):"


class Scope(object):
  STATIC_ID = itertools.count()

  def __init__(self,
               parent: 'Scope',
               open_statement_position: Position,
               close_statement_position: Position = None,
               type: Header.Type = Header.Type.UNKNOWN):
    self.id = next(Scope.STATIC_ID)
    self.blocks_of_instructions = BlocksOfInstructions()
    self.header = Header(open_statement_position.get_index(), type)
    self.parent = parent
    self.childs = []
    self.open_statement_position = Position(position=open_statement_position)
    if close_statement_position == None:
      self.close_statement_position = Position(position=open_statement_position)
    else:
      self.close_statement_position = Position(
          position=close_statement_position)

  def process_open(self, open_statement_position: Position) -> 'Scope':
    self.childs.append(Scope(self, open_statement_position))
    return self.childs[len(self.childs) - 1]

  def process_close(self, close_statement_position: Position) -> 'Scope':
    self.close_statement_position = Position(position=close_statement_position)
    return self.parent