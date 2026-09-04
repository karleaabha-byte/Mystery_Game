import streamlit as st

from game import Game
from case import CHARACTERS, ROOMS, QUESTIONS


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Who Is The Mole?",
    page_icon="🧟",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:
    st.session_state.game = Game()

game = st.session_state.game


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background: #0b0b0b;
    color: #eeeeee;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* Main title */

.main-title {
    text-align: center;
    font-size: 3rem;
    font-weight: 900;
    letter-spacing: 5px;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #888888;
    letter-spacing: 2px;
    margin-bottom: 2rem;
}

/* Cards */

.card {
    background: #171717;
    border: 1px solid #3d3d3d;
    border-radius: 8px;
    padding: 1.2rem;
    margin-bottom: 1rem;
}

.card-title {
    font-size: 1.3rem;
    font-weight: 700;
}

.muted {
    color: #999999;
}

/* Action counter */

.action-container {
    background: #151515;
    border: 2px solid #555555;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    margin-bottom: 2rem;
}

.action-number {
    font-size: 2.5rem;
    font-weight: 900;
}

.action-label {
    color: #888888;
    font-size: 0.75rem;
    letter-spacing: 3px;
}

/* Evidence */

.evidence {
    background: #1b1b1b;
    border-left: 4px solid #888888;
    padding: 1rem;
    margin: 0.5rem 0;
    border-radius: 4px;
}

/* Paper */

.paper {
    background: #ddd5bd;
    color: #29251d;
    padding: 2rem;
    border-radius: 4px;
    font-family: Georgia, serif;
}

/* Riddle */

.riddle {
    background: #cfc6ae;
    color: #25221c;
    padding: 2rem;
    border-radius: 5px;
    text-align: center;
    font-family: Georgia, serif;
    font-size: 1.1rem;
}

/* Warning */

.warning-box {
    background: #291717;
    border: 1px solid #784646;
    padding: 1rem;
    border-radius: 5px;
}

/* Success */

.success-box {
    background: #142417;
    border: 1px solid #4d8054;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
}

/* Failure */

.failure-box {
    background: #291717;
    border: 1px solid #8c4c4c;
    padding: 2rem;
    border-radius: 8px;
    text-align: center;
}

/* Optimal path */

.path-step {
    background: #191919;
    border-left: 3px solid #888888;
    padding: 0.8rem;
    margin: 0.4rem 0;
    border-radius: 3px;
}

/* Buttons */

