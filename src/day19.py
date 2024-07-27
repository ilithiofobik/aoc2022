import re
from enum import Enum
import copy

Mineral = Enum("Mineral", ["ORE", "CLAY", "OBSIDIAN", "GEODE"])


class State:
    def __init__(self):
        self.num_of_mineral = {mineral: 0 for mineral in Mineral}
        self.num_of_robots = {mineral: 0 for mineral in Mineral}
        self.num_of_robots[Mineral.ORE] = 1

    def buy_to_new(self, mineral):
        new_state = copy.deepcopy(self)
        new_state.num_of_robots[mineral] += 1
        return new_state

    def mine(self):
        for mineral, number in self.num_of_robots.items():
            self.num_of_mineral[mineral] += number

    def mine_to_new(self):
        new_state = copy.deepcopy(self)
        new_state.mine()
        return new_state


class Simulation:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.states = set([State()])

    def can_build(self, state, mineral):
        return all(
            state.num_of_mineral[m] >= self.blueprint[mineral][m] for m in Mineral
        )

    def perform_step(self):
        new_states = set()

        for state in self.states:
            mine_state = state.mine_to_new()
            new_states.add(mine_state)

            for mineral in Mineral:
                if self.can_build(state, mineral):
                    buy_state = state.buy_to_new(mineral)
                    buy_state.mine()
                    new_states.add(buy_state)

        self.states = new_states

    def max_geode(self):
        result = 0

        for state in self.states:
            result = max(result, state.num_of_mineral[Mineral.GEODE])

        return result


def read_blueprint(line):
    integers = re.findall(r"\d+", line)
    integers = list(map(int, integers))

    ore_cost = {mineral: 0 for mineral in Mineral}
    clay_cost = {mineral: 0 for mineral in Mineral}
    obsidian_cost = {mineral: 0 for mineral in Mineral}
    geode_cost = {mineral: 0 for mineral in Mineral}

    ore_cost[Mineral.ORE] = integers[1]
    clay_cost[Mineral.ORE] = integers[2]
    obsidian_cost[Mineral.ORE] = integers[3]
    obsidian_cost[Mineral.CLAY] = integers[4]
    geode_cost[Mineral.CLAY] = integers[5]
    geode_cost[Mineral.OBSIDIAN] = integers[6]

    all_costs = {
        Mineral.ORE: ore_cost,
        Mineral.CLAY: clay_cost,
        Mineral.OBSIDIAN: obsidian_cost,
        Mineral.GEODE: geode_cost,
    }
    return all_costs


NUMBER_OF_MINUTES = 24


def part1():
    with open("data/day19.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        result = 0

        for num, line in enumerate(lines, 1):
            blueprint = read_blueprint(line.strip())
            simulation = Simulation(blueprint)

            for _ in range(NUMBER_OF_MINUTES):
                simulation.perform_step()

            for state in simulation.states:
                print(state.num_of_mineral)
                print(state.num_of_robots)

            result += num * simulation.max_geode()

        return result
