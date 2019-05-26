from basic_playground import *
import math as math

#   global minimum is obtainable for xi=1, f(x)= 0
#   search space is limited to [0, 10]
#   search space needs to be at least 2 dimensional!
class Schwefel4Space:
    eps = 1
    n_dimensions = 5
    up_bound = 10
    low_bound = 0

    def __init__(self):
        self.x = []
        for i in range(Schwefel4Space.n_dimensions):
            self.x.append(random.uniform(Schwefel4Space.low_bound, Schwefel4Space.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        for i in range(1, Schwefel4Space.n_dimensions):
            self.y = self.y + (self.x[i] - 1)**2 + (self.x[0] - self.x[i]**2)**2
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(Schwefel4Space.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.05:
                new_x.append(random.uniform(Schwefel4Space.low_bound, Schwefel4Space.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-Schwefel4Space.eps, Schwefel4Space.eps))
                if new_x[i] - Schwefel4Space.low_bound < 0:
                    new_x[i] = Schwefel4Space.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - Schwefel4Space.up_bound > 0:
                    new_x[i] = Schwefel4Space.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(Schwefel4Space.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
