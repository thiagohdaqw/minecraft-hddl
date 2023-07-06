import pathlib

from typing import Iterable, Tuple, Union


PLACE_BLOCK = "placeblock"
REMOVE_BLOCK = "removeblock"
ACTIONS = [PLACE_BLOCK, REMOVE_BLOCK]

BLOCKAT = "blockat"

Block = str
Action = Union[PLACE_BLOCK, REMOVE_BLOCK]
Location = Tuple[int, int, int]


def parse_actions(filepath: pathlib.Path) -> Iterable[Tuple[Action, Location, Block]]:
    with open(filepath) as f:
        skip_until_solution(f)
        for line in f:
            index, answer = line.split(": ")
            try:
                action = next(a for a in ACTIONS if answer.startswith(a))
                location, block = answer.strip().split("(")[1][:-1].split(",")
                _, y, x, z = location.split("-")
                # print(f"Parser: {index} - {action}({location},{block})")
                yield (action, (int(x), int(y), int(z)), block)
            except StopIteration:
                continue


def skip_until_solution(file):
    for line in file:
        if line.startswith("SOLUTION SEQUENCE"):
            return


def parse_world(filepath: pathlib.Path) -> Iterable[Tuple[Location, Block]]:
    with open(filepath) as file:
        for line in file:
            for x in line.split(")"):
                y = x.split("(")
                if len(y) != 2:
                    continue
                predicate = y[1].split()
                if predicate[0] != BLOCKAT or len(predicate) != 3:
                    continue
                _, y, x, z = predicate[1].split("-")
                yield (predicate[0], (int(x), int(y), int(z)), predicate[2])
