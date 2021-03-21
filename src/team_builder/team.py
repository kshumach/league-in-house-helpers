import random


class TeamFullException(Exception):
    def __init__(self, name):
        self.message = f"Team {name} is full!"


class Team:
    def __init__(self, name):
        self.name = name

        self.assignments = {
            "top": None,
            "jng": None,
            "mid": None,
            "bot": None,
            "sup": None,
        }

        self.members: list = []

    # adds a player to the members list, order irrelevant for now
    def add_player(self, player):
        if not self.is_team_full():
            self.members.append(player)
        else:
            raise TeamFullException(self.name)

    def assign_roles(self):
        random.shuffle(self.members)

        for player in self.members:
            self._add_pref_1(player)

    def get_rating(self):
        total_rating: int = 0

        for role, player in self.assignments.items():
            total_rating = (player.average_rating_within_std_dev() * player.rating_modifier_for_role(role)) + total_rating

        return total_rating

    def get_player_rating(self):
        # indiv for role
        pass

    # if there's more than 1 player tied for the highest rating it will just return 1 of them
    def get_highest_rated_player(self):
        return sorted(self.members, key=lambda player: player.average_rating_within_std_dev())[-1]

    def is_team_full(self):
        return len(self.members) == 5

    # can add showing the rating in this string
    def __str__(self):
        team_name = self.name
        top = self._print_player_rating(self.assignments["top"], "top")
        jng = self._print_player_rating(self.assignments["jng"], "jng")
        mid = self._print_player_rating(self.assignments["mid"], "mid")
        bot = self._print_player_rating(self.assignments["bot"], "bot")
        sup = self._print_player_rating(self.assignments["sup"], "sup")

        return f'Team {team_name}\n-------\n Top: {top} \n Jungle: {jng} \n Mid: {mid} \n Bot: {bot} \n Support: {sup}'

    # adds player's first preference. Note the ELSE statement at the end
    def _add_pref_1(self, player):
        if player.pref1 == "top" and not self.assignments["top"]:
            self.assignments["top"] = player
        elif player.pref1 == "jng" and not self.assignments["jng"]:
            self.assignments["jng"] = player
        elif player.pref1 == "mid" and not self.assignments["mid"]:
            self.assignments["mid"] = player
        elif player.pref1 == "bot" and not self.assignments["bot"]:
            self.assignments["bot"] = player
        elif player.pref1 == "sup" and not self.assignments["sup"]:
            self.assignments["sup"] = player
        else:
            self._add_pref2(player)

    def _add_pref2(self, player):
        if player.pref2 == "top" and not self.assignments["top"]:
            self.assignments["top"] = player
        elif player.pref2 == "jng" and not self.assignments["jng"]:
            self.assignments["jng"] = player
        elif player.pref2 == "mid" and not self.assignments["mid"]:
            self.assignments["mid"] = player
        elif player.pref2 == "bot" and not self.assignments["bot"]:
            self.assignments["bot"] = player
        elif player.pref2 == "sup" and not self.assignments["sup"]:
            self.assignments["sup"] = player
        else:
            self._add_pref3(player)

    def _add_pref3(self, player):
        if player.pref3 == "top" and not self.assignments["top"]:
            self.assignments["top"] = player
        elif player.pref3 == "jng" and not self.assignments["jng"]:
            self.assignments["jng"] = player
        elif player.pref3 == "mid" and not self.assignments["mid"]:
            self.assignments["mid"] = player
        elif player.pref3 == "bot" and not self.assignments["bot"]:
            self.assignments["bot"] = player
        elif player.pref3 == "sup" and not self.assignments["sup"]:
            self.assignments["sup"] = player
        else:
            self._add_into_wtv_empty_role(player)

    def _add_into_wtv_empty_role(self, player):
        if not self.assignments["top"]:
            self.assignments["top"] = player
        elif not self.assignments["jng"]:
            self.assignments["jng"] = player
        elif not self.assignments["mid"]:
            self.assignments["mid"] = player
        elif not self.assignments["bot"]:
            self.assignments["bot"] = player
        elif not self.assignments["sup"]:
            self.assignments["sup"] = player
        else:
            pass

    def _print_player_rating(self, player, role):
        if player is None:
            return "Not Assigned"
        else:
            return player.print_rating_for_role(role)
