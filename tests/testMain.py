# This will hold all tests for the main program
# All future tests should follow the same namig convention (test<core_file>)
import unittest
from core.doMath import add

class MyTest(unittest.TestCase):
    def test_true(self):
        self.assertEqual(add(2,2), 4)

class AnotherTest(unittest.TestCase):
    def test_another(self):
        self.assertTrue(add(2,2) == 4)

unittest.main()