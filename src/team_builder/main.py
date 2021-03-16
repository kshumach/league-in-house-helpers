# import src.rankings_parser.parser as parser
from src.rankings_parser.parser import parse_rankings, parse_players, parse_preferred_roles
from src.team_builder.team import Team
from src.common.player import Player
import random


# builder itself
# 2 priorities: team balance 1st, then role preference

def are_teams_balanced(team_a, team_b):
    # using 4 for now, but can make it tighter tolerance in future
    return abs(team_a.get_rating() - team_b.get_rating()) <= 4


def swap(teamA, teamB):
    playerA = teamA.get_highest_rated_player()
    playerB = teamB.get_highest_rated_player()
    teamA.members.remove(playerA)
    teamB.members.remove(playerB)
    teamA.reshuffle()
    teamB.reshuffle()
    teamA.add_player(playerB)
    teamB.add_player(playerA)
    teamA.reshuffle()
    teamB.reshuffle()


# method to add a random player from the players map (of 10 or more) and then deletes chosen player from the map
def add(team, dict):
    chosen_player = random.choice(list(dict.values()))
    team.add_player(chosen_player)
    del dict[chosen_player.name]


def run():
    teamA = Team("A")
    teamB = Team("B")

    with open("C:\\Users\\Selim\\PycharmProjects\\league-in-house-helpers\\src\\team_builder\\rankings.csv") as file:
        list = parse_players(file)
        players_map = parse_rankings(file, list)
        # print(players_map)
        # print(players_map.__repr__())
        # print([(k, str(v)) for k, v in players_map.items()])

    with open("C:\\Users\\Selim\\PycharmProjects\\league-in-house-helpers\\src\\team_builder\\preffs.csv") as file:
        parse_preferred_roles(file, players_map)

    add(teamA, players_map)
    add(teamB, players_map)
    add(teamA, players_map)
    add(teamB, players_map)
    add(teamA, players_map)
    add(teamB, players_map)
    add(teamA, players_map)
    add(teamB, players_map)
    add(teamA, players_map)
    add(teamB, players_map)

    infinite_loop_helper: int = 0

    while True:

        # swap function needs work so I've put this as a failsafe
        if infinite_loop_helper == 10:
            print("I looped 10 times, that's enough for me.")
            print("Here's the best I could do:")
            print(teamA)
            print(f' Team Rating: {teamA.get_rating()}')
            print()
            print(teamB)
            print(f' Team Rating: {teamB.get_rating()}')
            break

        # if teams are balanced & full then prints each team composition with their rating
        if are_teams_balanced(teamA, teamB) and teamA.is_team_full() and teamB.is_team_full():
            print(teamA)
            print(f' Team Rating: {teamA.get_rating()}')
            print()
            print(teamB)
            print(f' Team Rating: {teamB.get_rating()}')
            break

        # if teams are unbalanced then uses swap function to try to balance
        if not are_teams_balanced(teamA, teamB):
            swap(teamA, teamB)
            print('\n Re-balancing teams... \n')

        infinite_loop_helper = infinite_loop_helper + 1


if __name__ == "__main__":
    run()
