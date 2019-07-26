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