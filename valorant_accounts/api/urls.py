from django.urls import path

from valorant_accounts.api.views import CreateValorantAccountView, DestroyValorantAccountView

urlpatterns = [
    path("register", CreateValorantAccountView.as_view(), name="create_valorant_account"),
    path("<in_game_name>/<tag_line>", DestroyValorantAccountView.as_view(), name="delete_valorant_account"),
]
