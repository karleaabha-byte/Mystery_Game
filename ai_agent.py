import random


# ============================================================
# MOLE AI
# ============================================================

class MoleAI:

    def __init__(self, name):

        self.name = name


    # ========================================================
    # QUESTION STRATEGY
    # ========================================================

    def choose_question_strategy(self, suspicion):

        if suspicion < 30:

            options = [
                "lie",
                "lie",
                "truth",
                "help"
            ]

        elif suspicion < 60:

            options = [
                "truth",
                "lie",
                "help",
                "truth"
            ]

        else:

            options = [
                "truth",
                "help",
                "help",
                "truth"
            ]

        return random.choice(options)


    # ========================================================
    # ROOM STRATEGY
    # ========================================================

    def choose_room_strategy(self, room, suspicion):

        # Laboratory is NEVER sabotaged.
        # It contains the most important clue.
        if room == "Laboratory":
            return "none"


        # Cafeteria sabotage is deliberately limited.
        if room == "Cafeteria":

            if suspicion < 30:

                options = [
                    "sabotage_cafeteria",
                    "none",
                    "none",
                    "none"
                ]

            elif suspicion < 60:

                options = [
                    "sabotage_cafeteria",
                    "none",
                    "none",
                    "none",
                    "help"
                ]

            else:

                options = [
                    "none",
                    "none",
                    "help",
                    "help"
                ]

            return random.choice(options)


        # Storage manipulation is also limited.
        if room == "Storage":

            if suspicion < 30:

                options = [
                    "manipulate_riddle",
                    "none",
                    "none",
                    "none"
                ]

            elif suspicion < 60:

                options = [
                    "manipulate_riddle",
                    "none",
                    "none",
                    "help"
                ]

            else:

                options = [
                    "none",
                    "none",
                    "help"
                ]

            return random.choice(options)


        return "none"
