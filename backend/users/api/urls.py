from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from backend.users.api.views import CreateUserView, ListUserView, LogoutView

urlpatterns = [
    path("", ListUserView.as_view(), name="get_users"),
    path("create", CreateUserView.as_view(), name="create_new_user"),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout", LogoutView.as_view(), name="logout")
]
