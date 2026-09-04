import random

#controller
class MoleAI:

    def __init__(self, name):
        self.name = name

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

    def choose_room_strategy(self, room, suspicion):

        if room == "Cafeteria":

            if suspicion < 30:
                options = [
                    "sabotage_cafeteria",
                    "sabotage_cafeteria",
                    "none"
                ]

            elif suspicion < 60:
                options = [
                    "sabotage_cafeteria",
                    "none",
                    "help",
                    "none"
                ]

            else:
                options = [
                    "help",
                    "none",
                    "none"
                ]

            return random.choice(options)

        if room == "Storage":

            if suspicion < 30:
                options = [
                    "manipulate_riddle",
                    "manipulate_riddle",
                    "none"
                ]

            elif suspicion < 60:
                options = [
                    "manipulate_riddle",
                    "help",
                    "none",
                    "none"
                ]

            else:
                options = [
                    "help",
                    "none",
                    "none"
                ]

            return random.choice(options)

        return "none"
