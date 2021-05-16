from rest_framework import serializers

from backend.common.api.fields import UserField
from backend.summoners.models import Summoner


class SummonerWriteSerializer(serializers.ModelSerializer):
    user = UserField()

    class Meta:
        model = Summoner
        fields = "__all__"


class SummonerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        fields = ["in_game_name"]

    def to_representation(self, instance):
        return instance.in_game_name
