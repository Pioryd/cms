import re


def insert(string: str, index: int, insert_string: str) -> str:
  """ Insert string to another string at given position.

  Args:
    string: string to which will be added additional string.
    index: index to palce inserted string. If less then 0 then palce at the
      begin. If greater then zero then place at the end.
    insert_string: inserted string.

  Returns:
    string: result of insert.
  """
  return string[:index] + insert_string + string[index:]


def replace(string: str, sub_index: int, sub_lenght: int, count: int,
            replace_to: str) -> str:
  """ Replace sub-string with given amount of strings.

  Args:
    string: string to which will be added additional string.
    sub_index: index of sub-string to replace.
    sub_lenght: lenght of sub-string to replace.
    count: how many times add new string in place of replaced sub-string
      Less then 0 mean 0.
    replace_to: string to replace.

  Returns:
    string: result of replace.

  Raises:
    IndexError: If sub-string or part of sub-string is out of range.
  """
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
  """ Erase sub-string.

  Args:
    string: string to work on.
    sub_index: index of sub-string to replace.
    sub_lenght(optional): lenght of sub-string to replace. Deafult is -1. 
      If -1 then erase to the end of the string

  Returns:
    string: string after erased sub-string.

  Raises:
    IndexError: If sub-string or part of sub-string is out of range.
  """
  if sub_lenght == 0 or sub_lenght < -1: return string
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
  """ Return sub-string.

  Args:
    string: string to work on.
    sub_index: index of sub-string.
    sub_lenght(optional): lenght of sub-string. Deafult is -1. 
      If less the 0 then take all characters until the end of string.

  Returns:
    string: string after erased sub-string.

  Raises:
    IndexError: If sub-string or part of sub-string is out of range.
  """
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
  """ Remove dobule spaces from the given string.

  It's change '  ' to ''.

  Args:
    string: string to work on.

  Returns:
    string: string without double spaces.
  """
  return re.sub("\s\s+", " ", string)


def find(string: str, sub_string: str, position: int = 0) -> int:
  """ Find sub-string in string.

  Args:
    string: string to search in.
    sub_string: sub-string to search.
    position: position of start seaching. Deafult is 0.

  Returns:
    int: Index of found sub-string. If not find then return -1.
  """
  if position >= len(string) or position < 0: return -1
  return string.find(sub_string, position)


def rfind(string: str, sub_string: str, position: int = -1) -> int:
  """ Reverse find sub-string in string.

  Args:
    string: string to search in.
    sub_string: sub-string to search.
    position: position of start seaching. Deafult is -1. If -1 the search in
      whole string.

  Returns:
    int: Index of found sub-string. If not find then return -1.
  """
  if position == -1: position = len(string) - 1
  if position >= len(string) or position < 0: return -1
  return string.rfind(sub_string, 0, position + 1)


def split_by_positions(string: str, positions: 'list[str]') -> 'list[str]':
  """ Split string by given positions.

  Splited string does not constains characters in given positions.
  Positions are sorted before split.

  Example:
    >>> util.split_by_positions("This is a string", [2, 5, 13])
    ["Th", "s ", "s a str", "ng"]

  Args:
    string: string to split.
    positions: position to split string.

  Returns:
    list[str]: splited string.
  """
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