import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
import convert.cms_syntax as cms_syntax
from convert.cms_syntax import EncryptedString


class TestCppSyntax(unittest.TestCase):

  def test_crypt_string(self):
    pass

  def test_escape_operators(self):
    pass

  def test_find_unsupported_syntax(self):
    pass


if __name__ == '__main__':
  unittest.main()
