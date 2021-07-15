from typing import Optional

from requests import Request, Session, Response
from requests.auth import AuthBase
from django.conf import settings

from common.riot_client.types import SummonerResponseType, ValorantAccountResponseType


class RiotAPiAuth(AuthBase):
    def __init__(self, api_key):
        self.api_key = api_key

    def __call__(self, request: Request) -> Request:
        request.headers["X-Riot-Token"] = self.api_key
        return request


def raise_for_status_hook(response: Response, *args, **kwargs) -> Response:
    response.raise_for_status()

    return response


class RiotClient:
    def __init__(self):
        session = Session()
        session.headers.update({"Accept": "application/json;charset=utf-8"})
        session.auth = RiotAPiAuth(settings.RIOT_API_KEY)
        session.hooks["response"].append(raise_for_status_hook)

        self._session = session
        self._default_routing_region = "na1"
        self._api_path = "api.riotgames.com/"

    def _make_request(self, method: str, path: str, **kwargs) -> Optional[dict]:
        request_func = getattr(self._session, method.lower())

        overrides = kwargs.pop("overrides") if "overrides" in kwargs else None

        routing_region = overrides["routing_region"] if "routing_region" in overrides else self._default_routing_region

        base_url = f"https://{routing_region}.api.riotgames.com/"

        response = request_func(f"{base_url}{path}", **kwargs)

        return response.json()

    def get_summoner_by_name(self, name: str) -> SummonerResponseType:
        path = f"lol/summoner/v4/summoners/by-name/{name}"

        response: SummonerResponseType = self._make_request("get", path)

        return response

    def get_valorant_account_by_name_and_tag(self, name: str, tag: str) -> ValorantAccountResponseType:
        path = f"riot/account/v1/accounts/by-riot-id/{name}/{tag}"

        response: ValorantAccountResponseType = self._make_request("get", path, overrides={"routing_region": "americas"})

        return response
