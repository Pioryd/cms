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
    pass

  def _set_headers_to_scopes(self, childs: 'list[Scope]'):
    pass

  def _set_header_to_scope(self, scope: Scope):
    pass

  def _set_instructions_to_scopes(self, childs: 'list<Scope>'):
    pass

  def _set_instructions_to_scope(self, scope: Scope):
    pass