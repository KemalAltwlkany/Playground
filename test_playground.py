import unittest

from basic_playground import *

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
    #   1.) Team.modify() should never result with a worse team_value after its run
    #   2.) Team.send_kids_home() should never send home the best solution (otherwise an error would be raised) and the
    #       number of kids sent home should never exceed the amount defined by the static attribute Team.home_sender
    #   3.) The number of new kids added should not exceed the amount of kids sent home.
    def test_algorithm_fundamentals(self):
        for i in range(500):
            if i > 250:
                Team.kid_problem_space = ProblemSpace2
            Team.n_kids = random.randint(100, 300)
            Team.home_sender = int(Team.n_kids/20)
            team_object = Team()

            old_value = team_object.compute_team_value()
            team_object.modify()
            new_value = team_object.compute_team_value()
            self.assertLessEqual(new_value, old_value)

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
                best_sol = team_object.compute_best_value()
                team_object.modify()
                new_best = team_object.compute_best_value()
                self.assertLessEqual(new_best, best_sol)
                team_object.send_kids_home()
                best_sol = new_best
                team_object.add_new_kids()
                new_best = team_object.compute_best_value()
                self.assertLessEqual(new_best, best_sol)
                self.assertEqual(team_object.squad[0].get_criteria(), new_best)

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

