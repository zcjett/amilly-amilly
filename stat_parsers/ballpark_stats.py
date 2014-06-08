from collections import defaultdict
import csv
import json

class BallparkStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')

        self.stats = defaultdict(dict)

        self.read_ballpark_stats()
        #self.printStats()


    def read_ballpark_stats(self):
        stats = ['overall', 'avg_lhb', 'avg_rhb', 'hr_lhb', 'hr_rhb']
        infile = '%s/Park Factor/Ball Park Factor.csv' %(self.statsDir)
        reader = csv.reader(open(infile), quotechar='"')
        header = reader.next()
        for items in reader:
            team = items[0].upper()
            for i, stat_val in enumerate([float(x) for x in items[1:6]]):
                self.stats[team][stats[i]] = stat_val


    def printStats(self):
        print json.dumps(self.stats, indent=4)