from django.urls import include, path

urlpatterns = [
    path("users/", include(("users.api.urls", "users"), namespace="users_api")),
]
