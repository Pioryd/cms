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
  CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

  def remove_folder_if_exist(self, folder_full_name: str):
    if os.path.exists(folder_full_name):
      shutil.rmtree(folder_full_name)
      # wait 1 sec to avoid bug by giving time to work for OS.
      time.sleep(1)
      self.assertFalse(os.path.exists(folder_full_name))

  def create_directory_with_files(self, directory_full_name: str,
                                  files_cout: int) -> 'list[str]':
    cms_file_body = ("#include <cms>\n"
                     'cms::string file = "STRING";\n'
                     "struct MyStruct {\n"
                     "void foo(int a){\n"
                     "print(a);\n"
                     "}};")

    os.mkdir(directory_full_name)
    self.assertTrue(os.path.exists(directory_full_name))

    created_files = []
    for i in range(1, files_cout + 1):
      file_full_name = os.path.join(directory_full_name,
                                    "module_{}.cms".format(i))
      with open(file_full_name, "w+") as file:
        file.write(cms_file_body.replace("STRING", file_full_name))
        created_files.append(file_full_name)
      self.assertTrue(os.path.exists(file_full_name))

    return created_files

  def test_convert_file(self):
    test_folder = os.path.join(self.CURRENT_DIRECTORY + "test_init_1")

    self.remove_folder_if_exist(test_folder)

    self.create_directory_with_files(test_folder, 3)

    file_full_name = os.path.join(os.path.join(test_folder, "module_2.cms"))
    self.assertEqual(convert.convert_file(file_full_name), "")
    self.assertTrue(os.path.exists(file_full_name + ".py"))

    self.remove_folder_if_exist(test_folder)

  def test_convert_files(self):
    test_folder = os.path.join(self.CURRENT_DIRECTORY, "test_init_2")

    self.remove_folder_if_exist(test_folder)

    created_files = self.create_directory_with_files(test_folder, 3)

    self.assertEqual(convert.convert_files(test_folder), "")

    for file in created_files:
      self.assertTrue(os.path.exists(file + ".py"))

    self.remove_folder_if_exist(test_folder)

  def test_convert_files_recursive(self):
    test_folder = os.path.join(self.CURRENT_DIRECTORY, "test_init_3")
    test_sub_folder_1 = os.path.join(test_folder, "sub_1")
    test_sub_folder_2 = os.path.join(test_folder, "sub_2")

    self.remove_folder_if_exist(test_folder)

    created_files = []
    created_files.extend(self.create_directory_with_files(test_folder, 3))
    created_files.extend(self.create_directory_with_files(test_sub_folder_1, 4))
    created_files.extend(self.create_directory_with_files(test_sub_folder_2, 6))

    self.assertEqual(convert.convert_files_recursive(test_folder), "")

    for file in created_files:
      self.assertTrue(os.path.exists(file + ".py"))

    self.remove_folder_if_exist(test_folder)


if __name__ == '__main__':
  unittest.main()
