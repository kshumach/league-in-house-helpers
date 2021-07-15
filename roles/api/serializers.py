from rest_framework import serializers

from common.api.fields import EnumModelField
from roles.models import LeagueRole, UserLeagueRolePreference, LEAGUE_ROLE


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
