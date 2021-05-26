from django.urls import path

from backend.rankings.api.views import UserRankingsUpdateView

urlpatterns = [path("rank", UserRankingsUpdateView.as_view(), name="update_user_ranking")]
