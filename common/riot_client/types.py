from typing import TypedDict


class SummonerResponseType(TypedDict):
    id: str
    accountId: str
    puuid: str
    name: str


class ValorantAccountResponseType(TypedDict):
    puuid: str
    tagLine: str
    gameName: str