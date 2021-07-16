from django.conf import settings
from django.db import models


class ValorantAccount(models.Model):
    tag_line = models.CharField(max_length=20, blank=False, null=False, unique=False)
    player_uuid = models.CharField(max_length=100, blank=False, null=False, unique=True)
    in_game_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
