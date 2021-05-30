import enum

from django.conf import settings
from django.db import models

ROLE_MULTIPLIER = {
    "primary": 1,
    "secondary": 0.85,
    "off": 0.65,
    # Autofill
    None: 0.4
}


class ROLE(enum.Enum):
    TOP = "TOP"
    JUNGLE = "JUNGLE"
    MID = "MID"
    MARKSMAN = "MARKSMAN"
    SUPPORT = "SUPPORT"

    @staticmethod
    def as_tuple_list():
        return list(map(lambda r: (r.name, r.value), ROLE))


class Role(models.Model):
    value = models.CharField(max_length=16, choices=ROLE.as_tuple_list())


class UserRolePreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="role_preferences", on_delete=models.CASCADE)
    primary_role = models.ForeignKey(Role, related_name="primary_preferences", null=True, on_delete=models.SET_NULL)
    secondary_role = models.ForeignKey(Role, related_name="secondary_preferences", null=True, on_delete=models.SET_NULL)
    off_role = models.ForeignKey(Role, related_name="off_role_preferences", null=True, on_delete=models.SET_NULL)