.stButton > button {
    border-radius: 5px;
    font-weight: 700;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #111111;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧟 WHO IS THE MOLE?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'ADVERSARIAL AI AGENT • ZOMBIE APOCALYPSE SIMULATION'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ACTION COUNTER
# ============================================================

st.markdown(
    f"""
    <div class="action-container">
        <div class="action-label">
            INVESTIGATION ACTIONS REMAINING
        </div>

        <div class="action-number">
            {game.actions_remaining}
            <span style="font-size:1.2rem;color:#777;">
                / {game.max_actions}
            </span>
        </div>

        <div class="action-label">
            MAXIMUM INVESTIGATION BUDGET
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("📁 CASE FILE")

    st.write("**CASE**")
    st.write("Zombie Apocalypse Mole Identification")

    st.write("**LOCATION**")
    st.write("Research Facility")

    st.write("**ROLE**")
    st.write("Researcher")

    st.divider()

    st.subheader("🎯 OBJECTIVE")

    st.write(
        "Identify the survivor secretly controlled "
        "by the adversarial AI."
    )

    st.divider()

    st.subheader("📋 RULES")

    st.write("• Maximum 12 actions")
    st.write("• Each room can be investigated once")
    st.write("• Each survivor can be questioned once")
    st.write("• AI actions do not consume your actions")
    st.write("• Accuse the suspected mole when ready")

    st.divider()

    st.subheader("🤖 AI BEHAVIOUR")

    st.write(
        "The mole adapts its behaviour according to "
        "your current suspicion."
    )

    st.write("The AI can:")

    st.write("• Lie")
    st.write("• Tell the truth")
    st.write("• Help the researcher")
    st.write("• Sabotage cafeteria evidence")
    st.write("• Manipulate the storage riddle")

    st.divider()

    if st.button(
        "🔄 RESTART CASE",
        use_container_width=True
    ):

        st.session_state.game = Game()
        st.rerun()


# ============================================================
# SURVIVORS
# ============================================================

st.header("👥 SURVIVORS")

survivor_columns = st.columns(len(CHARACTERS))

for i, character in enumerate(CHARACTERS):

    with survivor_columns[i]:

        suspicion = game.suspicion[character]

        st.markdown(
            f"""
            <div class="card">
                <div class="card-title">
                    {character}
                </div>

                <div class="muted">
                    Suspicion: {suspicion}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(suspicion / 100)


# ============================================================
# MAIN TABS
# ============================================================

room_tab, question_tab, accusation_tab = st.tabs(
    [
        "🚪 ROOMS",
        "💬 INTERROGATE",
        "⚖️ ACCUSATION"
    ]
)


# ============================================================
# ROOM TAB
# ============================================================

with room_tab:

    st.header("🚪 INVESTIGATION ROOMS")

    st.write(
        "Investigate the facility and search for physical evidence."
    )

    room_columns = st.columns(3)

    for i, room in enumerate(ROOMS):

        data = ROOMS[room]

        with room_columns[i]:

            st.subheader(
                f"{data['icon']} {room}"
            )

            st.write(data["description"])

            st.caption(
                f"Object: {data['object']}"
            )

            visited = room in game.visited_rooms

            if visited:

                st.success("✓ INVESTIGATED")

            elif game.game_over:

                st.info("CASE CLOSED")

            elif game.actions_remaining == 0:

                st.warning("NO ACTIONS REMAINING")

            else:

                if st.button(
                    f"ENTER {room.upper()}",
                    key=f"room_{room}",
                    use_container_width=True
                ):

                    game.visit_room(room)
                    st.rerun()


    # ========================================================
    # ROOM EVIDENCE
    # ========================================================

    if (
        game.last_event
        and game.last_event["type"] == "room"
    ):

        room = game.last_event["room"]

        st.divider()

        st.header(
            f"{ROOMS[room]['icon']} {room.upper()} — EVIDENCE"
        )


        # ----------------------------------------------------
        # LABORATORY
        # ----------------------------------------------------

        if room == "Laboratory":

            data = ROOMS["Laboratory"]["normal_clue"]

            st.markdown(
                f"""
                <div class="paper">

                <h2 style="text-align:center;">
                    {data["title"]}
                </h2>

                <h4>
                    {data["date"]}
                </h4>

                """,
                unsafe_allow_html=True
            )

            for time, event in data["lines"]:

                st.markdown(
                    f"""
                    <div style="
                        padding:7px;
                        border-bottom:1px solid #91876e;
                    ">
                        <b>{time}</b>
                        &nbsp;&nbsp;
                        {event}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                f"""
                <br>

                <b>FIELD NOTE</b>

                <p>
                    "{data["note"]}"
                </p>

                <p style="text-align:right;">
                    <i>{data["signature"]}</i>
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.info(
                "The report suggests that the saboteur knew "
                "which systems to target. Compare this with "
                "survivor testimony."
            )


        # ----------------------------------------------------
        # STORAGE
        # ----------------------------------------------------

        elif room == "Storage":

            data = ROOMS["Storage"]["normal_clue"]

            if game.riddle_manipulated:

                st.markdown(
                    """
                    <div class="warning-box">

                    <b>⚠ EVIDENCE TAMPERING DETECTED</b>

                    <p>
                    The original riddle appears to have been
                    deliberately modified.
                    </p>

                    <p>
                    Several words have been crossed out
                    and replaced.
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="riddle">

                    <h3>
                    HANDWRITTEN NOTE — BOX 17
                    </h3>

                    I have no feet, but I can follow.<br>
                    I have no mouth, but I can warn.<br><br>

                    <s>
                    I disappear when the lights go out.
                    </s>

                    <br><br>

                    <b>
                    "I disappear when nobody is watching."
                    </b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.warning(
                    "Someone may have deliberately altered "
                    "the evidence."
                )

            else:

                st.markdown(
                    f"""
                    <div class="riddle">

                    <h3>
                    {data["title"]}
                    </h3>

                    {data["text"].replace(chr(10), "<br>")}

                    <br><br>

                    <small>
                    {data["hint"].replace(chr(10), "<br>")}
                    </small>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ----------------------------------------------------
        # CAFETERIA
        # ----------------------------------------------------

        elif room == "Cafeteria":

            data = ROOMS["Cafeteria"]["normal_clue"]

            if game.cafeteria_sabotaged:

                st.markdown(
                    """
                    <div class="warning-box">

                    <h3>
                    ⚠ VENDING UNIT DAMAGED
                    </h3>

                    <p>
                    Someone has torn away part of the
                    maintenance note.
                    </p>

                    <p>
                    The original PIN instructions are
                    incomplete.
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.code(
                    """
SURVIVOR SUPPLY UNIT

PIN: 1_

SYSTEM STATUS:
PARTIAL EVIDENCE

[ MAINTENANCE NOTE DAMAGED ]
                    """,
                    language="text"
                )

            else:

                st.code(
                    f"""
SURVIVOR SUPPLY UNIT

ENTER EMERGENCY PIN

PIN: {data["pin"]}

SYSTEM STATUS:
OPERATIONAL
                    """,
                    language="text"
                )

                st.info(
                    f"{data['instruction']}  "
                    f"Current survivors: {data['survivors']}"
                )

                st.caption(data["note"])


# ============================================================
# QUESTION TAB
# ============================================================

with question_tab:

    st.header("💬 INTERROGATION ROOM")

    st.write(
        "Each survivor can be questioned only once."
    )

    q1, q2 = st.columns([1, 2])

    with q1:

        character = st.selectbox(
            "SURVIVOR",
            CHARACTERS,
            key="selected_character"
        )

        suspicion = game.suspicion[character]

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
                {character}
            </div>

            <p>
                Current suspicion: <b>{suspicion}%</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(suspicion / 100)

    with q2:

        question = st.selectbox(
            "QUESTION",
            QUESTIONS,
            key="selected_question"
        )

        already_questioned = (
            character in game.questioned_characters
        )

        if already_questioned:

            st.warning(
                f"{character} has already been questioned."
            )

        elif game.game_over:

            st.info("The case is closed.")

        elif game.actions_remaining <= 0:

            st.warning("You have no actions remaining.")

        else:

            if st.button(
                "💬 ASK QUESTION",
                use_container_width=True
            ):

                game.ask_question(
                    character,
                    question
                )

                st.rerun()


    # ========================================================
    # RESPONSE
    # ========================================================

    if (
        game.last_event
        and game.last_event["type"] == "question"
    ):

        event = game.last_event

        st.divider()

        st.subheader(
            f"💬 {event['character']}'s Response"
        )

        st.markdown(
            f"""
            <div class="paper">

            <b>QUESTION</b>

            <p>
            {event["question"]}
            </p>

            <hr>

            <b>RESPONSE</b>

            <p>
            {event["response"]}
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ACCUSATION TAB
# ============================================================

with accusation_tab:

    st.header("⚖️ FINAL ACCUSATION")

    st.write(
        "When you have enough evidence, identify the "
        "survivor controlled by the AI."
    )

    if not game.game_over:

        accused = st.selectbox(
            "WHO IS THE MOLE?",
            CHARACTERS,
            key="accused_character"
        )

        st.markdown(
            f"""
            <div class="card">

            <div class="card-title">
                Current Accusation: {accused}
            </div>

            <p>
                Suspicion level:
                <b>{game.suspicion[accused]}%</b>
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "⚖️ MAKE FINAL ACCUSATION",
            use_container_width=True
        ):

            game.accuse(accused)
            st.rerun()

    else:

        if game.researcher_won:

            st.markdown(
                f"""
                <div class="success-box">

                <h1>🏆 CASE SOLVED</h1>

                <h2>RESEARCHER WINS</h2>

                <p>
                Your accusation of
                <b>{game.accused}</b>
                was correct.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="failure-box">

                <h1>☠️ INVESTIGATION FAILED</h1>

                <h2>MOLE WINS</h2>

                <p>
                You accused
                <b>{game.accused}</b>.
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        st.subheader("🔓 CASE REVEALED")

        st.success(
            f"The AI-controlled mole was **{game.mole}**."
        )


# ============================================================
# EVIDENCE BOARD
# ============================================================

st.divider()

st.header("🗂️ EVIDENCE BOARD")

if not game.evidence:

    st.info(
        "No evidence collected yet. "
        "Investigate a room or question a survivor."
    )

else:

    for evidence in game.evidence:

        st.markdown(
            f"""
            <div class="evidence">
                🔎 {evidence}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ACTIVITY LOG
# ============================================================

with st.expander("📡 INVESTIGATION ACTIVITY LOG"):

    if not game.activity_log:

        st.write("No activity yet.")

    else:

        for item in reversed(game.activity_log):

            st.write(item)


# ============================================================
# GAME-END ANALYTICS
# ============================================================

if game.game_over:

    st.divider()

    st.header("📊 INVESTIGATION ANALYTICS")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Actions Used",
            game.actions_used
        )

    with col2:
        st.metric(
            "Actions Remaining",
            game.actions_remaining
        )

    with col3:
        st.metric(
            "AI Lies",
            game.ai_lie_count
        )

    with col4:
        st.metric(
            "AI Sabotage",
            game.ai_sabotage_count
        )


    st.subheader("🤖 AI BEHAVIOUR")

    ai1, ai2, ai3 = st.columns(3)

    with ai1:

        st.metric(
            "Truthful Responses",
            game.ai_truth_count
        )

    with ai2:

        st.metric(
            "Help Actions",
            game.ai_help_count
        )

    with ai3:

        st.metric(
            "Sabotage Actions",
            game.ai_sabotage_count
        )


    # ========================================================
    # COUNTERFACTUAL OPTIMAL PATH
    # ========================================================

    st.divider()

    st.header("🧠 COUNTERFACTUAL OPTIMAL PATH")

    st.write(
        "This shows how the investigation could have been "
        "completed using fewer actions."
    )

    optimal_path = [
        "Investigate Laboratory",
        "Investigate Cafeteria",
        "Question Raven",
        "Question Luca",
        "Question Zephyr",
        "Accuse Zephyr"
    ]

    optimal_actions = len(optimal_path)

    actual_actions = game.actions_used

    m1, m2 = st.columns(2)

    with m1:

        st.metric(
            "Your Investigation",
            f"{actual_actions} actions"
        )

    with m2:

        st.metric(
            "Suggested Solution",
            f"{optimal_actions} actions"
        )


    st.subheader("🔎 OPTIMAL INVESTIGATION PATH")

    for i, step in enumerate(
        optimal_path,
        start=1
    ):

        st.markdown(
            f"""
            <div class="path-step">
                <b>{i}.</b> {step}
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # EFFICIENCY
    # ========================================================

    if actual_actions > 0:

        efficiency = min(
            100,
            (optimal_actions / actual_actions) * 100
        )

        st.subheader("⚡ INVESTIGATION EFFICIENCY")

        st.progress(
            efficiency / 100
        )

        st.write(
            f"Efficiency: **{efficiency:.1f}%**"
        )
