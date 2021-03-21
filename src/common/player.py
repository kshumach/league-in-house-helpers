import statistics
from dataclasses import dataclass, field


@dataclass
class Player:
    name: str = ""
    pref1: str = ""
    pref2: str = ""
    pref3: str = ""
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

    def rating_modifier_for_role(self, role):
        if role == self.pref1:
            return 1

        if role == self.pref2:
            return 0.8

        if role == self.pref3:
            return 0.6

        return 0.3

    def print_rating_for_role(self, role):
        original_rating = self.average_rating_within_std_dev()
        rating = original_rating * self.rating_modifier_for_role(role)
        name = self.name

        return f"name:{name}, original_rating: {original_rating}, modified_rating: {rating}"

    def std_dev(self):
        return statistics.stdev(self.ratings)

    def __lt__(self, other):
        return self.average_rating_within_std_dev() < other.average_rating_within_std_dev()

    def __str__(self):
        name = f"{self.name}: "
        pref1 = f"pref1 = {self.pref1}. "
        pref2 = f"pref2 = {self.pref2}. "
        pref3 = f"pref3 = {self.pref3}. "
        avg = f"avg={self.average_rating()}. "
        std_dev = f"std_dev={self.std_dev()}. "
        avg_with_std_dev = f"avg_with_std_dev: {self.average_rating_within_std_dev()}. "
        ratings = f"ratings={self.ratings}"
        return f"{name}{avg_with_std_dev}{avg}{std_dev}{ratings}"
