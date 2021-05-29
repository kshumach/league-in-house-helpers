from django.urls import path

from summoners.api.views import CreateSummonerView, DestroySummonerView

urlpatterns = [
    path("register", CreateSummonerView.as_view(), name="create_summoner"),
    path("<in_game_name>", DestroySummonerView.as_view(), name="delete_summoner"),
]
