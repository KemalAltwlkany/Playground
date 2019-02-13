import random as random
import copy as copy
import time as time

epsilon = 0.00000001

class MyEvaluationError(LookupError):
    """Raise this error kemo"""

class ProblemSpace2:

    eps = 0.06

    def __init__(self):
        self.x = random.uniform(-2, 0)
        self.y = self.compute_value()

    def compute_value(self):
        self.y = pow(self.x, 8) + 3 * pow(self.x, 6) + 2 * pow(self.x, 5) - 17 * pow(self.x, 4) - 12 * pow(self.x, 3) \
                 - 11 * pow(self.x, 2) + self.x - 10
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.compute_value()

    def modify_solution(self):
        new_x = self.x + random.uniform(-ProblemSpace2.eps, ProblemSpace2.eps)
        new_crit = pow(new_x, 8) + 3 * pow(new_x, 6) + 2 * pow(new_x, 5) - 17 * pow(new_x, 4) - 12 * pow(new_x, 3) \
                 - 11 * pow(new_x, 2) + new_x - 10
        if new_crit - self.get_value() < 0:
            self.x = new_x
            self.y = new_crit

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x


class ProblemSpace1:

    eps = 0.06

    def __init__(self):
        self.x = [random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10)]
        self.y = self.compute_value()

    def compute_value(self):
        self.y = self.x[0]**2 + self.x[1]**2 + self.x[2]**2 + self.x[3]**2 + self.x[4]**2
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(len(self.x)):
            new_x.append(self.x[i] + random.uniform(-ProblemSpace1.eps, ProblemSpace1.eps))
        new_crit = new_x[0]**2 + new_x[1]**2 + new_x[2]**2 + new_x[3]**2 + new_x[4]**2
        if new_crit - self.get_value() < 0:
            self.x = new_x
            self.y = new_crit

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x


class Kid:

    grown_up_age = 4
    problem_space = ProblemSpace1

    def __init__(self):
        self.attribute = Kid.problem_space()
        self.is_captain = False
        self.age = 0  # should be set to 10 for initial children?
        self.criteria = self.evaluate()
        self.is_new_kid = True  # should be set to False for initial children??

    def evaluate(self):
        self.criteria = self.attribute.compute_value()
        return self.criteria

    def increment_age(self):
        self.age += 1
        if self.age >= Kid.grown_up_age:
            self.is_new_kid = False

# changes are only accepted if they give a better criteria function
    def modify_kid(self):
        self.attribute.modify_solution()
        self.criteria = self.attribute.get_value()

    def get_criteria(self):
        return self.criteria

    def get_age(self):
        return self.age

    def get_is_new_kid(self):
        return self.is_new_kid

    def get_is_captain(self):
        return self.is_captain

    def set_age(self, new_age):
        self.age = new_age
        if self.age >= Kid.grown_up_age:
            self.is_new_kid = False

    def set_is_captain(self, x):
        self.is_captain = x

    @staticmethod
    def set_growing_up_age(age):
        Kid.grown_up_age = age

    def print_child_info(self):
        print('------------------------------------------')
        print('The vector is =', self.attribute.x)
        print('Captain = ', self.is_captain)
        print('Child age is = ', self.age)
        print('New kid is = ', self.is_new_kid)
        print('Criteria is = ', self.criteria)
        print('------------------------------------------')

    def __lt__(self, other):
        return self.get_criteria() - other.get_criteria() < 0

    def __gt__(self, other):
        return self.get_criteria() - other.get_criteria() > 0

    def __le__(self, other):
        x = (self.get_criteria() - other.get_criteria() < 0 )
        y = ( abs(self.get_criteria() - other.get_criteria()) < epsilon )
        return x or y

# a local search, which should be used on the captain
    def local_search(self):
        pass

class Team:

    n_kids = 50
    home_sender = 2
    Kid_problem_space = ProblemSpace1

    def __init__(self):
        self.squad = []
        self.squad.append(Kid())
        self.captain = self.squad[0]
        self.team_value = self.squad[0].get_criteria()
        self.squad[0].set_age(Kid.grown_up_age)
        self.captain_ind = 0
        for i in range(1, Team.n_kids, 1):
            self.squad.append(Kid())
            self.squad[i].set_age(Kid.grown_up_age) # initial kids should all be prone to modifications
            if self.squad[i].get_criteria() - self.squad[self.captain_ind].get_criteria() < 0:
                self.captain = self.squad[i]
                self.captain_ind = i
            self.team_value += self.squad[i].get_criteria()
        self.squad[self.captain_ind].set_is_captain(True)
        self.team_value /= Team.n_kids
        if self.check_no_caps() is True:
            print("Error in constructor")

    def sort_team(self, sort_type):
        self.squad.sort(key=Kid.get_criteria, reverse=sort_type)

# method presupposes that the team is sorted into descending order
    def send_kids_home(self):
        new_team = []
        n_sent = 0
        for kid in self.squad:
            if not kid.get_is_new_kid() and n_sent != Team.home_sender:
                n_sent += 1
                if kid.get_is_captain():
                    raise MyEvaluationError('Error! Captain got sent home!')
                continue
            else:
                new_team.append(copy.deepcopy(kid))
        self.squad = list(reversed(new_team))
        if self.check_no_caps() is True:
            print("Error in send_kids_home")
# the result is a squad list but with not enough children. adding them should be done
# using binary insertion for efficiency

    def add_new_kids(self):
        for i in range(Team.n_kids - len(self.squad)):
            self.squad.append(Kid())
            # nice place for binary insertion
            if self.squad[-1].get_criteria() - self.captain.get_criteria() < 0:
                self.captain.set_is_captain(False)
                self.captain = self.squad[-1]
                self.captain.set_is_captain(True)
        if self.check_no_caps() is True:
            print("Error in add_new_kids")

# also increments age of every kid
    def modify(self):
        self.team_value = 0
        for i in range(Team.n_kids):
            self.squad[i].modify_kid()
            self.squad[i].increment_age()
            if self.squad[i].get_criteria() - self.captain.get_criteria() < 0:
                self.captain.set_is_captain(False)
                self.squad[i].set_is_captain(True)
                self.captain = self.squad[i]
            self.team_value += self.squad[i].get_criteria()
        self.team_value /= Team.n_kids
        if self.check_no_caps() is True:
            print("Error in modify")

    def print_team_info(self):
        print("Team has =", Team.n_kids, " kids.")
        print("Team value is =", self.team_value)
        print("Team captain is: ")
        self.captain.print_child_info()

    def print_rooster(self):
        print("Kids currently in team: ")
        for kid in self.squad:
            kid.print_child_info()

    def check_no_caps(self):
        cap = 0
        for kid in self.squad:
            if kid.get_is_captain() is True:
                cap += 1
        if cap > 1:
            return True
        return False




