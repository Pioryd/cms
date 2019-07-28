from convert.scope import Scope
from convert.scope import Header
from convert.python_source import PythonSource
from convert.file_source import Position
from convert.file_source import Source
import convert.util as util
import convert.cms_syntax as cms_syntax


class Converter(object):

  def __init__(self, file_path: str):
    self.source = Source(file_path)
    self.root_scope = Scope(parent=None,
                            open_statement_position=Position(self.source),
                            type=Header.Type.ROOT)
    self.python_source = None

  def convert(self):
    # Encrypt all strings to make enable search scopes by brackets. Otherwhise
    # brackets from strings can break search algorithm.
    self.source.str, encrypted_strings = cms_syntax.encrypt_strings(
        self.source.str)

    # Check if source constains any unsupported syntax.
    unsupported_syntax = cms_syntax.find_unsupported_syntax(self.source.str)
    if unsupported_syntax:
      raise Exception("Unupported syntax found: %s'" % (unsupported_syntax))

    # Only create tree of scopes with positions of scope begin, open statement
    # and close statement.
    self._create_scopes_by_brackets()

    # After created tree of scopes, strings dont have to be encrypted.
    self.source.str = cms_syntax.decrypt_strings(self.source.str,
                                                 encrypted_strings)

    # Convert scope's headers from c++ to python syntax.
    self._set_headers_to_scopes(self.root_scope.childs)

    # Convert scope's instructions from c++ to python syntax.
    self._set_instructions_to_scope(self.root_scope)
    self._set_instructions_to_scopes(self.root_scope.childs)

    # Convert tree of scopes to python source
    self.python_source = PythonSource(self.root_scope)

  def get_python_source(self) -> str:
    return self.python_source.as_text

  def _create_scopes_by_brackets(self):
    current_position = Position(self.source)
    current_scope = self.root_scope
    is_open = False

    while True:
      if current_position.get_character() == '{':
        current_scope = current_scope.process_open(current_position)
        is_open = True
      if current_position.get_character() == '}':
        current_scope = current_scope.process_close(current_position)
        is_open = False
      if not current_position.move(): break

    current_scope.process_close(current_position)

    if is_open: raise Exception("One or more brackets missing.")

  def _set_headers_to_scopes(self, childs: 'list[Scope]'):
    for child in childs:
      self._set_header_to_scope(child)
      self._set_headers_to_scopes(child.childs)

  def _set_header_to_scope(self, scope: Scope):
    current_position = Position(position=scope.open_statement_position)

    #  *  <-     *
    # ')' <- ')  {'
    current_position.set_before_spaces()

    scope_type = Header.Type.UNKNOWN
    scope_header_start = 0
    scope_header_size = 0

    its_not_function = False

    if current_position.get_character() == ')':
      # Possible: [function] or [while] or [if]

      #               * <-*
      # 'while( (a) > (b) )'
      found = util.rfind(self.source.str, '(', current_position.get_index())
      if found == -1:
        raise Exception("Not found left parenthesis: '('. %s" %
                        (current_position.to_string()))

      #  '( )'  33 % is function
      # '( (a) > (b) )' 100% is NOT function
      if (util.find((util.substr(self.source.str, found + 1,
                                 current_position.get_index() - found - 1)),
                    ")") != -1):  # Possible: [while] or [if]
        current_position.set_at_left_bound_parenthesis()
        its_not_function = True
      else:  # Possible: [function] or [while] or [if]
        current_position.rmove(current_position.get_index() - found)

      #   * <- *
      # 'if    (a)'
      current_position.set_before_spaces()

      if_statement = "if"
      while_statement = "while"
      start_index_of_if_statement = (current_position.get_index() -
                                     len(if_statement) + 1)
      start_index_of_while_statement = (current_position.get_index() -
                                        len(while_statement) + 1)

      if (util.substr(self.source.str, start_index_of_if_statement,
                      len(if_statement)) == if_statement):  # [IF]
        scope_type = Header.Type.IF_STATEMENT
        scope_header_start = start_index_of_if_statement
        scope_header_size = (scope.open_statement_position.get_index() -
                             start_index_of_if_statement)
      elif (util.substr(self.source.str, start_index_of_while_statement,
                        len(while_statement)) == while_statement):  # [WHILE]
        scope_type = Header.Type.LOOP_WHILE
        scope_header_start = start_index_of_while_statement
        scope_header_size = (scope.open_statement_position.get_index() -
                             start_index_of_while_statement)
      else:  # [FUNCTION]
        if its_not_function:
          raise Exception(
              "Wrong statement. Its not 'while' and not 'if': '('. " +
              current_position.to_string())

        start_index_of_function = -1
        if current_position.get_line_number() == 1:
          start_index_of_function = 0
        else:
          new_line_character = "\n"
          start_index_of_function = (
              util.rfind(self.source.str, new_line_character,
                         current_position.get_index()) +
              len(new_line_character))
          if start_index_of_function == -1:
            raise Exception("No function type: '('. %s" %
                            (current_position.to_string()))

        scope_type = Header.Type.FUNCTION
        scope_header_start = start_index_of_function
        scope_header_size = (scope.open_statement_position.get_index() -
                             start_index_of_function)

      # TODO
      # Check if position of '(' is outsdie of possile range like parent
      # openStatementPosition or previous child
      # closeStatementPosition
    else:  # [struct]
      # TODO
      # Check if position of 'struct' is outsdie of possile range like parent
      # openStatementPosition or previous child
      # closeStatementPosition

      scope_type = Header.Type.STRUCT

      found = util.rfind(self.source.str, "struct",
                         current_position.get_index())
      if found == -1:
        raise Exception("Not found struct statement: 'struct'. {}".format(
            current_position.to_string()))

      scope_header_start = found
      scope_header_size = (scope.open_statement_position.get_index() - found)

    if scope_type == Header.Type.UNKNOWN: raise Exception("Unknown scope type")

    scope.header.set(
        scope_type,
        util.substr(self.source.str, scope_header_start, scope_header_size),
        scope_header_start)

  def _set_instructions_to_scopes(self, childs: 'list<Scope>'):
    for child in childs:
      self._set_instructions_to_scope(child)
      self._set_instructions_to_scopes(child.childs)

  def _set_instructions_to_scope(self, scope: Scope):
    # Position of instruction is [right_side_child_index - 1]
    #            ins[-1]       child[0]    ins[0]     child[1]     ins[2]
    # 'fun(){ INSTRUCTIONS while(){...} INSTRUCTION while(){...} INSTRUCTIONS}'

    #current_position = Position(self.source)

    # Because CloseStatement '};' is set at ';'. It will be set to '}' later.
    fix_struct_close_statement_index = 0

    # Because we dont want close and open statements in sub-string.
    fix_open_statement_position = 1
    fix_close_statement_position = 1
    fix_header_start_position = 1

    if not scope.childs:
      if scope.header.type == Header.Type.STRUCT:
        fix_struct_close_statement_index = 1

      index = (scope.open_statement_position.get_index() +
               fix_open_statement_position)
      lenght = ((1) + scope.close_statement_position.get_index() -
                scope.open_statement_position.get_index() -
                fix_open_statement_position - fix_close_statement_position -
                fix_struct_close_statement_index)

      if scope.header.type == Header.Type.ROOT:
        index -= fix_open_statement_position
        lenght += fix_open_statement_position

      instructions = ""
      if lenght > 0:
        instructions = util.substr(self.source.str, index, lenght) + "\n"
        instructions = instructions.strip()
      if not instructions: instructions = "pass"
      scope.blocks_of_instructions.add(-1, instructions)

    i = 0
    while i < len(scope.childs):
      current_child = scope.childs[i]

      if i == 0:
        index = (scope.open_statement_position.get_index() +
                 fix_open_statement_position)
        lenght = ((1) + current_child.header.index_at_main_source -
                  scope.open_statement_position.get_index() -
                  fix_open_statement_position - fix_header_start_position)

        if scope.header.type == Header.Type.ROOT:
          index -= fix_open_statement_position

        if lenght > 0:
          instructions = util.substr(self.source.str, index, lenght) + "\n"
          instructions = instructions.strip()
          scope.blocks_of_instructions.add(i - 1, instructions)
      else:
        previous_child = scope.childs[i - 1]

        index = (previous_child.close_statement_position.get_index() +
                 fix_open_statement_position)
        lenght = ((1) + current_child.header.index_at_main_source -
                  previous_child.close_statement_position.get_index() -
                  fix_open_statement_position - fix_header_start_position)

        if lenght > 0:
          instructions = util.substr(self.source.str, index, lenght) + "\n"
          instructions = instructions.strip()
          scope.blocks_of_instructions.add(i - 1, instructions)

      if i == (len(scope.childs) - 1):
        if scope.header.type == Header.Type.STRUCT:
          fix_struct_close_statement_index = 1

        index = (current_child.close_statement_position.get_index() +
                 fix_open_statement_position)
        lenght = ((1) + scope.close_statement_position.get_index() -
                  current_child.close_statement_position.get_index() -
                  fix_struct_close_statement_index -
                  fix_open_statement_position - fix_close_statement_position)

        if scope.header.type == Header.Type.ROOT:
          lenght += fix_open_statement_position

        if lenght > 0:
          instructions = util.substr(self.source.str, index, lenght) + "\n"
          instructions = instructions.strip()
          scope.blocks_of_instructions.add(len(scope.childs), instructions)
      i += 1