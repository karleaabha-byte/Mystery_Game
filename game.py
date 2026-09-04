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

    def __init__(self, player_name="Researcher"):

        # --------------------------------------------------------
        # PLAYER
        # --------------------------------------------------------

        self.player_name = player_name


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

        if room not in ROOMS:
            return False


        self.use_action(
            f"Investigate {room}"
        )

        self.visited_rooms.add(room)


        # --------------------------------------------------------
        # AI DECISION
        # --------------------------------------------------------

        ai_strategy = self.ai.choose_room_strategy(
            room,
            self.suspicion[self.mole]
        )


        # ========================================================
        # LABORATORY
        # ========================================================

        if room == "Laboratory":

            self.change_suspicion(
                "Zephyr",
                35
            )

            self.evidence.append(
                "LABORATORY: Hidden capital letters in the field "
                "note spell ZEPHYR."
            )

            self.evidence.append(
                "LABORATORY: The access pattern suggests the mole "
                "already knew how to reach restricted systems."
            )

            self.activity_log.append(
                "🧪 Laboratory evidence strongly points toward Zephyr."
            )

            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": False
            }

            return True


        # ========================================================
        # STORAGE
        # ========================================================

        if room == "Storage":

            # Even when manipulated, the important access record
            # remains available.
            if ai_strategy == "manipulate_riddle":

                self.riddle_manipulated = True
                self.ai_sabotage_count += 1

                self.change_suspicion(
                    "Zephyr",
                    15
                )

                self.evidence.append(
                    "STORAGE: The riddle was tampered with, but "
                    "the access slip still shows initials Z.R."
                )

                self.activity_log.append(
                    "⚠ Storage evidence was manipulated, but the "
                    "access record survived."
                )

                self.last_event = {
                    "type": "room",
                    "room": room,
                    "sabotaged": True
                }

                return True


            # Normal storage investigation
            self.change_suspicion(
                "Zephyr",
                20
            )

            self.evidence.append(
                "STORAGE: Box 17 was accessed at 23:44 using "
                "authorized initials Z.R."
            )

            self.activity_log.append(
                "📦 Storage access records point toward Z.R."
            )

            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": False
            }

            return True


        # ========================================================
        # CAFETERIA
        # ========================================================

        if room == "Cafeteria":

            if ai_strategy == "sabotage_cafeteria":

                self.cafeteria_sabotaged = True
                self.ai_sabotage_count += 1

                # Important information survives.
                self.change_suspicion(
                    "Zephyr",
                    20
                )

                self.evidence.append(
                    "CAFETERIA: The vending-machine note was damaged, "
                    "but the surviving access record identifies ZEPHYR."
                )

                self.activity_log.append(
                    "⚠ Cafeteria evidence was partially damaged, "
                    "but the PIN and user record remain usable."
                )

                self.last_event = {
                    "type": "room",
                    "room": room,
                    "sabotaged": True
                }

                return True


            # Normal cafeteria evidence
            self.change_suspicion(
                "Zephyr",
                20
            )

            self.evidence.append(
                "CAFETERIA: Emergency PIN is 10. The access log "
                "records ZEPHYR as the last successful user."
            )

            self.activity_log.append(
                "🍔 Cafeteria access records point toward Zephyr."
            )

            self.last_event = {
                "type": "room",
                "room": room,
                "sabotaged": False
            }

            return True


        return False


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

        if character not in CHARACTERS:
            return False

        if question not in QUESTIONS:
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
                    -8
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

        if character not in CHARACTERS:
            return


        # Accusation uses one action if available.
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
