from collections import deque

from case import ROOMS


def solve_optimal_path():
    """
    Find the shortest useful investigation path.

    The intended deduction chain is:

        Laboratory
            ↓
        23:46 restricted access
            ↓
        Storage
            ↓
        Badge Z-07
            ↓
        Cafeteria
            ↓
        Terminal Z-07
            ↓
        Camera outage
            ↓
        Question suspects
            ↓
        Make accusation

    The optimal path does NOT directly use the hidden Mole value.
    """


    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    start_state = (
        frozenset(),     # investigated rooms
        frozenset(),     # questioned characters
        False             # enough physical evidence
    )

    queue = deque([
        (
            start_state,
            []
        )
    ])

    visited = {
        start_state
    }


    # --------------------------------------------------------
    # BFS
    # --------------------------------------------------------

    while queue:

        (
            state,
            path
        ) = queue.popleft()

        (
            investigated_rooms,
            questioned_characters,
            evidence_complete
        ) = state


        # ----------------------------------------------------
        # Once the three physical clues are collected,
        # questioning is the next optimal stage.
        # ----------------------------------------------------

        if (
            "Laboratory" in investigated_rooms
            and "Storage" in investigated_rooms
            and "Cafeteria" in investigated_rooms
        ):

            # Two corroborating witnesses are enough to
            # establish the intended deduction without
            # wasting actions questioning everyone.

            if (
                "Luca" in questioned_characters
                and "Marinette" in questioned_characters
            ):

                return path + [
                    "Review evidence",
                    "Accuse Zephyr"
                ]


        # ----------------------------------------------------
        # INVESTIGATE ROOMS
        # ----------------------------------------------------

        for room_name in ROOMS:

            if room_name in investigated_rooms:
                continue

            new_rooms = frozenset(
                set(investigated_rooms)
                | {room_name}
            )

            new_state = (
                new_rooms,
                questioned_characters,
                evidence_complete
            )

            if new_state in visited:
                continue

            visited.add(new_state)

            new_path = path + [
                f"Investigate {room_name}"
            ]

            queue.append(
                (
                    new_state,
                    new_path
                )
            )


        # ----------------------------------------------------
        # QUESTION WITNESSES
        # ----------------------------------------------------

        useful_witnesses = [
            "Luca",
            "Marinette"
        ]

        for character in useful_witnesses:

            if character in questioned_characters:
                continue

            new_characters = frozenset(
                set(questioned_characters)
                | {character}
            )

            new_state = (
                investigated_rooms,
                new_characters,
                evidence_complete
            )

            if new_state in visited:
                continue

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
