from enum import Enum


class EncryptedString(object):

  class Type(Enum):
    NONE = 1
    COMMENT = 2
    STRING_APOSTROPHE = 3
    STRING_QUOTATION = 4

  def __init__(self, type: Type):
    self.type = type