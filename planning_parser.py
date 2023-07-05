from typing import Tuple, Union, Iterable

PLACE_BLOCK = "placeblock"
REMOVE_BLOCK = "removeblock"
ACTIONS = [PLACE_BLOCK, REMOVE_BLOCK]

Block = str
Action = Union[PLACE_BLOCK, REMOVE_BLOCK]
Location = Tuple[int, int, int]

def parser_actions(filename: str) -> Iterable[Tuple[Action, Location, Block]]:
    with open(filename) as f:
        skip_until_solution(f)
        for line in f:
            index, answer = line.split(": ")
            try:
                action = next(a for a in ACTIONS if answer.startswith(a))
                location, block = answer.strip().split("(")[1][:-1].split(",")
                _, y, x, z = location.split('-')
                print(f"Parser: {index} - {action}({location},{block})")
                yield (action, (int(x), int(y), int(z)), block)
            except StopIteration:
                continue

def skip_until_solution(file):
    for line in file:
        if line.startswith("SOLUTION SEQUENCE"):
            return
