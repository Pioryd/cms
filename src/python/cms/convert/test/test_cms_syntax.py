import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
import convert.cms_syntax as cms_syntax
from convert.cms_syntax import EncryptedString

if __name__ == '__main__':
  unittest.main()
