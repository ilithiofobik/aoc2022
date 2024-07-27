snafu_to_digit = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}


def snafu_decode(snafu):
    number = 0

    for c in snafu:
        number = number * 5 + snafu_to_digit[c]

    return number


digit_to_snafu = {
    2: "2",
    1: "1",
    0: "0",
    4: "-",
    3: "=",
}


def snafu_encode(number):
    if number == 0:
        return "0"

    snafu = ""

    while number > 0:
        remainder = number % 5
        snafu = digit_to_snafu[remainder] + snafu
        if remainder in (3, 4):
            number += 5 - remainder
        number //= 5

    return snafu


def part1():
    with open("data/day25.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()

        normal_sum = 0

        for line in lines:
            normal_sum += snafu_decode(line.strip())

        print(normal_sum)
        return snafu_encode(normal_sum)
