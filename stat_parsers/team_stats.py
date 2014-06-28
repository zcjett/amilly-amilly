from collections import defaultdict
import csv
import json



TEAM_NAMES = {
    'COL': {'mascot': 'Rockies',
            'location': 'Colorado'},
    'TOR': {'mascot': 'Blue Jays',
            'location': 'Toronto'},
    'DET': {'mascot': 'Tigers',
            'location': 'Detroit'},
    'OAK': {'mascot': 'Athletics',
            'location': 'Oakland'},
    'MIA': {'mascot': 'Marlins',
            'location': 'Miami'},
    'LAA': {'mascot': 'Angels',
            'location': 'Los Angeles'},
    'LOS': {'mascot': 'Dodgers',
            'location': 'Los Angeles'},
    'CWS': {'mascot': 'White Sox',
            'location': 'Chicago'},
    'CLE': {'mascot': 'Indians',
            'location': 'Cleveland'},
    'TEX': {'mascot': 'Rangrs',
            'location': 'Texas'},
    'BAL': {'mascot': 'Orioles',
            'location': 'Baltimore'},
    'MIL': {'mascot': 'Brewers',
            'location': 'Milwaukee'},
    'NYY': {'mascot': 'Yankees',
            'location': 'New York'},
    'SFG': {'mascot': 'Giants',
            'location': 'San Francisco'},
    'PIT': {'mascot': 'Pirates',
            'location': 'Pittsburgh'},
    'BOS': {'mascot': 'Red Sox',
            'location': 'Boston'},
    'MIN': {'mascot': 'Twins',
            'location': 'Minnesota'},
    'HOU': {'mascot': 'Astros',
            'location': 'Houston'},
    'TAM': {'mascot': 'Rays',
            'location': 'Tampa Bay'},
    'STL': {'mascot': 'Cardinals',
            'location': 'St Louis'},
    'WAS': {'mascot': 'Nationals',
            'location': 'Washington'},
    'PHI': {'mascot': 'Phillies',
            'location': 'Philadelphia'},
    'ARI': {'mascot': 'Diaomndbacks',
            'location': 'Arizona'},
    'ATL': {'mascot': 'Braves',
            'location': 'Atlanta'},
    'CIN': {'mascot': 'Reds',
            'location': 'Cincinnati'},
    'NYM': {'mascot': 'Mets',
            'location': 'New York'},
    'CHC': {'mascot': 'Cubs',
            'location': 'Chicago'},
    'SEA': {'mascot': 'Mariners',
            'location': 'Seattle'},
    'KAN': {'mascot': 'Royals',
            'location': 'Kansas City'},
    'SDP': {'mascot': 'Padres',
            'location': 'San Diego'}
}

def get_teams():
    return TEAM_NAMES.keys()

def get_team_by_mascot(mascot):
    for k,v in TEAM_NAMES:
        if v[mascot].lower()==mascot.lower():
            return k
    return None

def get_team_by_city(city):
    for k,v in TEAM_NAMES:
        if v[city].lower()==city.lower():
            return k
    return None

def get_team_mascot(team):
    return TEAM_NAMES[team]['mascot']

def get_team_location(team):
    return TEAM_NAMES[team]['location']

class TeamStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')
        self.stats = defaultdict(lambda: defaultdict( lambda: defaultdict( lambda: defaultdict (dict))))

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
                team = self.get_team_by_mascot(items[0])
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
                    team = self.get_team_by_mascot(items[0])
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