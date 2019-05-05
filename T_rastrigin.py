from basic_playground import *
import math as math

#   global minimum is obtainable for xi=0, f(x)=0
#   search space is limited to [-5.12, 5.12]
class RastriginSpace:
    eps = 0.01
    n_dimensions = 10
    up_bound = -5.12
    low_bound = 5.12

    def __init__(self):
        self.x = []
        for i in range(RastriginSpace.n_dimensions):
            self.x.append(random.uniform(RastriginSpace.low_bound, RastriginSpace.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        self.y = 10*RastriginSpace.n_dimensions
        for i in range(RastriginSpace.n_dimensions):
            try:
                self.y = self.y + self.x[i]**2 - 10*math.cos(2*math.pi*self.x[i])
            except ValueError as ve:
                print(ve)
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        p = random.uniform(0, 1)
        if p < 0.12:
            new_x = []
            for i in range(RastriginSpace.n_dimensions):
                new_x.append(random.uniform(RastriginSpace.low_bound, RastriginSpace.up_bound))
        else:
            new_x = []
            #    ERROR IN LOGIC 100%
            #       --------------------------------------------------
            for i in range(RastriginSpace.n_dimensions):
                new_x.append(self.x[i] + self.x[i]*random.uniform(-RastriginSpace.eps, RastriginSpace.eps))
                if new_x[i] < RastriginSpace.low_bound:
                    new_x[i] = RastriginSpace.low_bound + math.fabs(self.x[i])*random.uniform(2*RastriginSpace.eps, 4*RastriginSpace.eps)
                if new_x[i] > RastriginSpace.up_bound:
                    new_x[i] = RastriginSpace.up_bound - self.x[i]*random.uniform(2*RastriginSpace.eps, 4*RastriginSpace.eps)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(RastriginSpace.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
