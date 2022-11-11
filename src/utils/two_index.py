import random


def two_index(length: int):
    index_one = 0
    index_two = 0

    while index_one == index_two:
        index_one = random.randint(0, length)
        index_two = random.randint(0, length)

    return index_one, index_two
