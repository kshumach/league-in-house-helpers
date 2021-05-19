from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from backend.rankings.api.serializers import UserRankingsWriteSerializer
from backend.rankings.models import UserRanking


class UserRankingsUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserRankingsWriteSerializer

    def get_object(self):
        try:
            target_user = get_user_model().objects.get(id=self.request.data['user_id'])
            return UserRanking.objects.get(rated_by=self.request.user.id, user=target_user)
        except ObjectDoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
