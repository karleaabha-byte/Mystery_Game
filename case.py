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
            "A dim research laboratory. Equipment is still running "
            "despite the evacuation."
        ),
        "object": (
            "A researcher’s desk covered with papers, samples and "
            "an incident report."
        ),
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
                "The person responsible knew exactly which systems "
                "to disable. Check the maintenance records before "
                "trusting anyone's story."
            ),
            "maintenance_note": (
                "Before leaving, verify the following:\n\n"
                "The technician must carry the proper identification.\n"
                "Access logs should be checked before equipment is moved.\n"
                "Keep restricted doors secured during an evacuation.\n"
                "Do not leave temporary credentials beside an active terminal.\n"
                "Every unusual access should be recorded."
            ),
            "signature": "— Dr. Morgan"
        }
    },

    "Storage": {
        "icon": "📦",
        "description": (
            "Boxes of emergency supplies are stacked against the walls. "
            "Something has been disturbed."
        ),
        "object": "A battered metal box marked RESTRICTED.",
        "normal_clue": {
            "type": "storage_log",
            "title": "RESTRICTED STORAGE ACCESS LOG",
            "entries": [
                "23:43 — Storage inspection completed.",
                "23:46 — Restricted terminal accessed.",
                "23:46 — Access badge detected: Z-07.",
                "23:47 — Restricted container opened.",
                "23:48 — Container closed."
            ],
            "note": (
                "The log does not identify the person carrying the badge. "
                "Only the badge identifier was recorded."
            ),
            "secondary_note": (
                "A handwritten note on the container reads:\n\n"
                "\"If you're looking for the person, don't start with the name. "
                "Start with the record.\""
            )
        }
    },

    "Cafeteria": {
        "icon": "🍔",
        "description": (
            "An abandoned cafeteria. The emergency vending machine "
            "is still powered on."
        ),
        "object": "An old Survivor Supply vending machine.",
        "normal_clue": {
            "type": "vending",
            "title": "SURVIVOR SUPPLY UNIT",
            "instruction": "Emergency PIN = number of survivors × 2",
            "survivors": 5,
            "terminal_id": "Z-07",
            "note": (
                "Maintenance note: The emergency system was accessed "
                "shortly before the security cameras went offline."
            ),
            "system_log": (
                "23:49 — Emergency access terminal activated.\n"
                "23:49 — Terminal ID: Z-07\n"
                "23:50 — Security camera network unavailable."
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
