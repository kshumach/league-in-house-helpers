import click
import csv
import statistics
from dataclasses import dataclass, field


@dataclass
class Player:
    name: str = ""
    ratings: list = field(default_factory=list)

    def average_rating(self):
        if len(self.ratings) == 0:
            return 0
        else:
            return round(sum(self.ratings) / len(self.ratings), 2)

    def average_rating_within_std_dev(self):
        if len(self.ratings) == 0:
            return 0
        else:
            std_dev = self.std_dev()
            unfiltered_average = self.average_rating()
            lower_bound = unfiltered_average - std_dev
            upper_bound = unfiltered_average + std_dev

            filtered_ratings = [rating for rating in self.ratings if (upper_bound >= rating >= lower_bound)]
            return round(sum(filtered_ratings) / len(filtered_ratings), 2)

    def std_dev(self):
        return statistics.stdev(self.ratings)

    def __lt__(self, other):
        return self.average_rating_within_std_dev() < other.average_rating_within_std_dev()

    def __repr__(self):
        name = f"{self.name}: "
        avg = f"avg={self.average_rating()}. "
        std_dev = f"std_dev={self.std_dev()}. "
        avg_with_std_dev = f"avg_with_std_dev: {self.average_rating_within_std_dev()}. "
        ratings = f"ratings={self.ratings}"
        return f"{name}{avg_with_std_dev}{avg}{std_dev}{ratings}"


RANKING_WEIGHT = {
    "S": 9,
    "A": 7,
    "B": 5,
    "C": 3,
    "D": 1,
    "N/A (Haven't played with them enough)": None,
    "": None
}

"""
Script to calculate average scores for each player based off a csv of ratings provided.

Use like so on a command line interface

> python src/rankings_parser/main.py --file /path/to/csv/file --ordered
"""
@click.command()
@click.option('--file', type=click.File(), help="CSV file of rankings.", required=True)
def parse_rankings(file):
    csv_reader = csv.reader(file)
    players_list = next(csv_reader)[1:]
    players_map = dict(zip(players_list, [Player(name=player) for player in players_list]))

    for ratings_row in csv_reader:
        # Column 1 is the timestamp value
        # Update player mapping with weighted score for each letter rank
        for col_idx, rating in enumerate(ratings_row[1:]):
            if RANKING_WEIGHT[rating] is not None:
                players_map[players_list[col_idx]].ratings.append(RANKING_WEIGHT[rating])

    click.secho("Ordered average rankings", fg='green')
    for _, player_class in _ordered_tuple_from(players_map):
        click.secho(str(player_class), fg='blue')


def _ordered_tuple_from(rankings_map):
    rankings_tuple = [(k, v) for k, v in rankings_map.items()]
    rankings_tuple.sort(key=lambda x: x[1], reverse=True)

    return rankings_tuple


if __name__ == "__main__":
    parse_rankings()
