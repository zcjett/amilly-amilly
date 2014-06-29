from collections import defaultdict
import csv
import json

TEAM_NAMES = {
    'COL': {'mascot': 'Rockies',
            'location': 'Colorado',
            'league': 'NL'},
    'TOR': {'mascot': 'Blue Jays',
            'location': 'Toronto',
            'league': 'AL'},
    'DET': {'mascot': 'Tigers',
            'location': 'Detroit',
            'league': 'AL'},
    'OAK': {'mascot': 'Athletics',
            'location': 'Oakland',
            'league': 'AL'},
    'MIA': {'mascot': 'Marlins',
            'location': 'Miami',
            'league': 'NL'},
    'LAA': {'mascot': 'Angels',
            'location': 'Los Angeles',
            'league': 'AL'},
    'LOS': {'mascot': 'Dodgers',
            'location': 'Los Angeles',
            'league': 'NL'},
    'CWS': {'mascot': 'White Sox',
            'location': 'Chicago',
            'league': 'AL'},
    'CLE': {'mascot': 'Indians',
            'location': 'Cleveland',
            'league': 'AL'},
    'TEX': {'mascot': 'Rangers',
            'location': 'Texas',
            'league': 'AL'},
    'BAL': {'mascot': 'Orioles',
            'location': 'Baltimore',
            'league': 'AL'},
    'MIL': {'mascot': 'Brewers',
            'location': 'Milwaukee',
            'league': 'NL'},
    'NYY': {'mascot': 'Yankees',
            'location': 'New York',
            'league': 'AL'},
    'SFG': {'mascot': 'Giants',
            'location': 'San Francisco',
            'league': 'NL'},
    'PIT': {'mascot': 'Pirates',
            'location': 'Pittsburgh',
            'league': 'NL'},
    'BOS': {'mascot': 'Red Sox',
            'location': 'Boston',
            'league': 'AL'},
    'MIN': {'mascot': 'Twins',
            'location': 'Minnesota',
            'league': 'AL'},
    'HOU': {'mascot': 'Astros',
            'location': 'Houston',
            'league': 'AL'},
    'TAM': {'mascot': 'Rays',
            'location': 'Tampa Bay',
            'league': 'AL'},
    'STL': {'mascot': 'Cardinals',
            'location': 'St Louis',
            'league': 'NL'},
    'WAS': {'mascot': 'Nationals',
            'location': 'Washington',
            'league': 'NL'},
    'PHI': {'mascot': 'Phillies',
            'location': 'Philadelphia',
            'league': 'NL'},
    'ARI': {'mascot': 'Diamondbacks',
            'location': 'Arizona',
            'league': 'NL'},
    'ATL': {'mascot': 'Braves',
            'location': 'Atlanta',
            'league': 'NL'},
    'CIN': {'mascot': 'Reds',
            'location': 'Cincinnati',
            'league': 'NL'},
    'NYM': {'mascot': 'Mets',
            'location': 'New York',
            'league': 'NL'},
    'CHC': {'mascot': 'Cubs',
            'location': 'Chicago',
            'league': 'NL'},
    'SEA': {'mascot': 'Mariners',
            'location': 'Seattle',
            'league': 'AL'},
    'KAN': {'mascot': 'Royals',
            'location': 'Kansas City',
            'league': 'AL'},
    'SDP': {'mascot': 'Padres',
            'location': 'San Diego',
            'league': 'NL'}
}

def get_teams():
    return TEAM_NAMES.keys()

def get_team_by_mascot(mascot):
    for k,v in TEAM_NAMES.items():
        if v['mascot'].lower()==mascot.lower():
            return k
    return None

def get_team_by_city(city):
    for k,v in TEAM_NAMES.items():
        if v['city'].lower()==city.lower():
            return k
    return None

def get_team_mascot(team):
    return TEAM_NAMES[team]['mascot']

def get_team_location(team):
    return TEAM_NAMES[team]['location']

def get_team_league(team):
    return TEAM_NAMES[team]['league']

class TeamStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')
        self.stats = defaultdict(lambda: defaultdict( lambda: defaultdict( lambda: defaultdict (dict))))

        self.read_team_stats()
        self.read_team_left_right()
        self.read_daily_matchups()
        self.read_fielding_stats()

        # self.printStats()


    def printStats(self):
        print json.dumps(self.stats, indent=4)

    def read_team_stats(self):
        years = [2013, 2014]
        for year in years:
            infile = '%s/Team/%d Team Stats.csv' %(self.statsDir, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                team = get_team_by_mascot(items[0])
                self.stats[team][year]['runs_team'] = float(items[1])

    def get_runs(self, year, team):
        return self.stats[team][year]['runs_team']

    def read_team_left_right(self):
        stats = ['so', 'pa', 'woba']
        years = [2013, 2014]
        for year in years:
            for hand in ['RHP', 'LHP']:
                infile = '%s/Team/%d Team Stats vs %s.csv' %(self.statsDir, year, hand)
                reader = csv.reader(open(infile), quotechar='"')
                header = reader.next()
                for items in reader:
                    team = get_team_by_mascot(items[0])
                    for i, stat_val in enumerate([float(x) for x in items[1:4]]):
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

    def get_woba(self, year, team, hand):
        if hand.lower()=='left':
            return self.stats[team][year]['woba']['LHP']
        elif hand.lower()=='right':
            return self.stats[team][year]['woba']['RHP']
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


    def read_fielding_stats(self):
        years = [2013, 2014]
        for year in years:
            infile = '%s/Team/%d Team Fielding Stats.csv' %(self.statsDir, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                team = get_team_by_mascot(items[0])
                self.stats[team][year]['sb_allowed'] = float(items[1])
                self.stats[team][year]['cs_fielding'] = float(items[2])

    def get_sb_allowed(self, year, team):
        return self.stats[team][year]['sb_allowed']

    def get_cs_fielding(self, year, team):
        return self.stats[team][year]['cs_fielding']