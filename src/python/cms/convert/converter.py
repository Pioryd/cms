from convert.scope import Scope


class Converter(object):

  def __init__(self, file_path: str):
    pass

  def convert(self):
    pass

  def get_python_source(self) -> str:
    pass

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