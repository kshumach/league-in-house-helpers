from src.rankings_parser.parser import parse_rankings, parse_players, parse_preferred_roles
from src.team_builder.team import Team
import random
import click


def are_teams_balanced(team_a, team_b):
    # using 4 for now, but can make it tighter tolerance in future
    return abs(team_a.get_rating() - team_b.get_rating()) <= 4


def swap(team_a, team_b):
    playerA = team_a.get_highest_rated_player()
    playerB = team_b.get_highest_rated_player()
    team_a.members.remove(playerA)
    team_b.members.remove(playerB)
    team_a.assign_roles()
    team_b.assign_roles()
    team_a.add_player(playerB)
    team_b.add_player(playerA)
    team_a.assign_roles()
    team_b.assign_roles()


# method to add a random player from the players map (of 10 or more) and then deletes chosen player from the map
def add(team, dict):
    chosen_player = random.choice(list(dict.values()))
    team.add_player(chosen_player)
    del dict[chosen_player.name]


@click.command()
@click.option('--rankings-file', type=click.File(), help="CSV file of rankings.", required=True)
@click.option('--roles-file', type=click.File(), help="CSV file of preferred roles.", required=True)
def run(roles_file, rankings_file):
    team_a = Team("A")
    team_b = Team("B")

    players = parse_players(rankings_file)
    players_map = parse_rankings(rankings_file, players)

    parse_preferred_roles(roles_file, players_map)

    add(team_a, players_map)
    add(team_b, players_map)
    add(team_a, players_map)
    add(team_b, players_map)
    add(team_a, players_map)
    add(team_b, players_map)
    add(team_a, players_map)
    add(team_b, players_map)
    add(team_a, players_map)
    add(team_b, players_map)

    team_a.assign_roles()
    team_b.assign_roles()

    infinite_loop_helper: int = 0

    while True:
        # swap function needs work so I've put this as a failsafe
        if infinite_loop_helper == 10:
            print("I looped 10 times, that's enough for me.")
            print("Here's the best I could do:")
            print(team_a)
            print(f' Team Rating: {team_a.get_rating()}')
            print()
            print(team_b)
            print(f' Team Rating: {team_b.get_rating()}')
            break

        # if teams are balanced & full then prints each team composition with their rating
        if are_teams_balanced(team_a, team_b) and team_a.is_team_full() and team_b.is_team_full():
            print(team_a)
            print(f' Team Rating: {team_a.get_rating()}')
            print()
            print(team_b)
            print(f' Team Rating: {team_b.get_rating()}')
            break

        # if teams are unbalanced then uses swap function to try to balance
        if not are_teams_balanced(team_a, team_b):
            swap(team_a, team_b)
            print('\n Re-balancing teams... \n')

        infinite_loop_helper = infinite_loop_helper + 1


if __name__ == "__main__":
    run()
