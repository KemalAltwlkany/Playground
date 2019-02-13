import unittest

from playground_vol2 import *

class TestChildClass(unittest.TestCase):

    def test_constructor(self):
        kid_object = Kid()
        Kid.set_growing_up_age(7)
        self.assertEqual(Kid.grown_up_age, 7)
        self.assertEqual(kid_object.attribute.get_value(), kid_object.get_criteria())
        self.assertEqual(kid_object.is_new_kid, True)
        self.assertEqual(kid_object.is_captain, False)

    def test_modification(self):
        kid_object = Kid()
        for i in range(100):
            a = kid_object.get_criteria()
            kid_object.modify_kid()
            b = kid_object.get_criteria()
            self.assertGreaterEqual(a,b)

    def test_aging(self):
        kid_object = Kid()
        Kid.set_growing_up_age(15)
        for i in range(14):
            kid_object.increment_age()
            self.assertTrue(kid_object.get_is_new_kid())
        kid_object.increment_age()
        self.assertFalse(kid_object.get_is_new_kid())

    def test_operators_initialization(self):
        kid_array = []
        for i in range(100):
            kid_array.append(Kid())
        for i in range(len(kid_array)-1):
            a = kid_array[i].get_criteria()
            b = kid_array[i+1].get_criteria()
            self.assertEqual(kid_array[i] < kid_array[i+1], a < b)
            self.assertEqual(kid_array[i] > kid_array[i+1], a > b)

# all of the tests above ran with the default problem_space attribute of class Kid.
# the following test runs them all again, using a different problem_space

    def test_different_attribute(self):
        Kid.problem_space = ProblemSpace2
        self.test_constructor()
        self.test_modification()
        self.test_aging()
        self.test_operators_initialization()


class TestTeamClass(unittest.TestCase):

    def test_constructor(self):
        pass



