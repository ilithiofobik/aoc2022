player_to_points = { 'X': 0, 'Y': 1, 'Z': 2}
opponent_to_points = { 'A': 1, 'B': 0, 'C': 2}

def part1():
    with open("data/day2.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        curr_sum = 0

        for line in lines:
            p = line[2]
            o = line[0]

            p_points = player_to_points[p]
            o_points = opponent_to_points[o]

            curr_sum += 1 + p_points
            curr_sum += 3 * ((p_points + o_points) % 3)

        return curr_sum

pair_to_points = {
        "A X": 3, 
        "B X": 1, 
        "C X": 2, 
        "A Y": 4, 
        "B Y": 5, 
        "C Y": 6,
        "A Z": 8,
        "B Z": 9,
        "C Z": 7
    }

def part2():
    with open("data/day2.txt", "r", encoding="utf-8") as data:
        return sum(pair_to_points[l[:3]] for l in  data.readlines())
