import random as random
import copy as copy
import time as time
import bisect as bisect

epsilon = 0.00000001

class MyEvaluationError(LookupError):
    """Raise this error kemo"""

class ProblemSpace2:

    eps = 0.2

    def __init__(self):
        self.x = random.uniform(-2, 0)
        self.y = self.compute_value()

    def compute_value(self):
        self.y = pow(self.x, 8) + 3 * pow(self.x, 6) + 2 * pow(self.x, 5) - 17 * pow(self.x, 4) - 12 * pow(self.x, 3) \
                 - 11 * pow(self.x, 2) + self.x - 10
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.compute_value()

    def modify_solution(self):
        new_x = self.x + random.uniform(-ProblemSpace2.eps, ProblemSpace2.eps)
        new_crit = pow(new_x, 8) + 3 * pow(new_x, 6) + 2 * pow(new_x, 5) - 17 * pow(new_x, 4) - 12 * pow(new_x, 3) \
                 - 11 * pow(new_x, 2) + new_x - 10
        if new_crit - self.get_value() < 0:
            self.x = new_x
            self.y = new_crit

    def unconditional_modification(self):
        new_x = self.x + random.uniform(-ProblemSpace2.eps, ProblemSpace2.eps)
        new_crit = pow(new_x, 8) + 3 * pow(new_x, 6) + 2 * pow(new_x, 5) - 17 * pow(new_x, 4) - 12 * pow(new_x, 3) \
                   - 11 * pow(new_x, 2) + new_x - 10
        self.x = new_x
        self.y = new_crit

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x


class ProblemSpace1:

    eps = 0.1

    def __init__(self):
        self.x = [random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10), random.randint(-10, 10)]
        self.y = self.compute_value()

    def compute_value(self):
        self.y = self.x[0]**2 + self.x[1]**2 + self.x[2]**2 + self.x[3]**2 + self.x[4]**2
        return self.y

    def set_solution(self, sol):
        self.x = sol
        self.compute_value()

    def modify_solution(self):
        new_x = []
        for i in range(len(self.x)):
            new_x.append(self.x[i] + random.uniform(-ProblemSpace1.eps, ProblemSpace1.eps))
        new_crit = new_x[0]**2 + new_x[1]**2 + new_x[2]**2 + new_x[3]**2 + new_x[4]**2
        if new_crit - self.get_value() < 0:
            self.x = new_x
            self.y = new_crit

    def get_value(self):
        return self.y

    def get_solution(self):
        return self.x


class Kid:

    grown_up_age = 4
    problem_space = ProblemSpace1

    def __init__(self):
        self.attribute = Kid.problem_space()
        self.is_captain = False
        self.age = 0  # should be set to 10 for initial children?
        self.criteria = self.evaluate()
        self.is_new_kid = True  # should be set to False for initial children??

    def evaluate(self):
        self.criteria = self.attribute.compute_value()
        return self.criteria

    def increment_age(self):
        self.age += 1
        if self.age >= Kid.grown_up_age:
            self.is_new_kid = False

# changes are only accepted if they give a better criteria function
    def modify_kid(self):
    #   self.attribute.modify_solution()
    #   self.criteria = self.attribute.get_value()
        self.attribute.unconditional_modification()
        self.criteria = self.attribute.get_value()

    def get_criteria(self):
        return self.criteria

    def get_age(self):
        return self.age

    def get_is_new_kid(self):
        return self.is_new_kid

    def get_is_captain(self):
        return self.is_captain

    def set_age(self, new_age):
        self.age = new_age
        if self.age >= Kid.grown_up_age:
            self.is_new_kid = False

    def set_is_captain(self, x):
        self.is_captain = x

    @staticmethod
    def set_growing_up_age(age):
        Kid.grown_up_age = age

    def print_child_info(self):
        print('------------------------------------------')
        print('The vector is =', self.attribute.x)
        print('Captain = ', self.is_captain)
        print('Child age is = ', self.age)
        print('New kid is = ', self.is_new_kid)
        print('Criteria is = ', self.criteria)
        print('------------------------------------------')

    def __lt__(self, other):
        return self.get_criteria() - other.get_criteria() < 0

    def __gt__(self, other):
        return self.get_criteria() - other.get_criteria() > 0

    def __le__(self, other):
        x = (self.get_criteria() - other.get_criteria() < 0 )
        y = ( abs(self.get_criteria() - other.get_criteria()) < epsilon )
        return x or y

# a local search, which should be used on the captain
    def local_search(self):
        pass


