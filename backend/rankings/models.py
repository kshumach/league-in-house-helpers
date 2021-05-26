import enum

from django.conf import settings
from django.db import models


class RANKING(enum.Enum):
    S = "S"
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    @staticmethod
    def as_tuple_list():
        return list(map(lambda r: (r.name, r.value), RANKING))


RANKINGS_DESCRIPTIONS = {
    RANKING.S: "",
    RANKING.A: "",
    RANKING.B: "",
    RANKING.C: "",
    RANKING.D: "",
}


class Ranking(models.Model):
    value = models.CharField(max_length=4, choices=RANKING.as_tuple_list())


class UserRanking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rankings", on_delete=models.CASCADE)
    ranking = models.ForeignKey(Ranking, null=True, on_delete=models.SET_NULL)
    rated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, related_name="ranking_ballots", on_delete=models.SET_NULL
    )
