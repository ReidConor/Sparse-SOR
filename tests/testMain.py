# This will hold all tests for the main program
# All future tests should follow the same namig convention (test<core_file>)
import unittest
from core.doMath import *
from scipy import sparse


class TestDoMath(unittest.TestCase):

    def test_hasZerosOnMainDiag(self):
        self.assertTrue(hasZerosOnMainDiag(np.zeros((5, 5))))
        self.assertFalse(hasZerosOnMainDiag(np.ones((5, 5))))

    def test_isStrictlyDiagonallyDominant(self):
        self.assertFalse(isStrictlyDiagonallyDominant(np.ones((5, 5))))
        test_array = np.array([[5, 1, 1, 1], [1, 5, 1, 1], [1, 1, 5, 1], [1, 1, 1, 5]])
        self.assertTrue(isStrictlyDiagonallyDominant(test_array))

    def test_findXDirect(self):
        A = sparse.csr_matrix(np.array([[3, 4, 5], [8, -5, 7], [-5, 1, 1]]))
        b = np.array([26, 19, 0])
        self.assertTrue(np.allclose(findX_direct(A, b), np.array([[1.0, 2.0, 3.0]])))

unittest.main()
