from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Subquery, F, OuterRef
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView
from rest_framework import status

from summoners.models import Summoner


class PlayerSelectorForm(forms.Form):
    players = forms.ModelMultipleChoiceField(
        queryset=get_user_model()
        .objects.annotate(
            primary_summoner_name=Subquery(Summoner.objects.filter(user=OuterRef("pk")).values("in_game_name")[:1])
        )
        .values_list("id", "primary_summoner_name"),
    )


class PlayerSelectorView(FormView):
    form_class = PlayerSelectorForm
    template_name = "admin/player_selector.html"


class MatchmakerView(View):
    def dispatch(self, request, *args, **kwargs):
        min_required_players = 10
        player_id_and_in_game_names = request.GET.getlist("players")

        if len(player_id_and_in_game_names) < min_required_players:
            content = (
                f"Must select at least {min_required_players} players. Got {len(player_id_and_in_game_names)} instead."
            )

            return HttpResponse(status=status.HTTP_422_UNPROCESSABLE_ENTITY, content=content)

        return HttpResponse(request.GET.getlist("players"))
