from basic_playground import *
import math as math

#   global minimum is obtainable for x1=0, x2=0, f(x)=0
#   search space is limited to [-100, 100]
class SchafferF6Space:
    eps = 1
    n_dimensions = 2
    up_bound = 100
    low_bound = -100

    def __init__(self):
        self.x = []
        for i in range(SchafferF6Space.n_dimensions):
            self.x.append(random.uniform(SchafferF6Space.low_bound, SchafferF6Space.up_bound))
        self.y = self.compute_value()

    # WARNING - ONLY WORKS FOR 2D FUNCTIONS!
    def compute_value(self):
        pom = self.x[0]**2 + self.x[1]**2
        self.y = (math.sin(math.sqrt(pom))**2 - 0.5) / ((1 + 0.001*pom)**2) + 0.5
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(SchafferF6Space.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.05:
                new_x.append(random.uniform(SchafferF6Space.low_bound, SchafferF6Space.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-SchafferF6Space.eps, SchafferF6Space.eps))
                if new_x[i] - SchafferF6Space.low_bound < 0:
                    new_x[i] = SchafferF6Space.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - SchafferF6Space.up_bound > 0:
                    new_x[i] = SchafferF6Space.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(SchafferF6Space.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
