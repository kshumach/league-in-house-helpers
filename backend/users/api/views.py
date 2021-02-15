from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserWriteSerializer, UserReadSerializer, UserListSerializer


class CreateUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserWriteSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        new_user_username = response.data["username"]
        user = get_user_model().objects.get(username=new_user_username)
        refresh = RefreshToken.for_user(user)

        response.data["token"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

        return response


class ListUserView(ListAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UserListSerializer

    # Temp hack to return the payload style I want. Need a custom serializer to handle this properly in the future
    # Regular ListAPIView calls the serializer with many=True
    # Ideally I'd like to just override how data is returned but there isn't an easy override path.
    # ListAPIView calls self.get which immediately calls self.list :(
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class RetrieveUserView(RetrieveAPIView):
    lookup_field = "username"

    serializer_class = UserReadSerializer
    permission_classes = (IsAuthenticated,)

