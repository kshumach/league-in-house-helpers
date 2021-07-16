import enum


class GAME_OPTIONS(enum.Enum):
    LEAGUE = "LEAGUE"
    VALORANT = "VALORANT"

    @staticmethod
    def as_tuple_list():
        return list(map(lambda r: (r.name, r.value), GAME_OPTIONS))
