# builder itself
# 2 priorities: team balance 1st, then role preference
from src.team_builder.team import Team
from src.common.player import Player
import random

def are_teams_balanced(team_a, team_b):
    # using 4 for now, but can make it tighter tolerance in future
    return team_a.total_rating() - team_b.total_rating() <= 4


# def swap(team_a, team_b):
#     if team_a.get_rating() > team_b.get_rating():
#         get highest rated player
#         swap at role
#     else:
#         get highest rated player
#         swap at role


# method to add a random player from the players list (of 10 or more) and removes chosen player from the list
def add(team, list):
    chosen_player = random.choice(list)
    team.add_player(chosen_player)
    list.remove(chosen_player)


def run():
    # teamA = Team("A")
    # teamB = Team("B")
    #
    # kevin = Player("th3crimsonchin", "top", "mid", "bot")
    # karim = Player("vit", "bot", "sup", "jng")
    # selim = Player("phaketoh", "bot", "top", "mid")
    # darren = Player("zero waste", "sup", "mid", "top")
    # rami = Player("pobu", "mid", "jng", "bot")
    #
    # players: list = [kevin, karim, selim, darren]
    # add(teamA, players)
    # add(teamB, players)
    # add(teamA, players)
    # add(teamB, players)
    print("Hello world")

# while True:
#     swap(teamA, teamB)
#
#     if are_teams_balanced(teamA, teamB) and teamA.is_team_full() and teamB.is_team_full():
#         break




if __name__ == "__main__":
    run()



