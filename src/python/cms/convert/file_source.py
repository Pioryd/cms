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
