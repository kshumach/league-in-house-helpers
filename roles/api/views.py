from django.db.models import ObjectDoesNotExist
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from roles.api.serializers import UserLeagueRolePreferenceWriteSerializer, UserValorantRolePreferenceWriteSerializer
from roles.models import UserLeagueRolePreference, UserValorantRolePreference


class UserLeagueRolePreferenceUpdateView(UpdateAPIView):
    serializer_class = UserLeagueRolePreferenceWriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return UserLeagueRolePreference.objects.get(user_id=self.request.user.id)
        except ObjectDoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")


class UserValorantRolePreferenceUpdateView(UpdateAPIView):
    serializer_class = UserValorantRolePreferenceWriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return UserValorantRolePreference.objects.get(user_id=self.request.user.id)
        except ObjectDoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
