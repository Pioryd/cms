class BlocksOfInstructions(object):

  def __init__(self):
    self.blocks = {}

  def add(self, position: int, source_of_block_of_instructions: str):
    pass

  def _split_block_of_instructions(self, position: int,
                                   source_of_block_of_instructions: str):
    pass

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