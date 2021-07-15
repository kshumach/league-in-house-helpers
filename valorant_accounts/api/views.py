from requests import HTTPError
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from common.riot_client.client import RiotClient
from common.riot_client.types import ValorantAccountResponseType
from valorant_accounts.api.serializers import ValorantAccountWriteSerializer
from valorant_accounts.models import ValorantAccount


class CreateValorantAccountView(CreateAPIView):
    serializer_class = ValorantAccountWriteSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        try:
            valorant_account: ValorantAccountResponseType = RiotClient().get_valorant_account_by_name_and_tag(
                request.data["name"],
                request.data["tag"]
            )
            serializer_data = {
                "tag_line": valorant_account["tagLine"],
                "player_uuid": valorant_account["puuid"],
                "in_game_name": valorant_account["gameName"],
                "user": request.user,
            }

            serializer = self.get_serializer(data=serializer_data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except HTTPError as err:
            if err.response.status_code == status.HTTP_404_NOT_FOUND:
                return Response({"error": {"detail": "Valorant account not found."}}, status=status.HTTP_404_NOT_FOUND)
            else:
                raise err


class DestroyValorantAccountView(DestroyAPIView):
    def get_object(self):
        return ValorantAccount.objects.get(in_game_name=self.kwargs["in_game_name"], tag_line=self.kwargs["tag_line"])

    permission_classes = (IsAuthenticated,)
