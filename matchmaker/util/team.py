from typing import Optional, List, Dict

from roles.models import ROLE
from users.models import User


class TeamFullException(Exception):
    def __init__(self, name):
        self.message = f"Team {name} is full!"


class RoleFilledException(Exception):
    def __init__(self, role, existing: User, attempted: User):
        self.message = f"Role {role} is already filled by {existing.primary_summoner_name}. Attempted to fill: {attempted.primary_summoner_name}"


Assignments = Dict[str, Optional[User]]


class Team:
    def __init__(self):
        self._assignments: Assignments = {
            ROLE.TOP.value: None,
            ROLE.JUNGLE.value: None,
            ROLE.MID.value: None,
            ROLE.MARKSMAN.value: None,
            ROLE.SUPPORT.value: None,
        }

    def _members(self) -> List[Optional[User]]:
        return [v for k, v in self._assignments.items() if v is not None]

    def add_role(self, role: ROLE, player: User):
        existing_player: Optional[User] = self._assignments.get(role.value)

        if existing_player is not None:
            raise RoleFilledException(role, existing_player, player)
        else:
            self._assignments[role.value] = player

    def get_average_team_rating(self):
        members = self._members()

        if len(members) == 0:
            return 0

        return sum([user.average_ranking_adjusted for user in members]) / len(members)

    def get_player_in_role(self, role: ROLE):
        return self._assignments[role.value]

    def get_highest_rated_player(self):
        return self._members().sort(key=lambda m: m.average_ranking_adjusted, reverse=True)[:1]

    def is_team_full(self):
        return len(self._members()) == 5

    # can add showing the rating in this string
    def __str__(self):
        top = self._assignments[ROLE.TOP.value]
        jng = self._assignments[ROLE.JUNGLE.value]
        mid = self._assignments[ROLE.MID.value]
        bot = self._assignments[ROLE.MARKSMAN.value]
        sup = self._assignments[ROLE.SUPPORT.value]

        top_rank_str = f"{top.average_ranking_adjusted} ~> {top.average_ranking_adjusted_for_role(ROLE.TOP)}"
        jng_rank_str = f"{jng.average_ranking_adjusted} ~> {jng.average_ranking_adjusted_for_role(ROLE.JUNGLE)}"
        mid_rank_str = f"{mid.average_ranking_adjusted} ~> {mid.average_ranking_adjusted_for_role(ROLE.MID)}"
        bot_rank_str = f"{bot.average_ranking_adjusted} ~> {bot.average_ranking_adjusted_for_role(ROLE.MARKSMAN)}"
        sup_rank_str = f"{sup.average_ranking_adjusted} ~> {sup.average_ranking_adjusted_for_role(ROLE.SUPPORT)}"

        return f"""
        {ROLE.TOP.value}: ({top.primary_summoner_name}: {top_rank_str})" \n
        {ROLE.JUNGLE.value}: ({jng.primary_summoner_name}: {jng_rank_str})" \n
        {ROLE.MID.value}: ({mid.primary_summoner_name}: {mid_rank_str})" \n
        {ROLE.MARKSMAN.value}: ({bot.primary_summoner_name}: {bot_rank_str})" \n
        {ROLE.SUPPORT.value}: ({sup.primary_summoner_name}: {sup_rank_str})"
        """
