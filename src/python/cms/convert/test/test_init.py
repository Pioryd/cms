import os
import sys
if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import time
import unittest
from unittest.mock import patch
import shutil

import convert


class TestInit(unittest.TestCase):

  def remove_folder_if_exist(self, folder_full_name: str):
    pass

  def create_directory_with_files(self, directory_full_name: str,
                                  files_cout: int) -> 'list[str]':
    pass

  def test_convert_file(self):
    pass

  def test_convert_files(self):
    pass

  def test_convert_files_recursive(self):
    pass


if __name__ == '__main__':
  unittest.main()
