from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView
from rest_framework import status

from matchmaker.util.league_matchmaker import LeagueMatchMaker, AttemptsExhaustionException
from matchmaker.util.valorant_matchmaker import ValorantMatchMaker


class LeaguePlayerSelectorForm(forms.Form):
    players = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(summoner__isnull=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["players"].widget.attrs.update({"style": "height: 25%;width:25%"})


class LeaguePlayerSelectorView(FormView):
    form_class = LeaguePlayerSelectorForm
    template_name = "admin/player_selector_league.html"


class LeagueMatchmakerView(View):
    def dispatch(self, request, *args, **kwargs):
        min_required_players = 10
        player_ids = request.GET.getlist("players")

        if len(player_ids) < min_required_players:
            content = f"Must select at least {min_required_players} players. Got {len(player_ids)} instead."

            return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)

        players = get_user_model().objects.filter(id__in=player_ids)

        matchmaker = LeagueMatchMaker(list(players))

        try:
            team_a, team_b = matchmaker.matchmake()

            content = f"Team A: {str(team_a)} \n\nTeam B: {str(team_b)}"

            return HttpResponse(status=status.HTTP_200_OK, content=content)
        except AttemptsExhaustionException as e:
            return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, content=e.message)


class ValorantPlayerSelectorForm(forms.Form):
    players = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.filter(valorantaccount__isnull=False)
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["players"].widget.attrs.update({"style": "height: 25%;width:25%"})


class ValorantPlayerSelectorView(FormView):
    form_class = ValorantPlayerSelectorForm
    template_name = "admin/player_selector_valorant.html"


class ValorantMatchmakerView(View):
    def dispatch(self, request, *args, **kwargs):
        min_required_players = 10
        player_ids = request.GET.getlist("players")

        if len(player_ids) < min_required_players:
            content = f"Must select at least {min_required_players} players. Got {len(player_ids)} instead."

            return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)

        players = get_user_model().objects.filter(id__in=player_ids)

        matchmaker = ValorantMatchMaker(list(players))

        try:
            team_a, team_b = matchmaker.matchmake()

            content = f"Team A: {str(team_a)} \n\nTeam B: {str(team_b)}"

            return HttpResponse(status=status.HTTP_200_OK, content=content)
        except AttemptsExhaustionException as e:
            return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, content=e.message)
