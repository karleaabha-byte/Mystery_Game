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

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top,
                #202020 0%,
                #101010 45%,
                #080808 100%
            );
        color: #eeeeee;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .game-title {
        text-align: center;
        font-size: 52px;
        font-weight: 900;
        letter-spacing: 7px;
        margin-top: 10px;
        margin-bottom: 0;
    }

    .game-subtitle {
        text-align: center;
        color: #999999;
        font-size: 16px;
        letter-spacing: 2px;
        margin-bottom: 25px;
    }

    .action-box {
        border: 2px solid #888888;
        background: #161616;
        padding: 15px;
        text-align: center;
        margin-bottom: 25px;
        border-radius: 8px;
    }

    .action-number {
        font-size: 34px;
        font-weight: bold;
    }

    .action-label {
        font-size: 12px;
        color: #999999;
        letter-spacing: 3px;
    }

    .card {
        background: #171717;
        border: 1px solid #444444;
        padding: 18px;
        border-radius: 7px;
        margin-bottom: 10px;
    }

    .card-title {
        font-size: 21px;
        font-weight: bold;
    }

    .muted {
        color: #aaaaaa;
        font-size: 14px;
        margin-top: 6px;
    }

    .room-card {
        background: #171717;
        border: 1px solid #444444;
        padding: 20px;
        min-height: 200px;
        border-radius: 7px;
        margin-bottom: 10px;
    }

    .room-icon {
        font-size: 45px;
    }

    .room-title {
        font-size: 24px;
        font-weight: bold;
    }

    .room-description {
        color: #aaaaaa;
        font-size: 14px;
        margin-top: 8px;
    }

    .paper {
        background: #d9d0b7;
        color: #25221c;
        padding: 28px;
        margin: 15px 0;
        border: 3px solid #81765c;
        box-shadow: 4px 4px 0px #000000;
        font-family: Georgia, serif;
        border-radius: 4px;
    }

    .paper-header {
        text-align: center;
        font-size: 22px;
        font-weight: bold;
        border-bottom: 2px solid #5d5543;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    .riddle {
        background: #c8c0aa;
        color: #211f1b;
        padding: 30px;
        border: 3px solid #726a57;
        box-shadow: 5px 5px 0px #000;
        font-family: Georgia, serif;
        font-size: 19px;
        text-align: center;
        border-radius: 4px;
        margin: 15px 0;
    }

    .riddle-title {
        font-size: 23px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    .vending {
        background: #1b1b1b;
        border: 4px solid #555555;
        padding: 25px;
        text-align: center;
        box-shadow: 5px 5px 0px #000;
        border-radius: 5px;
        margin: 15px 0;
    }

    .vending-screen {
        background: #101010;
        border: 2px solid #777777;
        padding: 20px;
        margin: 15px;
        font-family: monospace;
        font-size: 26px;
        letter-spacing: 6px;
    }

    .pin {
        font-size: 42px;
        font-weight: bold;
    }

    .warning-box {
        background: #241919;
        border: 2px solid #704545;
        padding: 25px;
        color: #e0b0b0;
        border-radius: 6px;
        margin: 15px 0;
    }

    .warning-title {
        font-weight: bold;
        font-size: 18px;
    }

    .evidence-card {
        background: #171717;
        border-left: 4px solid #888888;
        padding: 12px;
        margin: 8px 0;
        border-radius: 4px;
    }

    .win {
        background: #142417;
        border: 2px solid #4c8655;
        padding: 25px;
        text-align: center;
        border-radius: 8px;
    }

    .loss {
        background: #291717;
        border: 2px solid #8c4c4c;
        padding: 25px;
        text-align: center;
        border-radius: 8px;
    }

    .optimal {
        background: #171717;
        border: 2px solid #555555;
        padding: 25px;
        border-radius: 7px;
    }

    .path-step {
        background: #222222;
        border-left: 3px solid #999999;
        padding: 10px;
        margin: 6px 0;
        border-radius: 3px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="game-title">
        🧟 WHO IS THE MOLE?
    </div>

    <div class="game-subtitle">
        ADVERSARIAL AI AGENT • ZOMBIE APOCALYPSE SIMULATION
    </div>
    """
)


# ============================================================
# ACTION BAR
# ============================================================

st.html(
    f"""
    <div class="action-box">

        <div class="action-label">
            INVESTIGATION ACTIONS REMAINING
        </div>

        <div class="action-number">
            {game.actions_remaining}
            <span style="font-size:18px;color:#777;">
                / {game.max_actions}
            </span>
        </div>

        <div class="action-label">
            MAXIMUM INVESTIGATION BUDGET
        </div>

    </div>
    """
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
    st.write("• Make the final accusation when ready")

    st.divider()

    st.subheader("🤖 AI BEHAVIOUR")

    st.write(
        "The mole observes your investigation and "
        "changes its behaviour."
    )

    st.write("The AI can:")

    st.write("• Lie")
    st.write("• Tell the truth")
    st.write("• Help you")
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

survivor_columns = st.columns(5)

for i, character in enumerate(CHARACTERS):

    with survivor_columns[i]:

        suspicion = game.suspicion[character]

        st.html(
            f"""
            <div class="card">

                <div class="card-title">
                    {character}
                </div>

                <div class="muted">
                    Suspicion: {suspicion}%
                </div>

            </div>
            """
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
        "Search the facility for physical evidence."
    )

    room_columns = st.columns(3)

    for i, room in enumerate(ROOMS):

        data = ROOMS[room]

        with room_columns[i]:

            st.html(
                f"""
                <div class="room-card">

                    <div class="room-icon">
                        {data["icon"]}
                    </div>

                    <div class="room-title">
                        {room}
                    </div>

                    <div class="room-description">
                        {data["description"]}
                    </div>

                </div>
                """
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


        # ====================================================
        # LABORATORY
        # ====================================================

        if room == "Laboratory":

            data = ROOMS["Laboratory"]["normal_clue"]

            st.html(
                f"""
                <div class="paper">

                    <div class="paper-header">
                        {data["title"]}
                    </div>

                    <b>{data["date"]}</b>

                </div>
                """
            )

            for time, event in data["lines"]:

                st.markdown(
                    f"**{time}** — {event}"
                )

            st.html(
                f"""
                <div class="paper">

                    <b>FIELD NOTE</b>

                    <p>
                        "{data["note"]}"
                    </p>

                    <p style="text-align:right;">
                        <i>{data["signature"]}</i>
                    </p>

                </div>
                """
            )

            st.info(
                "The report suggests that the saboteur knew "
                "which systems to target. Compare this with "
                "survivor testimony."
            )


        # ====================================================
        # STORAGE
        # ====================================================

        elif room == "Storage":

            data = ROOMS["Storage"]["normal_clue"]

            if game.riddle_manipulated:

                st.html(
                    """
                    <div class="warning-box">

                        <div class="warning-title">
                            ⚠ EVIDENCE TAMPERING DETECTED
                        </div>

                        <p>
                            The original riddle appears to have
                            been deliberately modified.
                        </p>

                        <p>
                            Several words have been crossed out
                            and replaced.
                        </p>

                    </div>
                    """
                )

                st.html(
                    """
                    <div class="riddle">

                        <div class="riddle-title">
                            HANDWRITTEN NOTE — BOX 17
                        </div>

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
                    """
                )

                st.warning(
                    "Someone may have deliberately altered "
                    "the evidence."
                )

            else:

                riddle_text = data["text"].replace(
                    "\n",
                    "<br>"
                )

                hint_text = data["hint"].replace(
                    "\n",
                    "<br>"
                )

                st.html(
                    f"""
                    <div class="riddle">

                        <div class="riddle-title">
                            {data["title"]}
                        </div>

                        {riddle_text}

                        <br><br>

                        <small>
                            {hint_text}
                        </small>

                    </div>
                    """
                )


        # ====================================================
        # CAFETERIA
        # ====================================================

        elif room == "Cafeteria":

            data = ROOMS["Cafeteria"]["normal_clue"]

            if game.cafeteria_sabotaged:

                st.html(
                    """
                    <div class="warning-box">

                        <div class="warning-title">
                            ⚠ VENDING UNIT DAMAGED
                        </div>

                        <p>
                            Someone has torn away part of the
                            maintenance note.
                        </p>

                        <p>
                            The original PIN instructions are
                            incomplete.
                        </p>

                    </div>
                    """
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

                st.html(
                    f"""
                    <div class="vending">

                        <h2>
                            SURVIVOR SUPPLY UNIT
                        </h2>

                        <div class="vending-screen">

                            ENTER EMERGENCY PIN

                            <br><br>

                            <span class="pin">
                                {data["pin"]}
                            </span>

                        </div>

                        <h4>
                            MAINTENANCE NOTE
                        </h4>

                        <p>
                            {data["instruction"]}
                        </p>

                        <p>
                            Current survivors:
                            <b>{data["survivors"]}</b>
                        </p>

                    </div>
                    """
                )

                st.info(
                    data["note"]
                )


# ============================================================
# QUESTION TAB
# ============================================================

with question_tab:

    st.header("💬 INTERROGATION ROOM")

    st.write(
        "Each survivor can be questioned only once."
    )

    q_columns = st.columns([1, 2])

    with q_columns[0]:

        character = st.selectbox(
            "SURVIVOR",
            CHARACTERS,
            key="selected_character"
        )

        suspicion = game.suspicion[character]

        st.html(
            f"""
            <div class="card">

                <div class="card-title">
                    {character}
                </div>

                <div class="muted">
                    Current suspicion: {suspicion}%
                </div>

            </div>
            """
        )

        st.progress(suspicion / 100)

    with q_columns[1]:

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

            st.warning(
                "You have no actions remaining."
            )

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

        st.html(
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
            """
        )


# ============================================================
# ACCUSATION TAB
# ============================================================

with accusation_tab:

    st.header("⚖️ FINAL ACCUSATION")

    st.write(
        "When you believe you have enough evidence, "
        "identify the suspected AI-controlled survivor."
    )

    if not game.game_over:

        accused = st.selectbox(
            "WHO IS THE MOLE?",
            CHARACTERS,
            key="accused_character"
        )

        st.html(
            f"""
            <div class="card">

                <div class="card-title">
                    Your Accusation: {accused}
                </div>

                <div class="muted">
                    Current suspicion:
                    {game.suspicion[accused]}%
                </div>

            </div>
            """
        )

        if st.button(
            "⚖️ MAKE FINAL ACCUSATION",
            use_container_width=True
        ):

            game.accuse(accused)
            st.rerun()

    else:

        if game.researcher_won:

            st.html(
                f"""
                <div class="win">

                    <h1>
                        🏆 CASE SOLVED
                    </h1>

                    <h2>
                        RESEARCHER WINS
                    </h2>

                    <p>
                        Your accusation of
                        <b>{game.accused}</b>
                        was correct.
                    </p>

                </div>
                """
            )

        else:

            st.html(
                f"""
                <div class="loss">

                    <h1>
                        ☠️ INVESTIGATION FAILED
                    </h1>

                    <h2>
                        MOLE WINS
                    </h2>

                    <p>
                        You accused
                        <b>{game.accused}</b>.
                    </p>

                </div>
                """
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

        st.html(
            f"""
            <div class="evidence-card">
                🔎 {evidence}
            </div>
            """
        )


# ============================================================
# ACTIVITY LOG
# ============================================================

with st.expander(
    "📡 INVESTIGATION ACTIVITY LOG"
):

    if not game.activity_log:

        st.write("No activity yet.")

    else:

        for item in reversed(
            game.activity_log
        ):

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

    st.header(
        "🧠 COUNTERFACTUAL OPTIMAL PATH"
    )

    st.write(
        "Regardless of whether you won or lost, "
        "this shows a shorter investigation path "
        "that could have been used."
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

    st.html(
        f"""
        <div class="optimal">

            <h3>
                MINIMUM-ACTION SOLUTION
            </h3>

            <p>
                Your investigation:
                <b>{actual_actions} actions</b>
            </p>

            <p>
                Suggested optimal investigation:
                <b>{optimal_actions} actions</b>
            </p>

        </div>
        """
    )

    st.subheader(
        "🔎 OPTIMAL INVESTIGATION PATH"
    )

    for i, step in enumerate(
        optimal_path,
        start=1
    ):

        st.html(
            f"""
            <div class="path-step">

                <b>{i}.</b>
                {step}

            </div>
            """
        )


    # ========================================================
    # EFFICIENCY
    # ========================================================

    if actual_actions > 0:

        efficiency = min(
            100,
            (optimal_actions / actual_actions) * 100
        )

        st.subheader(
            "⚡ INVESTIGATION EFFICIENCY"
        )

        st.progress(
            efficiency / 100
        )

        st.write(
            f"Investigation efficiency: "
            f"**{efficiency:.1f}%**"
        )
