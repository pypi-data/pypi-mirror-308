from .internal import calc


def calc_2(x):
    return calc(2 * x)


def calc_3(x):
    return calc(3 * x)


def main():
    print(calc(10))
    print(calc_2(10))
