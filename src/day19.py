import re
import functools
import itertools
import math

from typing import Optional
from collections import namedtuple


OreCost = namedtuple("OreCost", ["ore"])
ClayCost = namedtuple("ClayCost", ["ore"])
ObsidianCost = namedtuple("ObsidianCost", ["ore", "clay"])
GeodeCost = namedtuple("GeodeCost", ["ore", "obsidian"])
Blueprint = namedtuple(
    "Blueprint", ["idx", "ore_cost", "clay_cost", "obsidian_cost", "geode_cost"]
)
Mineral = namedtuple("Mineral", ["ore", "clay", "obsidian", "geode"])
State = namedtuple("State", ["time_left", "num_of_mineral", "num_of_robots"])


def read_blueprint(line) -> Blueprint:
    integers = re.findall(r"\d+", line)
    integers = list(map(int, integers))

    return Blueprint(
        idx=integers[0],
        ore_cost=OreCost(ore=integers[1]),
        clay_cost=ClayCost(ore=integers[2]),
        obsidian_cost=ObsidianCost(ore=integers[3], clay=integers[4]),
        geode_cost=GeodeCost(ore=integers[5], obsidian=integers[6]),
    )


def read_input() -> list[Blueprint]:
    with open("data/day19.txt", "r", encoding="utf-8") as data:
        lines = data.readlines()
        return [read_blueprint(line.strip()) for line in lines]


def default_state(time_left: int) -> State:
    return State(
        time_left=time_left,
        num_of_mineral=Mineral(ore=0, clay=0, obsidian=0, geode=0),
        num_of_robots=Mineral(ore=1, clay=0, obsidian=0, geode=0),
    )


def can_buy_geode(blueprint: Blueprint, state: State) -> bool:
    return (
        state.num_of_mineral.ore >= blueprint.geode_cost.ore
        and state.num_of_mineral.obsidian >= blueprint.geode_cost.obsidian
    )


def try_buy_geode(blueprint: Blueprint, state: State) -> Optional[State]:
    if (
        state.num_of_mineral.ore < blueprint.geode_cost.ore
        or state.num_of_mineral.obsidian < blueprint.geode_cost.obsidian
    ):
        return None

    return State(
        time_left=state.time_left - 1,
        num_of_mineral=Mineral(
            ore=state.num_of_mineral.ore
            - blueprint.geode_cost.ore
            + state.num_of_robots.ore,
            clay=state.num_of_mineral.clay + state.num_of_robots.clay,
            obsidian=state.num_of_mineral.obsidian
            - blueprint.geode_cost.obsidian
            + state.num_of_robots.obsidian,
            geode=state.num_of_mineral.geode + state.num_of_robots.geode,
        ),
        num_of_robots=Mineral(
            ore=state.num_of_robots.ore,
            clay=state.num_of_robots.clay,
            obsidian=state.num_of_robots.obsidian,
            geode=state.num_of_robots.geode + 1,
        ),
    )


def try_buy_obsidian(blueprint: Blueprint, state: State) -> Optional[State]:
    if (
        state.num_of_mineral.ore < blueprint.obsidian_cost.ore
        or state.num_of_mineral.clay < blueprint.obsidian_cost.clay
    ):
        return None

    return State(
        time_left=state.time_left - 1,
        num_of_mineral=Mineral(
            ore=state.num_of_mineral.ore
            - blueprint.obsidian_cost.ore
            + state.num_of_robots.ore,
            clay=state.num_of_mineral.clay
            - blueprint.obsidian_cost.clay
            + state.num_of_robots.clay,
            obsidian=state.num_of_mineral.obsidian + state.num_of_robots.obsidian,
            geode=state.num_of_mineral.geode + state.num_of_robots.geode,
        ),
        num_of_robots=Mineral(
            ore=state.num_of_robots.ore,
            clay=state.num_of_robots.clay,
            obsidian=state.num_of_robots.obsidian + 1,
            geode=state.num_of_robots.geode,
        ),
    )


def try_buy_clay(blueprint: Blueprint, state: State) -> Optional[State]:
    if state.num_of_mineral.ore < blueprint.clay_cost.ore:
        return None

    return State(
        time_left=state.time_left - 1,
        num_of_mineral=Mineral(
            ore=state.num_of_mineral.ore
            - blueprint.clay_cost.ore
            + state.num_of_robots.ore,
            clay=state.num_of_mineral.clay + state.num_of_robots.clay,
            obsidian=state.num_of_mineral.obsidian + state.num_of_robots.obsidian,
            geode=state.num_of_mineral.geode + state.num_of_robots.geode,
        ),
        num_of_robots=Mineral(
            ore=state.num_of_robots.ore,
            clay=state.num_of_robots.clay + 1,
            obsidian=state.num_of_robots.obsidian,
            geode=state.num_of_robots.geode,
        ),
    )


def try_buy_ore(blueprint: Blueprint, state: State) -> Optional[State]:
    if state.num_of_mineral.ore < blueprint.ore_cost.ore:
        return None

    return State(
        time_left=state.time_left - 1,
        num_of_mineral=Mineral(
            ore=state.num_of_mineral.ore
            - blueprint.ore_cost.ore
            + state.num_of_robots.ore,
            clay=state.num_of_mineral.clay + state.num_of_robots.clay,
            obsidian=state.num_of_mineral.obsidian + state.num_of_robots.obsidian,
            geode=state.num_of_mineral.geode + state.num_of_robots.geode,
        ),
        num_of_robots=Mineral(
            ore=state.num_of_robots.ore + 1,
            clay=state.num_of_robots.clay,
            obsidian=state.num_of_robots.obsidian,
            geode=state.num_of_robots.geode,
        ),
    )


def no_buy(state: State) -> State:
    return State(
        time_left=state.time_left - 1,
        num_of_mineral=Mineral(
            ore=state.num_of_mineral.ore + state.num_of_robots.ore,
            clay=state.num_of_mineral.clay + state.num_of_robots.clay,
            obsidian=state.num_of_mineral.obsidian + state.num_of_robots.obsidian,
            geode=state.num_of_mineral.geode + state.num_of_robots.geode,
        ),
        num_of_robots=Mineral(
            ore=state.num_of_robots.ore,
            clay=state.num_of_robots.clay,
            obsidian=state.num_of_robots.obsidian,
            geode=state.num_of_robots.geode,
        ),
    )


@functools.cache
def max_geode(blueprint: Blueprint, state: State) -> int:
    if state.time_left == 0:
        return state.num_of_mineral.geode

    if geode_bought := try_buy_geode(blueprint, state):
        return max_geode(blueprint, geode_bought)

    if obsidian_bought := try_buy_obsidian(blueprint, state):
        return max_geode(blueprint, obsidian_bought)

    nothing_bought = no_buy(state)
    possible_outcomes = [max_geode(blueprint, nothing_bought)]

    if clay_bought := try_buy_clay(blueprint, state):
        possible_outcomes.append(max_geode(blueprint, clay_bought))

    if ore_bought := try_buy_ore(blueprint, state):
        possible_outcomes.append(max_geode(blueprint, ore_bought))

    return max(possible_outcomes)


def part1():
    blueprints = read_input()
    state = default_state(24)
    return sum(map(lambda bp: bp.idx * max_geode(bp, state), blueprints))


def part2():
    blueprints = read_input()
    state = default_state(24)  # 32
    return math.prod(map(lambda bp: max_geode(bp, state), blueprints[:3]))
