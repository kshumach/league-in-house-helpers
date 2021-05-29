from django.urls import include, path

urlpatterns = [
    path("users/", include(("users.api.urls", "users"), namespace="users_api")),
    path("summoners/", include(("summoners.api.urls", "summoners"), namespace="summoners_api")),
    path("roles/", include(("roles.api.urls", "roles"), namespace="roles_api")),
    path("rankings/", include(("rankings.api.urls", "rankings"), namespace="rankings_api")),
]