class Team:

    n_kids = 50
    home_sender = 2
    kid_problem_space = ProblemSpace1

    def __init__(self, make_team_empty=False):
        Kid.problem_space = Team.kid_problem_space
        self.best_value = None
        self.team_value = None
        self.squad = []
        if make_team_empty is False:
            for i in range(0, Team.n_kids, 1):
                self.squad.append(Kid())
                self.squad[i].set_age(Kid.grown_up_age)  # initial kids should all be prone to changes

    def sort_team(self, sort_type):
        self.squad.sort(key=Kid.get_criteria, reverse=sort_type)

    def send_kids_home(self):
        self.sort_team(False)  # sorts into ascending order
        self.best_value = self.squad[0].get_criteria()
        new_team = []
        n_sent = 0
        self.team_value = 0
        for i in range(Team.n_kids-1, -1, -1):
            if not self.squad[i].get_is_new_kid() and n_sent != Team.home_sender:
                n_sent += 1
                if i == 0:
                    raise MyEvaluationError('Error! Best kid got sent home')
                continue
            else:
                new_team.append(copy.deepcopy(self.squad[i]))
                self.team_value += self.squad[i].get_criteria()
        new_team = list(reversed(new_team))  # required!!!
        if n_sent != Team.home_sender:
            raise MyEvaluationError('Not enough kids sent home!')
        self.squad = new_team

    def add_new_kids(self):
        # precompute the keys to improve performance
        keys = []
        for i in range(Team.n_kids - Team.home_sender):
            keys.append(self.squad[i].get_criteria())
        for i in range(Team.home_sender):
            new_kid = Kid()
            position = bisect.bisect_right(keys, new_kid.get_criteria())
            keys.insert(position, new_kid.get_criteria())
            self.squad.insert(position, new_kid)
            self.team_value += new_kid.get_criteria()
            # the list remains sorted!!!!

    def modify(self):
        for i in range(Team.n_kids):
            self.squad[i].modify_kid()
            self.squad[i].increment_age()

    # presupposes that the team is sorted into ascending order
    def print_team_info(self):
        print("Team has =", Team.n_kids, " kids.")
        print("Team value is =", self.team_value)
        print("Team captain is: ")
        self.squad[0].print_child_info()

    def print_rooster(self):
        print("Kids currently in team: ")
        for kid in self.squad:
            kid.print_child_info()

    def get_best_value(self):
        return self.squad[0].get_criteria()

    def get_team_value(self):
        return self.team_value

    #  this method is for testing only. it should not modify any object attributes and it
    #  is inefficient
    def compute_team_value(self):
        sum_ = 0
        for kid in self.squad:
            sum_ += kid.get_criteria()
        return sum_

    #   this method is for testing only. it should not modify any object attributes and it
    #   is inefficient
    def compute_best_value(self):
        curr_best = self.squad[0].get_criteria()
        for i in range(1, len(self.squad), 1):
            if self.squad[i].get_criteria() - curr_best < 0:
                curr_best = self.squad[i].get_criteria()
        return curr_best

    # ------------ advanced methods start from here ------------
    def add_kid(self, new_kid):
        self.squad.append(new_kid)
        self.squad[-1].set_age(Kid.grown_up_age)  # new kids should be initially prone to changes

    def add_kid_slice(self, new_kids):
        for i in range(len(new_kids)):
            new_kids[i].set_age(Kid.grown_up_age)
        self.squad = self.squad + new_kids



class Playground:

    def __init__(self, x, y, z, p, q):
        Team.n_kids = x
        Team.home_sender = y
        Team.kid_problem_space = z
        self.max_iter = p
        Kid.grown_up_age = q
        self.teams = []

    def basic_search(self):
        for i in range(3):
            self.teams.append(Team())
        for i in range(self.max_iter):
            for j in range(3):
                self.teams[j].modify()
                self.teams[j].send_kids_home()
                self.teams[j].add_new_kids()
        for tms in self.teams:
            tms.print_team_info()

    def four_team_search(self):
        for i in range(4):
            self.teams.append(Team())
        for i in range(self.max_iter):
            for j in range(4):
                self.teams[j].modify()
                self.teams[j].send_kids_home()
                self.teams[j].add_new_kids()
            self.teams.sort(key=Team.get_best_value)

            if i % 2 == 0:
                # original idea
                new_ratings = [self.teams.pop(0)]
                self.teams.sort(key=Team.get_team_value)
                new_ratings.append(self.teams.pop(0))
                if self.teams[0].get_best_value() - self.teams[1].get_best_value() > 0:
                    self.teams[0], self.teams[1] = self.teams[1], self.teams[0]
                self.teams = new_ratings + self.teams
                #    1st team has best captain, 2nd team has best team value
                #    3rd team has a better captain compared to the 4th team
                #    this does not mean that team 2 has a better captain compared to team 3 nor 4
            #   modified idea
            else:
                self.teams.sort(key=Team.get_team_value)

            self.construct_teams()

        for tms in self.teams:
            tms.print_team_info()  # last team criteria is not of use anyways

    def construct_teams(self):
        new_teams = [Team(make_team_empty=True), Team(make_team_empty=True), Team(make_team_empty=True), Team()]
        # presuppose that the number of kids per team is divisible by 4
        kn = int(Team.n_kids / 4)
        for i in range(4):
            new_teams[0].add_kid_slice(self.teams[i].squad[0:kn])
            new_teams[1].add_kid_slice(self.teams[i].squad[kn:2*kn])
            new_teams[2].add_kid_slice(self.teams[i].squad[2*kn:3*kn])
            #new_teams[3].add_kid_slice(self.teams[i].squad[3*kn:])


def commit():
    print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    print("ooooooooooooooooooooooooooooo SIMPLE ALGORITHM ooooooooooooooooooooooooooooooooooooooooooooooo")
    print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    play_space = Playground(80, 10, ProblemSpace2, 1000, 6)
    start = time.time()
    play_space.basic_search()
    end = time.time()
    print("The algorithm ran for, t = ", end - start)

def commit_advanced():
    print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    print("ooooooooooooooooooooooooooooo ADVANCED ALGORITHM ooooooooooooooooooooooooooooooooooooooooooooo")
    print("oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    play_space = Playground(200, 5, ProblemSpace2, 1000, 25)
    start = time.time()
    play_space.four_team_search()
    end = time.time()
    print("The advanced algorithm ran for, t = ", end - start)

x = ProblemSpace2()
x.set_solution(1.527)
print(x.get_value())

commit()

commit_advanced()
