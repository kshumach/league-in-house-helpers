from rest_framework import serializers

from backend.summoners.models import Summoner


class SummonerWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summoner
        fields = "__all__"
