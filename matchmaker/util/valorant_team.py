from typing import Optional, List, Dict, Union

from common.api.enums import FLOAT_ROLE
from roles.models import VALORANT_ROLE
from users.models import User


class TeamFullException(Exception):
    def __init__(self, name):
        self.message = f"Team {name} is full!"


class RoleFilledException(Exception):
    def __init__(self, role, existing: User, attempted: User):
        self.message = f"Role {role} is already filled by {existing.primary_valorant_name}. Attempted to fill: {attempted.primary_valorant_name}"


Assignments = Dict[str, Optional[User]]


class ValorantTeam:
    def __init__(self):
        self._assignments: Assignments = {
            VALORANT_ROLE.CONTROLLER.value: None,
            VALORANT_ROLE.DUELIST.value: None,
            VALORANT_ROLE.INITIATOR.value: None,
            VALORANT_ROLE.SENTINEL.value: None,
            FLOAT_ROLE: None,
        }

    def _members(self) -> List[Optional[User]]:
        return [v for k, v in self._assignments.items() if v is not None]

    def add_role(self, role: Union[VALORANT_ROLE, FLOAT_ROLE], player: User):
        role_value = role.value if isinstance(role, VALORANT_ROLE) else role
        existing_player: Optional[User] = self._assignments.get(role_value)

        if existing_player is not None:
            raise RoleFilledException(role_value, existing_player, player)
        else:
            self._assignments[role_value] = player

    def get_average_team_rating(self):
        members = self._members()

        if len(members) == 0:
            return 0

        return sum([user.average_valorant_ranking_adjusted for user in members]) / len(members)

    def get_player_in_role(self, role: VALORANT_ROLE):
        return self._assignments[role.value]

    def get_highest_rated_player(self):
        return self._members().sort(key=lambda m: m.average_valorant_ranking_adjusted, reverse=True)[:1]

    def is_team_full(self):
        return len(self._members()) == 5

    # can add showing the rating in this string
    def __str__(self):
        controller = self._assignments[VALORANT_ROLE.CONTROLLER.value]
        duelist = self._assignments[VALORANT_ROLE.DUELIST.value]
        initiator = self._assignments[VALORANT_ROLE.INITIATOR.value]
        sentinel = self._assignments[VALORANT_ROLE.SENTINEL.value]
        float = self._assignments[FLOAT_ROLE]

        controller_rank_str = f"{controller.average_valorant_ranking_adjusted} ~> {controller.average_valorant_ranking_adjusted_for_role(VALORANT_ROLE.CONTROLLER)}"
        duelist_rank_str = f"{duelist.average_valorant_ranking_adjusted} ~> {duelist.average_valorant_ranking_adjusted_for_role(VALORANT_ROLE.DUELIST)}"
        initiator_rank_str = f"{initiator.average_valorant_ranking_adjusted} ~> {initiator.average_valorant_ranking_adjusted_for_role(VALORANT_ROLE.INITIATOR)}"
        sentinel_rank_str = f"{sentinel.average_valorant_ranking_adjusted} ~> {sentinel.average_valorant_ranking_adjusted_for_role(VALORANT_ROLE.SENTINEL)}"
        float_rank_str = f"{float.average_valorant_ranking_adjusted} ~> {float.average_valorant_ranking_adjusted_for_role(FLOAT_ROLE)}"

        return f"""
        {VALORANT_ROLE.CONTROLLER.value}: ({controller.primary_valorant_name}: {controller_rank_str})" \n
        {VALORANT_ROLE.DUELIST.value}: ({duelist.primary_valorant_name}: {duelist_rank_str})" \n
        {VALORANT_ROLE.INITIATOR.value}: ({initiator.primary_valorant_name}: {initiator_rank_str})" \n
        {VALORANT_ROLE.SENTINEL.value}: ({sentinel.primary_valorant_name}: {sentinel_rank_str})" \n
        {FLOAT_ROLE}: ({float.primary_valorant_name}: {float_rank_str})"
        """
