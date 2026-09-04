# app.py

import streamlit as st

from game import Game

from case import (
    CHARACTERS,
    ROOMS,
    QUESTIONS
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Who Is the Mole?",
    page_icon="🧟",
    layout="wide"
)


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #101010;
    }

    .title {
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        letter-spacing: 4px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .action-counter {
        border: 3px solid white;
        padding: 15px;
        text-align: center;
        font-size: 26px;
        font-weight: bold;
        margin-bottom: 25px;
    }

    .card {
        border: 2px solid #777;
        padding: 15px;
        margin-bottom: 10px;
        text-align: center;
    }

    .evidence {
        border: 2px dashed #777;
        padding: 20px;
        margin-top: 15px;
    }

    .optimal {
        border: 3px solid #777;
        padding: 20px;
        margin-top: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# INITIALIZE GAME
# ==================================================

if "game" not in st.session_state:

    st.session_state.game = Game()


game = st.session_state.game


# ==================================================
# HEADER
# ==================================================

st.markdown(
    '<div class="title">🧟 WHO IS THE MOLE?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'An Adversarial AI Agent in a Zombie Apocalypse Simulation'
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# ACTION COUNTER
# ==================================================

st.markdown(
    f"""
    <div class="action-counter">
        ACTIONS REMAINING:
        {game.actions_remaining} / {game.max_actions}
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:

    st.header("📁 CASE FILE")

    st.write(
        "**Case:** Zombie Apocalypse Mole Identification"
    )

    st.write(
        "**Setting:** Research Facility"
    )

    st.write(
        "**Role:** Researcher"
    )

    st.divider()

    st.header("📋 Investigation Rules")

    st.write(
        "• Maximum 12 actions"
    )

    st.write(
        "• Visit each room once"
    )

    st.write(
        "• Question each survivor once"
    )

    st.write(
        "• Make a final accusation"
    )

    st.write(
        "• AI decisions do not consume your actions"
    )

    st.divider()

    st.header("🤖 AI MOLE")

    st.write(
        "One survivor is secretly controlled "
        "by an AI agent."
    )

    st.write(
        "The AI adapts its behaviour according "
        "to the researcher's investigation."
    )

    st.divider()

    if st.button(
        "🔄 Restart Investigation"
    ):

        st.session_state.game = Game()

        st.rerun()


# ==================================================
# SURVIVORS
# ==================================================

st.header("👥 SURVIVORS")

columns = st.columns(5)

for i, character in enumerate(CHARACTERS):

    with columns[i]:

        suspicion = game.suspicion[character]

        st.markdown(
            f"""
            <div class="card">
                <h3>{character}</h3>
                <p>Suspicion: {suspicion}%</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# TABS
# ==================================================

room_tab, question_tab, accusation_tab = st.tabs(
    [
        "🚪 INVESTIGATE ROOMS",
        "❓ QUESTION SURVIVORS",
        "⚖️ FINAL ACCUSATION"
    ]
)


# ==================================================
# ROOM TAB
# ==================================================

with room_tab:

    st.subheader(
        "Investigate the Research Facility"
    )

    room_columns = st.columns(3)


    for i, room in enumerate(ROOMS):

        with room_columns[i]:

            st.markdown(
                f"### {room}"
            )

            st.write(
                ROOMS[room]["description"]
            )


            if room in game.visited_rooms:

                st.info(
                    "Already investigated."
                )

            elif game.actions_remaining == 0:

                st.warning(
                    "No actions remaining."
                )

            elif game.game_over:

                st.info(
                    "Investigation ended."
                )

            else:

                if st.button(
                    f"Enter {room}",
                    key=f"enter_{room}"
                ):

                    game.visit_room(room)

                    st.rerun()


    if game.last_result:

        st.markdown(
            '<div class="evidence">',
            unsafe_allow_html=True
        )

        st.subheader(
            "🔎 Investigation Result"
        )

        st.write(
            game.last_result
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ==================================================
# QUESTION TAB
# ==================================================

with question_tab:

    st.subheader(
        "Question the Survivors"
    )

    character = st.selectbox(
        "Choose a survivor",
        CHARACTERS,
        key="character_select"
    )

    question = st.selectbox(
        "Choose one question",
        QUESTIONS,
        key="question_select"
    )


    if character in game.questioned_characters:

        st.warning(
            f"You have already questioned {character}."
        )

    elif game.actions_remaining == 0:

        st.warning(
            "You have no actions remaining."
        )

    elif game.game_over:

        st.info(
            "The investigation has ended."
        )

    else:

        if st.button(
            "Ask Question",
            key="ask_button"
        ):

            game.ask_question(
                character,
                question
            )

            st.rerun()


    if game.last_result:

        st.markdown(
            '<div class="evidence">',
            unsafe_allow_html=True
        )

        st.subheader(
            "💬 Response"
        )

        st.write(
            game.last_result
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# ==================================================
# ACCUSATION TAB
# ==================================================

with accusation_tab:

    st.subheader(
        "⚖️ Make Your Final Accusation"
    )

    st.write(
        "Choose the survivor you believe is secretly "
        "controlled by the AI."
    )


    accused = st.selectbox(
        "Select suspected mole",
        CHARACTERS,
        key="accused"
    )


    if game.game_over:

        if game.researcher_won:

            st.success(
                "🎉 CASE SOLVED — RESEARCHER WINS"
            )

        else:

            st.error(
                "☠️ INVESTIGATION FAILED — MOLE WINS"
            )

        st.write(
            game.last_result
        )

        st.write(
            f"**Actual mole: {game.mole}**"
        )


    elif st.button(
        "⚖️ ACCUSE",
        key="accuse_button"
    ):

        game.accuse(accused)

        st.rerun()


# ==================================================
# EVIDENCE LOG
# ==================================================

st.divider()

st.header("📜 Evidence Log")


if not game.evidence:

    st.write(
        "No evidence collected yet."
    )

else:

    for evidence in game.evidence:

        st.write(
            "🔹 " + evidence
        )


# ==================================================
# ACTIVITY LOG
# ==================================================

st.header("📡 Investigation Activity")


if not game.activity_log:

    st.write(
        "No activity yet."
    )

else:

    for activity in reversed(
        game.activity_log[-10:]
    ):

        st.write(
            "• " + activity
        )


# ==================================================
# AI STATISTICS
# ==================================================

if game.game_over:

    st.divider()

    st.header("🤖 AI Behaviour Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "AI Lies",
            game.ai_lie_count
        )

    with col2:

        st.metric(
            "AI Truths",
            game.ai_truth_count
        )

    with col3:

        st.metric(
            "AI Help",
            game.ai_help_count
        )

    with col4:

        st.metric(
            "AI Sabotage",
            game.ai_sabotage_count
        )
