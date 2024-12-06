from .internal import calc


def calc_2(x):
    return calc(2 * x)


if __name__ == "__main__":
    print(calc(10))
    print(calc_2(10))
