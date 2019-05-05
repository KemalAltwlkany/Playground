from basic_playground import *
import math as math

#   global minimum is obtainable for xi=420.9687, f(x)=-418.9829*n
#   search space is limited to [-500, 500]
class SchwefelSpace:
    eps = 0.01
    n_dimensions = 10
    up_bound = -500
    low_bound = 500

    def __init__(self):
        self.x = []
        for i in range(SchwefelSpace.n_dimensions):
            self.x.append(random.uniform(SchwefelSpace.low_bound, SchwefelSpace.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        for i in range(SchwefelSpace.n_dimensions):
            self.y = self.y - self.x[i] * math.sin(math.sqrt(math.fabs(self.x[i])))
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        p = random.uniform(0, 1)
        if p < 0.02:
            new_x = []
            for i in range(SchwefelSpace.n_dimensions):
                new_x.append(random.uniform(SchwefelSpace.low_bound, SchwefelSpace.up_bound))
        else:
            new_x = []
            for i in range(SchwefelSpace.n_dimensions):
                new_x.append(self.x[i] + random.uniform(-SchwefelSpace.eps, SchwefelSpace.eps))
                if new_x[i] - SchwefelSpace.low_bound < 0:
                    new_x[i] = SchwefelSpace.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - SchwefelSpace.up_bound > 0:
                    new_x[i] = SchwefelSpace.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(SchwefelSpace.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
