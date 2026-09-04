from collections import deque

from case import CHARACTERS, ROOMS


def solve_optimal_path():

    """
    Find a short investigation path that gathers
    enough evidence to identify the mole.

    The strongest deterministic clue is the Laboratory,
    while Storage and Cafeteria provide confirmation.
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


        # --------------------------------------------------------
        # Goal
        # --------------------------------------------------------

        if "Laboratory" in visited_rooms:

            return path


        # --------------------------------------------------------
        # Visit rooms
        # --------------------------------------------------------

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


        # --------------------------------------------------------
        # Question survivors
        # --------------------------------------------------------

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
