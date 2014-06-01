#!/usr/bin/env python

import argparse
from player_salary_scores import PlayerSalaryScores
from knapsack import ModifiedKnapsack

CAPACITY = 30000
RESTRICTIONS = {'P': 1,
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
    args = parser.parse_args()

    players = PlayerSalaryScores()
    players.read_positions_and_salaries(args.salaries)
    players.add_fake_scores()

    names = players.get_names()
    classes = [players.get_position(n) for n in names]
    values = [players.get_score(n) for n in names]
    weights = [players.get_salary(n) for n in names]
    knapsack = ModifiedKnapsack(names, classes, values, weights, CAPACITY, RESTRICTIONS)

    knapsack.find_solution()

if __name__ == '__main__':
    main()
