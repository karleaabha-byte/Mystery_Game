import streamlit as st

from game import Game
from case import (
    CHARACTERS,
    MAX_ACTIONS,
    ROOMS,
    QUESTIONS,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Who Is The Mole?",
    page_icon="🕵️",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:
    st.session_state.game = Game()

if "started" not in st.session_state:
    st.session_state.started = False

if "last_room_result" not in st.session_state:
    st.session_state.last_room_result = None

if "last_response" not in st.session_state:
    st.session_state.last_response = None


game = st.session_state.game


# ============================================================
# FUNCTIONS
# ============================================================

def restart_game():
    st.session_state.game = Game()
    st.session_state.started = True
    st.session_state.last_room_result = None
    st.session_state.last_response = None
    st.rerun()


def get_clue_data(clue):
    if not isinstance(clue, dict):
        return {}

    data = clue.get("data", clue)

    if not isinstance(data, dict):
        return {}

    return data


def render_clue(clue):

    data = get_clue_data(clue)

    clue_type = data.get("type", "")

    # --------------------------------------------------------
    # LABORATORY
    # --------------------------------------------------------

    if clue_type in ("lab_report", "lab_note"):

        st.subheader(
            data.get(
                "title",
                "Incident Report",
            )
        )

        if data.get("date"):
            st.write(
                f"**Date:** {data['date']}"
            )

        events = data.get(
            "events",
            data.get("lines", []),
        )

        if events:

            st.write("### Incident Timeline")

            for event in events:

                if isinstance(
                    event,
                    (tuple, list),
                ) and len(event) >= 2:

                    st.write(
                        f"**{event[0]}** — {event[1]}"
                    )

                else:

                    st.write(
                        f"• {event}"
                    )

        maintenance = data.get(
            "maintenance",
            data.get(
                "maintenance_note",
                "",
            ),
        )

        if maintenance:

            st.write("### Maintenance Note")

            st.info(maintenance)

        if data.get("note"):

            st.write(
                f"**Note:** {data['note']}"
            )

        if data.get("signature"):

            st.caption(
                data["signature"]
            )


    # --------------------------------------------------------
    # STORAGE
    # --------------------------------------------------------

    elif clue_type == "storage_log":

        st.subheader(
            data.get(
                "title",
                "Restricted Storage Access Log",
            )
        )

        entries = data.get(
            "entries",
            [],
        )

        if entries:

            st.write("### Access Log")

            for entry in entries:

                st.write(
                    f"• {entry}"
                )

        if data.get("note"):

            st.info(
                data["note"]
            )

        handwritten = data.get(
            "handwritten",
            data.get(
                "secondary_note",
                "",
            ),
        )

        if handwritten:

            st.write("### Handwritten Note")

            st.warning(
                handwritten
            )


    # --------------------------------------------------------
    # CAFETERIA
    # --------------------------------------------------------

    elif clue_type in (
        "cafeteria_log",
        "vending",
    ):

        st.subheader(
            data.get(
                "title",
                "Cafeteria Security Log",
            )
        )

        if data.get("instruction"):

            st.write(
                f"**System instruction:** "
                f"{data['instruction']}"
            )

        if data.get("survivors") is not None:

            st.write(
                f"**Registered survivors:** "
                f"{data['survivors']}"
            )

        if data.get("terminal_id"):

            st.write(
                f"**Terminal ID:** "
                f"`{data['terminal_id']}`"
            )

        system_log = data.get(
            "system_log",
            "",
        )

        if system_log:

            st.write("### System Log")

            if isinstance(
                system_log,
                (list, tuple),
            ):

                system_log = "\n".join(
                    str(line)
                    for line in system_log
                )

            st.code(
                str(system_log)
            )

        if data.get("note"):

            st.info(
                data["note"]
            )


    # --------------------------------------------------------
    # PARTIAL EVIDENCE
    # --------------------------------------------------------

    elif clue_type == "partial":

        st.warning(
            data.get(
                "message",
                data.get(
                    "note",
                    "Some evidence is missing.",
                ),
            )
        )


    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    else:

        st.subheader(
            "Evidence"
        )

        for key, value in data.items():

            if key == "type":
                continue

            label = key.replace(
                "_",
                " ",
            ).title()

            st.write(
                f"**{label}:** {value}"
            )


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.started:

    st.title("🕵️ WHO IS THE MOLE?")

    st.caption(
        "A closed-room investigation in 12 moves."
    )

    st.divider()

    st.header(
        "Someone inside the team sabotaged the facility."
    )

    st.write(
        """
        At 23:40, the facility suffered a power fluctuation.
        Three minutes later, the security alarm activated.
        """
    )

    st.write(
        """
        By 23:50, restricted storage had been accessed,
        emergency systems had been used, and the cafeteria
        security cameras were offline.
        """
    )

    st.write(
        """
        Five people were inside.
        One of them is lying.
        """
    )

    st.write(
        """
        Your job is not to find a confession.

        Your job is to find the contradictions.
        """
    )

    st.divider()

    st.subheader("How To Play")

    st.write(
        """
        - Search the rooms.
        - Examine the evidence.
        - Question the suspects.
        - Compare their stories.
        - Look for contradictions.
        - Accuse the person you believe is the Mole.
        """
    )

    st.warning(
        "You have a limited number of investigation actions."
    )

    if st.button(
        "🔎 START INVESTIGATION",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.started = True
        st.session_state.game = Game()

        st.rerun()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🕵️ Investigation")

    st.metric(
        "Actions Remaining",
        game.actions_left,
    )

    if MAX_ACTIONS > 0:

        st.progress(
            game.actions_left / MAX_ACTIONS
        )

    st.divider()

    st.subheader("Status")

    st.write(
        f"🧪 Rooms searched: "
        f"{len(game.investigated_rooms)} / {len(ROOMS)}"
    )

    st.write(
        f"🗣️ People questioned: "
        f"{len(game.questioned_characters)} / "
        f"{len(CHARACTERS)}"
    )

    st.write(
        f"📁 Evidence collected: "
        f"{len(game.clues)}"
    )

    if game.investigated_rooms:

        st.divider()

        st.subheader("Searched")

        for room in game.investigated_rooms:

            icon = ROOMS[room].get(
                "icon",
                "📍",
            )

            st.write(
                f"✓ {icon} {room}"
            )

    if game.questioned_characters:

        st.divider()

        st.subheader("Questioned")

        for character in game.questioned_characters:

            st.write(
                f"✓ {character}"
            )

    st.divider()

    if st.button(
        "🔄 Restart Case",
        use_container_width=True,
    ):

        restart_game()


# ============================================================
# HEADER
# ============================================================

st.title("🕵️ WHO IS THE MOLE?")

st.caption(
    "Follow the evidence. Trust nobody."
)


# ============================================================
# GAME OVER
# ============================================================

if game.game_over:

    st.divider()

    if game.last_accusation_correct:

        st.success(
            "🎉 CASE SOLVED"
        )

    else:

        st.error(
            "❌ WRONG ACCUSATION"
        )

    if game.result:

        st.info(
            game.result
        )

    st.header(
        "📁 Evidence Collected"
    )

    if game.clues:

        for index, clue in enumerate(
            game.clues,
            start=1,
        ):

            room = clue.get(
                "room",
                "Unknown",
            )

            with st.expander(
                f"Evidence #{index} — {room}",
                expanded=True,
            ):

                render_clue(clue)

    else:

        st.info(
            "No physical evidence was collected."
        )

    st.divider()

    if st.button(
        "🔁 PLAY AGAIN",
        type="primary",
        use_container_width=True,
    ):

        restart_game()

    st.stop()


# ============================================================
# TABS
# ============================================================

tab_investigate, tab_question, tab_evidence, tab_accuse = st.tabs(
    [
        "🧪 Investigate",
        "🗣️ Question",
        "📁 Evidence",
        "⚖️ Accuse",
    ]
)


# ============================================================
# INVESTIGATE
# ============================================================

with tab_investigate:

    st.header(
        "Investigate Locations"
    )

    st.write(
        "Search a location to discover physical evidence."
    )

    room_names = list(ROOMS.keys())

    columns = st.columns(
        len(room_names)
    )

    for column, room_name in zip(
        columns,
        room_names,
    ):

        room = ROOMS[room_name]

        with column:

            st.subheader(
                f"{room.get('icon', '📍')} "
                f"{room_name}"
            )

            st.write(
                room.get(
                    "description",
                    "No description available.",
                )
            )

            if room_name in game.investigated_rooms:

                st.success(
                    "✓ Already investigated"
                )

            else:

                if st.button(
                    f"Search {room_name}",
                    key=f"search_{room_name}",
                    disabled=(
                        game.actions_left <= 0
                    ),
                    use_container_width=True,
                ):

                    result = game.investigate_room(
                        room_name
                    )

                    st.session_state.last_room_result = (
                        room_name,
                        result,
                    )

                    st.rerun()


    # --------------------------------------------------------
    # LATEST FINDING
    # --------------------------------------------------------

    if st.session_state.last_room_result:

        st.divider()

        st.header(
            "Latest Finding"
        )

        room_name, result = (
            st.session_state.last_room_result
        )

        st.info(
            result
        )

        room_clues = game.get_room_clues(
            room_name
        )

        if room_clues:

            render_clue(
                room_clues[-1]
            )


# ============================================================
# QUESTIONING
# ============================================================

with tab_question:

    st.header(
        "🗣️ Question The Suspects"
    )

    st.write(
        "Each suspect can be questioned once."
    )

    for character in CHARACTERS:

        with st.expander(
            character
        ):

            if character in game.questioned_characters:

                st.success(
                    "You already questioned this person."
                )

                continue

            question = st.selectbox(
                "Choose a question",
                QUESTIONS,
                key=f"question_{character}",
            )

            if st.button(
                f"Question {character}",
                key=f"ask_{character}",
                disabled=(
                    game.actions_left <= 0
                ),
                use_container_width=True,
            ):

                response = game.question_character(
                    character,
                    question,
                )

                st.session_state.last_response = (
                    character,
                    question,
                    response,
                )

                st.rerun()


    # --------------------------------------------------------
    # LATEST RESPONSE
    # --------------------------------------------------------

    if st.session_state.last_response:

        st.divider()

        st.header(
            "Latest Interview"
        )

        character, question, response = (
            st.session_state.last_response
        )

        st.write(
            f"### {character}"
        )

        st.write(
            f"**Question:** {question}"
        )

        st.info(
            f'"{response}"'
        )


# ============================================================
# EVIDENCE BOARD
# ============================================================

with tab_evidence:

    st.header(
        "📁 Evidence Board"
    )

    if not game.clues:

        st.info(
            "No evidence yet. Search a location."
        )

    else:

        for index, clue in enumerate(
            game.clues,
            start=1,
        ):

            room = clue.get(
                "room",
                "Unknown",
            )

            with st.expander(
                f"Evidence #{index} — {room}",
                expanded=True,
            ):

                render_clue(
                    clue
                )

    st.divider()

    st.subheader(
        "🔎 Investigator's Questions"
    )

    st.write(
        """
        When reviewing your evidence, ask yourself:

        **1. What happened?**

        **2. When did it happen?**

        **3. Which identifier appears more than once?**

        **4. Who could realistically have access?**

        **5. Does anyone's story conflict with the records?**

        Don't accuse someone simply because they seem suspicious.
        Build a chain of evidence.
        """
    )


# ============================================================
# ACCUSATION
# ============================================================

with tab_accuse:

    st.header(
        "⚖️ Make Your Accusation"
    )

    st.warning(
        "This is your final decision."
    )

    st.write(
        """
        Before accusing someone, make sure you can connect
        the physical evidence with what the suspects told you.
        """
    )

    accusation = st.selectbox(
        "Who is the Mole?",
        [
            "Select a suspect..."
        ] + CHARACTERS,
        key="accusation",
    )

    if accusation != "Select a suspect...":

        st.write(
            f"### Your choice: {accusation}"
        )

        st.warning(
            "Making this accusation will end the investigation."
        )

    if st.button(
        "⚖️ MAKE FINAL ACCUSATION",
        type="primary",
        disabled=(
            accusation == "Select a suspect..."
        ),
        use_container_width=True,
    ):

        game.accuse(
            accusation
        )

        st.rerun()


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "CASE FILE #047 • Trust the evidence, not the story."
)
