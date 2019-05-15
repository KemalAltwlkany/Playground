from basic_playground import *
import math as math

#   global minimum is obtainable for xi=0, f(x)=0
#   search space is limited to [-100, 100]
class SchafferF7Space:
    eps = 1
    n_dimensions = 5
    up_bound = -100
    low_bound = 100

    def __init__(self):
        self.x = []
        for i in range(SchafferF7Space.n_dimensions):
            self.x.append(random.uniform(SchafferF7Space.low_bound, SchafferF7Space.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        pom = 1/(SchafferF7Space.n_dimensions - 1)
        for i in range(SchafferF7Space.n_dimensions-1):
            si = math.sqrt(self.x[i]**2 + self.x[i+1]**2)
            self.y = self.y + (pom * math.sqrt(si) * (math.sin(50 * (si**0.2)) + 1))**2
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(SchafferF7Space.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.2:
                new_x.append(random.uniform(SchafferF7Space.low_bound, SchafferF7Space.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-SchafferF7Space.eps, SchafferF7Space.eps))
                if new_x[i] - SchafferF7Space.low_bound < 0:
                    new_x[i] = SchafferF7Space.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - SchafferF7Space.up_bound > 0:
                    new_x[i] = SchafferF7Space.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(SchafferF7Space.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
