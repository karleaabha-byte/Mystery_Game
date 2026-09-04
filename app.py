import streamlit as st

from game import Game
from case import (
    CHARACTERS,
    MOLE,
    ROOMS,
    QUESTIONS
)
from optimal_path import solve_optimal_path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Who Is The Mole?",
    page_icon="🕵️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                #202936 0%,
                #0d1117 45%,
                #080b0f 100%
            );
        color: #f5f5f5;
    }

    .main-title {
        text-align: center;
        font-size: 48px;
        font-weight: 900;
        letter-spacing: 4px;
        margin-top: 10px;
        margin-bottom: 0px;
    }

    .subtitle {
        text-align: center;
        color: #aeb7c2;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .researcher-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 18px;
    }

    .action-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
    }

    .room-card {
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 14px;
        padding: 20px;
        min-height: 180px;
        margin-bottom: 10px;
    }

    .room-title {
        font-size: 24px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .room-description {
        color: #b9c2cc;
        font-size: 14px;
        line-height: 1.5;
    }

    .clue-box {
        background: rgba(255, 255, 255, 0.06);
        border-left: 4px solid #d9a441;
        border-radius: 8px;
        padding: 18px;
        margin-top: 12px;
        margin-bottom: 15px;
    }

    .clue-title {
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .note-box {
        background: #11161d;
        border: 1px solid #303945;
        border-radius: 8px;
        padding: 18px;
        font-family: monospace;
        white-space: pre-wrap;
        line-height: 1.8;
    }

    .evidence-box {
        background: rgba(255, 255, 255, 0.045);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-radius: 10px;
        padding: 13px;
        margin-bottom: 8px;
    }

    .log-box {
        background: rgba(255, 255, 255, 0.035);
        border-radius: 8px;
        padding: 9px 12px;
        margin-bottom: 6px;
        color: #cbd3dc;
        font-size: 13px;
    }

    .suspect-safe {
        color: #8fd694;
        font-weight: 700;
    }

    .suspect-medium {
        color: #e6c85c;
        font-weight: 700;
    }

    .suspect-high {
        color: #ef7777;
        font-weight: 700;
    }

    .win-box {
        background: rgba(70, 180, 100, 0.12);
        border: 1px solid rgba(70, 180, 100, 0.4);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
    }

    .lose-box {
        background: rgba(200, 70, 70, 0.12);
        border: 1px solid rgba(200, 70, 70, 0.4);
        border-radius: 15px;
        padding: 30px;
        text-align: center;
    }

    .big-result {
        font-size: 36px;
        font-weight: 900;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "game" not in st.session_state:
    st.session_state.game = None

if "player_name" not in st.session_state:
    st.session_state.player_name = ""


# ============================================================
# START SCREEN
# ============================================================

if st.session_state.game is None:

    st.markdown(
        '<div class="main-title">🕵️ WHO IS THE MOLE?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'A mystery of deception, evidence and sabotage'
        '</div>',
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.markdown(
            """
            ### 🔎 Your Mission

            Five survivors remain inside an evacuated facility.

            One of them is secretly the **MOLE**.

            Investigate the rooms, decode hidden clues, question
            the survivors and use the evidence to identify the
            traitor.

            You have a limited number of actions, so choose carefully.
            """
        )

        st.divider()

        with st.form("start_game_form"):

            player_name = st.text_input(
                "Researcher name",
                placeholder="Enter your name..."
            )

            start_game = st.form_submit_button(
                "🚨 START INVESTIGATION",
                use_container_width=True
            )

            if start_game:

                if player_name.strip():

                    st.session_state.player_name = (
                        player_name.strip()
                    )

                    st.session_state.game = Game(
                        player_name=st.session_state.player_name
                    )

                    st.rerun()

                else:

                    st.warning(
                        "Please enter your name before starting."
                    )

    st.stop()


# ============================================================
# CURRENT GAME
# ============================================================

game = st.session_state.game


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🕵️ WHO IS THE MOLE?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'FACILITY INVESTIGATION SYSTEM'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="researcher-card">
        🔬 RESEARCHER:
        <b>{game.player_name}</b>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP ACTION BAR
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.markdown(
        f"""
        <div class="action-card">
            <div>⚡ ACTIONS REMAINING</div>
            <h2>{game.actions_remaining}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.markdown(
        f"""
        <div class="action-card">
            <div>🔎 ACTIONS USED</div>
            <h2>{game.actions_used}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:

    st.markdown(
        f"""
        <div class="action-card">
            <div>📁 ROOMS SEARCHED</div>
            <h2>{len(game.visited_rooms)}/{len(ROOMS)}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:

    st.markdown(
        f"""
        <div class="action-card">
            <div>🧾 EVIDENCE</div>
            <h2>{len(game.evidence)}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🕵️ Investigation")

    st.write(
        f"**Researcher:** {game.player_name}"
    )

    st.write(
        f"**Actions:** {game.actions_remaining} / {game.max_actions}"
    )

    st.divider()

    st.subheader("👥 Survivors")

    for character in CHARACTERS:

        suspicion = game.suspicion[character]

        if suspicion >= 60:
            status = "🔴 HIGH"
        elif suspicion >= 30:
            status = "🟡 MEDIUM"
        else:
            status = "🟢 LOW"

        st.write(
            f"**{character}** — {status} ({suspicion}%)"
        )

    st.divider()

    st.subheader("📌 Investigation Rules")

    st.caption(
        "Each room can only be investigated once."
    )

    st.caption(
        "Each survivor can only be questioned once."
    )

    st.caption(
        "You can accuse the suspect whenever you are ready."
    )

    st.divider()

    if st.button(
        "🔄 Restart Investigation",
        use_container_width=True
    ):

        st.session_state.game = Game(
            player_name=st.session_state.player_name
        )

        st.rerun()

    if st.button(
        "👤 Change Researcher",
        use_container_width=True
    ):

        st.session_state.game = None
        st.session_state.player_name = ""

        st.rerun()


# ============================================================
# GAME OVER
# ============================================================

if game.game_over:

    st.header("🏁 Investigation Complete")

    if game.researcher_won:

        st.markdown(
            f"""
            <div class="win-box">
                <div class="big-result">
                    🎉 CASE SOLVED
                </div>

                <p>
                    Excellent work, <b>{game.player_name}</b>.
                </p>

                <p>
                    <b>{game.accused}</b> was the mole.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="lose-box">
                <div class="big-result">
                    ❌ WRONG ACCUSATION
                </div>

                <p>
                    <b>{game.accused}</b> was not the mole.
                </p>

                <p>
                    The real mole was
                    <b>{MOLE}</b>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("📊 Investigation Statistics")

    stat1, stat2, stat3, stat4 = st.columns(4)

    with stat1:
        st.metric(
            "Actions Used",
            game.actions_used
        )

    with stat2:
        st.metric(
            "Rooms Investigated",
            len(game.visited_rooms)
        )

    with stat3:
        st.metric(
            "People Questioned",
            len(game.questioned_characters)
        )

    with stat4:
        st.metric(
            "Evidence Found",
            len(game.evidence)
        )

    st.divider()

    st.subheader("🤖 Mole AI Behaviour")

    ai1, ai2, ai3, ai4 = st.columns(4)

    with ai1:
        st.metric(
            "Lies",
            game.ai_lie_count
        )

    with ai2:
        st.metric(
            "Truthful Answers",
            game.ai_truth_count
        )

    with ai3:
        st.metric(
            "Help Attempts",
            game.ai_help_count
        )

    with ai4:
        st.metric(
            "Sabotages",
            game.ai_sabotage_count
        )

    st.divider()

    st.subheader("🧾 Evidence Board")

    if game.evidence:

        for evidence in game.evidence:

            st.markdown(
                f"""
                <div class="evidence-box">
                    🔎 {evidence}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.info(
            "No evidence was recorded."
        )

    st.divider()

    st.subheader("📜 Activity Log")

    if game.activity_log:

        for event in reversed(game.activity_log):

            st.markdown(
                f"""
                <div class="log-box">
                    {event}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    if st.button(
        "🔄 PLAY AGAIN",
        use_container_width=True
    ):

        st.session_state.game = Game(
            player_name=st.session_state.player_name
        )

        st.rerun()

    st.stop()


# ============================================================
# MAIN TABS
# ============================================================

tab_rooms, tab_question, tab_evidence, tab_accuse = st.tabs(
    [
        "🔎 INVESTIGATE ROOMS",
        "💬 QUESTION SURVIVORS",
        "🧾 EVIDENCE BOARD",
        "⚖️ ACCUSE"
    ]
)


# ============================================================
# ROOM INVESTIGATION
# ============================================================

with tab_rooms:

    st.header("🔎 Investigate the Facility")

    st.write(
        "Search the facility for clues. "
        "Some evidence may have been tampered with."
    )

    room_names = list(ROOMS.keys())

    room_columns = st.columns(
        len(room_names)
    )

    for index, room in enumerate(room_names):

        room_data = ROOMS[room]

        with room_columns[index]:

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-title">
                        {room_data["icon"]} {room}
                    </div>

                    <div class="room-description">
                        {room_data["description"]}
                    </div>

                    <br>

                    <b>Object:</b><br>
                    {room_data["object"]}

                </div>
                """,
                unsafe_allow_html=True
            )

            if room in game.visited_rooms:

                st.success(
                    "Investigation completed"
                )

            else:

                if st.button(
                    f"Investigate {room}",
                    key=f"investigate_{room}",
                    use_container_width=True,
                    disabled=(
                        game.actions_remaining <= 0
                    )
                ):

                    game.visit_room(room)

                    st.rerun()


    # --------------------------------------------------------
    # MOST RECENT ROOM EVENT
    # --------------------------------------------------------

    if game.last_event is not None:

        if game.last_event.get("type") == "room":

            room = game.last_event["room"]

            room_data = ROOMS[room]

            st.divider()

            st.subheader(
                f"{room_data['icon']} {room} Evidence"
            )

            sabotaged = game.last_event.get(
                "sabotaged",
                False
            )

            # ------------------------------------------------
            # LABORATORY
            # ------------------------------------------------

            if room == "Laboratory":

                st.markdown(
                    """
                    <div class="clue-box">

                    <div class="clue-title">
                        📄 INCIDENT REPORT #047
                    </div>

                    The maintenance note looks ordinary at first.

                    But six letters have been strangely capitalized.

                    <b>Read only those unusual capital letters.</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    """
                    <div class="note-box">
the terminal looked undamaZed after the alarm.
the access log was chEcked twice.
the storage route was maPped.
the corridor patH was reviewed.
the security entry was copYied.
the final report was signeR.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.info(
                    "Hidden message: Z E P H Y R"
                )

                st.success(
                    "The laboratory clue strongly points toward Zephyr."
                )

            # ------------------------------------------------
            # STORAGE
            # ------------------------------------------------

            elif room == "Storage":

                if sabotaged:

                    st.warning(
                        "⚠ The Mole tampered with part of this clue, "
                        "but the important badge evidence remains."
                    )

                    st.markdown(
                        """
                        <div class="clue-box">

                        <div class="clue-title">
                            📦 ALTERED STORAGE NOTE
                        </div>

                        I have no feet, but I can follow.<br>
                        I have no mouth, but I can warn.<br>
                        I disappear when the lights go out.<br><br>

                        <b>What am I?</b>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        """
                        <div class="note-box">
MOTION LOG

The written description has been damaged.

Badge detected: Z-07

The facility register identifies Z-07
as belonging to Zephyr.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.info(
                        "The riddle was tampered with, "
                        "but the badge evidence is still usable."
                    )

                else:

                    st.markdown(
                        """
                        <div class="clue-box">

                        <div class="clue-title">
                            📦 HANDWRITTEN NOTE — BOX 17
                        </div>

                        I have no feet, but I can follow.<br>
                        I have no mouth, but I can warn.<br>
                        I disappear when the lights go out.<br><br>

                        <b>What am I?</b>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        """
                        <div class="note-box">
Answer: A SHADOW

MOTION LOG

23:44 — Movement detected near Storage.

Badge detected: Z-07

Facility register:
Z-07 = Zephyr
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.success(
                        "The storage evidence links Zephyr to the area."
                    )

            # ------------------------------------------------
            # CAFETERIA
            # ------------------------------------------------

            elif room == "Cafeteria":

                if sabotaged:

                    st.warning(
                        "⚠ The cafeteria evidence was tampered with, "
                        "but the PIN and terminal ID are still readable."
                    )

                    st.markdown(
                        """
                        <div class="clue-box">

                        <div class="clue-title">
                            🍔 SURVIVOR SUPPLY UNIT
                        </div>

                        Emergency PIN =
                        number of survivors × 2

                        <br><br>

                        Survivors: <b>5</b>

                        <br>

                        PIN: <b>10</b>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        """
                        <div class="note-box">
ACCESS RECORD

Some details have been smeared.

PIN used: 10

Terminal ID: Z-07

Facility register:
Z-07 = Zephyr
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.info(
                        "The Mole damaged the record, "
                        "but the PIN clue and Zephyr connection survived."
                    )

                else:

                    st.markdown(
                        """
                        <div class="clue-box">

                        <div class="clue-title">
                            🍔 SURVIVOR SUPPLY UNIT
                        </div>

                        Emergency PIN =
                        number of survivors × 2

                        <br><br>

                        Survivors: <b>5</b>

                        <br>

                        Therefore:

                        <h2>5 × 2 = 10</h2>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        """
                        <div class="note-box">
ACCESS RECORD

Time: 23:47

PIN entered: 10

Terminal ID: Z-07

Facility register:
Z-07 = Zephyr
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.success(
                        "The cafeteria PIN activity connects Zephyr "
                        "to the restricted system."
                    )


# ============================================================
# QUESTIONING
# ============================================================

with tab_question:

    st.header("💬 Question the Survivors")

    st.write(
        "Each survivor can only be questioned once. "
        "Choose your question carefully."
    )

    available_characters = [
        character
        for character in CHARACTERS
        if character not in game.questioned_characters
    ]

    if not available_characters:

        st.info(
            "You have questioned everyone."
        )

    else:

        selected_character = st.selectbox(
            "Choose a survivor",
            available_characters
        )

        selected_question = st.selectbox(
            "Choose a question",
            QUESTIONS
        )

        if st.button(
            "💬 ASK QUESTION",
            use_container_width=True,
            disabled=(
                game.actions_remaining <= 0
            )
        ):

            game.ask_question(
                selected_character,
                selected_question
            )

            st.rerun()


    # --------------------------------------------------------
    # SHOW MOST RECENT ANSWER
    # --------------------------------------------------------

    if (
        game.last_event is not None
        and game.last_event.get("type") == "question"
    ):

        event = game.last_event

        st.divider()

        st.subheader(
            f"💬 {event['character']}'s Answer"
        )

        st.markdown(
            f"""
            <div class="clue-box">

            <b>Question:</b><br>
            {event["question"]}

            <br><br>

            <b>Answer:</b><br>
            {event["response"]}

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# EVIDENCE BOARD
# ============================================================

with tab_evidence:

    st.header("🧾 Evidence Board")

    st.write(
        "Review everything you have discovered so far."
    )

    if not game.evidence:

        st.info(
            "No evidence collected yet. "
            "Investigate a room to begin."
        )

    else:

        for number, evidence in enumerate(
            game.evidence,
            start=1
        ):

            st.markdown(
                f"""
                <div class="evidence-box">
                    <b>Evidence #{number}</b><br><br>
                    🔎 {evidence}
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    st.subheader("📊 Current Suspicion")

    for character in CHARACTERS:

        suspicion = game.suspicion[character]

        if suspicion >= 60:

            css_class = "suspect-high"
            label = "HIGH SUSPICION"

        elif suspicion >= 30:

            css_class = "suspect-medium"
            label = "MEDIUM SUSPICION"

        else:

            css_class = "suspect-safe"
            label = "LOW SUSPICION"

        st.markdown(
            f"""
            **{character}**

            <span class="{css_class}">
            {label} — {suspicion}%
            </span>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            suspicion / 100
        )


# ============================================================
# ACCUSATION
# ============================================================

with tab_accuse:

    st.header("⚖️ Make Your Accusation")

    st.write(
        "When you are confident, select the person you believe "
        "is the Mole."
    )

    st.warning(
        "⚠ Once you accuse someone, the investigation ends."
    )

    suspect = st.selectbox(
        "Who is the Mole?",
        CHARACTERS,
        key="accusation_select"
    )

    selected_suspicion = game.suspicion[suspect]

    st.write(
        f"Current suspicion of **{suspect}**: "
        f"**{selected_suspicion}%**"
    )

    if selected_suspicion >= 60:

        st.error(
            "🔴 High suspicion"
        )

    elif selected_suspicion >= 30:

        st.warning(
            "🟡 Medium suspicion"
        )

    else:

        st.success(
            "🟢 Low suspicion"
        )

    st.divider()

    if st.button(
        f"⚖️ ACCUSE {suspect.upper()}",
        use_container_width=True,
        disabled=(
            game.actions_remaining <= 0
        )
    ):

        game.accuse(
            suspect
        )

        st.rerun()


# ============================================================
# ACTIVITY LOG
# ============================================================

st.divider()

st.header("📜 Activity Log")

if game.activity_log:

    for event in reversed(
        game.activity_log[-8:]
    ):

        st.markdown(
            f"""
            <div class="log-box">
                {event}
            </div>
            """,
            unsafe_allow_html=True
        )

else:

    st.caption(
        "No activity recorded yet."
    )


# ============================================================
# OPTIMAL PATH
# ============================================================

with st.expander(
    "🧠 Developer / Strategy Information"
):

    st.write(
        "The guaranteed shortest solution is:"
    )

    optimal_path = solve_optimal_path()

    for number, step in enumerate(
        optimal_path,
        start=1
    ):

        st.write(
            f"**{number}.** {step}"
        )

    st.caption(
        "The Laboratory cannot be sabotaged, so the hidden "
        "capital-letter clue provides a guaranteed route "
        "toward the correct suspect."
    )
