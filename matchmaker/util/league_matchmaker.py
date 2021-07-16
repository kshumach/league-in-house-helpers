import random
from typing import List, Tuple

from common.api.enums import GAME_OPTIONS
from matchmaker.util.league_team import LeagueTeam
from rankings.models import DEFAULT_RANKING, RankingType
from roles.models import LEAGUE_ROLE
from users.models import User


Matchup = Tuple[User, User]


class EmptyPoolException(Exception):
    pass


class DeltaTooLargeException(Exception):
    pass


class AttemptsExhaustionException(Exception):
    def __init__(self, attempts=10):
        self.message = f"Could not find a balanced team after {attempts} tries."


class UnMatchableStateException(Exception):
    def __init__(self, message):
        self.message = message


class LeagueMatchMaker:
    def __init__(self, players: List[User]):
        assert len(players) == 10, "Cannot match make with less than 10 players"

        self._players = players

        self._player_rankings_map = dict.fromkeys([player.username for player in players])

        self._build_starting_dataset()

    def _build_starting_dataset(self):
        for player in self._players:
            player_rankings = player.rankings.filter(
                ranking_type=RankingType.objects.get(value=GAME_OPTIONS.LEAGUE.value)
            )

            if len(player_rankings) < 2:
                self._player_rankings_map[player.username] = DEFAULT_RANKING
            else:
                self._player_rankings_map[player.username] = player.average_league_ranking_adjusted

    def _get_complete_pool_for_role(self, role: LEAGUE_ROLE, from_player_pool=None) -> List[User]:
        primary_pool = self._get_primary_pool(role, from_player_pool=from_player_pool)
        secondary_pool = self._get_secondary_pool(role, from_player_pool=from_player_pool)
        off_pool = self._get_off_pool(role, from_player_pool=from_player_pool)

        return primary_pool + secondary_pool + off_pool

    def _get_primary_pool(self, role: LEAGUE_ROLE, from_player_pool=None) -> List[User]:
        player_pool = self._players if from_player_pool is None else from_player_pool

        return [player for player in player_pool if player.league_role_preferences.primary_role.value == role.value]

    def _get_secondary_pool(self, role: LEAGUE_ROLE, from_player_pool=None) -> List[User]:
        player_pool = self._players if from_player_pool is None else from_player_pool

        return [player for player in player_pool if player.league_role_preferences.secondary_role.value == role.value]

    def _get_off_pool(self, role: LEAGUE_ROLE, from_player_pool=None) -> List[User]:
        player_pool = self._players if from_player_pool is None else from_player_pool

        return [player for player in player_pool if player.league_role_preferences.off_role.value == role.value]

    def _get_ranking(self, user: User):
        return self._player_rankings_map[user.username]

    """
    Create a bucket for each player in the pool, we will then create matchups for that player against other players
    """

    def _match_pairs_from_pool(self, pool: List[User]) -> List[Matchup]:
        matchups = []

        for user in pool:
            for other_user in [u for u in pool if u.username != user.username]:
                matchups.append((user, other_user))

        return matchups

    """
    Return the difference in ranking between the first user and the second.
    
    Return a tuple of the difference and the User that has the higher ranking.
    """

    def _get_matchup_skew(self, matchup: Matchup, role: LEAGUE_ROLE) -> Tuple[float, Matchup]:
        first_user_rating = matchup[0].average_league_ranking_adjusted_for_role(role)
        second_user_rating = matchup[1].average_league_ranking_adjusted_for_role(role)

        skew = first_user_rating - second_user_rating

        return skew, matchup

    def _raise_for_unmatchable_dataset(self):
        complete_top_laner_pool = self._get_complete_pool_for_role(LEAGUE_ROLE.TOP)
        complete_jungler_pool = self._get_complete_pool_for_role(LEAGUE_ROLE.JUNGLE)
        complete_mid_laner_pool = self._get_complete_pool_for_role(LEAGUE_ROLE.MID)
        complete_marksman_pool = self._get_complete_pool_for_role(LEAGUE_ROLE.MARKSMAN)
        complete_support_pool = self._get_complete_pool_for_role(LEAGUE_ROLE.SUPPORT)

        top_laner_count = len(complete_top_laner_pool)
        jungler_count = len(complete_jungler_pool)
        mid_laner_count = len(complete_mid_laner_pool)
        marksman_count = len(complete_marksman_pool)
        support_count = len(complete_support_pool)

        # Let's see if we have enough variety across all pools to make a team. We could potentially still not have
        # enough due to how things spread out but lets make sure we can even try.
        if any(
            [
                not top_laner_count >= 2,
                not jungler_count >= 2,
                not mid_laner_count >= 2,
                not marksman_count >= 2,
                not support_count >= 2,
            ]
        ):
            count_detail = f"top: {top_laner_count}, jng: {jungler_count} mid: {mid_laner_count}, adc: {marksman_count}, supp: {support_count}"
            raise UnMatchableStateException(f"Not enough players within each role to create a team. {count_detail}")

        return None

    def _find_best_matchup_from_pool(self, pool: List[User], role: LEAGUE_ROLE) -> Tuple[float, Matchup]:
        matchups = self._match_pairs_from_pool(pool)

        matchups_with_skew: List[Tuple[float, Matchup]] = [
            self._get_matchup_skew(matchup, role) for matchup in matchups
        ]

        sorted_matchups_by_skew = sorted(matchups_with_skew, key=lambda m: abs(m[0]))

        return sorted_matchups_by_skew[0]

    """
    Performs the main matchmaking loop based off the current teams, remaining player pool and remaining roles to fill.
    
    Updates teams in line, returns updated player pool and roles to fill.
    """

    def _matchmake(
        self, team_a: LeagueTeam, team_b: LeagueTeam, player_pool: list[User], roles_to_fill: list[LEAGUE_ROLE]
    ) -> Tuple[list[User], list[LEAGUE_ROLE]]:
        if len(player_pool) == 2:
            # Last loop, we can skip some things. We know that there is only one more role to fill
            role_to_fill = roles_to_fill[0]

            # We also know the player pool is just two players
            complete_pool = player_pool
        else:
            # Pick a random roll to fill
            try:
                role_to_fill = roles_to_fill[random.randint(0, len(roles_to_fill) - 1)]
            except ValueError as e:
                raise e

            primary_pool = self._get_primary_pool(role_to_fill, from_player_pool=player_pool)
            secondary_pool = self._get_secondary_pool(role_to_fill, from_player_pool=player_pool)
            off_pool = self._get_off_pool(role_to_fill, from_player_pool=player_pool)

            complete_pool = primary_pool + secondary_pool + off_pool

            if len(complete_pool) == 0:
                raise EmptyPoolException()

        current_team_skew = team_a.get_average_team_rating() - team_b.get_average_team_rating()

        picked_matchup_with_skew = self._find_best_matchup_from_pool(complete_pool, role_to_fill)

        picked_matchup_skew = picked_matchup_with_skew[0]
        picked_matchup = picked_matchup_with_skew[1]

        # Start by assigning arbitrarily. We will swap if needed to account for current team skew
        team_a_player = picked_matchup[0]
        team_b_player = picked_matchup[1]

        if current_team_skew == 0:
            # Empty teams or evenly matched. Just use the matchup as is
            pass
        elif current_team_skew < 0:
            # team a is weaker. Let's make sure they get the player favoured in the matchup
            if picked_matchup_skew < 0:
                # If the matchup skew is negative that means the right player had a better ranking
                team_a_player, team_b_player = team_b_player, team_a_player
        else:
            # team b is weaker. Let's make sure they get the player favoured in the matchup
            if picked_matchup_skew > 0:
                # If the matchup skew is positive that means the left player had a better ranking
                team_a_player, team_b_player = team_b_player, team_a_player

        team_a.add_role(role_to_fill, team_a_player)
        team_b.add_role(role_to_fill, team_b_player)

        # Remove players from player pool and roles from roles to fill
        selected_players_usernames = [team_a_player.username, team_b_player.username]

        player_pool = [player for player in player_pool if player.username not in selected_players_usernames]

        roles_to_fill = [r for r in roles_to_fill if r.value != role_to_fill.value]

        return player_pool, roles_to_fill

    def matchmake(self) -> Tuple[LeagueTeam, LeagueTeam]:
        self._raise_for_unmatchable_dataset()

        max_attempts = 10
        delta_max = 2

        attempt = 1

        while attempt < max_attempts:
            team_a = LeagueTeam()
            team_b = LeagueTeam()

            roles_to_fill = [role for role in LEAGUE_ROLE]
            player_pool = self._players

            try:
                while len(player_pool) > 0:
                    updated_player_pool, updated_roles_to_fill = self._matchmake(
                        team_a, team_b, player_pool, roles_to_fill
                    )
                    player_pool = updated_player_pool
                    roles_to_fill = updated_roles_to_fill
                else:
                    # We have no more players left to matchmake. Let's check how the teams balance out
                    if abs(team_a.get_average_team_rating() - team_b.get_average_team_rating()) > delta_max:
                        raise DeltaTooLargeException()

                    return team_a, team_b
            except (EmptyPoolException, DeltaTooLargeException):
                attempt += 1
        else:
            raise AttemptsExhaustionException(attempts=max_attempts)
