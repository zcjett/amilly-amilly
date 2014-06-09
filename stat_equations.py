from collections import defaultdict

from stat_parsers.player_stats import PlayerStats
from stat_parsers.ballpark_stats import BallparkStats
from stat_parsers.team_stats import TeamStats
from stat_parsers.league_stats import LeagueStats

class StatEquations:

    def __init__(self, player_stats, team_stats, ballpark_stats, league_stats):

        self.player_stats = player_stats
        self.ballpark_stats = team_stats
        self.team_stats = ballpark_stats
        self.league_stats = league_stats

        self.year = 2014

    ############
    # PITCHERS #
    ############

    def points_expected_for_k(self, player):
        pitcher_k_per_9 = self.player_stats.get_k_pitched(self.year, player) / (self.player_stats.get_ip(self.year, player) / 9.0)
        expected_ip = self.player_stats.get_ip(self.year, player) / self.player_stats.get_gs(self.year, player)
        # TODO: get thesse stats
        opp_k_percentage_per_9 = 1

        return pitcher_k_per_9 * (expected_ip/9) * opp_k_percentage_per_9

