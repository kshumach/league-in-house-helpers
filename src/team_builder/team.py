# not sure how to import list from excel
from src.common.player import Player
import random

class Team:

    def __init__(self, name):
        self.name = name

        self.top: str = ""
        self.jng: str = ""
        self.mid: str = ""
        self.bot: str = ""
        self.sup: str = ""
        self.members: list = []
        # members list is just for counting

    # returns amount of roles filled so far
    def roles_filled(self):
        roles_filled: int = 0
        for x in self.members:
            if x:
                roles_filled += 1
        return roles_filled

    # adds a player to the members list, order irrelevant for now
    def add_player(self, player):
        if not self.is_team_full():
            self.members.append(player)
            self.add_pref1(player)

    # reshuffles a full team. trying to sort them into their ideal roles once again
    def reshuffle(self):
        self.top = ""
        self.jng = ""
        self.mid = ""
        self.bot = ""
        self.sup = ""
        random.shuffle(self.members)
        for x in self.members:
            self.add_pref1(x)

    # adds player's first preference. Note the ELSE statement at the end
    def add_pref1(self, player):
        if player.pref1 == "top" and not self.top:
            self.top = player.name
        elif player.pref1 == "jng" and not self.jng:
            self.jng = player.name
        elif player.pref1 == "mid" and not self.mid:
            self.mid = player.name
        elif player.pref1 == "bot" and not self.bot:
            self.bot = player.name
        elif player.pref1 == "sup" and not self.sup:
            self.sup = player.name
        else:
            self.add_pref2(player)

    def add_pref2(self, player):
        if player.pref2 == "top" and not self.top:
            self.top = player.name
        elif player.pref2 == "jng" and not self.jng:
            self.jng = player.name
        elif player.pref2 == "mid" and not self.mid:
            self.mid = player.name
        elif player.pref2 == "bot" and not self.bot:
            self.bot = player.name
        elif player.pref2 == "sup" and not self.sup:
            self.sup = player.name
        else:
            self.add_pref3(player)

    def add_pref3(self, player):
        if player.pref3 == "top" and not self.top:
            self.top = player.name
        elif player.pref3 == "jng" and not self.jng:
            self.jng = player.name
        elif player.pref3 == "mid" and not self.mid:
            self.mid = player.name
        elif player.pref3 == "bot" and not self.bot:
            self.bot = player.name
        elif player.pref3 == "sup" and not self.sup:
            self.sup = player.name
        else:
            self.add_into_wtv_empty_role(player)

    def add_into_wtv_empty_role(self, player):
        if not self.top:
            self.top = player.name
        elif not self.jng:
            self.jng = player.name
        elif not self.mid:
            self.mid = player.name
        elif not self.bot:
            self.bot = player.name
        elif not self.sup:
            self.sup = player.name
        else:
            print("This team " + self.name + " is full! add_player can't work")

    def get_rating(self):
        total_rating: int = 0
        for x in self.members:
            total_rating = x.average_rating_within_std_dev() + total_rating
        return total_rating

    def get_player_rating(self):
        # indiv for role
        pass

    # if there's more than 1 player tied for the highest rating it will just return 1 of them
    def get_highest_rated_player(self):
        highest_rating: int = 0
        player_to_be_returned = Player()
        for x in self.members:
            if highest_rating < x.average_rating_within_std_dev():
                highest_rating = x.average_rating_within_std_dev()
                player_to_be_returned = x
        return player_to_be_returned

    def is_team_full(self):
        return len(self.members) == 5

    # can add showing the rating in this string
    def __str__(self):
        return f'Team {self.name}\n-------\n Top: {self.top} \n Jungle: {self.jng} \n Mid: {self.mid} \n Bot: {self.bot} \n Support: {self.sup}'
