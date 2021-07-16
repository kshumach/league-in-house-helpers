from django.urls import path

from matchmaker.admin.views import LeaguePlayerSelectorView, LeagueMatchmakerView, ValorantPlayerSelectorView, \
    ValorantMatchmakerView

urlpatterns = [
    path("matchmaker/pick_league", LeaguePlayerSelectorView.as_view(), name="player_selector_league"),
    path("matchmaker/pick_valorant", ValorantPlayerSelectorView.as_view(), name="player_selector_valorant"),
    path("matchmaker/match_league", LeagueMatchmakerView.as_view(), name="match_make_league"),
    path("matchmaker/match_valorant", ValorantMatchmakerView.as_view(), name="match_make_valorant"),
]
