from typing import Optional

from requests import Request, Session, Response
from requests.auth import AuthBase
from django.conf import settings

from backend.common.riot_client.types import SummonerResponseType


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
        self._base_url = "https://na1.api.riotgames.com/"

    def _make_request(self, method: str, path: str, **kwargs) -> Optional[dict]:
        request_func = getattr(self._session, method.lower())

        response = request_func(f"{self._base_url}{path}", **kwargs)

        return response.json()

    def get_summoner_by_name(self, name: str) -> SummonerResponseType:
        path = f"lol/summoner/v4/summoners/by-name/{name}"

        response: SummonerResponseType = self._make_request("get", path)

        return response
