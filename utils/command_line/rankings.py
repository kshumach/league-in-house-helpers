import click

from rankings_parser import parse_rankings

"""
Script to calculate average scores for each player based off a csv of ratings provided.

Use like so on a command line interface

> python src/rankings_parser/parser.py --file /path/to/csv/file --ordered
"""


@click.command()
@click.option("--file", type=click.File(), help="CSV file of rankings.", required=True)
def parse_rankings_for_file(file):
    rankings = parse_rankings(file, order=True)

    click.secho("Ordered average rankings", fg="green")
    for _, player_class in rankings:
        click.secho(str(player_class), fg="blue")


def _ordered_tuple_from(rankings_map):
    rankings_tuple = [(k, v) for k, v in rankings_map.items()]
    rankings_tuple.sort(key=lambda x: x[1], reverse=True)

    return rankings_tuple


if __name__ == "__main__":
    parse_rankings_for_file()
