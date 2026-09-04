from collections import deque

from case import (
    ROOMS,
    MOLE
)


def solve_optimal_path():

    """
    Find the shortest guaranteed path to solving the case.

    The Laboratory cannot be sabotaged and contains a hidden
    capital-letter message spelling ZEPHYR.

    Therefore:

        1. Investigate Laboratory
        2. Accuse Zephyr

    BFS is used to demonstrate search over possible actions.
    """

    start_state = frozenset()

    queue = deque()

    queue.append(
        (
            start_state,
            []
        )
    )

    visited = set()
    visited.add(start_state)

    while queue:

        visited_rooms, path = queue.popleft()

        if "Laboratory" in visited_rooms:

            return path + [
                f"Accuse {MOLE}"
            ]

        for room in ROOMS:

            if room not in visited_rooms:

                new_rooms = frozenset(
                    set(visited_rooms) | {room}
                )

                if new_rooms not in visited:

                    visited.add(new_rooms)

                    new_path = path + [
                        f"Investigate {room}"
                    ]

                    queue.append(
                        (
                            new_rooms,
                            new_path
                        )
                    )

    return []
