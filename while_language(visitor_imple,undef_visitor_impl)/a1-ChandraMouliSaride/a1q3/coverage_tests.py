import unittest
from a1q3 import M

class CoverageTests (unittest.TestCase):
    def test_1 (self):
        """Test Paths for Node Coverage"""
        
        o = M ()

        #Test path is [3,8,9,12,23,26,27] and TRs for Node coverage covered are {3,8,9,12,23,26,27}
        o.m([],0)

        #Test path is [3,8,9,13,14,23,24,27] and TRs for Node coverage covered are {3,8,9,13,14,23,24,27}
        o.m([0],0)
        
        #Test path is [3,8,9,13,17,18,23,24,27] and TRs for Node coverage covered are {3,8,9,13,17,18,23,24,27}
        o.m([0,1],0)

        #Test path is [3,8,9,13,17,22,23,24,27] and TRs for Node coverage covered are {3,8,9,13,17,22,23,24,27}
        o.m([0,1,2],0)
        pass

    def test_2 (self):
        """Test Paths for Edge COverage"""
        o = M ()

        #Test path is [3,8,9,12,23,26,27] and TRs for Edge coverage covered are {[3,8],[8,9],[9,12],[12,23],[23,26],[26,27]}
        o.m([],0)

        #Test path is [3,9,13,14,23,24,27] and TRs for Edge coverage covered are {[3,9],[9,13],[13,14],[14,23],[23,24],[24,27]}
        o.m([0],1)
        
        #Test path is [3,9,13,17,18,23,24,27] and TRs for Edge coverage covered are {[3,9],[9,13],[13,17],[17,18],[18,23],[23,24],[24,27]}
        o.m([0,1],1)

        #Test path is [3,9,13,17,22,23,24,27] and TRs for Edge coverage covered are {[3,9],[9,13],[13,17],[17,22],[22,23],[23,24],[24,27]}
        o.m([0,1,2],1)

        pass
    def test_3 (self):
        """Test Paths for Edge Pair Coverage"""
        o = M ()

        #Test path is [3,8,9,12,23,26,27] and TRs for Edge-Pair coverage covered are {[3,8,9],[8,9,12],[9,12,23],[12,23,26],[23,26,27]}
        o.m([],0)


        #Test path is [3,9,12,23,26,27] and TRs for Edge-Pair coverage covered are {[3,9,12],[9,12,23],[12,23,26],[23,26,27]}
        o.m([],1)

        #Test path is [3,8,9,13,14,23,24,27] and TRs for Edge-Pair coverage covered are {[3,8,9],[8,9,13],[9,13,14],[13,14,23],[14,23,24],[23,24,27]}
        o.m([0],0)

        #Test path is [3,9,13,17,18,23,24,27] and TRs for Edge-Pair coverage covered are {[3,9,13],[9,13,17],[13,17,18],[17,18,23],[18,23,24],[23,24,27]}
        o.m([0,1],1)

        #Test path is [3,9,13,17,22,23,24,27] and TRs for Edge-Pair coverage covered are {[3,9,13],[9,13,17],[13,17,22],[17,22,23],[22,23,24],[23,24,27]}
        o.m([0,1,2],1)

        pass
    def test_4 (self):
        """Test Paths for Prime Path Coverage"""
        o = M ()

        #Test path is [3,8,9,12,23,26,27] and TRs for Prime-Path  coverage covered are {[3,8,9,12,23,26,27]}
        o.m([],0)

        #Test path is [3,9,12,23,26,27] and TRs for Prime-Path  coverage covered are {[3,9,12,23,26,27]}
        o.m([],1)
        
        #Test path is [3,8,9,13,14,23,24,27] and TRs for Prime-Path  coverage covered are {[3,8,9,13,14,23,24,27]}
        o.m([0],0)

        #Test path is [3,8,9,13,17,18,23,24,27] and TRs for Prime-Path  coverage covered are {[3,8,9,13,17,18,23,24,27]}
        o.m([0,1],0)

        #Test path is [3,8,9,13,17,22,23,24,27] and TRs for Prime-Path  coverage covered are {[3,8,9,13,17,22,23,24,27]}
        o.m([0,1,2],0)

        #Test path is [3,9,13,14,23,24,27] and TRs for Prime-Path  coverage covered are {[3,9,13,14,23,24,27]}
        o.m([0],1)

        #Test path is [3,9,13,17,18,23,24,27] and TRs for Prime-Path  coverage covered are {[3,9,13,17,18,23,24,27]}
        o.m([0,1],1)

        #Test path is [3,9,13,17,22,23,24,27] and TRs for Prime-Path  coverage covered are {[3,9,13,17,22,23,24,27]}
        o.m([0,1,2],1)
        pass
    
