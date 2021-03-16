import csv

from src.common.player import Player

RANKING_WEIGHT = {
    "S": 9,
    "A": 7,
    "B": 5,
    "C": 3,
    "D": 1,
    "N/A (Haven't played with them enough)": None,
    "": None
}


# creates the players dict/list
def parse_players(file):
    csv_reader = csv.reader(file)
    players_list = next(csv_reader)[1:]
    return players_list


# takes in a player list and updates it with rankings
def parse_rankings(file, players_list, order=False):
    csv_reader = csv.reader(file)
    players_map = dict(zip(players_list, [Player(name=player) for player in players_list]))

    for ratings_row in csv_reader:
        # Column 1 is the timestamp value
        # Update player mapping with weighted score for each letter rank
        for col_idx, rating in enumerate(ratings_row[1:]):
            if RANKING_WEIGHT[rating] is not None:
                players_map[players_list[col_idx]].ratings.append(RANKING_WEIGHT[rating])

    if order:
        return _ordered_tuple_from(players_map)
    else:
        return players_map


# updates players_map with preferences
# file must roles listed as follows: "top,jng,mid,bot,sup"
def parse_preferred_roles(file, players_map={}):
    csv_reader = csv.reader(file)
    # check each row in column 1. if cell in column 1 contains name that exists among the map's keys, then go thru
    # the next 3 columns for preffs and add them to that key
    # next() is just to skip the first line
    next(csv_reader)
    for ratings_column in csv_reader:
        # just a sampler for testing
        # if len(ratings_column[0]):
        #    print(ratings_column[0], ratings_column[1], ratings_column[2], ratings_column[3])

        # len() to skip over empty lines in the csv
        if len(ratings_column[0]):
            for k, v in players_map.items():
                if k.__contains__(ratings_column[0]):
                    # the following 3 lines are written 2 diff ways but the end result is the same
                    v.pref1 = ratings_column[1]
                    players_map[k].pref2 = ratings_column[2]
                    players_map[k].pref3 = ratings_column[3]

    if not are_roles_filled(players_map):
        print("There might be a Player missing roles.")


# [currently not working] function to make sure no roles are missing at the end of parse_preferred_roles() function
def are_roles_filled(players_map):
    for k, v in players_map.items():
        if not v.pref1 or not v.pref2 or not v.pref3:
            print(v)
            return False
        else:
            return True


def _ordered_tuple_from(rankings_map):
    rankings_tuple = [(k, v) for k, v in rankings_map.items()]
    rankings_tuple.sort(key=lambda x: x[1], reverse=True)

    return rankings_tuple