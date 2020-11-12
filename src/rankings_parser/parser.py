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


def parse_rankings(file, order=False):
    csv_reader = csv.reader(file)
    players_list = next(csv_reader)[1:]
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


def _ordered_tuple_from(rankings_map):
    rankings_tuple = [(k, v) for k, v in rankings_map.items()]
    rankings_tuple.sort(key=lambda x: x[1], reverse=True)

    return rankings_tuple
