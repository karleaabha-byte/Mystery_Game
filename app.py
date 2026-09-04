# app.py

import streamlit as st

from game import Game

from case import (
    CHARACTERS,
    ROOMS,
    QUESTIONS
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="Who Is The Mole?",
    page_icon="🧟",
    layout="wide"
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


/* ------------------------------
   HEADER
------------------------------ */

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


/* ------------------------------
   ACTION COUNTER
------------------------------ */

.action-box {
    border: 2px solid #888888;
    background: #161616;
    padding: 15px;
    text-align: center;
    margin-bottom: 25px;
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


/* ------------------------------
   ROOM CARD
------------------------------ */

.room-card {
    background: #171717;
    border: 1px solid #444444;
    padding: 20px;
    min-height: 220px;
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
}


/* ------------------------------
   NOTE
------------------------------ */

.note {
    background: #d9d0b7;
    color: #25221c;
    padding: 28px;
    margin: 15px 0;
    border: 3px solid #81765c;
    box-shadow:
        4px 4px 0px #000000;
    font-family: Georgia, serif;
}

.note-header {
    text-align: center;
    font-size: 22px;
    font-weight: bold;
    border-bottom: 2px solid #5d5543;
    padding-bottom: 10px;
    margin-bottom: 15px;
}

.note-body {
    font-size: 16px;
    line-height: 1.7;
}

.note-signature {
    text-align: right;
    margin-top: 20px;
    font-style: italic;
}


/* ------------------------------
   INCIDENT TABLE
------------------------------ */

.incident {
    width: 100%;
    border-collapse: collapse;
}

.incident td {
    padding: 7px;
    border-bottom: 1px solid #91876e;
}

.incident-time {
    font-weight: bold;
    width: 80px;
}


/* ------------------------------
   RIDDLE
------------------------------ */

.riddle {
    background: #c8c0aa;
    color: #211f1b;
    padding: 30px;
    border: 3px solid #726a57;
    box-shadow: 5px 5px 0px #000;
    font-family: Georgia, serif;
    font-size: 19px;
    white-space: pre-line;
    text-align: center;
}

.riddle-title {
    font-size: 23px;
    font-weight: bold;
    margin-bottom: 20px;
}


/* ------------------------------
   VENDING MACHINE
------------------------------ */

.vending {
    background: #1b1b1b;
    border: 4px solid #555555;
    padding: 25px;
    text-align: center;
    box-shadow: 5px 5px 0px #000;
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


/* ------------------------------
   SABOTAGE
------------------------------ */

.damaged {
    background: #241919;
    border: 2px solid #704545;
    padding: 25px;
    color: #e0b0b0;
}

.warning {
    font-weight: bold;
    font-size: 18px;
}


/* ------------------------------
   EVIDENCE
------------------------------ */

.evidence-card {
    background: #171717;
    border-left: 4px solid #888888;
    padding: 12px;
    margin: 8px 0;
}


/* ------------------------------
   SURVIVOR
------------------------------ */

.survivor {
    background: #171717;
    border: 1px solid #444444;
    padding: 15px;
    text-align: center;
    margin-bottom: 10px;
}

.survivor-name {
    font-size: 19px;
    font-weight: bold;
}

.suspicion {
    font-family: monospace;
    margin-top: 5px;
}


/* ------------------------------
   RESULT
------------------------------ */

.win {
    background: #142417;
    border: 2px solid #4c8655;
    padding: 25px;
    text-align: center;
}

.loss {
    background: #291717;
    border: 2px solid #8c4c4c;
    padding: 25px;
    text-align: center;
}


/* ------------------------------
   OPTIMAL PATH
------------------------------ */

.optimal {
    background: #171717;
    border: 2px solid #555555;
    padding: 25px;
}

.path-step {
    background: #222222;
    border-left: 3px solid #999999;
    padding: 10px;
    margin: 6px 0;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="game-title">🧟 WHO IS THE MOLE?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">'
    'ADVERSARIAL AI AGENT • ZOMBIE APOCALYPSE SIMULATION'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# ACTION BAR
# ============================================================

st.markdown(
    f"""
    <div class="action-box">
        <div class="action-label">
            MAXIMUM INVESTIGATION BUDGET
        </div>

        <div class="action-number">
            {game.actions_remaining}
            <span style="font-size:18px;color:#777;">
                / {game.max_actions}
            </span>
        </div>

        <div class="action-label">
            ACTIONS REMAINING
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 📁 CASE FILE")

    st.markdown(
        "**CASE**  \n"
        "Zombie Apocalypse Mole Identification"
    )

    st.markdown(
        "**LOCATION**  \n"
        "Research Facility"
    )

    st.markdown(
        "**ROLE**  \n"
        "Researcher"
    )

    st.divider()

    st.markdown("### 🎯 OBJECTIVE")

    st.write(
        "Identify the survivor secretly controlled "
        "by the adversarial AI."
    )

    st.divider()

    st.markdown("### 📋 RULES")

    st.write("• Maximum 12 actions")
    st.write("• Each room can be investigated once")
    st.write("• Each survivor can be questioned once")
    st.write("• AI actions do not consume your actions")
    st.write("• Make the final accusation when ready")

    st.divider()

    st.markdown("### 🤖 AI BEHAVIOUR")

    st.write(
        "The mole observes your investigation and "
        "changes its behaviour."
    )

    st.write(
        "It can:"
    )

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

st.markdown("## 👥 SURVIVORS")

survivor_columns = st.columns(5)

for i, character in enumerate(CHARACTERS):

    with survivor_columns[i]:

        suspicion = game.suspicion[character]

        st.markdown(
            f"""
            <div class="survivor">

                <div class="survivor-name">
                    {character}
                </div>

                <div class="suspicion">
                    Suspicion: {suspicion}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


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

    st.markdown("## 🚪 INVESTIGATION ROOMS")

    st.write(
        "Search the facility for physical evidence."
    )

    room_columns = st.columns(3)


    for i, room in enumerate(ROOMS):

        data = ROOMS[room]

        with room_columns[i]:

            visited = room in game.visited_rooms

            st.markdown(
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
                """,
                unsafe_allow_html=True
            )


            if visited:

                st.success(
                    "✓ INVESTIGATED"
                )

            elif game.game_over:

                st.info(
                    "CASE CLOSED"
                )

            elif game.actions_remaining == 0:

                st.warning(
                    "NO ACTIONS"
                )

            else:

                if st.button(
                    f"ENTER {room.upper()}",
                    key=f"room_{room}",
                    use_container_width=True
                ):

                    game.visit_room(room)

                    st.rerun()


    # ========================================================
    # SHOW ROOM EVIDENCE
    # ========================================================

    if (
        game.last_event
        and game.last_event["type"] == "room"
    ):

        room = game.last_event["room"]

        st.divider()

        st.markdown(
            f"## {ROOMS[room]['icon']} {room.upper()} — EVIDENCE"
        )


        # ====================================================
        # LABORATORY
        # ====================================================

        if room == "Laboratory":

            data = ROOMS["Laboratory"]["normal_clue"]

            st.markdown(
                f"""
                <div class="note">

                    <div class="note-header">
                        {data["title"]}
                    </div>

                    <b>{data["date"]}</b>

                    <br><br>

                    <table class="incident">
                        {
                            ''.join(
                                f'''
                                <tr>
                                    <td class="incident-time">
                                        {time}
                                    </td>
                                    <td>
                                        {event}
                                    </td>
                                </tr>
                                '''
                                for time, event in data["lines"]
                            )
                        }
                    </table>

                    <br>

                    <b>FIELD NOTE</b>

                    <p>
                        "{data["note"]}"
                    </p>

                    <div class="note-signature">
                        {data["signature"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            st.info(
                "The note suggests that the saboteur knew "
                "which systems to target. This clue should "
                "be compared with survivor testimony."
            )


        # ====================================================
        # STORAGE
        # ====================================================

        elif room == "Storage":

            data = ROOMS["Storage"]["normal_clue"]


            if game.riddle_manipulated:

                st.markdown(
                    """
                    <div class="damaged">

                        <div class="warning">
                            ⚠ EVIDENCE TAMPERING DETECTED
                        </div>

                        <br>

                        The original riddle appears to have been
                        modified.

                        <br><br>

                        Several words have been crossed out
                        and replaced.

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="riddle">

                        <div class="riddle-title">
                            HANDWRITTEN NOTE — BOX 17
                        </div>

                        I have no feet, but I can follow.<br>
                        I have no mouth, but I can warn.<br>

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

                        <div class="riddle-title">
                            {data["title"]}
                        </div>

                        {data["text"].replace(chr(10), "<br>")}

                        <br><br>

                        <small>
                            {data["hint"]}
                        </small>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # ====================================================
        # CAFETERIA
        # ====================================================

        elif room == "Cafeteria":

            data = ROOMS["Cafeteria"]["normal_clue"]


            if game.cafeteria_sabotaged:

                st.markdown(
                    """
                    <div class="damaged">

                        <div class="warning">
                            ⚠ VENDING UNIT DAMAGED
                        </div>

                        <br>

                        Someone has torn away part of the
                        maintenance note.

                        <br><br>

                        The original PIN instructions are
                        incomplete.

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.markdown(
                    """
                    <div class="vending">

                        <h2>
                            SURVIVOR SUPPLY UNIT
                        </h2>

                        <div class="vending-screen">
                            PIN: 1_
                        </div>

                        <p>
                            SYSTEM STATUS:
                            <b>PARTIAL EVIDENCE</b>
                        </p>

                        <p>
                            [ MAINTENANCE NOTE DAMAGED ]
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
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
                    """,
                    unsafe_allow_html=True
                )

                st.info(
                    data["note"]
                )


# ============================================================
# QUESTION TAB
# ============================================================

with question_tab:

    st.markdown("## 💬 INTERROGATION ROOM")

    st.write(
        "Each survivor can be questioned only once."
    )


    q_columns = st.columns([1, 2])


    with q_columns[0]:

        character = st.selectbox(
            "SURVIVOR",
            CHARACTERS
        )


        st.markdown(
            f"""
            <div class="survivor">

                <div class="survivor-name">
                    {character}
                </div>

                <div class="suspicion">
                    Current suspicion:
                    {game.suspicion[character]}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with q_columns[1]:

        question = st.selectbox(
            "QUESTION",
            QUESTIONS
        )


        already_questioned = (
            character
            in game.questioned_characters
        )


        if already_questioned:

            st.warning(
                f"{character} has already been questioned."
            )

        elif game.game_over:

            st.info(
                "The case is closed."
            )

        elif game.actions_remaining <= 0:

            st.warning(
                "You have no actions remaining."
            )

        else:

            if st.button(
                "ASK QUESTION",
                use_container_width=True
            ):

                game.ask_question(
                    character,
                    question
                )

                st.rerun()


    # ========================================================
    # SHOW RESPONSE
    # ========================================================

    if (
        game.last_event
        and game.last_event["type"] == "question"
    ):

        event = game.last_event

        st.divider()

        st.markdown(
            f"### 💬 {event['character']}'s Response"
        )


        st.markdown(
            f"""
            <div class="note">

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

    st.markdown("## ⚖️ FINAL ACCUSATION")

    st.write(
        "When you believe you have enough evidence, "
        "identify the suspected AI-controlled survivor."
    )


    if not game.game_over:

        accused = st.selectbox(
            "WHO IS THE MOLE?",
            CHARACTERS
        )


        st.markdown(
            f"""
            <div class="survivor">

                <div class="survivor-name">
                    Your accusation:
                    {accused}
                </div>

                <div class="suspicion">
                    Current suspicion:
                    {game.suspicion[accused]}%
                </div>

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

        # ====================================================
        # WIN
        # ====================================================

        if game.researcher_won:

            st.markdown(
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
                """,
                unsafe_allow_html=True
            )


        # ====================================================
        # LOSS
        # ====================================================

        else:

            st.markdown(
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
                """,
                unsafe_allow_html=True
            )


        st.divider()

        st.markdown(
            "### 🔓 CASE REVEALED"
        )

        st.write(
            f"The AI-controlled mole was **{game.mole}**."
        )


# ============================================================
# EVIDENCE BOARD
# ============================================================

st.divider()

st.markdown("## 🗂️ EVIDENCE BOARD")


if not game.evidence:

    st.info(
        "No evidence collected yet. "
        "Investigate a room or question a survivor."
    )

else:

    for evidence in game.evidence:

        st.markdown(
            f"""
            <div class="evidence-card">
                🔎 {evidence}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ACTIVITY LOG
# ============================================================

with st.expander(
    "📡 INVESTIGATION ACTIVITY LOG"
):

    if not game.activity_log:

        st.write(
            "No activity yet."
        )

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

    st.markdown("## 📊 INVESTIGATION ANALYTICS")


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


    st.markdown("### 🤖 AI BEHAVIOUR")

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
    # OPTIMAL PATH
    # ========================================================

    st.divider()

    st.markdown(
        "## 🧠 COUNTERFACTUAL OPTIMAL PATH"
    )

    st.write(
        "Regardless of whether you won or lost, "
        "the system compares your investigation with "
        "a minimum-action solution."
    )


    # --------------------------------------------------------
    # Current simple optimal solution
    #
    # For this case, the most informative combination
    # is based on evidence that points toward Zephyr.
    # --------------------------------------------------------

    optimal_path = [

        "Investigate Laboratory",

        "Investigate Cafeteria",

        "Question Raven",

        "Question Luca",

        "Question Zephyr",

        "Accuse Zephyr"
    ]


    optimal_actions = len(
        optimal_path
    )


    actual_actions = game.actions_used


    st.markdown(
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
        """,
        unsafe_allow_html=True
    )


    st.markdown("### 🔎 OPTIMAL INVESTIGATION PATH")


    for i, step in enumerate(
        optimal_path,
        start=1
    ):

        st.markdown(
            f"""
            <div class="path-step">

                <b>
                    {i}.
                </b>

                {step}

            </div>
            """,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # EFFICIENCY
    # --------------------------------------------------------

    if actual_actions > 0:

        efficiency = min(
            100,
            (optimal_actions / actual_actions) * 100
        )

        st.progress(
            efficiency / 100
        )

        st.write(
            f"Investigation efficiency: "
            f"**{efficiency:.1f}%**"
        )
