from __future__ import annotations

import statistics
from typing import List

from django.contrib.auth.models import AbstractUser

from common.api.enums import GAME_OPTIONS
from rankings.models import RANKING_WEIGHT, RankingType
from roles.models import LEAGUE_ROLE, ROLE_MULTIPLIER


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
    def _league_rankings(self) -> List[int]:
        return [
            RANKING_WEIGHT[ranking[0]]
            for ranking in self.rankings.filter(
                ranking_type=RankingType.objects.get(value=GAME_OPTIONS.LEAGUE.value)
            ).values_list("ranking__value")
        ]

    @property
    def primary_summoner_name(self):
        if not self.summoner_set.exists():
            return self.username
        else:
            return self.summoner_set.first().in_game_name

    def visualize_league_ranking(self, rankings=None):
        rankings = self._league_rankings() if rankings is None else rankings

        name = f"{self.summoner_set.first().in_game_name}: "
        avg = f"avg={self.average_league_ranking(rankings=rankings)}. "
        std_dev = f"std_dev={std_dev_from(rankings)}. "
        avg_with_std_dev = f"avg_with_std_dev: {self._average_league_ranking_adjusted(rankings=rankings)}. "
        ratings = f"ratings={rankings}"

        return f"{name}{avg_with_std_dev}{avg}{std_dev}{ratings}"

    def average_league_ranking(self, rankings=None) -> float:
        rankings = self._league_rankings() if rankings is None else rankings

        return average_from(rankings)

    # Internal utility to avoid recomputes
    def _average_league_ranking_adjusted(self, rankings=None):
        rankings = self._league_rankings() if rankings is None else rankings

        if len(rankings) == 0:
            return 0
        else:
            std_dev = std_dev_from(rankings)
            unfiltered_average = average_from(rankings)
            lower_bound = unfiltered_average - std_dev
            upper_bound = unfiltered_average + std_dev

            filtered_ratings = [ranking for ranking in rankings if (upper_bound >= ranking >= lower_bound)]
            return round(sum(filtered_ratings) / len(filtered_ratings), 2)

    @property
    def average_league_ranking_adjusted(self):
        rankings = self._league_rankings()

        if len(rankings) == 0:
            return 0
        else:
            std_dev = std_dev_from(rankings)
            unfiltered_average = average_from(rankings)
            lower_bound = unfiltered_average - std_dev
            upper_bound = unfiltered_average + std_dev

            filtered_ratings = [ranking for ranking in rankings if (upper_bound >= ranking >= lower_bound)]
            return round(sum(filtered_ratings) / len(filtered_ratings), 2)

    def preference_for_league_role(self, role: LEAGUE_ROLE):
        if not hasattr(self, "league_role_preferences"):
            return None

        if self.league_role_preferences.primary_role.value == role.value:
            role_type_for_user = "primary"
        elif self.league_role_preferences.secondary_role.value == role.value:
            role_type_for_user = "secondary"
        elif self.league_role_preferences.off_role.value == role.value:
            role_type_for_user = "off"
        else:
            role_type_for_user = None

        return role_type_for_user

    def average_league_ranking_adjusted_for_role(self, role: LEAGUE_ROLE):
        return round(self.average_league_ranking_adjusted * ROLE_MULTIPLIER[self.preference_for_league_role(role)], 1)
