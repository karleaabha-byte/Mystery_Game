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
        clue = room["normal_clue"]

        strategy = self.mole_ai.choose_room_strategy(
            room_name,
            self.get_mole_suspicion()
        )

        if strategy == "sabotage_cafeteria":
            self.clues.append({
                "room": room_name,
                "type": "partial",
                "data": {
                    "title": clue["title"],
                    "instruction": clue["instruction"],
                    "survivors": clue["survivors"],
                    "terminal_id": clue["terminal_id"],
                    "note": (
                        "The display flickers before you can inspect "
                        "the rest of the system log."
                    )
                }
            })

        elif strategy == "manipulate_riddle":
            self.clues.append({
                "room": room_name,
                "type": "partial",
                "data": {
                    "title": clue["title"],
                    "entries": clue["entries"],
                    "note": clue["secondary_note"]
                }
            })

        else:
            self.clues.append({
                "room": room_name,
                "type": clue["type"],
                "data": clue
            })

        return f"You investigated the {room_name}."

    def question_character(self, character, question):
        if self.game_over:
            return "The investigation is already over."

        if self.actions_left <= 0:
            return "You have no actions remaining."

        if character not in CHARACTERS:
            return "Unknown character."

        if question not in QUESTIONS:
            return "Unknown question."

        self.actions_left -= 1
        self.questioned_characters.add(character)

        strategy = self.mole_ai.choose_question_strategy(
            self.get_mole_suspicion()
        )

        response = CHARACTER_RESPONSES[character][question]

        if character == MOLE:
            if strategy == "lie":
                response = self._mole_lie(question, response)

            elif strategy == "help":
                response = self._mole_partial_truth(
                    question,
                    response
                )

        self._update_suspicion(
            character,
            question,
            response
        )

        return response

    def _mole_lie(self, question, original_response):
        lies = {
            QUESTIONS[0]:
                "I was in my quarters the entire time. Nobody came near me.",

            QUESTIONS[1]:
                "No. I didn't hear anything unusual anywhere.",

            QUESTIONS[2]:
                "No. I never went anywhere near the cafeteria.",

            QUESTIONS[3]:
                "I only heard that Luca had been moving things.",

            QUESTIONS[4]:
                "Raven. She's been trying to make everyone suspicious."
        }

        return lies.get(question, original_response)

    def _mole_partial_truth(self, question, original_response):
        truths = {
            QUESTIONS[0]:
                "I was in my quarters for most of that period.",

            QUESTIONS[1]:
                "I noticed something was wrong, but I didn't investigate.",

            QUESTIONS[2]:
                "I may have passed through the area earlier.",

            QUESTIONS[3]:
                "I noticed the storage area had been disturbed.",

            QUESTIONS[4]:
                "Raven has been asking a lot of questions."
        }

        return truths.get(question, original_response)

    def _update_suspicion(self, character, question, response):
        if character == MOLE:
            self.suspicion[character] += 8

        if "Zephyr" in response and character != "Zephyr":
            self.suspicion["Zephyr"] += 3

        if "Luca" in response and character != "Luca":
            self.suspicion["Luca"] += 2

    def get_mole_suspicion(self):
        return self.suspicion.get(MOLE, 0)

    def get_clues(self):
        return self.clues

    def get_remaining_actions(self):
        return self.actions_left

    def accuse(self, character):
        if self.game_over:
            return self.result

        if character not in CHARACTERS:
            return "Unknown character."

        if self.actions_left <= 0:
            return "You have no actions remaining."

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
