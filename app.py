import streamlit as st

from case import (
    CHARACTERS,
    ROOMS,
    QUESTIONS,
    MAX_ACTIONS
)

from game import Game


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Who Is The Mole?",
    page_icon="🕵️",
    layout="wide"
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "game" not in st.session_state:
    st.session_state.game = None

if "player_name" not in st.session_state:
    st.session_state.player_name = ""

if "selected_character" not in st.session_state:
    st.session_state.selected_character = None

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .main-title {
        font-size: 3.2rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .room-card {
        border: 1px solid #333;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 12px;
        background-color: rgba(255,255,255,0.02);
    }

    .character-card {
        border: 1px solid #333;
        border-radius: 12px;
        padding: 15px;
        background-color: rgba(255,255,255,0.02);
    }

    .action-box {
        border: 1px solid #444;
        border-radius: 10px;
        padding: 12px;
        text-align: center;
    }

    .clue-box {
        border-left: 4px solid #888;
        padding: 12px 16px;
        margin: 10px 0;
        background-color: rgba(255,255,255,0.03);
        border-radius: 6px;
    }

    .warning-box {
        border: 1px solid #7a5a00;
        border-radius: 10px;
        padding: 12px;
        background-color: rgba(255,180,0,0.05);
    }

    .success-box {
        border: 1px solid #26734d;
        border-radius: 10px;
        padding: 15px;
        background-color: rgba(0,180,100,0.05);
    }

    .danger-box {
        border: 1px solid #8b3030;
        border-radius: 10px;
        padding: 15px;
        background-color: rgba(200,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# START SCREEN
# ---------------------------------------------------------

if st.session_state.game is None:

    st.markdown(
        '<div class="main-title">🕵️ WHO IS THE MOLE?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A mystery of sabotage, deception and deduction.</div>',
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("## 🔐 Mission Briefing")

    st.write(
        """
        Something has gone wrong inside the facility.

        Systems were accessed without authorization.
        Supplies have been disturbed.
        Security cameras went offline.

        One person among the survivors is secretly working against you.

        **Your job is to investigate the facility, question the survivors,
        connect the evidence, and identify the Mole.**
        """
    )

    st.warning(
        "You have a limited number of actions. Choose carefully."
    )

    st.write("### Researcher identification")

    player_name = st.text_input(
        "Enter your name:",
        placeholder="e.g. Alex",
        max_chars=30
    )

    if st.button(
        "🚪 Enter the Facility",
        type="primary",
        use_container_width=True
    ):
        if not player_name.strip():
            st.error("Enter your name first.")
        else:
            st.session_state.player_name = player_name.strip()
            st.session_state.game = Game(
                player_name=st.session_state.player_name
            )
            st.rerun()

    st.stop()


# ---------------------------------------------------------
# GAME OBJECT
# ---------------------------------------------------------

game = st.session_state.game


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">🕵️ WHO IS THE MOLE?</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="subtitle">Researcher: {game.player_name}</div>',
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# STATUS BAR
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Actions Remaining",
        game.get_remaining_actions()
    )

with col2:
    st.metric(
        "Rooms Investigated",
        len(game.investigated_rooms)
    )

with col3:
    st.metric(
        "People Questioned",
        len(game.questioned_characters)
    )


st.divider()


# ---------------------------------------------------------
# GAME OVER
# ---------------------------------------------------------

if game.game_over:

    if game.accusation == "Zephyr":
        st.success("## ✅ Case Solved")
        st.write(game.result)
    else:
        st.error("## ❌ Incorrect Accusation")
        st.write(game.result)

    st.divider()

    st.write("### Investigation Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Rooms investigated:**")
        if game.investigated_rooms:
            for room in game.investigated_rooms:
                st.write(f"- {room}")
        else:
            st.write("None")

    with col2:
        st.write("**People questioned:**")
        if game.questioned_characters:
            for character in game.questioned_characters:
                st.write(f"- {character}")
        else:
            st.write("None")

    if st.button(
        "🔄 Start a New Investigation",
        use_container_width=True
    ):
        st.session_state.game = None
        st.session_state.player_name = ""
        st.session_state.selected_character = None
        st.session_state.selected_question = None
        st.rerun()

    st.stop()


# ---------------------------------------------------------
# MAIN TABS
# ---------------------------------------------------------

tab1, tab2, tab3 = st.tabs(
    [
        "🗺️ Investigate",
        "🗣️ Question Survivors",
        "📋 Evidence"
    ]
)


# =========================================================
# INVESTIGATE TAB
# =========================================================

with tab1:

    st.subheader("🗺️ Facility Investigation")

    st.write(
        "Choose a location to investigate. Each investigation costs one action."
    )

    room_columns = st.columns(len(ROOMS))

    for index, (room_name, room) in enumerate(ROOMS.items()):

        with room_columns[index]:

            st.markdown(
                f"""
                <div class="room-card">
                <h3>{room["icon"]} {room_name}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write(room["description"])

            st.caption(
                f"Object of interest: {room['object']}"
            )

            if room_name in game.investigated_rooms:

                st.success("Investigated")

            else:

                if st.button(
                    f"Investigate {room_name}",
                    key=f"investigate_{room_name}",
                    disabled=game.get_remaining_actions() <= 0,
                    use_container_width=True
                ):
                    message = game.investigate_room(room_name)

                    st.session_state.last_action = message

                    st.rerun()


# =========================================================
# QUESTION TAB
# =========================================================

with tab2:

    st.subheader("🗣️ Question the Survivors")

    st.write(
        "Ask questions and compare everyone's stories. "
        "Not everyone will tell you the whole truth."
    )

    character_columns = st.columns(len(CHARACTERS))

    for index, character in enumerate(CHARACTERS):

        with character_columns[index]:

            st.markdown(
                f"""
                <div class="character-card">
                <h3>{character}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            if character in game.questioned_characters:
                st.caption("Previously questioned")

            question = st.selectbox(
                "Question",
                QUESTIONS,
                key=f"question_{character}"
            )

            if st.button(
                f"Question {character}",
                key=f"ask_{character}",
                disabled=game.get_remaining_actions() <= 0,
                use_container_width=True
            ):

                response = game.question_character(
                    character,
                    question
                )

                st.session_state[f"response_{character}"] = response

                st.rerun()

            if f"response_{character}" in st.session_state:

                st.markdown("**Response:**")

                st.info(
                    st.session_state[f"response_{character}"]
                )


# =========================================================
# EVIDENCE TAB
# =========================================================

with tab3:

    st.subheader("📋 Evidence Board")

    clues = game.get_clues()

    if not clues:

        st.info(
            "No evidence collected yet. Investigate locations to begin."
        )

    else:

        for clue in clues:

            room_name = clue["room"]
            clue_type = clue["type"]
            data = clue["data"]

            st.markdown(
                f'<div class="clue-box"><strong>{room_name}</strong></div>',
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # LABORATORY
            # -------------------------------------------------

            if clue_type == "lab_note":

                st.subheader(data["title"])

                st.caption(data["date"])

                for timestamp, line in data["lines"]:
                    st.write(
                        f"**{timestamp}** — {line}"
                    )

                st.write("---")

                st.write(data["note"])

                st.write("### Maintenance Note")

                st.code(
                    data["maintenance_note"],
                    language="text"
                )

                st.caption(data["signature"])

                st.info(
                    "Something about the maintenance note may be worth examining closely."
                )

            # -------------------------------------------------
            # STORAGE
            # -------------------------------------------------

            elif clue_type == "storage_log":

                st.subheader(data["title"])

                for entry in data["entries"]:
                    st.write(entry)

                st.write("---")

                st.write(data["note"])

                st.write(data["secondary_note"])

            # -------------------------------------------------
            # CAFETERIA
            # -------------------------------------------------

            elif clue_type == "vending":

                st.subheader(data["title"])

                st.write(
                    f"**Instruction:** {data['instruction']}"
                )

                st.write(
                    f"**Survivors:** {data['survivors']}"
                )

                st.write(
                    f"**Terminal identifier:** `{data['terminal_id']}`"
                )

                st.write(data["note"])

                st.write("### System Log")

                st.code(
                    data["system_log"],
                    language="text"
                )

                st.info(
                    "Work out what the emergency system was doing "
                    "and compare its identifier with the other evidence."
                )

            # -------------------------------------------------
            # PARTIAL / SABOTAGED EVIDENCE
            # -------------------------------------------------

            elif clue_type == "partial":

                st.subheader(data["title"])

                if "instruction" in data:
                    st.write(
                        f"**Instruction:** {data['instruction']}"
                    )

                if "survivors" in data:
                    st.write(
                        f"**Survivors:** {data['survivors']}"
                    )

                if "terminal_id" in data:
                    st.write(
                        f"**Terminal identifier:** `{data['terminal_id']}`"
                    )

                if "entries" in data:
                    for entry in data["entries"]:
                        st.write(entry)

                if "note" in data:
                    st.write(data["note"])

            st.divider()


# ---------------------------------------------------------
# ACCUSATION SECTION
# ---------------------------------------------------------

st.subheader("⚖️ Make Your Accusation")

st.write(
    "When you're confident you've connected the evidence, "
    "choose who you believe is the Mole."
)

accuse_col1, accuse_col2 = st.columns([2, 1])

with accuse_col1:

    accusation = st.selectbox(
        "Who is the Mole?",
        CHARACTERS,
        key="accusation_select"
    )

with accuse_col2:

    st.write("")
    st.write("")

    if st.button(
        "⚠️ ACCUSE",
        type="primary",
        use_container_width=True,
        disabled=game.get_remaining_actions() <= 0
    ):

        game.accuse(accusation)
        st.rerun()


# ---------------------------------------------------------
# ACTION WARNING
# ---------------------------------------------------------

if game.get_remaining_actions() <= 3 and game.get_remaining_actions() > 0:

    st.warning(
        f"⚠️ Only {game.get_remaining_actions()} actions remaining. "
        "Choose your next move carefully."
    )

elif game.get_remaining_actions() == 0:

    st.error(
        "You have used all of your actions. "
        "You must make an accusation."
    )
