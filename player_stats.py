from collections import defaultdict
import csv
import json

class PlayerStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')

        self.stats = defaultdict(lambda: defaultdict( lambda: defaultdict( lambda: defaultdict (dict))))

        self.read_pitcher_home_away()
        self.read_pitcher_left_right()
        self.read_pitcher_total_stats()
        self.read_catcher_stats()
        self.read_batter_left_right()
        self.read_batter_total_stats()

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
                    self.stats[player][year][stat][loc] = xfip


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
                        self.stats[player][year][stats[i]][hand] = stat_val


    def read_pitcher_total_stats(self):
        stats = ['gs_total', 'k_pitched_total', 'ip_total']
        years = [2013, 2014]
        for year in years:
            infile = '%s/Pitcher/%d/%d Total Pitcher Stats.csv' %(self.statsDir, year, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                player = items[0].lower()
                for i, stat_val in enumerate([float(x) for x in items[2:5]]):
                    self.stats[player][year][stats[i]] = stat_val


    def read_catcher_stats(self):
        stats = ['sb_catcher', 'cs_catcher']
        years = [2013, 2014]
        for year in years:
            infile = '%s/Catcher/%d Catcher Stats.csv' %(self.statsDir, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                player = items[0].lower()
                for i, stat_val in enumerate([float(x) for x in items[2:4]]):
                    self.stats[player][year][stats[i]] = stat_val

    def read_batter_left_right(self):
        stats = ['pa', 'hr', 'k', 'woba']
        years = [2013, 2014]
        for year in years:
            for hand in ['RHP', 'LHP']:
                infile = '%s/Batter/%d/%d Batter Stats vs %s.csv' %(self.statsDir, year, year, hand)
                reader = csv.reader(open(infile), quotechar='"')
                header = reader.next()
                for items in reader:
                    player = items[0].lower()
                    for i, stat_val in enumerate([float(x) for x in items[2:6]]):
                        self.stats[player][year][stats[i]][hand] = stat_val


    def read_batter_total_stats(self):
        stats = ['1b_total',
                 '2b_total',
                 '3b_total',
                 'h_total',
                 'bb_total',
                 'bb_percent_total',
                 'hr_total',
                 'ab_total',
                 'pa_total',
                 'ba_total',
                 'g_total',
                 'sb_total',
                 'cs_total']
        years = [2013, 2014]
        for year in years:
            infile = '%s/Batter/%d/%d Total Batter Stats.csv' %(self.statsDir, year, year)
            reader = csv.reader(open(infile), quotechar='"')
            header = reader.next()
            for items in reader:
                player = items[0].lower()
                for i, stat_val in enumerate([float(x.rstrip('%')) for x in items[2:15]]):
                    if stats[i]=='bb_percent_total':
                        stat_val/=100.0
                    self.stats[player][year][stats[i]] = stat_val


    def printStats(self):
        print json.dumps(self.stats, indent=4)