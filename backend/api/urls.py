from django.urls import include, path

urlpatterns = [
    path("users/", include(("users.api.urls", "users"), namespace="users_api")),
    path("summoners/", include(("summoners.api.urls", "summoners"), namespace="summoners_api")),
]
