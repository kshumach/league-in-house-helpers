from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import CreateUserSerializer


class CreateUser(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        confirmation_token = request.data["confirmation_token"]

        if confirmation_token == "correct":
            return super().create(request, *args, **kwargs)
        else:
            raise AuthenticationFailed(detail="Invalid confirmation token.")
