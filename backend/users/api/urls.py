from django.urls import path, re_path

from backend.users.api.views import CreateUserView, ListUserView

urlpatterns = [
    path("", ListUserView.as_view(), name="get_users"),
    path("create", CreateUserView.as_view(), name="create_new_user")
]
