from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.api.enums import GAME_OPTIONS
from common.api.fields import EnumModelField, UserField
from rankings.models import UserRanking, RANKING, Ranking, RankingType


class UserRankingsReadSerializer(serializers.ModelSerializer):
    ranking = EnumModelField[Ranking](RANKING, Ranking)
    user_id = UserField
    rated_by = UserField()
    ranking_type = EnumModelField[RankingType](GAME_OPTIONS, RankingType)

    class Meta:
        model = UserRanking
        fields = ["ranking", "user_id", "rated_by", "ranking_type"]


class UserRankingsWriteSerializer(serializers.ModelSerializer):
    ranking = EnumModelField[Ranking](RANKING, Ranking)
    user_id = serializers.IntegerField()
    rated_by = UserField(passes_in_id=True, lookup_model=get_user_model())
    ranking_type = EnumModelField[RankingType](GAME_OPTIONS, RankingType)

    class Meta:
        model = UserRanking
        fields = ["ranking", "user_id", "rated_by", "ranking_type"]
