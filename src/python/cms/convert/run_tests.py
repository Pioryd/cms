import os
import sys
import unittest

if __name__ == '__main__':
  sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

loader = unittest.TestLoader()
suite = loader.discover(os.path.dirname(os.path.abspath(__file__)) + "/test")
runner = unittest.TextTestRunner()
runner.run(suite)