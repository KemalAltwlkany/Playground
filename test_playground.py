import unittest

from T_de_jong import *
from T_rastrigin import *
from T_Schwefel import *

class TestChildClass(unittest.TestCase):

    def test_constructor(self):
        kid_object = Kid()
        Kid.set_growing_up_age(7)
        self.assertEqual(Kid.grown_up_age, 7)
        self.assertEqual(kid_object.attribute.get_value(), kid_object.get_criteria())
        self.assertEqual(kid_object.is_new_kid, True)
        self.assertEqual(kid_object.is_captain, False)

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
        self.test_aging()
        self.test_operators_initialization()


class TestTeamClass(unittest.TestCase):

    #  This test checks if the insertion which is being done in the add_new_kids method keeps the order
    #  of the Team.squad list. The order should be ascending.
    def test_insertion(self):
        Team.n_kids = 200
        Team.home_sender = 50
        for i in range(100):
            if i > 50:
                Team.kid_problem_space = ProblemSpace2
            for p in range(10):
                team_object = Team()
                team_object.modify()
                team_object.send_kids_home()
                team_object.add_new_kids()
                for j in range(Team.n_kids - 1):
                    self.assertLessEqual(team_object.squad[j].get_criteria(), team_object.squad[j+1].get_criteria())

    #   This test check whether the algorithms core methods are valid. That is:
    #   1.) Team.send_kids_home() should never send home the best solution (otherwise an error would be raised) and the
    #       number of kids sent home should never exceed the amount defined by the static attribute Team.home_sender
    #   2.) The number of new kids added should not exceed the amount of kids sent home.
    def test_algorithm_fundamentals(self):
        for i in range(500):
            if i > 250:
                Team.kid_problem_space = ProblemSpace2
            Team.n_kids = random.randint(100, 300)
            Team.home_sender = int(Team.n_kids/20)
            team_object = Team()

            team_object.modify()
            team_object.send_kids_home()
            self.assertEqual(len(team_object.squad), Team.n_kids - Team.home_sender)
            team_object.add_new_kids()
            self.assertEqual(len(team_object.squad), Team.n_kids)

    #   This test checks whether the best solution is always kept or updated regardless of which methods are run
    def test_best_solution_inheritance(self):
        for i in range(50):
            Team.kid_problem_space = ProblemSpace1
            Team.n_kids = random.randint(100, 300)
            Team.home_sender = int(Team.n_kids / 20)
            team_object = Team()

            for j in range(50):
                team_object.modify()
                team_object.send_kids_home()
                best_sol = team_object.compute_best_value()
                team_object.add_new_kids()
                new_best = team_object.compute_best_value()
                self.assertLessEqual(new_best, best_sol)
                self.assertEqual(team_object.squad[0].get_criteria(), new_best)

    #   Tests whether the team values are kept in a descending order
    def test_team_value_update(self):
        for i in range(500):
            if i > 250:
                Team.kid_problem_space = ProblemSpace2
            Team.n_kids = random.randint(100, 300)
            Team.home_sender = int(Team.n_kids/20)
            team_object = Team()

            team_object.modify()
            team_object.send_kids_home()
            team_object.add_new_kids()
            attribute_value = team_object.get_team_value()
            manually_computed = team_object.compute_team_value()
            self.assertAlmostEqual(attribute_value, manually_computed, 3)

#   This test cannot fail. It runs the matchday algorithm searching for local minima of the First DeJong function
#   dimensionality ranges from 1-10
class TestDeJong(unittest.TestCase):

    def test_2D_DeJong(self):
        DeJongSpace.n_dimensions = 2
        playground_obj = Playground(100, 5, DeJongSpace, 1000, 8, 0.0001, 0.0000001, 40)
        start = time.time()
        playground_obj.matchday_search(5)
        end = time.time()
        print("The matchday algorithm ran for, t = ", end - start)

    def test_multi_dimensional_DeJong(self):
        for i in range(1, 10):
            print('------------------Iteration    ', i, '    -----------------')
            DeJongSpace.n_dimensions = i
            playground_obj = Playground(50, 5, DeJongSpace, 1000, 5, 0.0001, 0.0000001, 40)
            start = time.time()
            playground_obj.matchday_search(4)
            end = time.time()
            print("The matchday algorithm ran for, t = ", end - start)

class TestRastrigin(unittest.TestCase):

    # test a single n-dimensional Rastrigin function
    def test_single_rastrigin(self, n):
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
        for i in range(1, 21):
            print('---->>>>---->>>>---->>>>---->>>>---- iteration ', i, ' ----<<<<----<<<<----<<<<----<<<<----')
            self.test_single_rastrigin(i)
            print('-------------------------------------------------------------------------------------------')
        print('*****************************************************************************************************')

class TestSchwefel(unittest.TestCase):

    # test a single n-dimensional Schwefel function
    def test_single_schwefel(self, n):
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
            self.test_single_schwefel(i)
            print('-------------------------------------------------------------------------------------------')
        print('*****************************************************************************************************')

    # test a single n-dimensional Rastrigin function
    def test_single_rastrigin(self, n):
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
            self.test_single_rastrigin(i)
            print('-------------------------------------------------------------------------------------------')
        print('*****************************************************************************************************')
