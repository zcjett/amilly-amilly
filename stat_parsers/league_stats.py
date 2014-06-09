from collections import defaultdict
import csv
import json

class LeagueStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')

        self.stats = defaultdict(dict)

        self.read_league_stats()

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

    def get_k_percent(self, year):
        return self.stats[year]['k_percent']

    def get_ops(self, year):
        return self.stats[year]['ops']

    def get_sb(self, year):
        return self.stats[year]['sb']

    def get_cs(self, year):
        return self.stats[year]['cs']

    def get_hr(self, year):
        return self.stats[year]['hr']

    def get_pa(self, year):
        return self.stats[year]['pa']

    def get_bb(self, year):
        return self.stats[year]['bb']

    def get_r(self, year):
        return self.stats[year]['r']

    def get_woba(self, year):
        return self.stats[year]['woba']

    def print_stats(self):
        print json.dumps(self.stats, indent=4)