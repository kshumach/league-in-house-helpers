from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserListSerializer, UserReadSerializer, UserWriteSerializer, PasswordChangeSerializer


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserWriteSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        new_user_username = response.data["username"]
        user = get_user_model().objects.get(username=new_user_username)
        refresh = RefreshToken.for_user(user)

        response.data["token"] = {"refresh": str(refresh), "access": str(refresh.access_token)}

        return response


class ListUserView(ListAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer


class RetrieveUserView(RetrieveAPIView):
    serializer_class = UserReadSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class LogoutView(DestroyAPIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        encoded_token = request.data["token"]
        token = RefreshToken(encoded_token)

        token.blacklist()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordUpdateView(UpdateAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def put(self, request, *args, **kwargs):
        super().put(request, *args, **kwargs)

        return Response(status=status.HTTP_204_NO_CONTENT)
