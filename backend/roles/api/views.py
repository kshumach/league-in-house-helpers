from django.db.models import ObjectDoesNotExist
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from backend.roles.api.serializers import UserRolePreferenceWriteSerializer
from backend.roles.models import UserRolePreference


class UserRolePreferenceUpdateView(UpdateAPIView):
    serializer_class = UserRolePreferenceWriteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        try:
            return UserRolePreference.objects.get(user_id=self.request.user.id)
        except ObjectDoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")
