from django.urls import path

from matchmaker.admin.views import LeaguePlayerSelectorView, LeagueMatchmakerView

urlpatterns = [
    path("matchmaker/pick_league", LeaguePlayerSelectorView.as_view(), name="player_selector_league"),
    path("matchmaker/pick_valorant", LeaguePlayerSelectorView.as_view(), name="player_selector_valorant"),
    path("matchmaker/match_league", LeagueMatchmakerView.as_view(), name="match_make_league"),
    path("matchmaker/match_valorant", LeagueMatchmakerView.as_view(), name="match_make_valorant"),
]
