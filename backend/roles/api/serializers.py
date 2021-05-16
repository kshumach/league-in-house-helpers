from rest_framework import serializers

from backend.common.api.fields import EnumModelField
from backend.roles.models import Role, UserRolePreference, ROLE


class UserRolePreferenceReadSerializer(serializers.ModelSerializer):
    primary_role = EnumModelField[Role](ROLE, Role)
    secondary_role = EnumModelField[Role](ROLE, Role)
    off_role = EnumModelField[Role](ROLE, Role)

    class Meta:
        model = UserRolePreference
        fields = ["primary_role", "secondary_role", "off_role"]


class UserRolePreferenceWriteSerializer(serializers.ModelSerializer):
    primary_role = EnumModelField[Role](ROLE, Role)
    secondary_role = EnumModelField[Role](ROLE, Role)
    off_role = EnumModelField[Role](ROLE, Role)
    user_id = serializers.IntegerField()

    class Meta:
        model = UserRolePreference
        fields = ["primary_role", "secondary_role", "off_role", "user_id"]
