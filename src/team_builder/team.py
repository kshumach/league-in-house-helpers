# not sure how to import list from excel

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

        adder: int = 0
        for x in self.members:
            adder += x.average_rating
        self.totalRating = adder

    # returns amount of roles filled so far
    def roles_filled(self):
        roles_filled: int = 0
        members_list: list = [self.top, self.jng, self.mid, self.bot, self.sup]
        for x in members_list:
            if not (x.isEmpty()):
                roles_filled += 1
        return roles_filled

    # adds a player to the members list, order irrelevant for now
    def add_player(self, player):
        if not (self.is_team_full()):
            self.members.append(player)
            self.add_pref1(player)

    # adds player's first preference. Not sure about this ELSE statement
    def add_pref1(self, player):
        if player.pref1.equals("top") and self.top.isEmpty():
            self.top = player.name
        elif player.pref1.equals("jng") and self.jng.isEmpty():
            self.jng = player.name
        elif player.pref1.equals("mid") and self.mid.isEmpty():
            self.mid = player.name
        elif player.pref1.equals("bot") and self.bot.isEmpty():
            self.bot = player.name
        elif player.pref1.equals("sup") and self.sup.isEmpty():
            self.sup = player.name
        else:
            self.add_pref2(player)

    def add_pref2(self, player):
        if player.pref2.equals("top") and self.top.isEmpty():
            self.top = player.name
        elif player.pref2.equals("jng") and self.jng.isEmpty():
            self.jng = player.name
        elif player.pref2.equals("mid") and self.mid.isEmpty():
            self.mid = player.name
        elif player.pref2.equals("bot") and self.bot.isEmpty():
            self.bot = player.name
        elif player.pref2.equals("sup") and self.sup.isEmpty():
            self.sup = player.name
        else:
            self.add_pref3(player)

    def add_pref3(self, player):
        if player.pref3.equals("top") and self.top.isEmpty():
            self.top = player.name
        elif player.pref3.equals("jng") and self.jng.isEmpty():
            self.jng = player.name
        elif player.pref3.equals("mid") and self.mid.isEmpty():
            self.mid = player.name
        elif player.pref3.equals("bot") and self.bot.isEmpty():
            self.bot = player.name
        elif player.pref3.equals("sup") and self.sup.isEmpty():
            self.sup = player.name
        else:
            self.add_into_wtv_empty_role(player)

    def add_into_wtv_empty_role(self, player):
        if self.top.isEmpty():
            self.top = player.name
        elif self.jng.isEmpty():
            self.jng = player.name
        elif self.jng.isEmpty():
            self.jng = player.name
        elif self.bot.isEmpty():
            self.bot = player.name
        elif self.bot.isEmpty():
            self.sup = player.name
        else:
            print("This team " + self.name + " is full! add_player can't work")

    def get_rating(self):
        # avg of rating
        return self.totalRating

    def get_player_rating(self):
        #indiv for role
        pass

    def get_highest_rated_player(self):
        highest_rating: int = 0
        # new Player =
        for x in self.members:
            if highest_rating < x.average_rating_within_std_dev:
                highest_rating = x.average_rating

        return highest_rating

    def is_team_full(self):
        return len(self.members) == 5

    # can add showing the rating in this string
    def __str__(self):
        return f'Top: {self.top}/n Jungle: {self.jng}/n Mid: {self.mid}/n Bot: {self.bot}/n Support: {self.sup}'
