# case.py

CHARACTERS = [
    "Raven",
    "Zephyr",
    "Luca",
    "Marinette",
    "Adrien"
]

MOLE = "Zephyr"

MAX_ACTIONS = 12


# ============================================================
# ROOM DATA
# ============================================================

ROOMS = {

    "Laboratory": {

        "icon": "🧪",

        "description":
            "A dim research laboratory. Equipment is still running "
            "despite the evacuation.",

        "object":
            "A researcher's desk covered with papers, samples and "
            "an incident report.",

        "normal_clue": {

            "type": "lab_note",

            "title": "INCIDENT REPORT #047",

            "date": "17 OCTOBER — 23:40",

            "lines": [
                ("23:40", "Power fluctuation detected."),
                ("23:42", "Security alarm activated."),
                ("23:43", "Research equipment checked."),
                ("23:46", "Restricted storage terminal accessed."),
                ("23:49", "Cafeteria security cameras went offline.")
            ],

            "note": (
                "the emergency response system recorded a strange sequence. "
                "the technician who reviewed the access trail wrote the "
                "following note:\n\n"

                "there was no forced entry into the restricted systems. "
                "the person already knew the access route. "
                "the security terminal registered an unfamiliar pattern. "
                "the maintenance team could not explain it. "
                "the access record was later checked against survivor logs. "
                "the final entry remained unexplained.\n\n"

                "Look carefully at the capitalization in this note."
            ),

            "capital_clue": (
                "the emergency response system recorded a strange sequence. "
                "the technician who reviewed the access trail wrote the "
                "following note:\n\n"

                "there was no forced entry into the restricted systems. "
                "the person already knew the access route. "
                "the security terminal registered an unfamiliar pattern. "
                "the maintenance team could not explain it. "
                "the access record was later checked against survivor logs. "
                "the final entry remained unexplained.\n\n"

                "Look carefully at the capitalization in this note."
            ),

            "hidden_message": "ZEPHYR",

            "note_explanation": (
                "The capital letters hidden inside the field note spell "
                "ZEPHYR. This strongly suggests that Zephyr had access "
                "to the systems used during the sabotage."
            ),

            "signature": "— Dr. Morgan"
        }
    },


    "Storage": {

        "icon": "📦",

        "description":
            "Boxes of emergency supplies are stacked against the walls. "
            "Something has been disturbed.",

        "object":
            "A battered metal box marked RESTRICTED.",

        "normal_clue": {

            "type": "riddle",

            "title": "HANDWRITTEN NOTE — BOX 17",

            "text": (
                "I have no feet, but I can follow.\n"
                "I have no mouth, but I can warn.\n"
                "I disappear when the lights go out.\n\n"
                "What am I?"
            ),

            "hint": (
                "Underneath the riddle is a handwritten reminder:\n\n"
                "\"Think about what follows you when you investigate.\""
            ),

            "answer": "A shadow",

            "extra_clue": (
                "Beside the riddle is a storage access slip. "
                "It shows that Box 17 was opened shortly before "
                "the cafeteria cameras failed.\n\n"
                "The initials on the access slip are: Z.R."
            ),

            "manipulated_clue": (
                "The riddle has been altered, but the storage access "
                "slip underneath it is still readable.\n\n"
                "ACCESS TIME: 23:44\n"
                "AUTHORIZED INITIALS: Z.R.\n\n"
                "The tampering changes the riddle, but not the access record."
            )
        }
    },


    "Cafeteria": {

        "icon": "🍔",

        "description":
            "An abandoned cafeteria. The emergency vending machine "
            "is still powered on.",

        "object":
            "An old Survivor Supply vending machine.",

        "normal_clue": {

            "type": "vending",

            "title": "SURVIVOR SUPPLY UNIT",

            "instruction":
                "Emergency PIN = number of survivors × 2",

            "survivors": 5,

            "pin": "10",

            "note":
                "Maintenance note: The emergency system was accessed "
                "shortly before the security cameras went offline.",

            "pin_clue": (
                "PIN CLUE:\n"
                "The emergency PIN is 10.\n\n"
                "The maintenance access log shows that PIN 10 was "
                "successfully entered from the terminal assigned to "
                "survivor ZEPHYR.\n\n"
                "The PIN itself opens the supply unit, while the access "
                "record identifies who used it."
            ),

            "sabotaged_pin_clue": (
                "The maintenance note has been damaged, but the "
                "vending machine still displays the emergency PIN: 10.\n\n"
                "A surviving fragment of the access log reads:\n\n"
                "LAST SUCCESSFUL USER: ZEPHYR\n"
                "PIN: 10\n\n"
                "The sabotage removed some details, but the important "
                "access information remains readable."
            )
        }
    }
}


# ============================================================
# QUESTIONS
# ============================================================

QUESTIONS = [

    "Where were you when the security alarm went off?",

    "Did you notice anything suspicious?",

    "Did you enter the cafeteria today?",

    "Do you know anything about the missing supplies?",

    "Who do you trust the least?"
]


# ============================================================
# CHARACTER RESPONSES
# ============================================================

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
            "No. Everything seemed completely normal to me.",

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
