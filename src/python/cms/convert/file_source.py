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
