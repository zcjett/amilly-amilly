from collections import defaultdict
import csv
import json

class LeagueStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')

        self.stats = defaultdict(dict)

        self.read_league_stats()
        #self.print_stats()


    def read_league_stats(self):
        stats = ['k_percent', 'ops', 'sb', 'cs', 'hr', 'pa', 'bb', 'r', 'woba']
        years = [2013, 2014]
        for year in years:
            infile = '%s/League/%d League Stats.csv' %(self.statsDir, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                for i, stat_val in enumerate([float(x.rstrip('%')) for x in items[1:10]]):
                    if stats[i]=='k_percent':
                        stat_val/=100.0
                    self.stats[year][stats[i]] = stat_val

    def print_stats(self):
        print json.dumps(self.stats, indent=4)