from basic_playground import *
import math as math

#   global minimum is obtainable for xi=0, f(x)=0
#   search space is limited to [-35, 35]
class Ackley1Space:
    eps = 1
    n_dimensions = 5
    up_bound = 35
    low_bound = -35

    def __init__(self):
        self.x = []
        for i in range(Ackley1Space.n_dimensions):
            self.x.append(random.uniform(Ackley1Space.low_bound, Ackley1Space.up_bound))
        self.y = self.compute_value()

    def compute_value(self):
        pom1 = 0
        pom2 = 0
        for i in range(Ackley1Space.n_dimensions):
            pom1 = pom1 + self.x[i]**2
            pom2 = pom2 + math.cos(2*math.pi*self.x[i])
        pom1 = -0.02 * math.sqrt(pom1/Ackley1Space.n_dimensions)
        pom2 = pom2 / Ackley1Space.n_dimensions
        self.y = -20*math.e**pom1 - math.e ** pom2 + 20 + math.e
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.y = self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(Ackley1Space.n_dimensions):
            p = random.uniform(0, 1)
            if p < 0.05:
                new_x.append(random.uniform(Ackley1Space.low_bound, Ackley1Space.up_bound))
            else:
                #PROMIJENIO U RANDOM.CHOICE!!!!!!!!!!!!!!!!-------------------------------------------------------------
                new_x.append(self.x[i] + random.choice([-Ackley1Space.eps, Ackley1Space.eps]))
                if new_x[i] - Ackley1Space.low_bound < 0:
                    new_x[i] = Ackley1Space.low_bound * random.uniform(0.88, 0.98)
                if new_x[i] - Ackley1Space.up_bound > 0:
                    new_x[i] = Ackley1Space.up_bound * random.uniform(0.88, 0.98)
        self.set_solution(new_x)

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x

    def measure_difference(self, other):
        diff = 0
        for i in range(Ackley1Space.n_dimensions):
            diff = diff + (self.x[i] - other.x[i])**2
        diff = math.sqrt(diff)
        return diff
