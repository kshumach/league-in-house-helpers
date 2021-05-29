import random


def ban_from(ban_list):
    while True:
        if len(ban_list) == 1:
            return ban_list[0]
        else:
            index_to_remove = random.randrange(0, len(ban_list))
            del ban_list[index_to_remove]


__all__ = [ban_from]
