from basic_playground import *
import math as math

#   global minimum is obtainable for xi=1, f(x)=0
#   search space is limited to [-2.048, 2.048]
class RosenbrockSpace:
    eps = 0.001
    n_dimensions = 5
    up_bound = 2.048
    low_bound = -2.048

    def __init__(self):
        self.x = []
        for i in range(RosenbrockSpace.n_dimensions):
            self.x.append(random.uniform(RosenbrockSpace.low_bound, RosenbrockSpace.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        for i in range(RosenbrockSpace.n_dimensions-1):
            self.y = self.y + 100*(self.x[i+1] - self.x[i]**2)**2 + (1 - self.x[i])**2
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(RosenbrockSpace.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.15:
                new_x.append(random.uniform(RosenbrockSpace.low_bound, RosenbrockSpace.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-RosenbrockSpace.eps, RosenbrockSpace.eps))
                if new_x[i] - RosenbrockSpace.low_bound < 0:
                    new_x[i] = RosenbrockSpace.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - RosenbrockSpace.up_bound > 0:
                    new_x[i] = RosenbrockSpace.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(RosenbrockSpace.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
