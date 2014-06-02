from random import choice, shuffle
from collections import defaultdict

class TeamMCMC:

    def __init__(self, names, classes, values, costs, capacity, object_composition):

        self.names = names
        self.values = dict(zip(names, values))
        self.costs = dict(zip(names, costs))
        self.classes = dict(zip(names, classes))
        self.capacity = capacity
        self.valid_comp = []
        for c, count in object_composition.items():
            self.valid_comp.extend([c]*count)

        self.available_names_by_class = defaultdict(list)
        for i, n in enumerate(names):
            self.available_names_by_class[classes[i]].append(n)
        self.unavailable_names_by_class = dict([(c, []) for c in self.available_names_by_class.keys()])

        # current team status to be updated during MCMC
        self.current_team = []
        self.current_value = None
        self.current_cost = None


    def get_available(self, object_class):
        return self.available_names_by_class[object_class]

    def make_random_team(self):
        team_found = False
        while not team_found:
            random_comp = list(self.valid_comp)
            shuffle(random_comp)
            # reset team
            self.current_team = []
            self.current_cost = 0
            self.current_value = 0
            for new_class in random_comp:
                candidates = [name for name in self.get_available(new_class) if (self.costs[name] + self.current_cost) < self.capacity]
                if len(candidates) == 0:
                    break
                new_name = choice(candidates)
                # update team with random candidate player
                self.current_team.append(new_name)
                self.current_cost += self.costs[new_name]
                self.current_value += self.values[new_name]
            team_found = True

    def find_solution(self):
        teams = []
        for i in range(10000):
            self.make_random_team()
            teams.append( (self.current_cost, self.current_value, self.current_team) )

        teams.sort(key=lambda x: x[1])

        for cost, val, team in teams:
            print '$%d' % cost, val, team