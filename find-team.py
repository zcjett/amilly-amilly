#!/usr/bin/env python

import argparse
import csv
import sys
from random import randint, choice

def clean_name(name):
    # Returns a tuple (name, status) where status is "DL" or None
    if name.endswith('DL'):
        return name.lower()[:-2], 'DL'
    elif name.endswith('P'):
        return name.lower()[:-1], None
    else:
        return name.lower(), None


def clean_salary(salary):
    # Returns a numerical value for the given salary string
    return int(salary.strip().replace('$', '').replace(',', ''))


def parse_salaries(infile):
    reader = csv.reader(open(infile), quotechar='"')
    salaries = []
    for line in reader:
        # Sample entry:  OF,Colby RasmusDL,2.3,37,TAM@TOR,"$3,500 ",Add
        position = line[0]
        player, status = clean_name(line[1])
        salary = clean_salary(line[5])
        salaries.append((player, position, salary, status))
    return salaries


def fake_score(position):
    if position == 'P':
        return randint(5, 20) + choice([0.0, 0.33, 0.66])
    else:
        return randint(-1, 10) + choice([0.0, 0.25, 0.5, 0.75])


def main(argv):
    parser = argparse.ArgumentParser(description='Find dat team.')
    parser.add_argument('salaries', help='File containing player salaries.')
    parser.add_argument('projections', help='File containing projected points.')
    args = parser.parse_args()

    salaries = parse_salaries(args.salaries)

    projections = [(name, fake_score(pos)) for name, pos, salary, status in salaries]


if __name__ == '__main__':
    main(sys.argv)
