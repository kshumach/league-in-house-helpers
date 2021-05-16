from django.urls import path

from backend.roles.api.views import UserRolePreferenceUpdateView

urlpatterns = [
    path("preferences", UserRolePreferenceUpdateView.as_view(), name="update_user_roles"),
]
