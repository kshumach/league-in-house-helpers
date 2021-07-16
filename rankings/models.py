import enum

from django.conf import settings
from django.db import models

from common.api.enums import GAME_OPTIONS


class RANKING(enum.Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    @staticmethod
    def as_tuple_list():
        return list(map(lambda r: (r.name, r.value), RANKING))


RANKING_WEIGHT = {
    "S": 9,
    "A": 7,
    "B": 5,
    "C": 3,
    "D": 1,
    "": None
}

RANKINGS_DESCRIPTIONS = {
    RANKING.S: "",
    RANKING.A: "",
    RANKING.B: "",
    RANKING.C: "",
    RANKING.D: "",
}

DEFAULT_RANKING = 4


class RankingType(models.Model):
    value = models.CharField(max_length=20, choices=GAME_OPTIONS.as_tuple_list())


class Ranking(models.Model):
    value = models.CharField(max_length=4, choices=RANKING.as_tuple_list())


class UserRanking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rankings", on_delete=models.CASCADE)
    ranking = models.ForeignKey(Ranking, null=True, on_delete=models.SET_NULL)
    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="ranking_ballots", on_delete=models.SET_NULL
    )
    ranking_type = models.ForeignKey(RankingType, null=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "rated_by"], name="unique_rating_per_user")]
