import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
from unittest.mock import patch

from convert.file_source import Source
from convert.file_source import Position
from convert.scope import BlocksOfInstructions
from convert.scope import Header
from convert.scope import Scope

if __name__ == '__main__':
  unittest.main()