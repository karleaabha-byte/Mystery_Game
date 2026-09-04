import random


class MoleAI:
    def __init__(self, name):
        self.name = name

    def choose_question_strategy(self, suspicion):
        if suspicion < 30:
            options = [
                "truth",
                "truth",
                "lie",
                "help"
            ]

        elif suspicion < 60:
            options = [
                "truth",
                "truth",
                "lie",
                "help",
                "help"
            ]

        else:
            options = [
                "truth",
                "truth",
                "help",
                "help",
                "truth"
            ]

        return random.choice(options)

    def choose_room_strategy(self, room, suspicion):
        # The Laboratory contains the foundational clue.
        # Never sabotage it.
        if room == "Laboratory":
            return "none"

        if room == "Cafeteria":
            if suspicion < 30:
                options = [
                    "none",
                    "none",
                    "none",
                    "none",
                    "sabotage_cafeteria"
                ]

            elif suspicion < 60:
                options = [
                    "none",
                    "none",
                    "none",
                    "none",
                    "none",
                    "sabotage_cafeteria"
                ]

            else:
                options = [
                    "none",
                    "none",
                    "none",
                    "help",
                    "none"
                ]

            return random.choice(options)

        if room == "Storage":
            if suspicion < 30:
                options = [
                    "none",
                    "none",
                    "none",
                    "none",
                    "manipulate_riddle"
                ]

            elif suspicion < 60:
                options = [
                    "none",
                    "none",
                    "none",
                    "none",
                    "none",
                    "manipulate_riddle"
                ]

            else:
                options = [
                    "none",
                    "none",
                    "none",
                    "help"
                ]

            return random.choice(options)

        return "none"
