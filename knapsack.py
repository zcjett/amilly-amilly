from collections import defaultdict


class ModifiedKnapsack:

    def __init__(self, names, classes, values, weights, capacity, class_restrictions):

        self.names = names
        self.all_classes = set(classes)
        self.values = values
        self.weights = weights
        self.capacity = capacity
        self.class_restrictions = class_restrictions

        self.name_index = dict([(name, i) for i, name in enumerate(names)])

        self.names_by_class = defaultdict(list)
        for i, n in enumerate(names):
            self.names_by_class[classes[i]].append(n)

    def name_ind(self, name):
        return self.name_index[name]

    def find_solution(self):
        start = min(self.values)

        for c, names in self.names_by_class.items():
            print c, len(names), names