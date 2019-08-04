from enum import Enum
from typing import List, Dict

import convert.util as util


class EncryptedString(object):
  """ Encrypt string.

  Args:
    type: Type
      Type of encrypted string.
    data: str
      Encrypted string.
    position: int
      Position at source of encrypted string.
  """

  class Type(Enum):
    NONE = 1
    COMMENT = 2
    STRING_APOSTROPHE = 3
    STRING_QUOTATION = 4

  def __init__(self, type: Type, position: int, data: str):
    self.type = type
    self.data = data
    self.position = position


def encrypt_strings(data: str,
                    types_to_encrypt: list = [EncryptedString.Type.NONE]
                   ) -> (str, List[EncryptedString]):
  """ Encrypt data.

  Example:
    ["abc"] -> [?????] or ['abc'] -> [?????] or [//abc] -> [?????]

  Args:
    data: data to encrypt.
    types_to_encrypt(optional): types to encrpyt. Default is [NONE]. 
      If [NONE] is set then encrypt all types. Otherwhise encrypt 
      strings with types given in list [types_to_encrypt]

  Returns:
    str: encrypted data.
    List[EncryptedString]: encrypted_strings: encrypted strings.
  """
  encrypted_strings = []  # List[EncryptedString]
  type_of_found_string = EncryptedString.Type.NONE
  index_of_found_open_statement = -1
  index_of_found_close_statement = -1

  i = 0
  while i < len(data):
    if type_of_found_string == EncryptedString.Type.NONE:
      if data[i] == '/' and (i + 1) < len(data) and data[i + 1] == '/':
        type_of_found_string = EncryptedString.Type.COMMENT
        index_of_found_open_statement = i
        index_of_found_close_statement = -1
      elif data[i] == "'":
        type_of_found_string = EncryptedString.Type.STRING_APOSTROPHE
        index_of_found_open_statement = i
        index_of_found_close_statement = -1
      elif data[i] == '"':
        type_of_found_string = EncryptedString.Type.STRING_QUOTATION
        index_of_found_open_statement = i
        index_of_found_close_statement = -1
    elif type_of_found_string == EncryptedString.Type.COMMENT:
      if data[i] == "\n": index_of_found_close_statement = i
    elif type_of_found_string == EncryptedString.Type.STRING_APOSTROPHE:
      if data[i] == "'" and (i - 1) >= 0 and data[i - 1] != '\\':
        index_of_found_close_statement = i
    elif type_of_found_string == EncryptedString.Type.STRING_QUOTATION:
      if data[i] == '"' and (i - 1) >= 0 and data[i - 1] != '\\':
        index_of_found_close_statement = i

    # Check if it's comment without close statement '\n', becouse of eof.
    if i == (len(data) - 1) and index_of_found_open_statement != -1:
      index_of_found_close_statement = i

    if (index_of_found_open_statement == -1 or
        index_of_found_close_statement == -1):
      i += 1
      continue

    # Encrypt string if is same type as types to encrypt.
    if (EncryptedString.Type.NONE in types_to_encrypt or
        type_of_found_string in types_to_encrypt):
      string_lenght = ((1) + index_of_found_close_statement -
                       index_of_found_open_statement)

      # Comment must be encrypted without close statement '\n'
      if (type_of_found_string == EncryptedString.Type.COMMENT and
          (i != (len(data) - 1))):
        string_lenght -= 1

      encrypted_strings.append(
          EncryptedString(
              type_of_found_string, index_of_found_open_statement,
              util.substr(data, index_of_found_open_statement, string_lenght)))

      # ["abc"] -> [?????] or ['abc'] -> [?????] or [//abc] -> [?????]
      data = util.replace(data, index_of_found_open_statement, string_lenght,
                          string_lenght, '?')

    type_of_found_string = EncryptedString.Type.NONE
    index_of_found_open_statement = -1
    index_of_found_close_statement = -1
    i += 1

  return data, encrypted_strings


