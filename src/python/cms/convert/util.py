import re


def insert(string: str, index: int, insert_string: str) -> str:
  return string[:index] + insert_string + string[index:]


def replace(string: str, sub_index: int, sub_lenght: int, count: int,
            replace_to: str) -> str:
  if (sub_index < 0 or sub_index >= len(string) or
      sub_index + sub_lenght - (1) >= len(string) or
      sub_index + sub_lenght - (1) < 0):
    raise IndexError("\nstring:[{}]"
                     "\nstring lenght:[{}]"
                     "\nsub-string index:[{}]"
                     "\nsub-string lenght:[{}]"
                     "\ncount:[{}]"
                     "\nreplace to:[{}]".format(string, len(string), sub_index,
                                                sub_lenght, count, replace_to))

  return (string[:sub_index] + (replace_to * count) +
          string[sub_index + sub_lenght:])


def erase(string: str, sub_index: int, sub_lenght: int = -1) -> str:
  if sub_lenght == 0: return string
  if sub_lenght == -1: sub_lenght = len(string) - sub_index

  if (sub_index < 0 or sub_index >= len(string) or
      sub_index + sub_lenght - (1) >= len(string) or
      sub_index + sub_lenght - (1) < 0):
    raise IndexError(
        ("\nstring:[{}]"
         "\nstring lenght:[{}]"
         "\nsub-string index:[{}]"
         "\nsub-string lenght:[{}]").format(string, len(string), sub_index,
                                            sub_lenght))

  return string[:sub_index] + string[sub_index + sub_lenght:]


def substr(string: str, sub_index: int, sub_lenght: int = -1) -> str:
  if sub_lenght == 0: return string
  if sub_lenght < 0: sub_lenght = len(string) - sub_index

  if (sub_index < 0 or sub_index >= len(string) or
      sub_index + sub_lenght - (1) >= len(string) or
      sub_index + sub_lenght - (1) < 0):
    raise IndexError(
        ("\nstring:[{}]"
         "\nstring lenght:[{}]"
         "\nsub-string index:[{}]"
         "\nsub-string lenght:[{}]").format(string, len(string), sub_index,
                                            sub_lenght))

  return string[sub_index:sub_index + sub_lenght]


def remove_double_spaces(string: str) -> str:
  return re.sub("\s\s+", " ", string)


def find(string: str, sub_string: str, position: int = 0) -> int:
  if position >= len(string) or position < 0: return -1
  return string.find(sub_string, position)


def rfind(string: str, sub_string: str, position: int = -1) -> int:
  if position == -1: position = len(string) - 1
  if position >= len(string) or position < 0: return -1
  return string.rfind(sub_string, 0, position + 1)


def split_by_positions(string: str, positions: 'list[str]') -> 'list[str]':
  positions.sort()

  splited = []
  last_position = 0
  for position in positions:
    if position < 0 or position >= len(string):
      raise IndexError(("\nstring:[{}]"
                        "\nstring lenght:[{}]"
                        "\nwrong position:[{}]"
                        "\npositions:[{}]").format(string, len(string),
                                                   position, positions))
    splited.append(string[last_position:position])
    last_position = position + 1

  splited.append(string[last_position:])

  splited = list(filter(None, splited))
  return splited