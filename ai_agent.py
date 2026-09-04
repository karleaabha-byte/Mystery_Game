import random


class MoleAI:

    def __init__(self, name):
        self.name = name

    def choose_question_strategy(self, suspicion):

        if suspicion < 20:
            options = [
                "truth",
                "truth",
                "truth",
                "lie"
            ]

        elif suspicion < 50:
            options = [
                "truth",
                "truth",
                "lie",
                "lie",
                "partial"
            ]

        elif suspicion < 75:
            options = [
                "lie",
                "lie",
                "partial",
                "partial",
                "truth"
            ]

        else:
            options = [
                "lie",
                "lie",
                "lie",
                "partial"
            ]

        return random.choice(options)


    def choose_room_strategy(self, room, suspicion):

        # The laboratory is the foundational evidence.
        # Never sabotage it.
        if room == "Laboratory":
            return "normal"


        if room == "Storage":

            if suspicion < 30:
                options = [
                    "normal",
                    "normal",
                    "normal",
                    "normal",
                    "distort"
                ]

            elif suspicion < 60:
                options = [
                    "normal",
                    "normal",
                    "normal",
                    "distort",
                    "distort"
                ]

            else:
                options = [
                    "normal",
                    "distort",
                    "distort",
                    "distort"
                ]

            return random.choice(options)


        if room == "Cafeteria":

            if suspicion < 30:
                options = [
                    "normal",
                    "normal",
                    "normal",
                    "normal",
                    "partial"
                ]

            elif suspicion < 60:
                options = [
                    "normal",
                    "normal",
                    "partial",
                    "partial"
                ]

            else:
                options = [
                    "normal",
                    "partial",
                    "partial"
                ]

            return random.choice(options)


        return "normal"
