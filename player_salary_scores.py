import csv
from random import randint, choice


class PlayerSalaryScores:

    def __init__(self):
        self.players = {}

    def get_names(self, position=None):
        if position:
            return [name for name in self.players.keys() if self.get_position(name) == position]
        else:
            return self.players.keys()

    def get_salary(self, name):
        return self.players[name]['salary'] if (self.has_player(name)) else None

    def set_salary(self, name, salary):
        if self.has_player(name):
            self.players[name]['salary'] = salary
        else:
            self.players[name] = {'position': None, 'salary': salary, 'score': None}

    def get_score(self, player):
        return self.players[player]['score'] if (self.has_player(player)) else None

    def set_score(self, name, score):
        if self.has_player(name):
            self.players[name]['score'] = score
        else:
            self.players[name] = {'position': None, 'salary': None, 'score': score}

    def get_position(self, player):
        return self.players[player]['position'] if (self.has_player(player)) else None

    def set_position(self, name, position):
        if self.has_player(name):
            self.players[name]['position'] = position
        else:
            self.players[name] = {'position': position, 'salary': None, 'score': None}

    def has_player(self, name):
        return name in self.players

    def remove_player(self, name):
        self.players.pop(name, None)

    def read_positions_and_salaries(self, infile):
        reader = csv.reader(open(infile), quotechar='"')
        for line in reader:
            # Sample entry:
            # OF,Colby RasmusDL,2.3,37,TAM@TOR,"$3,500 ",Add
            position = line[0]
            name, status = self._clean_name(line[1])
            salary = self._clean_salary(line[5])
            self.set_salary(name, salary)
            self.set_position(name, position)

    def read_projections(self, infile):
        reader = csv.reader(open(infile), quotechar='"')
        for line in reader:
            name = line[0].strip()
            score = float(line[1])
            self.set_score(name, score)

    def add_fake_scores(self):
        print 'WARNING: using fake scores.'
        for name in self.get_names():
            self.set_score(name, self._fake_score(self.get_position(name)))

    def _clean_name(self, name):
        # Returns a tuple (name, status) where status is "DL" or None
        if name.endswith('DL'):
            return name.lower()[:-2], 'DL'
        elif name.endswith('P'):
            return name.lower()[:-1], None
        else:
            return name.lower(), None

    def _clean_salary(self, salary):
        # Returns a numerical value for the given salary string
        return int(salary.strip().replace('$', '').replace(',', ''))

    def _fake_score(self, position):
        if position == 'P':
            return randint(5, 20) + choice([0.0, 0.33, 0.66])
        else:
            return randint(-1, 10) + choice([0.0, 0.25, 0.5, 0.75])