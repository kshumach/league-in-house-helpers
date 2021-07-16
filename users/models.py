from __future__ import annotations

import statistics
from typing import List, Union

from django.contrib.auth.models import AbstractUser

from common.api.enums import GAME_OPTIONS, FLOAT_ROLE
from rankings.models import RANKING_WEIGHT, RankingType
from roles.models import LEAGUE_ROLE, ROLE_MULTIPLIER, VALORANT_ROLE


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

    def _valorant_rankings(self) -> List[int]:
        return [
            RANKING_WEIGHT[ranking[0]]
            for ranking in self.rankings.filter(
                ranking_type=RankingType.objects.get(value=GAME_OPTIONS.VALORANT.value)
            ).values_list("ranking__value")
        ]

    @property
    def primary_summoner_name(self):
        if not self.summoner_set.exists():
            return self.username
        else:
            return self.summoner_set.first().in_game_name

    @property
    def primary_valorant_name(self):
        if not self.valorantaccount_set.exists():
            return self.username
        else:
            first_account = self.valorantaccount_set.first()
            return f"{first_account.in_game_name}#{first_account.tag_line}"

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

    @property
    def average_valorant_ranking_adjusted(self):
        rankings = self._valorant_rankings()

        if len(rankings) == 0:
            return 0
        else:
            std_dev = std_dev_from(rankings)
            unfiltered_average = average_from(rankings)
            lower_bound = unfiltered_average - std_dev
            upper_bound = unfiltered_average + std_dev

            filtered_ratings = [ranking for ranking in rankings if (upper_bound >= ranking >= lower_bound)]
            return round(sum(filtered_ratings) / len(filtered_ratings), 2)

    def visualize_league_ranking(self, rankings=None):
        rankings = self._league_rankings() if rankings is None else rankings

        name = f"{self.primary_summoner_name}: "
        avg = f"avg={self.average_league_ranking(rankings=rankings)}. "
        std_dev = f"std_dev={std_dev_from(rankings)}. "
        avg_with_std_dev = f"avg_with_std_dev: {self._average_league_ranking_adjusted(rankings=rankings)}. "
        ratings = f"ratings={rankings}"

        return f"{name}{avg_with_std_dev}{avg}{std_dev}{ratings}"

    def visualize_valorant_ranking(self, rankings=None):
        rankings = self._valorant_rankings() if rankings is None else rankings

        name = f"{self.primary_valorant_name}: "
        avg = f"avg={self.average_valorant_ranking(rankings=rankings)}. "
        std_dev = f"std_dev={std_dev_from(rankings)}. "
        avg_with_std_dev = f"avg_with_std_dev: {self._average_valorant_ranking_adjusted(rankings=rankings)}. "
        ratings = f"ratings={rankings}"

        return f"{name}{avg_with_std_dev}{avg}{std_dev}{ratings}"

    def average_league_ranking(self, rankings=None) -> float:
        rankings = self._league_rankings() if rankings is None else rankings

        return average_from(rankings)

    def average_valorant_ranking(self, rankings=None) -> float:
        rankings = self._valorant_rankings() if rankings is None else rankings

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

    # Internal utility to avoid recomputes
    def _average_valorant_ranking_adjusted(self, rankings=None):
        rankings = self._valorant_rankings() if rankings is None else rankings

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

    def preference_for_valorant_role(self, role: Union[VALORANT_ROLE, FLOAT_ROLE]):
        if not hasattr(self, "valorant_role_preferences"):
            return None

        role_value = role.value if isinstance(role, VALORANT_ROLE) else role

        # Valorant allows a floater, we assume they will pick their primary role
        if role_value == FLOAT_ROLE or self.valorant_role_preferences.primary_role.value == role_value:
            role_type_for_user = "primary"
        elif self.valorant_role_preferences.secondary_role.value == role_value:
            role_type_for_user = "secondary"
        elif self.valorant_role_preferences.off_role.value == role_value:
            role_type_for_user = "off"
        else:
            role_type_for_user = None

        return role_type_for_user

    def average_league_ranking_adjusted_for_role(self, role: LEAGUE_ROLE):
        return round(self.average_league_ranking_adjusted * ROLE_MULTIPLIER[self.preference_for_league_role(role)], 1)

    def average_valorant_ranking_adjusted_for_role(self, role: Union[VALORANT_ROLE, FLOAT_ROLE]):
        return round(self.average_valorant_ranking_adjusted * ROLE_MULTIPLIER[self.preference_for_valorant_role(role)], 1)
