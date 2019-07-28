import os
from convert.converter import Converter


def convert_file(full_file_name: str) -> str:
  if not '.cms' in full_file_name:
    return "Wrong file type: [{}].".format(full_file_name)
  if not os.path.isfile(full_file_name):
    return "File doesn't exist: [{}].".format(full_file_name)

  converter = Converter(full_file_name)
  converter.convert()

  with open(full_file_name + ".py", "w") as file:
    file.write(converter.get_python_source())

  return ""


def convert_files(full_directory_name: str) -> str:
  returnValues = ""

  files_full_name = [
      os.path.join(full_directory_name, file)
      for file in os.listdir(full_directory_name)
      if os.path.isfile(os.path.join(full_directory_name, file))
  ]

  for file in files_full_name:
    error = convert_file(file)
    if error: returnValues += "\n\t" + error

  if returnValues: returnValues = "Errors:" + returnValues
  return returnValues


def convert_files_recursive(full_directory_name: str) -> str:
  returnValues = ""

  for root, directories, files in os.walk(full_directory_name):
    for file in files:
      error = convert_file(os.path.join(root, file))
      if error: returnValues += "\n\t" + error

  if returnValues: returnValues = "Errors:" + returnValues
  return returnValues