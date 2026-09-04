# optimal_path.py

from collections import deque

from case import (
    CHARACTERS,
    ROOMS,
    MOLE
)


def solve_optimal_path():

    """
    Find the minimum number of investigation actions
    required to obtain enough deterministic evidence
    to identify the mole.

    For this case, the Laboratory clue directly reveals
    the mole's identity.

    BFS is used to demonstrate search over possible
    investigation sequences.
    """

    start_state = (
        frozenset(),
        frozenset()
    )

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

        (visited_rooms, questioned), path = queue.popleft()


        # ---------------------------------------------
        # Goal condition
        # ---------------------------------------------

        if "Laboratory" in visited_rooms:

            return path


        # ---------------------------------------------
        # Visit rooms
        # ---------------------------------------------

        for room in ROOMS:

            if room not in visited_rooms:

                new_rooms = frozenset(
                    set(visited_rooms) | {room}
                )

                new_state = (
                    new_rooms,
                    questioned
                )

                if new_state not in visited:

                    visited.add(new_state)

                    new_path = path + [
                        f"Investigate {room}"
                    ]

                    queue.append(
                        (
                            new_state,
                            new_path
                        )
                    )


        # ---------------------------------------------
        # Ask characters
        # ---------------------------------------------

        for character in CHARACTERS:

            if character not in questioned:

                new_questioned = frozenset(
                    set(questioned) | {character}
                )

                new_state = (
                    visited_rooms,
                    new_questioned
                )

                if new_state not in visited:

                    visited.add(new_state)

                    new_path = path + [
                        f"Question {character}"
                    ]

                    queue.append(
                        (
                            new_state,
                            new_path
                        )
                    )


    return []
