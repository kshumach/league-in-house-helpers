from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from rankings.api.serializers import UserRankingsWriteSerializer
from rankings.models import UserRanking, RankingType


class UserRankingsUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRankingsWriteSerializer

    def get_object(self):
        try:
            target_user = get_user_model().objects.get(id=self.request.data["user_id"])
            ranking_type = RankingType.objects.get(value=self.request.data["ranking_type"])
            return UserRanking.objects.get(rated_by=self.request.user.id, user=target_user, ranking_type=ranking_type)
        except ObjectDoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
