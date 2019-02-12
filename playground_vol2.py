import random as random
import copy as copy
import time as time

epsilon = 0.00000001

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

    def __init__(self, growing_age, attrib):
        self.attribute = attrib()
        self.is_captain = False
        self.age = 0  # should be set to 10 for initial children?
        self.criteria = self.evaluate()
        self.is_new_kid = True  # should be set to False for initial children??
        Kid.grown_up_age = growing_age

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