def decrypt_strings(data: str,
                    encrypted_strings: List[EncryptedString],
                    types_to_decrypt: list = [EncryptedString.Type.NONE]
                   ) -> str:
  """ Decrypt data.

  Example:
    [?????] -> ["abc"] or [?????] -> ['abc'] or [?????] -> [//abc]

  Args:
    data: data to decrypt.
    encrypted_strings: encrypted strings.
    types_to_decrypt(optional): types to decrypt. Default is [NONE]. 
      If [NONE] is set then decrypt all encryped string. Otherwise decrypt 
      strings with types given in list[types_to_decrypt]

  Returns:
    str: decrypted data.
  """
  for encrypted_string in encrypted_strings:
    if encrypted_string.position >= len(data):
      raise Exception(
          ("Position of encrypted data is out of data range."
           " EncryptedString end position: %s. Source size: %s.") %
          (encrypted_string.position + len(encrypted_string.data), len(data)))

    # [?????] -> ["abc"] or [?????] -> ['abc'] or [?????] -> [//abc]
    if (EncryptedString.Type.NONE in types_to_decrypt or
        encrypted_string.type in types_to_decrypt):
      data = util.replace(data, encrypted_string.position,
                          len(encrypted_string.data), 1, encrypted_string.data)
  return data


def escape_operators(data: str) -> str:
  """ Add spaces to operators on both sides if spaces not exist.

  Support for single and double operators. If there will bemore operators 
    in row, then first will split them to double operators or to single if last.
  List of operators:
    ['+', '-', '*', '/', '%', '=', '!', '<', '>', '&', '|', '^', '~']
  Example_1:
    from: "&abs*abc % abc/ abc +abc^"
      to: " & abs * abc % abc / abc + abc ^ "
  Example_2:
    from: "&&abs**abc %% abc// abc ++abc^^"
      to: " & abs * abc % abc / abc + abc ^ "
      
  Args:
    data: data to escape.

  Returns:
    str: escaped data.
  """
  if not data: return data
  operators = ['+', '-', '*', '/', '%', '=', '!', '<', '>', '&', '|', '^', '~']
  i = 0
  while i < len(data):
    if data[i] in operators:
      if i - 1 < 0 or data[i - 1] != " ":
        data = util.insert(data, i, " ")
        i += 1

      # check if it's double operator
      if i + 1 < len(data) and data[i + 1] in operators:
        #data = util.insert(data, i + 1, " ")
        i += 1

      if i == (len(data) - 1):
        data += (" ")
        break
      elif data[i + 1] != " ":
        data = util.insert(data, i + 1, " ")
        i += 1
    i += 1
  return data


def find_unsupported_syntax(data: str) -> str:
  """ Search for unsupported syntax.

  Search for: ["++", "--", "->"]

  Args:
    data: data to search for.

  Returns:
    str: 
      found unsupported syntax or empty data if not found.
  """
  unsupported_syntaxes = ["++", "--", "->"]

  for unsupported_syntax in unsupported_syntaxes:
    if data.find(unsupported_syntax) != -1: return unsupported_syntax

  return ""


def remove_macros(data: str) -> str:
  """ Remove macros.

  Macros: "CMS_BEGIN" and "CMS_END"

  Args:
    data: data to remove macros.

  Returns:
    data: data with removed macros.
  """
  encryped_cms_begin = "%^$!$#@@#"
  encryped_cms_end = "!*$%#@%"

  encrypted_data, encrypted_strings = encrypt_strings(data)

  encrypted_data = encrypted_data.replace("CMS_BEGIN", encryped_cms_begin)
  encrypted_data = encrypted_data.replace("CMS_END", encryped_cms_end)

  decrypted_data = decrypt_strings(encrypted_data, encrypted_strings)

  while True:
    found = decrypted_data.find(encryped_cms_begin)
    if found == -1: break
    decrypted_data = util.erase(decrypted_data, found,
                                decrypted_data.find(')', found) - found + 1)

  while True:
    found = decrypted_data.find(encryped_cms_end)
    if found == -1: break
    decrypted_data = util.erase(decrypted_data, found,
                                decrypted_data.find(')', found) - found + 1)
  return decrypted_data