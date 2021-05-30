from django.contrib.admin.apps import AdminConfig


class LeagueHelpersAdminConfig(AdminConfig):
    default_site = 'league_helpers.admin.LeagueHelpersAdmin'
