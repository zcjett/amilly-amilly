from collections import defaultdict
import csv
import json

class TeamStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')

        self.stats = defaultdict(dict)

        self.name_map = {'Rockies': 'COL',
                    'Blue Jays': 'TOR',
                    'Tigers': 'DET',
                    'Athletics': 'OAK',
                    'Marlins': 'MIA',
                    'Angels': 'LAA',
                    'Dodgers': 'LOS',
                    'White Sox': 'CWS',
                    'Indians': 'CLE',
                    'Rangers': 'TEX',
                    'Orioles': 'BAL',
                    'Brewers': 'MIL',
                    'Yankees': 'NYY',
                    'Giants': 'SFG',
                    'Pirates': 'PIT',
                    'Red Sox': 'BOS',
                    'Twins': 'MIN',
                    'Astros': 'HOU',
                    'Rays': 'TAM',
                    'Cardinals': 'STL',
                    'Nationals': 'WAS',
                    'Phillies': 'PHI',
                    'Diamondbacks': 'ARI',
                    'Braves': 'ATL',
                    'Reds': 'CIN',
                    'Mets': 'NYM',
                    'Cubs': 'CHC',
                    'Mariners': 'SEA',
                    'Royals': 'KAN',
                    'Padres': 'SDP'}


        self.read_team_stats()
        #self.printStats()


    def read_team_stats(self):
        years = [2013, 2014]
        for year in years:
            infile = '%s/Team/%d Team Stats.csv' %(self.statsDir, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                team = self.get_name(items[0])
                self.stats[team]['runs_team'] = float(items[1])

    def get_name(self, mascot):
        return self.name_map[mascot]

    def printStats(self):
        print json.dumps(self.stats, indent=4)