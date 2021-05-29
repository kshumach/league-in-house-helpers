from django.contrib.auth import get_user_model
from rest_framework import serializers

from common.api.fields import EnumModelField, UserField
from rankings.models import UserRanking, RANKING, Ranking


class UserRankingsReadSerializer(serializers.ModelSerializer):
    ranking = EnumModelField[Ranking](RANKING, Ranking)
    user_id = UserField
    rated_by = UserField()

    class Meta:
        model = UserRanking
        fields = ["ranking", "user_id", "rated_by"]


class UserRankingsWriteSerializer(serializers.ModelSerializer):
    ranking = EnumModelField[Ranking](RANKING, Ranking)
    user_id = serializers.IntegerField()
    rated_by = UserField(passes_in_id=True, lookup_model=get_user_model())

    class Meta:
        model = UserRanking
        fields = ["ranking", "user_id", "rated_by"]
