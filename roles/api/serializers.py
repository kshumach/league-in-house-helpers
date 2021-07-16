from rest_framework import serializers

from common.api.fields import EnumModelField
from roles.models import LeagueRole, UserLeagueRolePreference, LEAGUE_ROLE, ValorantRole, UserValorantRolePreference, \
    VALORANT_ROLE


class UserLeagueRolePreferenceReadSerializer(serializers.ModelSerializer):
    primary_role = EnumModelField[LeagueRole](LEAGUE_ROLE, LeagueRole)
    secondary_role = EnumModelField[LeagueRole](LEAGUE_ROLE, LeagueRole)
    off_role = EnumModelField[LeagueRole](LEAGUE_ROLE, LeagueRole)

    class Meta:
        model = UserLeagueRolePreference
        fields = ["primary_role", "secondary_role", "off_role"]


class UserLeagueRolePreferenceWriteSerializer(serializers.ModelSerializer):
    primary_role = EnumModelField[LeagueRole](LEAGUE_ROLE, LeagueRole)
    secondary_role = EnumModelField[LeagueRole](LEAGUE_ROLE, LeagueRole)
    off_role = EnumModelField[LeagueRole](LEAGUE_ROLE, LeagueRole)
    user_id = serializers.IntegerField()

    class Meta:
        model = UserLeagueRolePreference
        fields = ["primary_role", "secondary_role", "off_role", "user_id"]


class UserValorantRolePreferenceReadSerializer(serializers.ModelSerializer):
    primary_role = EnumModelField[ValorantRole](VALORANT_ROLE, ValorantRole)
    secondary_role = EnumModelField[ValorantRole](VALORANT_ROLE, ValorantRole)
    off_role = EnumModelField[ValorantRole](VALORANT_ROLE, ValorantRole)

    class Meta:
        model = UserValorantRolePreference
        fields = ["primary_role", "secondary_role", "off_role"]


class UserValorantRolePreferenceWriteSerializer(serializers.ModelSerializer):
    primary_role = EnumModelField[ValorantRole](VALORANT_ROLE, ValorantRole)
    secondary_role = EnumModelField[ValorantRole](VALORANT_ROLE, ValorantRole)
    off_role = EnumModelField[ValorantRole](VALORANT_ROLE, ValorantRole)
    user_id = serializers.IntegerField()

    class Meta:
        model = UserValorantRolePreference
        fields = ["primary_role", "secondary_role", "off_role", "user_id"]
