from requests import HTTPError
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.response import Response

from backend.common.riot_client.client import RiotClient
from backend.common.riot_client.types import SummonerResponseType
from backend.summoners.api.serializers import SummonerWriteSerializer
from backend.summoners.models import Summoner


class CreateSummonerView(CreateAPIView):
    serializer_class = SummonerWriteSerializer

    def create(self, request, *args, **kwargs):
        try:
            summoner: SummonerResponseType = RiotClient().get_summoner_by_name(request.data["in_game_name"])
            serializer_data = {
                "summoner_id": summoner["id"],
                "riot_account_id": summoner["accountId"],
                "player_uuid": summoner["puuid"],
                "in_game_name": summoner["name"],
                "user": request.user,
            }

            serializer = self.get_serializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except HTTPError as err:
            if err.response.status_code == status.HTTP_404_NOT_FOUND:
                return Response({"error": {"detail": "summoner not found."}}, status=status.HTTP_404_NOT_FOUND)
            else:
                raise err


class DestroySummonerView(DestroyAPIView):
    lookup_url_kwarg = "in_game_name"
    lookup_field = "in_game_name"
    queryset = Summoner.objects.all()
