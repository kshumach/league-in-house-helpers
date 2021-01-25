from django.urls import path

from backend.users.api.views import CreateUser as CreateUserView

urlpatterns = [
    path("create", CreateUserView.as_view(), name="create_new_user"),
]
