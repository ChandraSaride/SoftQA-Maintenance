import unittest
from a2q3.magic_square import solve_magic_square,puzzle
import z3
class PuzzleTests (unittest.TestCase):

    def setUp (self):
        """Reset Z3 context between tests"""
        import z3
        z3._main_ctx = None
    def tearDown (self):
        """Reset Z3 context after test"""
        import z3
        z3._main_ctx = None

    def test_1 (self):
        res = puzzle(3, 1, 1, 5)
        if(res==None):
            print("Cannot find matrix with given inputs that match the requirements")
        
        # since the solution may not be unique, the best way to test
        # is to check the all the sums
        else:
            self.assertEquals (sum([res[0][j] for j in range(3)]), 15)
            self.assertEquals (sum([res[1][j] for j in range(3)]), 15)
            self.assertEquals (sum([res[2][j] for j in range(3)]), 15)
            self.assertEquals (sum([res[i][0] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][1] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][2] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][i] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][3 - i - 1] for i in range(3)]), 15)

    def test_2 (self):
        res = puzzle(4, 1, 1, 5)
        if(res==None):
            print("Cannot find matrix with given inputs that match the requirements")
        
        # since the solution may not be unique, the best way to test
        # is to check the all the sums
        else:
            self.assertEquals (sum([res[0][j] for j in range(4)]), 34)
            self.assertEquals (sum([res[1][j] for j in range(4)]), 34)
            self.assertEquals (sum([res[2][j] for j in range(4)]), 34)
            self.assertEquals (sum([res[i][0] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][1] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][2] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][i] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][4 - i - 1] for i in range(4)]), 34)
        pass

    def test_3 (self):
        res = puzzle(4, 3, 3, 12)
        if(res==None):
            print("Cannot find matrix with given inputs that match the requirements")
        
        # since the solution may not be unique, the best way to test
        # is to check the all the sums
        else:
            self.assertEquals (sum([res[0][j] for j in range(4)]), 34)
            self.assertEquals (sum([res[1][j] for j in range(4)]), 34)
            self.assertEquals (sum([res[2][j] for j in range(4)]), 34)
            self.assertEquals (sum([res[i][0] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][1] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][2] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][i] for i in range(4)]), 34)
            self.assertEquals (sum([res[i][4 - i - 1] for i in range(4)]), 34)
        pass

    def test_4 (self):
        res = puzzle(3, 1, 1, 8)
        if(res==None):
            print("Cannot find matrix with given inputs that match the requirements")
        
        # since the solution may not be unique, the best way to test
        # is to check the all the sums
        else:
            self.assertEquals (sum([res[0][j] for j in range(3)]), 15)
            self.assertEquals (sum([res[1][j] for j in range(3)]), 15)
            self.assertEquals (sum([res[2][j] for j in range(3)]), 15)
            self.assertEquals (sum([res[i][0] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][1] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][2] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][i] for i in range(3)]), 15)
            self.assertEquals (sum([res[i][3 - i - 1] for i in range(3)]), 15)

        pass
