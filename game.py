from case import (
    CHARACTERS,
    MOLE,
    ROOMS,
    QUESTIONS,
    CHARACTER_RESPONSES,
    MAX_ACTIONS
)

from ai_agent import MoleAI


class Game:

    def __init__(self, player_name="Player"):
        self.player_name = player_name

        self.max_actions = MAX_ACTIONS
        self.actions_remaining = MAX_ACTIONS
        self.actions_used = 0

        self.mole = MOLE
        self.ai = MoleAI(MOLE)

        self.visited_rooms = set()
        self.questioned_characters = set()

        self.suspicion = {
            character: 0
            for character in CHARACTERS
        }

        self.evidence = []

        self.activity_log = []
        self.action_history = []

        self.ai_lie_count = 0
        self.ai_truth_count = 0
        self.ai_help_count = 0
        self.ai_sabotage_count = 0

        self.cafeteria_sabotaged = False
        self.riddle_manipulated = False

        self.game_over = False
        self.researcher_won = False
        self.accused = None
        self.last_event = None

    def use_action(self, action_name):
        if self.actions_remaining <= 0:
            return False

        self.actions_remaining -= 1
        self.actions_used += 1
        self.action_history.append(action_name)

        return True

    def change_suspicion(self, character, amount):
        if character not in self.suspicion:
            return

        self.suspicion[character] = max(
            0,
            min(
                100,
                self.suspicion[character] + amount
            )
        )

    def visit_room(self, room):

        if self.game_over:
            return False

        if self.actions_remaining <= 0:
            return False

        if room in self.visited_rooms:
            return False

        if room not in ROOMS:
            return False

        self.use_action(
            f"Investigate {room}"
        )

        self.visited_rooms.add(room)

        ai_strategy = self.ai.choose_room_strategy(
            room,
            self.suspicion[self.mole]
        )

        room_data = ROOMS[room]

        # --------------------------------------------------
        # LABORATORY
        # --------------------------------------------------

        if room == "Laboratory":

            self.evidence.append(
                "Laboratory clue discovered: the strange capital letters "
                "in the maintenance note spell ZEPHYR."
            )

            self.change_suspicion(
                "Zephyr",
                40
            )

            self.activity_log.append(
                "🔬 Laboratory evidence points toward Zephyr."
            )

            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": False,
                "clue": "ZEPHYR"
            }

            return True

        # --------------------------------------------------
        # CAFETERIA
        # --------------------------------------------------

        if room == "Cafeteria":

            if ai_strategy == "sabotage_cafeteria":

                self.cafeteria_sabotaged = True
                self.ai_sabotage_count += 1

                self.evidence.append(
                    "Cafeteria evidence was tampered with, "
                    "but the emergency PIN 10 is still readable. "
                    "Terminal Z-07 was also identified as the terminal "
                    "connected to Zephyr."
                )

                self.change_suspicion(
                    "Zephyr",
                    15
                )

                self.activity_log.append(
                    "⚠ Cafeteria evidence was tampered with, "
                    "but the main PIN clue survived."
                )

                self.last_event = {
                    "type": "room",
                    "room": room,
                    "sabotaged": True
                }

                return True

            self.evidence.append(
                "Cafeteria clue: 5 survivors × 2 = PIN 10. "
                "The access record shows PIN 10 was used from terminal Z-07, "
                "which is assigned to Zephyr."
            )

            self.change_suspicion(
                "Zephyr",
                25
            )

            self.activity_log.append(
                "🍔 Cafeteria evidence links terminal Z-07 to Zephyr."
            )

            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": False
            }

            return True

        # --------------------------------------------------
        # STORAGE
        # --------------------------------------------------

        if room == "Storage":

            if ai_strategy == "manipulate_riddle":

                self.riddle_manipulated = True
                self.ai_sabotage_count += 1

                self.evidence.append(
                    "The Storage riddle was slightly altered, "
                    "but the motion log still shows badge Z-07. "
                    "The facility register identifies Z-07 as Zephyr."
                )

                self.change_suspicion(
                    "Zephyr",
                    10
                )

                self.activity_log.append(
                    "⚠ The Storage riddle was tampered with, "
                    "but the badge evidence remains usable."
                )

                self.last_event = {
                    "type": "room",
                    "room": room,
                    "sabotaged": True
                }

                return True

            self.evidence.append(
                "Storage clue: the riddle points toward a shadow. "
                "A nearby motion log records badge Z-07 moving through "
                "the storage corridor. Z-07 belongs to Zephyr."
            )

            self.change_suspicion(
                "Zephyr",
                20
            )

            self.activity_log.append(
                "📦 Storage evidence links badge Z-07 to Zephyr."
            )

            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": False
            }

            return True

        return False

    def ask_question(self, character, question):

        if self.game_over:
            return False

        if self.actions_remaining <= 0:
            return False

        if character in self.questioned_characters:
            return False

        if character not in CHARACTER_RESPONSES:
            return False

        if question not in QUESTIONS:
            return False

        self.use_action(
            f"Question {character}"
        )

        self.questioned_characters.add(
            character
        )

        normal_response = CHARACTER_RESPONSES[
            character
        ][question]

        # --------------------------------------------------
        # QUESTIONING THE MOLE
        # --------------------------------------------------

        if character == self.mole:

            strategy = self.ai.choose_question_strategy(
                self.suspicion[self.mole]
            )

            if strategy == "lie":

                response = self.generate_lie()

                self.change_suspicion(
                    self.mole,
                    12
                )

                self.ai_lie_count += 1

                self.activity_log.append(
                    "⚠ Zephyr's answer contained suspicious information."
                )

            elif strategy == "help":

                response = (
                    normal_response
                    + "\n\n"
                    "They offer to help you investigate the facility."
                )

                self.change_suspicion(
                    self.mole,
                    -5
                )

                self.ai_help_count += 1

                self.activity_log.append(
                    "🤝 Zephyr cooperated with the investigation."
                )

            else:

                response = normal_response

                self.ai_truth_count += 1

                self.activity_log.append(
                    "💬 Zephyr answered directly."
                )

        # --------------------------------------------------
        # QUESTIONING OTHER CHARACTERS
        # --------------------------------------------------

        else:

            response = normal_response

            if "Zephyr" in response:

                self.change_suspicion(
                    "Zephyr",
                    18
                )

                self.activity_log.append(
                    f"🔎 {character}'s testimony increased "
                    "suspicion toward Zephyr."
                )

            else:

                self.activity_log.append(
                    f"💬 {character} answered your question."
                )

        self.last_event = {
            "type": "question",
            "character": character,
            "question": question,
            "response": response
        }

        return True

    def generate_lie(self):

        lies = [
            "I was nowhere near the cafeteria when that happened.",
            "I don't remember seeing anything unusual.",
            "I was helping someone else in the facility.",
            "I think Raven was acting suspiciously.",
            "I'm certain Luca was near the storage area.",
            "Everything was completely normal."
        ]

        index = (
            self.ai_lie_count
            % len(lies)
        )

        return lies[index]

    def accuse(self, character):

        if self.game_over:
            return

        if character not in CHARACTERS:
            return

        if self.actions_remaining > 0:
            self.use_action(
                f"Accuse {character}"
            )

        self.accused = character
        self.game_over = True

        if character == self.mole:

            self.researcher_won = True

            result = (
                f"Correct. {character} was the mole."
            )

            self.activity_log.append(
                f"🎉 {self.player_name} correctly identified "
                f"{character} as the mole."
            )

        else:

            self.researcher_won = False

            result = (
                f"Incorrect. {character} was not the mole."
            )

            self.activity_log.append(
                f"❌ {self.player_name} accused {character}, "
                "but the accusation was incorrect."
            )

        self.last_event = {
            "type": "accusation",
            "result": result
        }

    def best_suspect(self):

        return max(
            self.suspicion,
            key=self.suspicion.get
        )
