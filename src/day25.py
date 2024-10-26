def snafu_decode(snafu: str) -> int:
    snafu_to_digit = {
        "2": 2,
        "1": 1,
        "0": 0,
        "-": -1,
        "=": -2,
    }

    def snafu_decode_helper(snafu: str, number: int = 0) -> int:
        if snafu:
            c = snafu[0]
            return snafu_decode_helper(snafu[1:], number * 5 + snafu_to_digit[c])
        return number

    return snafu_decode_helper(snafu)


def snafu_encode(number: int) -> str:
    digit_to_snafu = {
        2: "2",
        1: "1",
        0: "0",
        4: "-",
        3: "=",
    }

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
        normal_sum = sum(snafu_decode(line.strip()) for line in lines)
        return snafu_encode(normal_sum)
