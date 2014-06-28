class StatEquations:

    def __init__(self, player_stats, team_stats, ballpark_stats, league_stats, daily_stats):
        self.player_stats = player_stats
        ''':type: PlayerStats'''
        self.ballpark_stats = ballpark_stats
        ''':type: BallparkStats'''
        self.team_stats = team_stats
        ''':type: TeamStats'''
        self.league_stats = league_stats
        ''':type: LeagueStats'''
        self.daily_stats = daily_stats
        ''':type: DailyStats'''

        self.year = 2014

    ############
    # PITCHERS #
    ############

    def points_expected_for_k(self, player):
        pitcher_k_per_9 = self.player_stats.get_k_pitched(self.year, player) / (self.player_stats.get_ip(self.year, player) / 9.0)
        expected_ip = self.player_stats.get_ip(self.year, player) / self.player_stats.get_gs(self.year, player)

        playerTeam = self.player_stats.get_team(player)
        playerPitchHand = self.player_stats.get_throwing_hand(player)
        oppTeam = self.team_stats.get_opponent(playerTeam)

        opp_k_percentage = (self.team_stats.get_so(self.year, oppTeam, playerPitchHand) / self.team_stats.get_pa(self.year, oppTeam, playerPitchHand)) / self.league_stats.get_k_percent(self.year)

        return pitcher_k_per_9 * (expected_ip/9) * opp_k_percentage
