# game.py

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

    def __init__(self):

        # -----------------------------
        # Action system
        # -----------------------------

        self.max_actions = MAX_ACTIONS
        self.actions_remaining = MAX_ACTIONS


        # -----------------------------
        # Mole
        # -----------------------------

        self.mole = MOLE
        self.ai = MoleAI(self.mole)


        # -----------------------------
        # Investigation
        # -----------------------------

        self.visited_rooms = set()
        self.questioned_characters = set()


        # -----------------------------
        # Suspicion
        # -----------------------------

        self.suspicion = {
            character: 0
            for character in CHARACTERS
        }


        # -----------------------------
        # Evidence
        # -----------------------------

        self.evidence = []


        # -----------------------------
        # Logs
        # -----------------------------

        self.activity_log = []


        # -----------------------------
        # AI state
        # -----------------------------

        self.cafeteria_sabotaged = False
        self.riddle_manipulated = False

        self.ai_sabotage_count = 0
        self.ai_help_count = 0
        self.ai_lie_count = 0
        self.ai_truth_count = 0


        # -----------------------------
        # Game state
        # -----------------------------

        self.game_over = False
        self.researcher_won = False

        self.last_result = ""


    # ==================================================
    # USE ACTION
    # ==================================================

    def use_action(self):

        if self.actions_remaining <= 0:
            return False

        self.actions_remaining -= 1

        return True


    # ==================================================
    # VISIT ROOM
    # ==================================================

    def visit_room(self, room):

        if self.game_over:
            return "The investigation is already over."

        if self.actions_remaining <= 0:
            return "You have no actions remaining."

        if room in self.visited_rooms:
            return "You have already visited this room."

        # Human action consumes one action.
        self.use_action()

        self.visited_rooms.add(room)

        # AI reacts internally.
        ai_strategy = self.ai.choose_room_strategy(
            room,
            self.suspicion[self.mole]
        )

        clue = ROOMS[room]["clue"]


        # ==================================================
        # CAFETERIA
        # ==================================================

        if room == "Cafeteria":

            if ai_strategy == "sabotage_cafeteria":

                self.cafeteria_sabotaged = True
                self.ai_sabotage_count += 1

                clue = (
                    "You find the vending machine.\n\n"
                    "However, something seems wrong.\n\n"
                    "The note beside it has been damaged. "
                    "Part of the PIN information is difficult "
                    "to read.\n\n"
                    "Someone may have tampered with the evidence."
                )

                self.evidence.append(
                    "Cafeteria clue appears to have been sabotaged."
                )

                self.activity_log.append(
                    "The Cafeteria evidence appeared damaged."
                )

            else:

                self.evidence.append(
                    "Cafeteria: Vending machine PIN clue found."
                )

                self.activity_log.append(
                    "You investigated the Cafeteria."
                )


        # ==================================================
        # STORAGE
        # ==================================================

        elif room == "Storage":

            if ai_strategy == "manipulate_riddle":

                self.riddle_manipulated = True
                self.ai_sabotage_count += 1

                clue = (
                    "You find a locked box containing a riddle.\n\n"
                    '"I travel endlessly without moving,\n'
                    'I speak though I have no voice,\n'
                    'I vanish the instant I am understood.\n\n'
                    'What am I?"\n\n'
                    "The wording appears to have been altered."
                )

                self.evidence.append(
                    "Storage riddle may have been manipulated."
                )

                self.activity_log.append(
                    "The Storage riddle appeared unusually difficult."
                )

            else:

                self.evidence.append(
                    "Storage: Riddle discovered."
                )

                self.activity_log.append(
                    "You investigated the Storage room."
                )


        # ==================================================
        # LABORATORY
        # ==================================================

        elif room == "Laboratory":

            self.evidence.append(
                "Laboratory: Capitalized letters reveal "
                "a hidden clue."
            )

            self.activity_log.append(
                "You investigated the Laboratory."
            )


        self.last_result = clue

        return clue


    # ==================================================
    # ASK QUESTION
    # ==================================================

    def ask_question(self, character, question):

        if self.game_over:
            return "The investigation is already over."

        if self.actions_remaining <= 0:
            return "You have no actions remaining."

        if character in self.questioned_characters:
            return f"You have already questioned {character}."

        if question not in QUESTIONS:
            return "Invalid question."

        # Human action consumes one action.
        self.use_action()

        self.questioned_characters.add(character)

        response = CHARACTER_RESPONSES[
            character
        ][question]


        # ==================================================
        # MOLE
        # ==================================================

        if character == self.mole:

            strategy = self.ai.choose_question_strategy(
                self.suspicion[self.mole]
            )


            # ------------------------------------------
            # LIE
            # ------------------------------------------

            if strategy == "lie":

                response = self.generate_lie()

                self.suspicion[self.mole] = min(
                    100,
                    self.suspicion[self.mole] + 10
                )

                self.ai_lie_count += 1

                self.activity_log.append(
                    f"{character} gave an inconsistent answer."
                )


            # ------------------------------------------
            # HELP
            # ------------------------------------------

            elif strategy == "help":

                response += (
                    "\n\n"
                    "They then offer to help you "
                    "with the investigation."
                )

                self.suspicion[self.mole] = max(
                    0,
                    self.suspicion[self.mole] - 10
                )

                self.ai_help_count += 1

                self.activity_log.append(
                    f"{character} cooperated and offered assistance."
                )


            # ------------------------------------------
            # TRUTH
            # ------------------------------------------

            else:

                self.ai_truth_count += 1

                self.activity_log.append(
                    f"{character} gave a straightforward answer."
                )


        # ==================================================
        # OTHER CHARACTERS
        # ==================================================

        else:

            if "Zephyr" in response:

                self.suspicion["Zephyr"] = min(
                    100,
                    self.suspicion["Zephyr"] + 15
                )

                self.activity_log.append(
                    "The response increased suspicion toward Zephyr."
                )

            else:

                self.activity_log.append(
                    f"{character} answered your question."
                )


        self.last_result = response

        return response


    # ==================================================
    # GENERATE LIE
    # ==================================================

    def generate_lie(self):

        lies = [

            "I was nowhere near the cafeteria when that happened.",

            "I don't remember seeing anything unusual.",

            "I was helping someone else in the facility.",

            "I think Raven was acting suspiciously.",

            "I'm certain Luca was near the storage area.",

            "Everything was completely normal."
        ]

        return lies[
            self.ai_lie_count % len(lies)
        ]


    # ==================================================
    # FINAL ACCUSATION
    # ==================================================

    def accuse(self, character):

        if self.game_over:

            return "The investigation has already ended."


        # Accusation itself consumes one action
        # if an action is available.
        if self.actions_remaining > 0:

            self.use_action()


        self.game_over = True


        if character == self.mole:

            self.researcher_won = True

            result = (
                f"CORRECT!\n\n"
                f"{character} was the mole.\n\n"
                "The AI agent was successfully identified."
            )

        else:

            self.researcher_won = False

            result = (
                f"INCORRECT!\n\n"
                f"{character} was not the mole.\n\n"
                f"The actual mole was {self.mole}."
            )


        self.last_result = result

        return result


    # ==================================================
    # RESULT
    # ==================================================

    def get_result(self):

        if not self.game_over:
            return None

        if self.researcher_won:
            return "RESEARCHER WINS"

        return "MOLE WINS"


    # ==================================================
    # GAME STATE
    # ==================================================

    def get_state(self):

        return {
            "actions_remaining": self.actions_remaining,

            "visited_rooms": tuple(
                sorted(self.visited_rooms)
            ),

            "questioned_characters": tuple(
                sorted(self.questioned_characters)
            ),

            "suspicion": tuple(
                sorted(self.suspicion.items())
            )
        }
