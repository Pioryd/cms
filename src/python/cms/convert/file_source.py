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