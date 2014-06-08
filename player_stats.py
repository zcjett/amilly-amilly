from collections import defaultdict
import csv
import json

class PlayerStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')

        self.stats = defaultdict(lambda: defaultdict( lambda: defaultdict( lambda: defaultdict (dict))))


        # self.read_pitcher_home_away()
        # self.read_pitcher_left_right()
        # self.read_pitcher_total_stats()
        self.read_catcher_stats()

        self.printStats()

    def read_pitcher_home_away(self):
        stat = 'xfip'
        years = [2013, 2014]
        for year in years:
            for loc in ['Home', 'Away']:
                infile = '%s/Pitcher/%d/%d %s Pitcher Stats.csv' %(self.statsDir, year, year, loc)
                reader = csv.reader(open(infile), quotechar='"')
                header = reader.next()
                for items in reader:
                    player = items[0].lower()
                    xfip = float(items[2])
                    self.stats[player][stat][year][loc] = xfip


    def read_pitcher_left_right(self):
        stats = ['hr_allowed', 'bb_allowed', 'tbf', 'woba_allowed']
        years = [2013, 2014]
        for year in years:
            for hand in ['RHB', 'LHB']:
                infile = '%s/Pitcher/%d/%d Pitcher Stats vs %s.csv' %(self.statsDir, year, year, hand)
                reader = csv.reader(open(infile), quotechar='"')
                header = reader.next()
                for items in reader:
                    player = items[0].lower()
                    for i, stat_val in enumerate([float(x) for x in items[2:6]]):
                        self.stats[player][stats[i]][year][hand] = stat_val


    def read_pitcher_total_stats(self):
        stats = ['gs', 'k', 'ip']
        years = [2013, 2014]
        for year in years:
            infile = '%s/Pitcher/%d/%d Total Pitcher Stats.csv' %(self.statsDir, year, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                player = items[0].lower()
                for i, stat_val in enumerate([float(x) for x in items[2:5]]):
                    self.stats[player][stats[i]][year] = stat_val


    def read_catcher_stats(self):
        stats = ['sb_allowed', 'cs']
        years = [2013, 2014]
        for year in years:
            infile = '%s/Catcher/%d Catcher Stats.csv' %(self.statsDir, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                player = items[0].lower()
                for i, stat_val in enumerate([float(x) for x in items[2:4]]):
                    self.stats[player][stats[i]][year] = stat_val


    def printStats(self):
        print json.dumps(self.stats, indent=4)

