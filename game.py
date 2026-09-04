from case import (
    CHARACTERS,
    MOLE,
    MAX_ACTIONS,
    ROOMS,
    QUESTIONS,
    CHARACTER_RESPONSES
)

from ai_agent import MoleAI


class Game:

    def __init__(self, player_name="Player"):

        self.player_name = player_name

        self.actions_left = MAX_ACTIONS

        self.investigated_rooms = set()
        self.questioned_characters = set()

        self.clues = []

        self.suspicion = {
            character: 0
            for character in CHARACTERS
        }

        self.mole_ai = MoleAI(MOLE)

        self.game_over = False
        self.accusation = None
        self.result = None


    # ========================================================
    # ROOM INVESTIGATION
    # ========================================================

    def investigate_room(self, room_name):

        if self.game_over:
            return "The investigation is already over."

        if self.actions_left <= 0:
            return "You have no actions remaining."

        if room_name not in ROOMS:
            return "Unknown room."

        if room_name in self.investigated_rooms:
            return "You have already investigated this room."

        self.actions_left -= 1

        self.investigated_rooms.add(room_name)

        room = ROOMS[room_name]

        strategy = self.mole_ai.choose_room_strategy(
            room_name,
            self.get_mole_suspicion()
        )

        clue = self._generate_room_clue(
            room_name,
            room["clue"],
            strategy
        )

        self.clues.append({
            "room": room_name,
            "data": clue
        })

        return self._room_result_message(
            room_name,
            strategy
        )


    def _room_result_message(self, room_name, strategy):

        if strategy == "distort":
            return (
                f"You investigated the {room_name}. "
                "Something about the records seems incomplete."
            )

        if strategy == "partial":
            return (
                f"You investigated the {room_name}. "
                "You recovered part of the available record."
            )

        return (
            f"You investigated the {room_name}. "
            "You recovered useful evidence."
        )


    def _generate_room_clue(self, room_name, clue, strategy):

        # ----------------------------------------------------
        # LABORATORY
        # ----------------------------------------------------

        if room_name == "Laboratory":

            return {
                "type": "lab_report",
                "title": clue["title"],
                "date": clue["date"],
                "events": clue["events"],
                "note": clue["note"],
                "maintenance": clue["maintenance"],
                "signature": clue["signature"]
            }


        # ----------------------------------------------------
        # STORAGE
        # ----------------------------------------------------

        if room_name == "Storage":

            if strategy == "distort":

                return {
                    "type": "storage_log",
                    "title": clue["title"],
                    "entries": [
                        "23:43 — Routine storage inspection completed.",
                        "23:46 — Restricted terminal accessed.",
                        "23:46 — Badge identifier recorded: Z-07.",
                        "23:47 — Restricted container opened."
                    ],
                    "note": (
                        "The final system entry appears to have "
                        "been overwritten."
                    )
                }

            return {
                "type": "storage_log",
                "title": clue["title"],
                "entries": clue["entries"],
                "note": clue["note"],
                "handwritten": clue["handwritten"]
            }


        # ----------------------------------------------------
        # CAFETERIA
        # ----------------------------------------------------

        if room_name == "Cafeteria":

            if strategy == "partial":

                return {
                    "type": "cafeteria_log",
                    "title": clue["title"],
                    "instruction": clue["instruction"],
                    "survivors": clue["survivors"],
                    "terminal_id": clue["terminal_id"],
                    "system_log": [
                        "23:49 — Emergency access terminal activated.",
                        "23:49 — Terminal identifier: Z-07."
                    ],
                    "note": (
                        "The security camera status line "
                        "cannot be recovered."
                    )
                }

            return {
                "type": "cafeteria_log",
                "title": clue["title"],
                "instruction": clue["instruction"],
                "survivors": clue["survivors"],
                "terminal_id": clue["terminal_id"],
                "system_log": clue["system_log"],
                "note": clue["note"]
            }


        return clue


    # ========================================================
    # QUESTIONING
    # ========================================================

    def question_character(self, character, question):

        if self.game_over:
            return "The investigation is already over."

        if self.actions_left <= 0:
            return "You have no actions remaining."

        if character not in CHARACTERS:
            return "Unknown character."

        if question not in QUESTIONS:
            return "Unknown question."

        if character in self.questioned_characters:
            return f"You have already questioned {character}."


        self.actions_left -= 1

        self.questioned_characters.add(character)

        response = CHARACTER_RESPONSES[
            character
        ][question]


        # Only the Mole gets AI-generated deception.
        if character == MOLE:

            strategy = self.mole_ai.choose_question_strategy(
                self.get_mole_suspicion()
            )

            if strategy == "lie":
                response = self._mole_lie(question)

            elif strategy == "partial":
                response = self._mole_partial_truth(question)


        self._update_suspicion(
            character,
            question,
            response
        )

        return response


    # ========================================================
    # MOLE RESPONSES
    # ========================================================

    def _mole_lie(self, question):

        lies = {

            QUESTIONS[0]:
                "I was in my quarters the entire time. "
                "I never went near storage.",

            QUESTIONS[1]:
                "No. I didn't hear or see anything unusual.",

            QUESTIONS[2]:
                "No. I stayed away from the cafeteria.",

            QUESTIONS[3]:
                "I only heard that Luca had been moving supplies.",

            QUESTIONS[4]:
                "Raven. She has been watching everyone."
        }

        return lies[question]


    def _mole_partial_truth(self, question):

        truths = {

            QUESTIONS[0]:
                "I was in my quarters for most of that period. "
                "I may have left briefly.",

            QUESTIONS[1]:
                "I noticed something was wrong, "
                "but I didn't investigate.",

            QUESTIONS[2]:
                "I may have passed through the cafeteria earlier.",

            QUESTIONS[3]:
                "I noticed the storage area had been disturbed.",

            QUESTIONS[4]:
                "Raven has been asking a lot of questions."
        }

        return truths[question]


    # ========================================================
    # SUSPICION
    # ========================================================

    def _update_suspicion(
        self,
        character,
        question,
        response
    ):

        # Asking the Mole questions naturally raises suspicion
        # because the player gets more chances to catch contradictions.
        if character == MOLE:
            self.suspicion[MOLE] += 7

        # Other characters independently mentioning Zephyr
        # provides corroboration.
        if "Zephyr" in response and character != MOLE:
            self.suspicion[MOLE] += 5

        # Accusations against Luca create a small amount of
        # suspicion but don't dominate the investigation.
        if "Luca" in response and character != "Luca":
            self.suspicion["Luca"] += 2

        self.suspicion[character] = min(
            self.suspicion[character],
            100
        )

        self.suspicion[MOLE] = min(
            self.suspicion[MOLE],
            100
        )


    def get_mole_suspicion(self):

        return self.suspicion.get(
            MOLE,
            0
        )


    # ========================================================
    # EVIDENCE
    # ========================================================

    def get_clues(self):

        return self.clues


    # ========================================================
    # ACTIONS
    # ========================================================

    def get_remaining_actions(self):

        return self.actions_left


    # ========================================================
    # ACCUSATION
    # ========================================================

    def accuse(self, character):

        if self.game_over:
            return self.result

        if character not in CHARACTERS:
            return "Unknown character."

        # Accusing is the final decision.
        # It does NOT consume an action.
        self.game_over = True

        self.accusation = character

        if character == MOLE:

            self.result = (
                f"Correct! {character} was the Mole."
            )

        else:

            self.result = (
                f"Wrong. {character} was not the Mole. "
                f"The Mole was {MOLE}."
            )

        return self.result
