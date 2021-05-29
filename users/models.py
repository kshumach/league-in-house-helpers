from __future__ import annotations

import statistics
from typing import List

from django.contrib.auth.models import AbstractUser

from rankings.models import RANKING_WEIGHT


def average_from(values) -> float:
    if len(values) == 0:
        return 0
    else:
        return round(sum(values) / len(values), 2)


def std_dev_from(values) -> float:
    if len(values) < 2:
        return 0

    return statistics.stdev(values)


class User(AbstractUser):
    def _rankings(self) -> List[int]:
        return [RANKING_WEIGHT[ranking[0]] for ranking in self.rankings.values_list('ranking__value')]

    @property
    def primary_summoner_name(self):
        if not self.summoner_set.exists():
            return None
        else:
            return self.summoner_set.first().in_game_name

    """
    Utility method to compare rankings of users.
    
    Compares values rounded to 1 decimal place. Higher precision doesn't really make a difference.
    
    Returns 0 if values are equal.
    Returns 1 if this user has a higher ranking.
    Returns -1 if this user has a lower ranking.
    """
    def compare_ranking_to(self, other: User) -> int:
        this_user_ranking = round(self.average_ranking_adjusted(), 1)
        other_user_ranking = round(other.average_ranking_adjusted(), 1)

        if this_user_ranking == other_user_ranking:
            return 0
        elif this_user_ranking > other_user_ranking:
            return 1
        else:
            return 0

    def visualize_ranking(self, rankings=None):
        rankings = self._rankings() if rankings is None else rankings

        name = f"{self.summoner_set.first().in_game_name}: "
        avg = f"avg={self.average_ranking(rankings=rankings)}. "
        std_dev = f"std_dev={std_dev_from(rankings)}. "
        avg_with_std_dev = f"avg_with_std_dev: {self.average_ranking_adjusted(rankings=rankings)}. "
        ratings = f"ratings={rankings}"

        return f"{name}{avg_with_std_dev}{avg}{std_dev}{ratings}"

    def average_ranking(self, rankings=None) -> float:
        rankings = self._rankings() if rankings is None else rankings

        return average_from(rankings)

    @property
    def average_ranking_adjusted(self, rankings=None):
        rankings = self._rankings() if rankings is None else rankings

        if len(rankings) == 0:
            return 0
        else:
            std_dev = std_dev_from(rankings)
            unfiltered_average = average_from(rankings)
            lower_bound = unfiltered_average - std_dev
            upper_bound = unfiltered_average + std_dev

            filtered_ratings = [ranking for ranking in rankings if (upper_bound >= ranking >= lower_bound)]
            return round(sum(filtered_ratings) / len(filtered_ratings), 2)
