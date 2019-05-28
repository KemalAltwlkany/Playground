import unittest

from T_rastrigin import *
from T_Schwefel import *
from T_rosenbrock import *
from T_schaffer_F6 import *
from T_schaffer_F7 import *
from T_bohachevsky import *
from T_griewank import *
from T_ackley1 import *
from T_alpine2 import *
from T_paviani import *

#this test validates whether the value of the minima is computed exactly
class TestMinima(unittest.TestCase):

    def test_rastrigin(self):
        RastriginSpace.eps = 0.001
        RastriginSpace.up_bound = 5.12
        RastriginSpace.low_bound = -5.12
        for i in range(1, 100):
            RastriginSpace.n_dimensions = i
            obj = RastriginSpace()
            pom = [0 for j in range(0, i)]
            obj.set_solution(pom)
            self.assertEqual(obj.compute_value(), 0.0)

    def test_schwefel(self):
        SchwefelSpace.eps = 5
        SchwefelSpace.up_bound = 500
        SchwefelSpace.low_bound = -500
        for i in range(1, 100):
            SchwefelSpace.n_dimensions = i
            obj = SchwefelSpace()
            pom = [420.9687 for j in range(0, i)]
            obj.set_solution(pom)
            self.assertAlmostEqual(obj.compute_value(), -418.9829*i, places=2)

    def test_griewank(self):
        GriewankSpace.eps = 5
        GriewankSpace.up_bound = 100
        GriewankSpace.low_bound = -100
        for i in range(1, 100):
            GriewankSpace.n_dimensions = i
            obj = GriewankSpace()
            pom = [0 for j in range(0, i)]
            obj.set_solution(pom)
            self.assertEqual(obj.compute_value(), 0)

    def test_schaffer_F6(self):
        SchafferF6Space.eps = 1
        SchafferF6Space.up_bound = 100
        SchafferF6Space.low_bound = -100
        SchafferF6Space.n_dimensions = 2
        obj = SchafferF6Space()
        obj.set_solution([0, 0])
        self.assertEqual(obj.compute_value(), 0)

    def test_schaffer_F7(self):
        SchafferF7Space.eps = 1
        SchafferF7Space.up_bound = 100
        SchafferF7Space.low_bound = -100
        for i in range(2, 100):
            SchafferF7Space.n_dimensions = i
            obj = SchafferF7Space()
            pom = [0 for j in range(0, i)]
            obj.set_solution(pom)
            self.assertEqual(obj.compute_value(), 0)

    def test_bohachevsky(self):
        BohachevskySpace.eps = 0.1
        BohachevskySpace.up_bound = 100
        BohachevskySpace.low_bound = -100
        BohachevskySpace.n_dimensions = 2
        obj = BohachevskySpace()
        obj.set_solution([0, 0])
        self.assertEqual(obj.compute_value(), 0)

    def test_rosenbrock(self):
        RosenbrockSpace.eps = 0.01
        RosenbrockSpace.up_bound = 2.048
        RosenbrockSpace.low_bound = -2.048
        for i in range(2, 100):
            RosenbrockSpace.n_dimensions = i
            obj = RosenbrockSpace()
            pom = [1 for j in range(0, i)]
            obj.set_solution(pom)
            self.assertEqual(obj.compute_value(), 0)

    def test_ackley1(self):
        Ackley1Space.eps = 0.01
        Ackley1Space.up_bound = 35
        Ackley1Space.low_bound = -35
        for i in range(2, 100):
            Ackley1Space.n_dimensions = i
            obj = Ackley1Space()
            pom = [0 for j in range(0, i)]
            obj.set_solution(pom)
            self.assertAlmostEqual(obj.compute_value(), 0, places=4)

    def test_alpine2(self):
        Alpine2Space.eps = 0.01
        Alpine2Space.up_bound = 10
        Alpine2Space.low_bound = 0
        for i in range(1, 20):
            Alpine2Space.n_dimensions = i
            obj = Alpine2Space()
            pom = [7.9170526982459462172 for j in range(0, i)]
            obj.set_solution(pom)
            # print(math.fabs(obj.compute_value() + 2.8081311800070053291 ** i))
            self.assertEqual(math.fabs(obj.compute_value() + 2.8081311800070053291 ** i) < 1e-6, True)

    def test_paviani(self):
        PavianiSpace.eps = 0.01
        PavianiSpace.up_bound = 9.999
        PavianiSpace.low_bound = 2.001
        for i in range(1, 20):
            PavianiSpace.n_dimensions = i
            obj = PavianiSpace()
            pom = [9.350266 for j in range(0, i)]
            obj.set_solution(pom)
            print(math.fabs(obj.compute_value()))
            self.assertEqual(math.fabs(obj.compute_value() - 45.7784684040686) < 1e-2, True)
