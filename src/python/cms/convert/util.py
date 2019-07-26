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