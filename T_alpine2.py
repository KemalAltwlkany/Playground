from basic_playground import *
import math as math

#   global minimum is obtainable for xi=7.9170526982459462172
#   f(x)= -1* 2.8081311800070053291**n_dim
#   search space is limited to [0, 10]
class Alpine2Space:
    eps = 0.01
    n_dimensions = 5
    up_bound = 10
    low_bound = 0

    def __init__(self):
        self.x = []
        for i in range(Alpine2Space.n_dimensions):
            self.x.append(random.uniform(Alpine2Space.low_bound, Alpine2Space.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = -1
        for i in range(Alpine2Space.n_dimensions):
            self.y = self.y * math.sin(self.x[i]) * math.sqrt(self.x[i])
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(Alpine2Space.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.05:
                new_x.append(random.uniform(Alpine2Space.low_bound, Alpine2Space.up_bound))
            else:
                new_x.append(self.x[i] + random.uniform(-Alpine2Space.eps, Alpine2Space.eps))
                if new_x[i] - Alpine2Space.low_bound < 0:
                    new_x[i] = random.uniform(0.001, 0.999)  # bugfix!
                if new_x[i] - Alpine2Space.up_bound > 0:
                    new_x[i] = Alpine2Space.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(Alpine2Space.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
