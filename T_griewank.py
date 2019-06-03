from basic_playground import *
import math as math

#   global minimum is obtainable for xi=0, f(x)=0
#   search space is limited to [-100, 100]
class GriewankSpace:
    eps = 1
    n_dimensions = 10
    up_bound = 600
    low_bound = -600

    def __init__(self):
        self.x = []
        for i in range(GriewankSpace.n_dimensions):
            self.x.append(random.uniform(GriewankSpace.low_bound, GriewankSpace.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        pom1 = 0
        pom2 = 1
        for i in range(GriewankSpace.n_dimensions):
            pom1 = math.pow(self.x[i], 2) + pom1
            pom2 = math.cos(self.x[i] / math.sqrt(i+1)) * pom2
        pom1 = pom1 / 4000
        self.y = pom1 - pom2 + 1
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(GriewankSpace.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.05:
                new_x.append(random.uniform(GriewankSpace.low_bound, GriewankSpace.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-GriewankSpace.eps, GriewankSpace.eps))
                if new_x[i] - GriewankSpace.low_bound < 0:
                    new_x[i] = GriewankSpace.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - GriewankSpace.up_bound > 0:
                    new_x[i] = GriewankSpace.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(GriewankSpace.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
