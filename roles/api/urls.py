from django.urls import path

from roles.api.views import UserLeagueRolePreferenceUpdateView, UserValorantRolePreferenceUpdateView

urlpatterns = [
    path("league_preferences", UserLeagueRolePreferenceUpdateView.as_view(), name="update_user_league_roles"),
    path("valorant_preferences", UserValorantRolePreferenceUpdateView.as_view(), name="update_user_valorant_roles"),
]
