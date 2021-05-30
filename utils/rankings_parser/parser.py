import csv
from dataclasses import dataclass, field
from users.models import average_from, std_dev_from

RANKING_WEIGHT = {"S": 9, "A": 7, "B": 5, "C": 3, "D": 1, "N/A (Haven't played with them enough)": None, "": None}

"""
This is mainly a utility wrapper for running this locally without the need for a database connection.

The interface is consumed by `command_line.rankings.py`.
"""


@dataclass
class Player:
    name: str = ""
    ratings: list = field(default_factory=list)

    def average_rating_within_std_dev(self):
        ratings = self.ratings

        if len(ratings) == 0:
            return 0
        else:
            std_dev = std_dev_from(ratings)
            unfiltered_average = average_from(ratings)
            lower_bound = unfiltered_average - std_dev
            upper_bound = unfiltered_average + std_dev

            filtered_ratings = [rating for rating in ratings if (upper_bound >= rating >= lower_bound)]
            return round(sum(filtered_ratings) / len(filtered_ratings), 2)

    def __lt__(self, other):
        return self.average_rating_within_std_dev() < other.average_rating_within_std_dev()

    def __repr__(self):
        ratings = self.ratings

        name = f"{self.name}: "
        avg = f"avg={average_from(ratings)}. "
        std_dev = f"std_dev={std_dev_from(ratings)}. "
        avg_with_std_dev = f"avg_with_std_dev: {self.average_rating_within_std_dev()}. "
        ratings = f"ratings={ratings}"
        return f"{name}{avg_with_std_dev}{avg}{std_dev}{ratings}"


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
