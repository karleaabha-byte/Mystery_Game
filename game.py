from case import (
    CHARACTERS,
    MOLE,
    MAX_ACTIONS,
    ROOMS,
    QUESTIONS,
    CHARACTER_RESPONSES,
)

from ai_agent import MoleAI


class Game:
    """
    Main game controller.

    Responsibilities:
    - Track remaining actions
    - Track investigated rooms
    - Track questioned characters
    - Store collected evidence
    - Handle Mole deception
    - Track suspicion
    - Handle final accusation

    The UI should not need to know who the Mole is.
    That information stays inside this class.
    """

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, player_name="Player"):

        self.player_name = player_name

        # ----------------------------------------------------
        # ACTIONS
        # ----------------------------------------------------

        self.actions_left = MAX_ACTIONS

        # ----------------------------------------------------
        # INVESTIGATION STATE
        # ----------------------------------------------------

        self.investigated_rooms = set()
        self.questioned_characters = set()

        # ----------------------------------------------------
        # EVIDENCE
        # ----------------------------------------------------

        self.clues = []

        # ----------------------------------------------------
        # SUSPICION
        # ----------------------------------------------------

        self.suspicion = {
            character: 0
            for character in CHARACTERS
        }

        # ----------------------------------------------------
        # MOLE AI
        # ----------------------------------------------------

        self.mole_ai = MoleAI(MOLE)

        # ----------------------------------------------------
        # END GAME
        # ----------------------------------------------------

        self.game_over = False
        self.accusation = None
        self.result = None
        self.last_accusation_correct = False


    # ========================================================
    # ROOM INVESTIGATION
    # ========================================================

    def investigate_room(self, room_name):
        """
        Investigate a room.

        Returns a short status message.

        The actual evidence is stored in self.clues.
        """

        if self.game_over:
            return "The investigation is already over."

        if self.actions_left <= 0:
            return "You have no actions remaining."

        if room_name not in ROOMS:
            return "Unknown room."

        if room_name in self.investigated_rooms:
            return "You have already investigated this room."

        # ----------------------------------------------------
        # Spend action
        # ----------------------------------------------------

        self.actions_left -= 1

        self.investigated_rooms.add(room_name)

        room = ROOMS[room_name]

        # ----------------------------------------------------
        # Ask Mole AI whether the evidence is interfered with.
        #
        # Laboratory is intentionally protected from sabotage
        # by MoleAI.
        # ----------------------------------------------------

        strategy = self.mole_ai.choose_room_strategy(
            room_name,
            self.get_mole_suspicion(),
        )

        # ----------------------------------------------------
        # Get the room's base clue.
        #
        # This supports both:
        #
        # ROOMS["Laboratory"]["clue"]
        #
        # and, for compatibility, older versions using
        # "normal_clue".
        # ----------------------------------------------------

        clue = room.get("clue")

        if clue is None:
            clue = room.get("normal_clue")

        if clue is None:
            # Don't crash the game if a room has accidentally
            # been configured without evidence.
            clue = {
                "type": "unknown",
                "title": "UNRECOVERED EVIDENCE",
                "note": "No usable record was recovered.",
            }

        # ----------------------------------------------------
        # Generate actual evidence
        # ----------------------------------------------------

        generated_clue = self._generate_room_clue(
            room_name,
            clue,
            strategy,
        )

        # ----------------------------------------------------
        # Store evidence
        # ----------------------------------------------------

        self.clues.append(
            {
                "room": room_name,
                "data": generated_clue,
            }
        )

        return self._room_result_message(
            room_name,
            strategy,
        )


    # ========================================================
    # ROOM RESULT MESSAGE
    # ========================================================

    def _room_result_message(self, room_name, strategy):

        if strategy == "distort":
            return (
                f"You investigated the {room_name}. "
                "Something about the records seems incomplete."
            )

        if strategy == "partial":
            return (
                f"You investigated the {room_name}. "
                "You recovered only part of the available record."
            )

        return (
            f"You investigated the {room_name}. "
            "You recovered useful evidence."
        )


    # ========================================================
    # GENERATE ROOM CLUE
    # ========================================================

    def _generate_room_clue(
        self,
        room_name,
        clue,
        strategy,
    ):
        """
        Creates the evidence shown to the player.

        The Mole can interfere with some evidence, but cannot
        completely erase the investigation.
        """

        # ====================================================
        # LABORATORY
        # ====================================================

        if room_name == "Laboratory":

            return {
                "type": "lab_report",

                "title": clue.get(
                    "title",
                    "INCIDENT REPORT #047",
                ),

                "date": clue.get(
                    "date",
                    "",
                ),

                "events": clue.get(
                    "events",
                    clue.get("lines", []),
                ),

                "note": clue.get(
                    "note",
                    "",
                ),

                "maintenance": clue.get(
                    "maintenance",
                    clue.get("maintenance_note", ""),
                ),

                "signature": clue.get(
                    "signature",
                    "",
                ),
            }


        # ====================================================
        # STORAGE
        # ====================================================

        if room_name == "Storage":

            # ------------------------------------------------
            # MOLE DISTORTION
            # ------------------------------------------------

            if strategy == "distort":

                original_entries = clue.get(
                    "entries",
                    [],
                )

                # Keep the important first part of the record
                # but make the final access information
                # incomplete.
                entries = []

                for entry in original_entries:

                    if "23:48" in entry:
                        continue

                    entries.append(entry)

                if not entries:

                    entries = [
                        "23:43 — Routine storage inspection completed.",
                        "23:46 — Restricted terminal accessed.",
                        "23:46 — Badge identifier recorded: Z-07.",
                        "23:47 — Restricted container opened.",
                    ]

                return {
                    "type": "storage_log",

                    "title": clue.get(
                        "title",
                        "RESTRICTED STORAGE ACCESS LOG",
                    ),

                    "entries": entries,

                    "note": (
                        "The final system entry appears to have "
                        "been overwritten."
                    ),

                    "handwritten": clue.get(
                        "handwritten",
                        "",
                    ),
                }

            # ------------------------------------------------
            # NORMAL STORAGE RECORD
            # ------------------------------------------------

            return {
                "type": "storage_log",

                "title": clue.get(
                    "title",
                    "RESTRICTED STORAGE ACCESS LOG",
                ),

                "entries": clue.get(
                    "entries",
                    [],
                ),

                "note": clue.get(
                    "note",
                    "",
                ),

                "handwritten": clue.get(
                    "handwritten",
                    clue.get("secondary_note", ""),
                ),
            }


        # ====================================================
        # CAFETERIA
        # ====================================================

        if room_name == "Cafeteria":

            # ------------------------------------------------
            # MOLE PARTIAL INTERFERENCE
            # ------------------------------------------------

            if strategy == "partial":

                return {
                    "type": "cafeteria_log",

                    "title": clue.get(
                        "title",
                        "CAFETERIA SECURITY LOG",
                    ),

                    "instruction": clue.get(
                        "instruction",
                        "",
                    ),

                    "survivors": clue.get(
                        "survivors",
                        5,
                    ),

                    "terminal_id": clue.get(
                        "terminal_id",
                        "UNKNOWN",
                    ),

                    "system_log": (
                        "23:49 — Emergency access terminal activated.\n"
                        "23:49 — Terminal identifier: Z-07."
                    ),

                    "note": (
                        "The security camera status line "
                        "cannot be recovered."
                    ),
                }

            # ------------------------------------------------
            # NORMAL CAFETERIA RECORD
            # ------------------------------------------------

            return {
                "type": "cafeteria_log",

                "title": clue.get(
                    "title",
                    "CAFETERIA SECURITY LOG",
                ),

                "instruction": clue.get(
                    "instruction",
                    "",
                ),

                "survivors": clue.get(
                    "survivors",
                    5,
                ),

                "terminal_id": clue.get(
                    "terminal_id",
                    "UNKNOWN",
                ),

                "system_log": self._format_system_log(
                    clue.get(
                        "system_log",
                        "",
                    )
                ),

                "note": clue.get(
                    "note",
                    "",
                ),
            }


        # ====================================================
        # UNKNOWN ROOM
        # ====================================================

        return clue


    # ========================================================
    # SYSTEM LOG FORMATTER
    # ========================================================

    def _format_system_log(self, log):
        """
        Ensures the UI always receives system logs as text.

        Accepts:
        - string
        - list
        - tuple
        """

        if isinstance(log, str):
            return log

        if isinstance(log, (list, tuple)):
            return "\n".join(
                str(line)
                for line in log
            )

        return str(log)


    # ========================================================
    # QUESTIONING
    # ========================================================

    def question_character(
        self,
        character,
        question,
    ):
        """
        Question a character once.

        Only the Mole gets dynamically deceptive answers.
        """

        if self.game_over:
            return "The investigation is already over."

        if self.actions_left <= 0:
            return "You have no actions remaining."

        if character not in CHARACTERS:
            return "Unknown character."

        if question not in QUESTIONS:
            return "Unknown question."

        if character in self.questioned_characters:
            return (
                f"You have already questioned {character}."
            )

        # ----------------------------------------------------
        # Spend action
        # ----------------------------------------------------

        self.actions_left -= 1

        self.questioned_characters.add(character)

        # ----------------------------------------------------
        # Get normal response
        # ----------------------------------------------------

        character_responses = CHARACTER_RESPONSES.get(
            character,
            {},
        )

        response = character_responses.get(
            question,
            "I don't know anything about that.",
        )

        # ----------------------------------------------------
        # Mole deception
        # ----------------------------------------------------

        if character == MOLE:

            strategy = self.mole_ai.choose_question_strategy(
                self.get_mole_suspicion(),
            )

            if strategy == "lie":

                response = self._mole_lie(
                    question
                )

            elif strategy == "partial":

                response = self._mole_partial_truth(
                    question
                )

        # ----------------------------------------------------
        # Update suspicion
        # ----------------------------------------------------

        self._update_suspicion(
            character,
            question,
            response,
        )

        return response


    # ========================================================
    # MOLE LIES
    # ========================================================

    def _mole_lie(self, question):

        lies = {

            QUESTIONS[0]:
                (
                    "I was in my quarters the entire time. "
                    "I never went near storage."
                ),

            QUESTIONS[1]:
                (
                    "No. I didn't hear or see anything unusual."
                ),

            QUESTIONS[2]:
                (
                    "No. I stayed away from the cafeteria."
                ),

            QUESTIONS[3]:
                (
                    "I only heard that Luca had been "
                    "moving supplies."
                ),

            QUESTIONS[4]:
                (
                    "Raven. She has been watching everyone."
                ),
        }

        return lies.get(
            question,
            "I don't know anything about that.",
        )


    # ========================================================
    # MOLE PARTIAL TRUTHS
    # ========================================================

    def _mole_partial_truth(self, question):

        truths = {

            QUESTIONS[0]:
                (
                    "I was in my quarters for most of that period. "
                    "I may have left briefly."
                ),

            QUESTIONS[1]:
                (
                    "I noticed something was wrong, "
                    "but I didn't investigate."
                ),

            QUESTIONS[2]:
                (
                    "I may have passed through the cafeteria earlier."
                ),

            QUESTIONS[3]:
                (
                    "I noticed the storage area had been disturbed."
                ),

            QUESTIONS[4]:
                (
                    "Raven has been asking a lot of questions."
                ),
        }

        return truths.get(
            question,
            "I don't remember anything useful.",
        )


    # ========================================================
    # SUSPICION
    # ========================================================

    def _update_suspicion(
        self,
        character,
        question,
        response,
    ):
        """
        Updates internal suspicion values.

        This is deliberately not shown as a definitive
        'Mole probability' to the player.

        Suspicion is only a gameplay mechanic used by MoleAI.
        """

        # ----------------------------------------------------
        # Questioning the Mole gives the Mole more opportunity
        # to contradict itself.
        # ----------------------------------------------------

        if character == MOLE:

            self.suspicion[MOLE] += 7

        # ----------------------------------------------------
        # If another character independently mentions Zephyr,
        # it gives the player corroborating information.
        # ----------------------------------------------------

        if (
            "Zephyr" in response
            and character != MOLE
        ):

            self.suspicion[MOLE] += 5

        # ----------------------------------------------------
        # Mentions of Luca create a small alternative lead.
        # This prevents the mystery from feeling completely
        # obvious.
        # ----------------------------------------------------

        if (
            "Luca" in response
            and character != "Luca"
        ):

            self.suspicion["Luca"] += 2

        # ----------------------------------------------------
        # Keep all values within 0-100.
        # ----------------------------------------------------

        for name in self.suspicion:

            self.suspicion[name] = max(
                0,
                min(
                    self.suspicion[name],
                    100,
                ),
            )


    # ========================================================
    # MOLE SUSPICION
    # ========================================================

    def get_mole_suspicion(self):

        return self.suspicion.get(
            MOLE,
            0,
        )


    # ========================================================
    # EVIDENCE
    # ========================================================

    def get_clues(self):

        return self.clues


    def get_room_clues(self, room_name):

        return [
            clue
            for clue in self.clues
            if clue.get("room") == room_name
        ]


    # ========================================================
    # GAME STATE
    # ========================================================

    def get_remaining_actions(self):

        return self.actions_left


    def is_finished(self):

        return self.game_over


    # ========================================================
    # ACCUSATION
    # ========================================================

    def accuse(self, character):
        """
        Make the final accusation.

        Accusing does NOT consume an action.

        Returns the result message.
        """

        if self.game_over:
            return self.result

        if character not in CHARACTERS:
            return "Unknown character."

        # ----------------------------------------------------
        # The investigation ends immediately.
        # ----------------------------------------------------

        self.game_over = True

        self.accusation = character

        # ----------------------------------------------------
        # Correct accusation
        # ----------------------------------------------------

        if character == MOLE:

            self.last_accusation_correct = True

            self.result = (
                f"Correct! {character} was the Mole."
            )

        # ----------------------------------------------------
        # Wrong accusation
        # ----------------------------------------------------

        else:

            self.last_accusation_correct = False

            self.result = (
                f"Wrong. {character} was not the Mole. "
                f"The Mole was {MOLE}."
            )

        return self.result


    # ========================================================
    # RESET
    # ========================================================

    def reset(self):

        self.actions_left = MAX_ACTIONS

        self.investigated_rooms = set()
        self.questioned_characters = set()

        self.clues = []

        self.suspicion = {
            character: 0
            for character in CHARACTERS
        }

        self.game_over = False

        self.accusation = None
        self.result = None

        self.last_accusation_correct = False
