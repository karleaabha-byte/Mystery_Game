# ai_agent.py

import random


class MoleAI:

    def __init__(self, name):
        self.name = name

    def choose_question_strategy(self, suspicion):
        """
        Decide how the mole responds to questioning.

        The AI adapts its behaviour according to
        the current suspicion level.
        """

        # Low suspicion:
        # The mole is relatively safe and can deceive.
        if suspicion < 30:

            options = [
                "lie",
                "lie",
                "truth",
                "help"
            ]

        # Medium suspicion:
        # The mole becomes more cautious.
        elif suspicion < 60:

            options = [
                "truth",
                "lie",
                "help",
                "truth"
            ]

        # High suspicion:
        # The mole prioritizes maintaining its cover.
        else:

            options = [
                "truth",
                "help",
                "help",
                "truth"
            ]

        return random.choice(options)

    def choose_room_strategy(self, room, suspicion):
        """
        Decide how the mole reacts when the researcher
        investigates a room.

        AI actions do NOT consume researcher actions.
        """

        # Cafeteria
        if room == "Cafeteria":

            if suspicion < 30:

                options = [
                    "sabotage_cafeteria",
                    "none",
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

        # Storage
        if room == "Storage":

            if suspicion < 30:

                options = [
                    "manipulate_riddle",
                    "none",
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

        # Laboratory
        return "none"
