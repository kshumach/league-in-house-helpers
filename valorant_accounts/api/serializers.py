from rest_framework import serializers

from common.api.fields import UserField
from valorant_accounts.models import ValorantAccount


class ValorantAccountWriteSerializer(serializers.ModelSerializer):
    user = UserField()

    class Meta:
        model = ValorantAccount
        fields = "__all__"


class ValorantAccountReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValorantAccount
        fields = ["in_game_name", "tag_line"]

    def to_representation(self, instance):
        return f"{instance.in_game_name}#{instance.tag_line}"
