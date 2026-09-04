CHARACTERS = [
    "Raven",
    "Zephyr",
    "Luca",
    "Marinette",
    "Adrien"
]

MOLE = "Zephyr"

MAX_ACTIONS = 12


ROOMS = {

    "Laboratory": {
        "icon": "🧪",
        "description": (
            "A dim research laboratory. Emergency lights pulse over "
            "equipment that should have been shut down during evacuation."
        ),
        "object": (
            "A researcher's desk containing the incident report and "
            "a handwritten maintenance checklist."
        ),

        "clue": {
            "type": "lab_report",
            "title": "INCIDENT REPORT #047",
            "date": "17 OCTOBER — NIGHT SHIFT",

            "events": [
                ("23:40", "Power fluctuation detected."),
                ("23:42", "Security alarm activated."),
                ("23:43", "Research equipment checked."),
                ("23:46", "Restricted storage terminal accessed."),
                ("23:49", "Cafeteria security cameras went offline.")
            ],

            "note": (
                "The failures did not occur randomly. Each affected "
                "system was accessed separately, several minutes apart."
            ),

            "maintenance": [
                "Restricted systems require an authorized badge.",
                "Terminal identifiers are recorded automatically.",
                "Temporary credentials must never be left unattended.",
                "Security camera controls are located in the cafeteria."
            ],

            "signature": "— Dr. Morgan"
        }
    },


    "Storage": {
        "icon": "📦",
        "description": (
            "Emergency supplies are stacked against the walls. "
            "One restricted container appears to have been opened recently."
        ),
        "object": (
            "A battered metal container labelled RESTRICTED."
        ),

        "clue": {
            "type": "storage_log",
            "title": "RESTRICTED STORAGE ACCESS",

            "entries": [
                "23:43 — Routine storage inspection completed.",
                "23:46 — Restricted terminal accessed.",
                "23:46 — Badge identifier recorded: Z-07.",
                "23:47 — Restricted container opened.",
                "23:48 — Container secured."
            ],

            "note": (
                "The system records the badge, not the person wearing it."
            ),

            "handwritten": (
                "Maintenance shorthand:\n\n"
                "Z-series badges are issued to personnel with "
                "restricted-system clearance."
            )
        }
    },


    "Cafeteria": {
        "icon": "🍔",
        "description": (
            "An abandoned cafeteria. The emergency vending terminal "
            "is still receiving power."
        ),
        "object": (
            "An old Survivor Supply terminal beside the security console."
        ),

        "clue": {
            "type": "cafeteria_log",
            "title": "EMERGENCY SUPPLY TERMINAL",

            "instruction": (
                "Emergency verification requires the number of survivors × 2."
            ),

            "survivors": 5,

            "terminal_id": "Z-07",

            "system_log": [
                "23:49 — Emergency access terminal activated.",
                "23:49 — Terminal identifier: Z-07.",
                "23:50 — Security camera network unavailable."
            ],

            "note": (
                "The supply terminal and the security camera controls "
                "share the same local access network."
            )
        }
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
            "I heard the alarm and noticed someone moving toward the storage corridor.",

        QUESTIONS[2]:
            "Yes, briefly. I went there looking for water.",

        QUESTIONS[3]:
            "I noticed some emergency supplies were missing, but I didn't touch them.",

        QUESTIONS[4]:
            "Zephyr has been unusually quiet since the alarm."
    },


    "Zephyr": {

        QUESTIONS[0]:
            "I was in my quarters. I didn't hear the alarm clearly.",

        QUESTIONS[1]:
            "No. Everything seemed normal to me.",

        QUESTIONS[2]:
            "No, I stayed away from the cafeteria.",

        QUESTIONS[3]:
            "I heard Luca had been moving things in storage.",

        QUESTIONS[4]:
            "Raven. She seems determined to make everyone suspicious."
    },


    "Luca": {

        QUESTIONS[0]:
            "I was in storage checking the emergency supplies.",

        QUESTIONS[1]:
            "I heard someone near the storage terminal around the time of the alarm.",

        QUESTIONS[2]:
            "No. I stayed mostly in storage.",

        QUESTIONS[3]:
            "Some boxes had definitely been moved without my permission.",

        QUESTIONS[4]:
            "I don't completely trust Zephyr."
    },


    "Marinette": {

        QUESTIONS[0]:
            "I was in the laboratory with Raven for part of the incident.",

        QUESTIONS[1]:
            "The vending terminal was behaving strangely after the alarm.",

        QUESTIONS[2]:
            "Yes, but only briefly.",

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
            "Yes, I went through the cafeteria earlier.",

        QUESTIONS[3]:
            "I saw several boxes moved around.",

        QUESTIONS[4]:
            "Luca was acting nervous earlier."
    }
}
