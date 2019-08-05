import os
import sys
if __name__ == '__main__':
  sys.path.append(
      os.path.dirname(os.path.abspath(__file__)) + "/../src/python/cms")
import convert

print(
    convert.convert_file(
        os.path.dirname(os.path.abspath(__file__)) + "/modules/stats.cpp"))
