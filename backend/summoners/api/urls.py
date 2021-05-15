from django.urls import path

from backend.summoners.api.views import RegisterSummonerView

urlpatterns = [path("register/<in_game_name>", RegisterSummonerView.as_view(), name="summoner_by_name")]
