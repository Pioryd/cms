class _Indent(object):

  def __init__(self, size: int):
    self._size = size
    self.count = 0
    self.as_text = ""

  def increase(self, count=1):
    self.count += count
    self._update_text()

  def decrease(self, count=1):
    self.count = max(self.count - count, 0)
    self._update_text()

  def _update_text(self):
    self.as_text = ' ' * (self._size * self.count)


class PythonSource(object):

  def __init__(self, root_scope: Scope):
    self.as_text = ""
    self._indent = _Indent(2)
    self._found_new_line_instruction = False

    self._convert(root_scope)

  def _convert(self, scope: Scope):
    self.as_text += self._indent.as_text + scope.header.header_source + "\n"

    if scope.header.type != Header.Type.ROOT:
      self._found_new_line_instruction = False
      self._indent.increase()

    childs = scope.childs

    block_of_instructions = scope.blocks_of_instructions.blocks

    if (not childs):
      for index, blocks in block_of_instructions.items():
        for block in blocks:
          self._found_new_line_instruction = False
          self.as_text += self._indent.as_text + block + "\n"
    else:
      i = 0
      while i < len(childs):
        child = childs[i]

        if (i - 1) in block_of_instructions:
          for block in block_of_instructions[i - 1]:
            self._found_new_line_instruction = False
            self.as_text += self._indent.as_text + block + "\n"
        self._convert(child)
        i += 1
      if len(childs) in block_of_instructions:
        for block in block_of_instructions[len(childs)]:
          self._found_new_line_instruction = False
          self.as_text += self._indent.as_text + block + "\n"

    if scope.header.type != Header.Type.ROOT:
      self._indent.decrease()
      if (self._found_new_line_instruction == False):
        self.as_text += "\n"
        _found_new_line_instruction = True
