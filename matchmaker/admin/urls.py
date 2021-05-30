from django.urls import path

from matchmaker.admin.views import PlayerSelectorView, MatchmakerView

urlpatterns = [
    path("matchmaker/pick", PlayerSelectorView.as_view(), name="player_selector"),
    path("matchmaker/match", MatchmakerView.as_view(), name="match_make")
]
