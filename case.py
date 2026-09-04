# case.py

CHARACTERS = [
    "Raven",
    "Zephyr",
    "Luca",
    "Marinette",
    "Adrien"
]

# Fixed mole for the current case
MOLE = "Zephyr"

MAX_ACTIONS = 12


ROOMS = {
    "Laboratory": {
        "description": (
            "A research laboratory filled with equipment, "
            "notes and computers."
        ),
        "clue": (
            "You find a handwritten note on a laboratory desk.\n\n"
            "Most of the note looks ordinary, but several letters "
            "are strangely capitalized.\n\n"
            "The capitalized letters spell:\n\n"
            "Z E P H Y R"
        )
    },

    "Storage": {
        "description": (
            "A storage room containing emergency supplies "
            "and research materials."
        ),
        "clue": (
            'You find a locked box containing a riddle:\n\n'
            '"I move without legs,\n'
            'I speak without a mouth,\n'
            'I disappear when you find me.\n\n'
            'What am I?"'
        )
    },

    "Cafeteria": {
        "description": (
            "An abandoned cafeteria containing an old "
            "vending machine."
        ),
        "clue": (
            "Beside the vending machine you find a note:\n\n"
            '"The PIN is the number of survivors currently '
            'inside the facility multiplied by 2."\n\n'
            "There are 5 survivors.\n\n"
            "PIN = 10"
        )
    }
}


QUESTIONS = [
    "Where were you when the security alarm went off?",
    "Did you notice anything suspicious?",
    "Did you enter the cafeteria today?",
    "Do you know anything about the missing supplies?",
    "Who do you trust the least?"
]


CHARACTER_RESPONSES = {

    "Raven": {
        QUESTIONS[0]:
            "I was in the laboratory checking the research equipment.",

        QUESTIONS[1]:
            "I thought I heard someone near the cafeteria.",

        QUESTIONS[2]:
            "Yes, briefly. I was looking for water.",

        QUESTIONS[3]:
            "No. I only noticed that some supplies were missing.",

        QUESTIONS[4]:
            "Zephyr has been acting unusually quiet."
    },

    "Zephyr": {
        QUESTIONS[0]:
            "I was in my quarters. I didn't hear anything.",

        QUESTIONS[1]:
            "No. Everything seemed normal to me.",

        QUESTIONS[2]:
            "No, I stayed away from the cafeteria.",

        QUESTIONS[3]:
            "I saw Luca near the storage area earlier.",

        QUESTIONS[4]:
            "Raven. She seems to be investigating everyone."
    },

    "Luca": {
        QUESTIONS[0]:
            "I was helping organize supplies in storage.",

        QUESTIONS[1]:
            "I saw someone leaving the cafeteria.",

        QUESTIONS[2]:
            "No, I was mostly in storage.",

        QUESTIONS[3]:
            "Some equipment was moved without my permission.",

        QUESTIONS[4]:
            "I don't completely trust Zephyr."
    },

    "Marinette": {
        QUESTIONS[0]:
            "I was in the laboratory with Raven.",

        QUESTIONS[1]:
            "The vending machine was behaving strangely.",

        QUESTIONS[2]:
            "Yes, but only for a minute.",

        QUESTIONS[3]:
            "No, I haven't touched the supplies.",

        QUESTIONS[4]:
            "I'm not sure yet."
    },

    "Adrien": {
        QUESTIONS[0]:
            "I was checking the main hallway.",

        QUESTIONS[1]:
            "I heard a noise coming from storage.",

        QUESTIONS[2]:
            "Yes, I went there earlier.",

        QUESTIONS[3]:
            "I saw some boxes moved around.",

        QUESTIONS[4]:
            "Luca was acting nervous earlier."
    }
}
