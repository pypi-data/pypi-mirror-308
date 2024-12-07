from fractions import Fraction


def average(x: list[Fraction]):
    x2 = x[:]
    if not x2:
        return Fraction(0)
    size = len(x2)
    return Fraction(sum(x2), size)


def median(x: list[Fraction]):
    x2 = x[:]
    if not x2:
        return Fraction(0)
    size = len(x2)
    if size % 2 == 0:
        r = (x2[size // 2] + x2[size // 2 - 1])
        return Fraction(r, 2)
    else:
        return x2[size // 2]


def mode(x: list[Fraction]):
    x2 = x[:]
    if not x2:
        return Fraction(0)
    size = len(x2)
    s = set(x2)
    while len(s) != len(x2):
        for i in s:
            x2.remove(i)
        s = set(x2)
    if size == len(x2):
        return None
    else:
        x2.sort()
        return x2


def sub(x: list[Fraction]):
    x2 = x[:]
    if not x2:
        return Fraction(0)
    size = len(x2)
    aver = average(x2)
    result = {}
    for i in range(size):
        result[x2[i]] = x2[i] - aver
    return result


def square(x: list[Fraction]):
    x2 = x[:]
    if not x2:
        return Fraction(0)
    r = sub(x2)
    return {i: r[i] ** 2 for i in r}


def square_sum(x: list[Fraction]):
    x2 = x[:]
    if not x2:
        return Fraction(0)
    size = len(x2)
    aver = average(x2)
    result = Fraction(0)
    for i in range(size):
        result += (x2[i] - aver) ** 2
    return result


def breakup(x: list[Fraction]):
    x2 = x[:]
    if not x2:
        return Fraction(0)
    r = square_sum(x2)
    return Fraction(r, len(x2))


def deviation(x: list[Fraction]) -> Fraction | float:
    x2 = x[:]
    return breakup(x2) ** (1 / 2)


if __name__ == '__main__':
    ml = [1, 3, 3, 4]
    ml = [Fraction(i, 1) for i in ml]
    print(average(ml))
    print(median(ml))
    print(mode(ml))
    print(sub(ml))
    print(square(ml))
    print(square_sum(ml))
    print(breakup(ml))
    print(deviation(ml))
    del ml
