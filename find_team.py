#!/usr/bin/env python

import argparse

from stat_parsers.player_stats import PlayerStats
from stat_parsers.ballpark_stats import BallparkStats
from stat_parsers.team_stats import TeamStats
from stat_parsers.league_stats import LeagueStats
from stat_equations import StatEquations



CAPACITY = 35000
TEAM_COMP = {'P': 1,
             'C': 1,
             '1B': 1,
             '2B': 1,
             'SS': 1,
             '3B': 1,
             'OF': 3}

def main():
    parser = argparse.ArgumentParser(description='Find dat team.')
    parser.add_argument('salaries', help='File containing player salaries and positions.')
    parser.add_argument('projections', help='File containing projected points.')
    parser.add_argument('stats', help='Directory containing all stats.')
    parser.add_argument('--knapsack', help='Find a team using the modified knapsack approach.')
    parser.add_argument('--mcmc', action='store_true', help='Find a team using the MCMC approach.')
    args = parser.parse_args()

    # players = PlayerSalaryScores()
    # players.read_positions_and_salaries(args.salaries)
    # players.read_projections(args.projections)
    #
    # names = players.get_names()
    # classes = [players.get_position(n) for n in names]
    # values = [players.get_score(n) for n in names]
    # weights = [players.get_salary(n) for n in names]
    #
    # if args.knapsack:
    #     knapsack = ModifiedKnapsack(names, classes, values, weights, CAPACITY, TEAM_COMP)
    #    #knapsack.find_solution()
    #
    # if args.mcmc:
    #     mcmc = TeamMCMC(names, classes, values, weights, CAPACITY, TEAM_COMP)
    #     mcmc.find_simulated_annealing_solution()

    player_stats = PlayerStats(args.stats)
    ballpark_stats = BallparkStats(args.stats)
    team_stats = TeamStats(args.stats)
    league_stats = LeagueStats(args.stats)

    # start computing some stats here
    eq = StatEquations(player_stats, team_stats, ballpark_stats, league_stats)

    names = ['felix hernandez',
     'ubaldo jimenez',
     'cliff lee']
    for n in names:
        print n, eq.points_expected_for_k(n)



if __name__ == '__main__':
    main()
