import random


def generete_code():
    random.seed()
    return str(random.randint(100000, 999999))


CODE = generete_code()
