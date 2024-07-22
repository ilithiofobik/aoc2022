def interpret_sensor_data(line):
    words = line.split()

    x_s = int(words[2][2:-1])
    y_s = int(words[3][2:-1])
    x_b = int(words[8][2:-1])
    y_b = int(words[9][2:])

    return x_s, y_s, x_b, y_b


MAGIC_Y = 2000000


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


class Intervals:
    def __init__(self):
        self.intervals = []

    def are_overlapping(self, a, b):
        a_s, a_t = a
        b_s, b_t = b
        return a_s <= b_t and b_s <= a_t

    def merge_two_intervals(self, a, b):
        a_s, a_t = a
        b_s, b_t = b
        return min(a_s, b_s), max(a_t, b_t)

    def add_interval(self, s, t):
        print("before adding interval {}, {}".format(s, t))
        print(self.intervals)

        new_interval = (s, t)
        new_intervals = []

        for i in self.intervals:
            if self.are_overlapping(i, new_interval):
                new_interval = self.merge_two_intervals(i, new_interval)
            else:
                new_intervals.append(i)

        new_intervals.append(new_interval)
        self.intervals = new_intervals

        print("after adding interval {}, {}".format(s, t))
        print(self.intervals)

    def get_length(self):
        return sum(t - s + 1 for s, t in self.intervals)


def part1():
    with open("data/day15.txt", "r", encoding="utf-8") as data:
        forbidden = Intervals()
        beacons = set()

        for line in data.readlines():
            x_s, y_s, x_b, y_b = interpret_sensor_data(line.strip())
            distance = manhattan_dist(x_s, y_s, x_b, y_b)
            distance_to_magic_y = manhattan_dist(x_s, y_s, x_s, MAGIC_Y)
            x_distance = distance - distance_to_magic_y

            if y_b == MAGIC_Y:
                beacons.add(x_b)

            if x_distance >= 0:
                forbidden.add_interval(x_s - x_distance, x_s + x_distance)

        print(forbidden.intervals)
        return forbidden.get_length() - len(beacons)
