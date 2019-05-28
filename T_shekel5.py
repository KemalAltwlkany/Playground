from basic_playground import *
import math as math

#   global minimum is obtainable for xi=4, f(x)= -10.1527
#   search space is limited to [0, 10]
#   search space needs to be at least 2 dimensional!
class Shekel5Space:
    eps = 1
    n_dimensions = 4
    up_bound = 10
    low_bound = 0
    A = [[4, 4, 4, 4], [1, 1, 1, 1], [8, 8, 8, 8], [6, 6, 6, 6], [3, 7, 3, 7]]
    c = [0.1, 0.2, 0.2, 0.4, 0.6]

    def __init__(self):
        self.x = []
        for i in range(Shekel5Space.n_dimensions):
            self.x.append(random.uniform(Shekel5Space.low_bound, Shekel5Space.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        for i in range(0, 5):
            pom = 0
            for j in range(0, 4):
                pom = pom + (self.x[j] - Shekel5Space.A[i][j]) ** 2
            self.y = self.y - 1/(pom + Shekel5Space.c[i])
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(Shekel5Space.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.05:
                new_x.append(random.uniform(Shekel5Space.low_bound, Shekel5Space.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-Shekel5Space.eps, Shekel5Space.eps))
                if new_x[i] - Shekel5Space.low_bound < 0:
                    new_x[i] = Shekel5Space.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - Shekel5Space.up_bound > 0:
                    new_x[i] = Shekel5Space.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(Shekel5Space.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
