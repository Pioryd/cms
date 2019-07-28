import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
import convert.cms_syntax as cms_syntax
from convert.cms_syntax import EncryptedString


class TestCmsSyntax(unittest.TestCase):

  def test_crypt_string(self):
    # Setup source
    working_directory = os.path.dirname(os.path.abspath(__file__))
    test_source_path = working_directory + "/source_cms_syntax.cms.txt"
    source = Source(test_source_path)
    source_as_string = ("#define some_define\n"
                        "\n"
                        "// hello \" 'w' \"abc\" // \"\n"
                        "auto string = \"'string//'' \\\" '\";\n"
                        "auto character = 'c'; // comment 'foo' / \"//\"\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {'a', 'b', 'c'};\n"
                        "a++;\n"
                        "auto string_array = {\"abc\", \"zxc\", \"poi\"}\n"
                        "// end of file")
    self.assertEqual(source.str, source_as_string)

    # Crypt default
    encrypted_source = ("#define some_define\n"
                        "\n"
                        "?????????????????????????\n"
                        "auto string = ??????????????????;\n"
                        "auto character = ???; ???????????????????????\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {???, ???, ???};\n"
                        "a++;\n"
                        "auto string_array = {?????, ?????, ?????}\n"
                        "??????????????")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(source.str)
    self.assertEqual(encrypted_data, encrypted_source)
    #
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings)
    self.assertEqual(decrypted_data, source.str)

    # Crypt comments only
    encrypted_source = ("#define some_define\n"
                        "\n"
                        "?????????????????????????\n"
                        "auto string = \"'string//'' \\\" '\";\n"
                        "auto character = 'c'; ???????????????????????\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {'a', 'b', 'c'};\n"
                        "a++;\n"
                        "auto string_array = {\"abc\", \"zxc\", \"poi\"}\n"
                        "??????????????")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(
        source.str, [EncryptedString.Type.COMMENT])
    self.assertEqual(encrypted_data, encrypted_source)
    #
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings)
    self.assertEqual(decrypted_data, source.str)

    # Crypt strings as apostrophe only
    encrypted_source = ("#define some_define\n"
                        "\n"
                        "// hello \" 'w' \"abc\" // \"\n"
                        "auto string = \"'string//'' \\\" '\";\n"
                        "auto character = ???; // comment 'foo' / \"//\"\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {???, ???, ???};\n"
                        "a++;\n"
                        "auto string_array = {\"abc\", \"zxc\", \"poi\"}\n"
                        "// end of file")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(
        source.str, [EncryptedString.Type.STRING_APOSTROPHE])
    self.assertEqual(encrypted_data, encrypted_source)
    #
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings)
    self.assertEqual(decrypted_data, source.str)

    # Crypt strings as quotation only
    encrypted_source = ("#define some_define\n"
                        "\n"
                        "// hello \" 'w' \"abc\" // \"\n"
                        "auto string = ??????????????????;\n"
                        "auto character = 'c'; // comment 'foo' / \"//\"\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {'a', 'b', 'c'};\n"
                        "a++;\n"
                        "auto string_array = {?????, ?????, ?????}\n"
                        "// end of file")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(
        source.str, [EncryptedString.Type.STRING_QUOTATION])
    self.assertEqual(encrypted_data, encrypted_source)
    #
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings)
    self.assertEqual(decrypted_data, source.str)

    # Crypt comments and strings as quotation only
    encrypted_source = ("#define some_define\n"
                        "\n"
                        "?????????????????????????\n"
                        "auto string = ??????????????????;\n"
                        "auto character = 'c'; ???????????????????????\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {'a', 'b', 'c'};\n"
                        "a++;\n"
                        "auto string_array = {?????, ?????, ?????}\n"
                        "??????????????")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(
        source.str,
        [EncryptedString.Type.COMMENT, EncryptedString.Type.STRING_QUOTATION])
    self.assertEqual(encrypted_data, encrypted_source)
    #
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings)
    self.assertEqual(decrypted_data, source.str)

    #Encryp all and decrypt comments only
    encrypted_source = ("#define some_define\n"
                        "\n"
                        "?????????????????????????\n"
                        "auto string = ??????????????????;\n"
                        "auto character = ???; ???????????????????????\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {???, ???, ???};\n"
                        "a++;\n"
                        "auto string_array = {?????, ?????, ?????}\n"
                        "??????????????")
    decrypted_comments_only = (
        "#define some_define\n"
        "\n"
        "// hello \" 'w' \"abc\" // \"\n"
        "auto string = ??????????????????;\n"
        "auto character = ???; // comment 'foo' / \"//\"\n"
        "auto a = 1 + 2;\n"
        "auto char_array = {???, ???, ???};\n"
        "a++;\n"
        "auto string_array = {?????, ?????, ?????}\n"
        "// end of file")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(source.str)
    self.assertEqual(encrypted_data, encrypted_source)
    #
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings,
                                                [EncryptedString.Type.COMMENT])
    self.assertEqual(decrypted_data, decrypted_comments_only)

    #Encryp all and decrypt nothing
    encrypted_source = ("#define some_define\n"
                        "\n"
                        "?????????????????????????\n"
                        "auto string = ??????????????????;\n"
                        "auto character = ???; ???????????????????????\n"
                        "auto a = 1 + 2;\n"
                        "auto char_array = {???, ???, ???};\n"
                        "a++;\n"
                        "auto string_array = {?????, ?????, ?????}\n"
                        "??????????????")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(source.str)
    self.assertEqual(encrypted_data, encrypted_source)
    #
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings, [])
    self.assertEqual(decrypted_data, encrypted_source)

    # Empty string
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings("")
    self.assertEqual(encrypted_data, "")
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings)
    self.assertEqual(decrypted_data, "")
    #
    encrypted_data, encrypted_strings = cms_syntax.encrypt_strings(" ")
    self.assertEqual(encrypted_data, " ")
    decrypted_data = cms_syntax.decrypt_strings(encrypted_data,
                                                encrypted_strings)
    self.assertEqual(decrypted_data, " ")

  def test_escape_operators(self):
    pass

  def test_find_unsupported_syntax(self):
    pass


if __name__ == '__main__':
  unittest.main()
