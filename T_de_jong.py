from basic_playground import *
import math as math

#   global minimum is obtainable for xi=0, f(x)=0
#   search space is limited to [-5.12, 5.12]
class DeJongSpace:
    eps = 0.2
    n_dimensions = 10

    def __init__(self):
        self.x = []
        for i in range(DeJongSpace.n_dimensions):
            self.x.append(random.uniform(-5.12, 5.12))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 0
        for i in range(DeJongSpace.n_dimensions):
            self.y = self.y + self.x[i]**2
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(DeJongSpace.n_dimensions):
            new_x.append(self.x[i] + random.uniform(-DeJongSpace.eps, DeJongSpace.eps))
            if new_x[i] < -5.12:
                new_x[i] = -5.12
            if new_x[i] > 5.12:
                new_x[i] = 5.12
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(DeJongSpace.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff

