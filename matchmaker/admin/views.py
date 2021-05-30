from django import forms
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView
from rest_framework import status

from matchmaker.util.matchmaker import MatchMaker, AttemptsExhaustionException


class PlayerSelectorForm(forms.Form):
    players = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.all())


class PlayerSelectorView(FormView):
    form_class = PlayerSelectorForm
    template_name = "admin/player_selector.html"


class MatchmakerView(View):
    def dispatch(self, request, *args, **kwargs):
        min_required_players = 3
        player_ids = request.GET.getlist("players")

        if len(player_ids) < min_required_players:
            content = (
                f"Must select at least {min_required_players} players. Got {len(player_ids)} instead."
            )

            return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)

        players = get_user_model().objects.filter(id__in=player_ids)

        matchmaker = MatchMaker(list(players))

        try:
            team_a, team_b = matchmaker.matchmake()

            content = f"Team A: {str(team_a)} \n\nTeam B: {str(team_b)}"

            return HttpResponse(status=status.HTTP_200_OK, content=content)
        except AttemptsExhaustionException as e:
            return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, content=e.message)
