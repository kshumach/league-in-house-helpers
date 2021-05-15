from django.conf import settings
from django.db import models


class Summoner(models.Model):
    summoner_id = models.CharField(max_length=100, blank=False, null=False, unique=True)
    riot_account_id = models.CharField(max_length=100, blank=False, null=False, unique=True)
    player_uuid = models.CharField(max_length=100, blank=False, null=False, unique=True)
    in_game_name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
