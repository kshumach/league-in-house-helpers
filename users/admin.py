from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from summoners.models import Summoner
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'primary_summoner', 'average_ranking_adjusted', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'primary_summoner',)
    readonly_fields = ('average_ranking_adjusted',)
    ordering = ('username',)

    def primary_summoner(self, obj):
        summoner: Summoner = obj.summoner_set.first()

        return summoner.in_game_name if summoner is not None else ""
