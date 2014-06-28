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

    def pitcher_points_expected_for_k(self, player):
        pitcher_k_per_9 = self.player_stats.get_k_pitched(self.year, player) / (self.player_stats.get_ip(self.year, player) / 9.0)
        expected_ip = self.player_stats.get_ip(self.year, player) / self.player_stats.get_gs(self.year, player)

        playerTeam = self.player_stats.get_team(player)
        playerPitchHand = self.player_stats.get_throwing_hand(player)
        oppTeam = self.team_stats.get_opponent(playerTeam)

        opp_k_percentage = (self.team_stats.get_so(self.year, oppTeam, playerPitchHand) / self.team_stats.get_pa(self.year, oppTeam, playerPitchHand)) / self.league_stats.get_k_percent(self.year)

        return pitcher_k_per_9 * (expected_ip/9) * opp_k_percentage

    def pitcher_expected_ip(self, player):
        return self.player_stats.get_ip(self.year, player) / self.player_stats.get_gs(self.year, player)

    def pitcher_points_expected_for_win(self, player):
        # TODO: need vegas lines
        return 2

    def pitcher_points_expected_for_er(self, player):
        player_team = self.player_stats.get_team(player)
        opp_team = self.team_stats.get_opponent(player_team)
        player_loc = self.team_stats.get_home_or_away(player_team)
        xfip = self.player_stats.get_xfip(self.year, player, player_loc)

        if player_loc=='home':
            park_team = player_team
        else:
            park_team = opp_team
        park_factor = self.ballpark_stats.get_overall_park_factor(park_team)

        player_hand = self.player_stats.get_throwing_hand(player)
        pitcher_hand_hits = self.team_stats.get_woba(self.year, opp_team, player_hand) / self.league_stats.get_woba(self.year)

        return -1.0/9 * xfip * park_factor * pitcher_hand_hits * self.expected_ip(player)

    ###########
    # BATTERS #
    ###########


    def batter_points_expected_for_hits(self, player):
        adj_slg = (1.0 * self.player_stats.get_1b_total(self.year, player) + \
                   2.0 * self.player_stats.get_2b_total(self.year, player) + \
                   3.0 * self.player_stats.get_3b_total(self.year, player) - \
                   0.25 * (self.player_stats.get_ab_total(self.year, player) - self.player_stats.get_h_total(self.year, player))) / \
                  (self.player_stats.get_ab_total(self.year, player) - self.player_stats.get_hr_total(self.year, player))

        exp_ab = 1.0 * self.player_stats.get_ab_total(self.year, player) / self.player_stats.get_g_total(self.year, player)

        player_team = self.player_stats.get_team(player)
        player_hand = self.player_stats.get_batting_hand(player)
        opp_team = self.team_stats.get_opponent(player_team)
        opp_pitcher = self.player_stats.get_starting_pitcher(opp_team)
        opp_pitcher_woba = self.player_stats.get_woba_allowed(self.year, opp_pitcher, player_hand)
        opp_pitcher_eff = opp_pitcher_woba / self.league_stats.get_woba(self.year)

        opp_pitcher_hand = self.player_stats.get_throwing_hand(opp_pitcher)
        player_bat_eff = self.player_stats.get_woba(self.year, player, opp_pitcher_hand) / self.league_stats.get_woba(self.year)

        if self.team_stats.get_home_or_away(player_team)=='home':
            park = player_team
        else:
            park = opp_team
        park_factor = self.ballpark_stats.get_overall_park_factor(park)

        return adj_slg * exp_ab * opp_pitcher_eff * player_bat_eff * park_factor


    def batter_points_expected_for_walks(self, player):
        batter_walk_percentage = self.player_stats.get_bb_percent_total(self.year, player)

        exp_ab = 1.0 * self.player_stats.get_ab_total(self.year, player) / self.player_stats.get_g_total(self.year, player)

        player_team = self.player_stats.get_team(player)
        player_hand = self.player_stats.get_batting_hand(player)
        opp_team = self.team_stats.get_opponent(player_team)
        opp_pitcher = self.player_stats.get_starting_pitcher(opp_team)
        pitcher_bb_perc = self.player_stats.get_bb_allowed(self.year, opp_pitcher, player_hand) / self.player_stats.get_tbf(self.year, opp_pitcher, player_hand)
        league_bb_perc = self.league_stats.get_bb(self.year) / self.league_stats.get_pa(self.year)
        pitcher_eff_walk = pitcher_bb_perc / league_bb_perc

        return batter_walk_percentage * exp_ab * pitcher_eff_walk

    def batter_points_expected_for_hr(self, player):
        batter_hr_percentage = self.player_stats.get_hr_total(self,year,player) /


