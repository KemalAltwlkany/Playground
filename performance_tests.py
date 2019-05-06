import unittest

from T_de_jong import *
from T_rastrigin import *
from T_Schwefel import *

class TestRastrigin(unittest.TestCase):

    # test a single n-dimensional Rastrigin function
    @staticmethod
    def single_rastrigin(n):
        RastriginSpace.n_dimensions = n
        RastriginSpace.up_bound = 5.12
        RastriginSpace.low_bound = -5.12
        RastriginSpace.eps = 0.001
        playground_obj = Playground(200, 6, RastriginSpace, 5000, 30, 0.00000001, 0.00000001, 300)
        start = time.time()
        playground_obj.matchday_search(3)
        end = time.time()
        print("The matchday algorithm ran for, t = ", end - start)

    # for loop defines which dimensional rastrigin functions are tested
    def test_multiple_rastrigins(self):
        print('******************************* RUNNING RASTRIGIN FUNCTION TESTS *************************************')
        for i in range(1, 5):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            TestRastrigin.single_rastrigin(i)
            print('-------------------------------------------------------------------------------------------')
        print('*****************************************************************************************************')

class TestSchwefel(unittest.TestCase):

    # test a single n-dimensional Schwefel function
    @staticmethod
    def single_schwefel(n):
        SchwefelSpace.n_dimensions = n
        SchwefelSpace.up_bound = 500
        SchwefelSpace.low_bound = -500
        SchwefelSpace.eps = 5
        playground_obj = Playground(200, 6, SchwefelSpace, 5000, 30, 0.0001, 0.0001, 200)
        start = time.time()
        playground_obj.matchday_search(3)
        end = time.time()
        print("The matchday algorithm ran for, t = ", end - start)

    # for loop defines which dimensional schwefel functions are tested
    def test_multiple_schwefels(self):
        print('******************************* RUNNING SCHWEFEL FUNCTION TESTS *************************************')
        for i in range(1, 5):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            TestSchwefel.single_schwefel(i)
            print('-------------------------------------------------------------------------------------------')
        print('*****************************************************************************************************')
