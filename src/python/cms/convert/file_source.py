class Source(object):

  def __init__(self, file_name: str):
    self.file_name = file_name
    self.str = ""
    self._oryginal = ""

    self.reload()

  def reload(self):
    with open(self.file_name, "r") as file:
      self._oryginal = file.read()
    self.str = self._oryginal

  def restore(self):
    self.str = self._oryginal

  def get_oryginal(self):
    return self._oryginal


class Position(object):

  def __init__(self, source: Source = None, position: 'Position' = None):
    if ((not (source and type(source) is Source)) and
        (not (position and type(position) is Position))):
      raise Exception("Unable to create Position."
                      "\n\tsource is not None: {}"
                      "\n\tsource is type of Source: {}[{}]"
                      "\n\tposition is not None: {}"
                      "\n\tposition is type of Position: {}[{}]".format(
                          bool(source), bool(type(source) is Source),
                          type(source), bool(position),
                          bool(type(position) is Position), type(position)))

    if source:
      self._index = 0
      self._line_number = 1
      self._line_position = 1
      self.source = source
    else:
      self._index = position._index
      self._line_number = position._line_number
      self._line_position = position._line_position
      self.source = position.source

  def move(self, count: int = 1) -> bool:
    index_last = len(self.source.str) - 1
    if self._index + count > index_last: return False

    i = 0
    while i < count:
      if self._index + 1 > index_last: return False

      if self.get_character() == '\n':
        self._line_number += 1
        self._line_position = 1
      else:
        self._line_position += 1

      self._index += 1

      i += 1

    return True

  def rmove(self, count: int = 1) -> bool:
    if self._index - count < 0: return False

    i = 0
    while i < count:
      if self._index - 1 < 0: return False

      if self.source.str[self._index - 1] == '\n':
        self._line_number -= 1

        # detect line lenght
        found = self.source.str.rfind('\n', 0, self._index - 1)
        if found == -1:
          self._line_position = self._index
        else:
          self._line_position = self._index - 1 - found
      else:
        self._line_position -= 1

      self._index -= 1
      i += 1

    return True


def go_to_begin_of_line(self, line: int = 0) -> bool:
  if line < 1: line = self._line_number
  old_position = Position(position=self)

  while not (line == self._line_number and self._line_position == 1):
    if self._line_number > line:
      if not self.rmove():
        self.__init__(position=old_position)
        return False
    elif self._line_number < line:
      if not self.move():
        self.__init__(position=old_position)
        return False
    elif self._line_position > 1:
      if not self.rmove():
        self.__init__(position=old_position)
        return False
  return True


def go_to_end_of_line(self, line: int = 0):
  if line < 1: line = self._line_number
  old_position = Position(position=self)

  index_end = len(self.source.str) - 1
  while (not (line == self._line_number and
              (self.get_character() == '\n' or self._index == index_end))):
    if self._line_number > line:
      if not self.rmove():
        self.__init__(position=old_position)
        return False
    elif self._line_number < line:
      if not self.move():
        self.__init__(position=old_position)
        return False
    elif self.get_character() != '\n':
      if self._index < (len(self.source.str) - 1):
        if not self.move():
          self.__init__(position=old_position)
          return False
  return True


def set_after_spaces(self) -> bool:
  old_position = Position(position=self)

  while self.move():
    if not self.get_character().isspace(): return True

  self.__init__(position=old_position)
  return False


def set_before_spaces(self) -> bool:
  old_position = Position(position=self)

  while self.rmove():
    if not self.get_character().isspace(): return True

  self.__init__(position=old_position)
  return False


def set_at_left_bound_parenthesis(self) -> bool:
  if self.get_character() != ')': return False

  old_position = Position(position=self)
  opened = 0
  while True:
    if self.get_character() == ')': opened += 1
    elif self.get_character() == '(': opened -= 1

    if opened == 0: break
    if not self.rmove():
      self.__init__(position=old_position)
      return False
  return True


def set_at_right_bound_parenthesis(self) -> bool:
  if self.get_character() != '(': return False

  old_position = Position(position=self)
  opened = 0
  while True:
    if self.get_character() == '(': opened += 1
    elif self.get_character() == ')': opened -= 1

    if opened == 0: break
    if not self.move():
      self.__init__(position=old_position)
      return False
  return True