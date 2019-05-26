from basic_playground import *
import math as math

#   global minimum is obtainable for xi=9.350266, f(x)= -45.7784684040686
#   search space is limited to [2.001, 9.999]
#   dimensions are limited from 2-10
class PavianiSpace:
    eps = 1
    n_dimensions = 4
    up_bound = 9.999
    low_bound = 2.001

    def __init__(self):
        self.x = []
        for i in range(PavianiSpace.n_dimensions):
            self.x.append(random.uniform(PavianiSpace.low_bound, PavianiSpace.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        pom1 = 0
        pom2 = 1
        for i in range(PavianiSpace.n_dimensions):
            pom1 = pom1 + math.pow(math.log(self.x[i] - 2), 2) + math.pow(math.log(10 - self.x[i]), 2)
            pom2 = pom2 * self.x[i]
        self.y = pom1 - math.pow(pom2, 0.2)
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(PavianiSpace.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.05:
                new_x.append(random.uniform(PavianiSpace.low_bound, PavianiSpace.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-PavianiSpace.eps, PavianiSpace.eps))
                if new_x[i] - PavianiSpace.low_bound < 0:
                    #FATAL ERROR-------------------------------------------
                    new_x[i] = PavianiSpace.low_bound * random.uniform(1.02, 1.12)
                if new_x[i] - PavianiSpace.up_bound > 0:
                    new_x[i] = PavianiSpace.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(PavianiSpace.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff

