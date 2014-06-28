from collections import defaultdict
import csv
import json


class TeamStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')
        self.stats = defaultdict(lambda: defaultdict( lambda: defaultdict( lambda: defaultdict (dict))))

        self.team_names = {
            'COL': {'mascot': 'Rockies',
                    'locaiton': 'Colorado'},
            'TOR': {'mascot': 'Blue Jays',
                    'location': ''},
            'DET': {'mascot': 'Tigers',
                    'location': ''},
            'OAK': {'mascot': 'Athletics',
                    'location': ''},
            'MIA': {'mascot': 'Marlins',
                    'location': ''},
            'LAA': {'mascot': 'Angels',
                    'location': ''},
            'LOS': {'mascot': 'Dodgers',
                    'location': ''},
            'CWS': {'mascot': 'White Sox',
                    'location': ''},
            'CLE': {'mascot': 'Indians',
                    'location': ''},
            'TEX': {'mascot': 'Rangrs',
                    'location': ''},
            'BAL': {'mascot': 'Orioles',
                    'location': ''},
            'MIL': {'mascot': 'Brewers',
                    'location': ''},
            'NYY': {'mascot': 'Yankees',
                    'location': ''},
            'SFG': {'mascot': 'Giants',
                    'location': ''},
            'PIT': {'mascot': 'Pirates',
                    'location': ''},
            'BOS': {'mascot': 'Red Sox',
                    'location': ''},
            'MIN': {'mascot': 'Twins',
                    'location': ''},
            'HOU': {'mascot': 'Astros',
                    'location': ''},
            'TAM': {'mascot': 'Rays',
                    'location': ''},
            'STL': {'mascot': 'Cardinals',
                    'location': ''},
            'WAS': {'mascot': 'Nationals',
                    'location': ''},
            'PHI': {'mascot': 'Phillies',
                    'location': ''},
            'ARI': {'mascot': 'Diaomndbacks',
                    'location': ''},
            'ATL': {'mascot': 'Braves',
                    'location': ''},
            'CIN': {'mascot': 'Reds',
                    'location': ''},
            'NYM': {'mascot': 'Mets',
                    'location': ''},
            'CHC': {'mascot': 'Cubs',
                    'location': ''},
            'SEA': {'mascot': 'Mariners',
                    'location': ''},
            'KAN': {'mascot': 'Royals',
                    'location': ''},
            'SDP': {'mascot': 'Padres',
                    'location': ''}
        }

        self.read_team_stats()
        self.read_team_left_right()
        self.read_daily_matchups()

    def printStats(self):
        print json.dumps(self.stats, indent=4)

    def read_team_stats(self):
        years = [2013, 2014]
        for year in years:
            infile = '%s/Team/%d Team Stats.csv' %(self.statsDir, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                team = get_team_name(items[0])
                self.stats[team][year]['runs_team'] = float(items[1])

    def get_runs(self, year, team):
        return self.stats[team][year]['runs_team']

    def read_team_left_right(self):
        stats = ['so', 'pa']
        years = [2013, 2014]
        for year in years:
            for hand in ['RHP', 'LHP']:
                infile = '%s/Team/%d Team Stats vs %s.csv' %(self.statsDir, year, hand)
                reader = csv.reader(open(infile), quotechar='"')
                header = reader.next()
                for items in reader:
                    team = get_team_name(items[0])
                    for i, stat_val in enumerate([float(x) for x in items[1:3]]):
                        self.stats[team][year][stats[i]][hand] = stat_val

    def get_so(self, year, team, hand):
        if hand.lower()=='left':
            return self.stats[team][year]['so']['LHP']
        elif hand.lower()=='right':
            return self.stats[team][year]['so']['RHP']
        else:
            return None

    def get_pa(self, year, team, hand):
        if hand.lower()=='left':
            return self.stats[team][year]['pa']['LHP']
        elif hand.lower()=='right':
            return self.stats[team][year]['pa']['RHP']
        else:
            return None

    def read_daily_matchups(self):
        # TODO: hard-coded daily stats
        infile = '%s/Test Data/Salaries/Fanduel- 6.3.2014 Salaries.csv' %(self.statsDir)
        reader = csv.reader(open(infile), quotechar='"')
        for items in reader:
            away, home = items[4].split('@')
            self.stats[home]['home_or_away'] = 'home'
            self.stats[away]['home_or_away'] = 'away'
            self.stats[home]['opponent'] = away
            self.stats[away]['opponent'] = home

    def get_home_or_away(self, team):
        return self.stats[team]['home_or_away']

    def get_opponent(self, team):
        return self.stats[team]['opponent']


    def get_teams(self):
        return self.team_mascot.values()

    def get_team_by_mascot(self, mascot):
        for k,v in self.team_names:
            if v[mascot]
        return self.team_mascot[mascot]

    def get_team_by_city(self, city):
        return self.team_city[city]
