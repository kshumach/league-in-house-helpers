import click
import csv

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
@click.option('--ordered', is_flag=True, default=False)
def parse_rankings(ordered, file):
    csv_reader = csv.reader(file)
    players_list = next(csv_reader)[1:]
    player_rankings_map = dict(zip(players_list, [[] for _ in players_list]))

    for ratings_row in csv_reader:
        # Column 1 is the timestamp value
        # Update player mapping with weighted score for each letter rank
        for col_idx, rating in enumerate(ratings_row[1:]):
            player_rankings_map[players_list[col_idx]].append(RANKING_WEIGHT[rating])

    # Filter out non letter ratings, and average them out for each player
    for player, ratings in player_rankings_map.items():
        filtered_ratings = [rating for rating in ratings if rating is not None]
        player_rankings_map[player] = round(sum(filtered_ratings) / len(filtered_ratings), 2)

    # If ordered is requested, we convert to a list of tuples, and order by average score
    if ordered:
        click.secho("Ordered average rankings", fg='green')
        for p, r in _ordered_tuple_from(player_rankings_map):
            click.secho(f"{p}: {r}", fg='blue')
    else:
        click.secho("Average rankings", fg='green')
        click.secho(str(player_rankings_map), fg='blue')


def _ordered_tuple_from(rankings_map):
    rankings_tuple = [(k, v) for k, v in rankings_map.items()]
    rankings_tuple.sort(key=lambda x: x[1], reverse=True)

    return rankings_tuple


if __name__ == "__main__":
    parse_rankings()
