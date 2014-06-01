#!/usr/bin/env python

import argparse
from player_salary_scores import PlayerSalaryScores

def main():
    parser = argparse.ArgumentParser(description='Find dat team.')
    parser.add_argument('salaries', help='File containing player salaries and positions.')
    parser.add_argument('projections', help='File containing projected points.')
    args = parser.parse_args()

    players = PlayerSalaryScores()

    players.read_positions_and_salaries(args.salaries)
    players.add_fake_scores()

    positions = set()
    for name in players.get_names():
        positions.add(players.get_position(name))

    for pos in positions:
        print pos, len(players.get_names(position=pos))


if __name__ == '__main__':
    main()
