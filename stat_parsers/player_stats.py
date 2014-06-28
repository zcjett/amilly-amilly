from team_stats import *
from collections import defaultdict
import csv
import json
import urllib2
import re

from bs4 import BeautifulSoup
from random import randint

class PlayerStats:

    def __init__(self, statsDir):
        self.statsDir = statsDir.rstrip('/')

        self.stats = defaultdict(lambda: defaultdict( lambda: defaultdict( lambda: defaultdict (dict))))

        # self.read_pitcher_home_away()
        # self.read_pitcher_left_right()
        # self.read_pitcher_total_stats()
        # self.read_catcher_stats()
        # self.read_batter_left_right()
        # self.read_batter_total_stats()
        # self.read_handedness()
        # self.read_positions_and_salaries()
        self.read_rosters()

        # print len([name for name, stats in self.stats.items() if 'bats' in stats])
        # print len([name for name, stats in self.stats.items() if 2014 in stats])
        # print len([name for name, stats in self.stats.items() if 2013 in stats])

        self.printStats()

    def printStats(self):
        print json.dumps(self.stats, indent=4)

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

    def get_xfip(self, year, player, homeOrAway):
        return self.stats[player][year]['xfip'][homeOrAway]

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

    def get_hr_allowed(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['hr_allowed']['LHB']
        elif hand.lower()=='right':
            return self.stats[player][year]['hr_allowed']['RHB']
        else:
            return None

    def get_bb_allowed(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['bb_allowed']['LHB']
        elif hand.lower()=='right':
            return self.stats[player][year]['bb_allowed']['RHB']
        else:
            return None

    def get_tbf(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['tbf']['LHB']
        elif hand.lower()=='right':
            return self.stats[player][year]['tbf']['RHB']
        else:
            return None

    def get_woba_allowed(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['woba_allowed']['LHB']
        elif hand.lower()=='right':
            return self.stats[player][year]['woba_allowed']['RHB']
        else:
            return None

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

    def get_gs(self, year, player):
        return self.stats[player][year]['gs_total']

    def get_k_pitched(self, year, player):
        return self.stats[player][year]['k_pitched_total']

    def get_ip(self, year, player):
        return self.stats[player][year]['ip_total']

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

    def get_catcher_sb(self, year, player):
        return self.stats[player][year]['sb_catcher']

    def get_catcher_cs(self, year, player):
        return self.stats[player][year]['cs_catcher']

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

    def get_pa(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['pa']['LHP']
        elif hand.lower()=='right':
            return self.stats[player][year]['pa']['RHP']
        else:
            return None

    def get_hr(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['hr']['LHP']
        elif hand.lower()=='right':
            return self.stats[player][year]['hr']['RHP']
        else:
            return None

    def get_k(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['k']['LHP']
        elif hand.lower()=='right':
            return self.stats[player][year]['k']['RHP']
        else:
            return None

    def get_woba(self, year, player, hand):
        if hand.lower()=='left':
            return self.stats[player][year]['woba']['LHP']
        elif hand.lower()=='right':
            return self.stats[player][year]['woba']['RHP']
        else:
            return None

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

    def get_1b_total(self, year, player):
        return self.stats[player][year]['1b_total']

    def get_2b_total(self, year, player):
        return self.stats[player][year]['2b_total']

    def get_3b_total(self, year, player):
        return self.stats[player][year]['3b_total']

    def get_h_total(self, year, player):
        return self.stats[player][year]['h_total']

    def get_bb_total(self, year, player):
        return self.stats[player][year]['bb_total']

    def get_bb_percent_total(self, year, player):
        return self.stats[player][year]['bb_percent_total']

    def get_hr_total(self, year, player):
        return self.stats[player][year]['hr_total']

    def get_ah_total(self, year, player):
        return self.stats[player][year]['ah_total']

    def get_pa_total(self, year, player):
        return self.stats[player][year]['pa_total']

    def get_ba_total(self, year, player):
        return self.stats[player][year]['ba_total']

    def get_g_total(self, year, player):
        return self.stats[player][year]['g_total']

    def get_sb_total(self, year, player):
        return self.stats[player][year]['sb_total']

    def get_cs_total(self, year, player):
        return self.stats[player][year]['cs_total']

    def read_positions_and_salaries(self):
        # TODO: this is a daily stat
        infile = '%s/Test Data/Salaries/Fanduel- 6.3.2014 Salaries.csv' %(self.statsDir)
        reader = csv.reader(open(infile), quotechar='"')
        for items in reader:
            # Sample entry:
            # OF,Colby RasmusDL,2.3,37,TAM@TOR,"$3,500 ",Add
            position = items[0]
            player, status = self._clean_name(items[1])
            salary = self._clean_salary(items[5])
            self.stats[player]['fielding_position'] = position
            self.stats[player]['salary'] = salary
            self.stats[player]['availability'] = status

    def _clean_name(self, name):
        # Returns a tuple (name, status) where status is "P", "DL" or None
        if name.endswith('DL'):
            return name.lower()[:-2], 'DL'
        elif name.endswith('P'):
            return name.lower()[:-1], 'P'
        else:
            return name.lower(), None

    def _clean_salary(self, salary):
        # Returns a numerical value for the given salary string
        return int(salary.strip().replace('$', '').replace(',', ''))

    def get_fielding_position(self, player):
        return self.stats[player]['fielding_position']

    def get_salary(self, player):
        return self.stats[player]['salary']

    def get_availability(self, player):
        return self.stats[player]['availability']


    def read_positions_and_salaries(self):
        # TODO: this is a daily stat
        infile = '%s/Test Data/Salaries/Fanduel- 6.3.2014 Salaries.csv' %(self.statsDir)
        reader = csv.reader(open(infile), quotechar='"')
        for items in reader:
            # Sample entry:
            # OF,Colby RasmusDL,2.3,37,TAM@TOR,"$3,500 ",Add
            position = items[0]
            player, status = self._clean_name(items[1])
            salary = self._clean_salary(items[5])
            self.stats[player]['fielding_position'] = position
            self.stats[player]['salary'] = salary
            self.stats[player]['availability'] = status

    def read_rosters(self):
        handMap = {'R': 'right',
                   'L': 'left',
                   'B': 'switch',
                   'S': 'switch'}

        for team in get_teams():
            url_team = team
            if team=='LOS':
                url_team = 'LAD'
            elif team=='CWS':
                url_team='CHW'
            elif team=='SDP':
                url_team='SD'
            elif team=='SFG':
                url_team='SF'

            url_mascot = get_team_mascot(team).lower().replace(' ', '-')
            url_location = get_team_location(team).lower().replace(' ', '-')
            url = 'http://espn.go.com/mlb/team/roster/_/name/%s/sort/lastName/%s-%s' %(url_team.lower(), url_location, url_mascot)
            doc = urllib2.urlopen(url).read()
            soup = BeautifulSoup(doc)
            tab = soup.find('table')
            # header = [td.text for td in tab.find_all('tr')[1].find_all('td')]
            # Header for data is : ['NO.', 'NAME', 'POS', 'BAT', 'THW', 'AGE', 'HT', 'WT', 'BIRTH PLACE', 'SALARY']
            player_data = [[td.text for td in tr.find_all('td')] for tr in tab.find_all('tr')[2:]]
            for p in player_data:
                # TODO: could use this DL information.
                player = re.sub('DL[0-9]*$', '', p[1]).strip().lower()
                # TODO: could use this position info
                position = p[2]
                self.stats[player]['team'] = team
                self.stats[player]['bats'] = handMap[p[3]]
                self.stats[player]['throws'] = handMap[p[4]]

    def get_throwing_hand(self, player):
        return self.stats[player]['throws']

    def get_batting_hand(self, player):
        return self.stats[player]['bats']

    def get_team(self, player):
        return self.stats[player]['team']


    # fix these...
    def get_batting_position(self, player):
        return randint(1, 9)