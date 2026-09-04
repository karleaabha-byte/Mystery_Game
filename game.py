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

        # --------------------------------------------------------
        # ACTIONS
        # --------------------------------------------------------

        self.max_actions = MAX_ACTIONS
        self.actions_remaining = MAX_ACTIONS
        self.actions_used = 0


        # --------------------------------------------------------
        # AI
        # --------------------------------------------------------

        self.mole = MOLE
        self.ai = MoleAI(MOLE)


        # --------------------------------------------------------
        # INVESTIGATION
        # --------------------------------------------------------

        self.visited_rooms = set()
        self.questioned_characters = set()


        # --------------------------------------------------------
        # SUSPICION
        # --------------------------------------------------------

        self.suspicion = {
            character: 0
            for character in CHARACTERS
        }


        # --------------------------------------------------------
        # EVIDENCE
        # --------------------------------------------------------

        self.evidence = []


        # --------------------------------------------------------
        # ACTIVITY
        # --------------------------------------------------------

        self.activity_log = []

        self.action_history = []


        # --------------------------------------------------------
        # AI STATS
        # --------------------------------------------------------

        self.ai_lie_count = 0
        self.ai_truth_count = 0
        self.ai_help_count = 0
        self.ai_sabotage_count = 0


        # --------------------------------------------------------
        # SABOTAGE STATE
        # --------------------------------------------------------

        self.cafeteria_sabotaged = False
        self.riddle_manipulated = False


        # --------------------------------------------------------
        # GAME STATE
        # --------------------------------------------------------

        self.game_over = False
        self.researcher_won = False
        self.accused = None
        self.last_event = None


    # ============================================================
    # ACTION SYSTEM
    # ============================================================

    def use_action(self, action_name):

        if self.actions_remaining <= 0:
            return False

        self.actions_remaining -= 1
        self.actions_used += 1

        self.action_history.append(action_name)

        return True


    # ============================================================
    # SUSPICION
    # ============================================================

    def change_suspicion(self, character, amount):

        self.suspicion[character] = max(
            0,
            min(
                100,
                self.suspicion[character] + amount
            )
        )


    # ============================================================
    # VISIT ROOM
    # ============================================================

    def visit_room(self, room):

        if self.game_over:
            return False

        if self.actions_remaining <= 0:
            return False

        if room in self.visited_rooms:
            return False


        self.use_action(
            f"Investigate {room}"
        )

        self.visited_rooms.add(room)


        # AI makes an internal decision.
        ai_strategy = self.ai.choose_room_strategy(
            room,
            self.suspicion[self.mole]
        )


        room_data = ROOMS[room]


        # ========================================================
        # CAFETERIA SABOTAGE
        # ========================================================

        if (
            room == "Cafeteria"
            and ai_strategy == "sabotage_cafeteria"
        ):

            self.cafeteria_sabotaged = True

            self.ai_sabotage_count += 1


            self.evidence.append(
                "The Cafeteria vending-machine note "
                "appears to have been damaged."
            )


            self.activity_log.append(
                "⚠ AI sabotage detected: cafeteria evidence altered."
            )


            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": True
            }


            return True


        # ========================================================
        # STORAGE RIDDLE MANIPULATION
        # ========================================================

        if (
            room == "Storage"
            and ai_strategy == "manipulate_riddle"
        ):

            self.riddle_manipulated = True

            self.ai_sabotage_count += 1


            self.evidence.append(
                "The Storage riddle appears to have "
                "been deliberately altered."
            )


            self.activity_log.append(
                "⚠ AI sabotage detected: storage riddle manipulated."
            )


            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": True
            }


            return True


        # ========================================================
        # NORMAL ROOM
        # ========================================================

        self.evidence.append(
            f"{room} investigation completed."
        )


        self.activity_log.append(
            f"🔎 Investigated the {room}."
        )


        self.last_event = {
            "type": "room",
            "room": room,
            "sabotaged": False
        }


        return True


    # ============================================================
    # QUESTION CHARACTER
    # ============================================================

    def ask_question(self, character, question):

        if self.game_over:
            return False

        if self.actions_remaining <= 0:
            return False

        if character in self.questioned_characters:
            return False


        self.use_action(
            f"Question {character}"
        )

        self.questioned_characters.add(character)


        normal_response = CHARACTER_RESPONSES[
            character
        ][question]


        # ========================================================
        # MOLE RESPONSE
        # ========================================================

        if character == self.mole:

            strategy = self.ai.choose_question_strategy(
                self.suspicion[self.mole]
            )


            # ----------------------------------------------------
            # LIE
            # ----------------------------------------------------

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


            # ----------------------------------------------------
            # HELP
            # ----------------------------------------------------

            elif strategy == "help":

                response = (
                    normal_response
                    +
                    "\n\n"
                    "They offer to help you investigate "
                    "the facility."
                )

                self.change_suspicion(
                    self.mole,
                    -10
                )

                self.ai_help_count += 1

                self.activity_log.append(
                    "🤝 Zephyr cooperated with the investigation."
                )


            # ----------------------------------------------------
            # TRUTH
            # ----------------------------------------------------

            else:

                response = normal_response

                self.ai_truth_count += 1

                self.activity_log.append(
                    "💬 Zephyr answered directly."
                )


        # ========================================================
        # OTHER SURVIVORS
        # ========================================================

        else:

            response = normal_response


            if "Zephyr" in response:

                self.change_suspicion(
                    "Zephyr",
                    18
                )

                self.activity_log.append(
                    f"🔎 {character}'s testimony increased "
                    f"suspicion toward Zephyr."
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


    # ============================================================
    # LIE GENERATOR
    # ============================================================

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


    # ============================================================
    # ACCUSATION
    # ============================================================

    def accuse(self, character):

        if self.game_over:
            return

        # Accusation uses an action if available.
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

        else:

            self.researcher_won = False

            result = (
                f"Incorrect. {character} was not the mole."
            )


        self.last_event = {
            "type": "accusation",
            "result": result
        }


    # ============================================================
    # BEST CURRENT SUSPECT
    # ============================================================

    def best_suspect(self):

        return max(
            self.suspicion,
            key=self.suspicion.get
        )
