from django.urls import path

from roles.api.views import UserLeagueRolePreferenceUpdateView

urlpatterns = [
    path("league_preferences", UserLeagueRolePreferenceUpdateView.as_view(), name="update_user_league_roles"),
]
