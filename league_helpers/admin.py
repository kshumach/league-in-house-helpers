from django.contrib.admin import AdminSite
from django.contrib.auth.models import Group
from matchmaker.admin.urls import urlpatterns as matchmaker_urls
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

from users.models import User


class LeagueHelpersAdmin(AdminSite):
    site_header = "League Helpers Admin"

    def get_urls(self):
        urlpatterns = super().get_urls()

        return matchmaker_urls + urlpatterns


admin_site = LeagueHelpersAdmin(name="league_helpers_admin")

admin_site.register(User)
admin_site.register(BlacklistedToken)
admin_site.register(OutstandingToken)
admin_site.register(Group)
