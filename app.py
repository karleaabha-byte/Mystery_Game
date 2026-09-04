import streamlit as st

from game import Game
from case import CHARACTERS, MOLE, MAX_ACTIONS, ROOMS, QUESTIONS


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Who Is The Mole?",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
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
                #18243a 0%,
                #0d1422 40%,
                #080d16 100%
            );
        color: #f5f7fa;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        text-align: center;
        color: #aeb8c8;
        margin-bottom: 2rem;
    }

    .researcher-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        padding: 1rem 1.3rem;
        margin-bottom: 1.5rem;
    }

    .metric-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        min-height: 120px;
    }

    .metric-label {
        color: #9da8ba;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 800;
        margin-top: 0.3rem;
    }

    .room-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 18px;
        padding: 1.2rem;
        margin-bottom: 1rem;
    }

    .room-title {
        font-size: 1.35rem;
        font-weight: 750;
        color: #ffffff;
    }

    .room-description {
        color: #aeb8c8;
        margin-top: 0.4rem;
    }

    .clue-card {
        background: rgba(0,0,0,0.25);
        border-left: 4px solid #718096;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }

    .evidence-card {
        background: rgba(255,255,255,0.045);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }

    .win-card {
        background: rgba(30, 120, 70, 0.18);
        border: 1px solid rgba(70, 200, 120, 0.35);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .lose-card {
        background: rgba(150, 45, 45, 0.18);
        border: 1px solid rgba(230, 90, 90, 0.35);
        border-radius: 18px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    [data-testid="stSidebar"] {
        background: #0b111c;
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

if "last_room_result" not in st.session_state:
    st.session_state.last_room_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = None

if "accusation_result" not in st.session_state:
    st.session_state.accusation_result = None


game = st.session_state.game


# ============================================================
# START SCREEN
# ============================================================

if game is None:

    st.markdown(
        '<div class="main-title">🕵️ WHO IS THE MOLE?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">A mystery of sabotage, secrets, and conflicting stories.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="researcher-card">
            <h3>🔬 Begin Your Investigation</h3>
            <p style="color:#aeb8c8;">
                Five survivors remain inside the facility.
                One of them is secretly working against you.
                Search the rooms, question the survivors,
                compare the evidence, and identify the Mole.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.form("start_game_form"):

        player_name = st.text_input(
            "Researcher name",
            placeholder="Enter your name..."
        )

        submitted = st.form_submit_button(
            "🚨 START INVESTIGATION",
            use_container_width=True
        )

        if submitted:

            if not player_name.strip():

                st.warning(
                    "Please enter your researcher name."
                )

            else:

                st.session_state.player_name = (
                    player_name.strip()
                )

                st.session_state.game = Game(
                    player_name=player_name.strip()
                )

                st.rerun()

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🕵️ Researcher")

    st.markdown(
        f"""
        <div class="researcher-card">
            <strong>{game.player_name}</strong><br>
            <span style="color:#9da8ba;">
                Lead Investigator
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### ⚡ Investigation Status")

    st.write(
        f"**Actions remaining:** "
        f"{game.actions_left} / {MAX_ACTIONS}"
    )

    st.progress(
        game.actions_left / MAX_ACTIONS
    )

    st.markdown("### 👁️ Suspicion")

    for character in CHARACTERS:

        suspicion = min(
            game.suspicion.get(character, 0),
            100
        )

        st.write(
            f"**{character}** — {suspicion}%"
        )

        st.progress(
            suspicion / 100
        )

    st.markdown("---")

    st.markdown("### 📜 Rules")

    st.markdown(
        """
        - You have a limited number of actions.
        - Investigating a room costs 1 action.
        - Questioning a survivor costs 1 action.
        - You may accuse when you are ready.
        - Evidence can be incomplete or misleading.
        - Cross-reference different clues.
        """
    )

    st.markdown("---")

    if st.button(
        "🔄 Restart Investigation",
        use_container_width=True
    ):

        st.session_state.game = Game(
            player_name=st.session_state.player_name
        )

        st.session_state.last_room_result = None
        st.session_state.last_question = None
        st.session_state.accusation_result = None

        st.rerun()

    if st.button(
        "👤 Change Researcher",
        use_container_width=True
    ):

        st.session_state.game = None

        st.session_state.last_room_result = None
        st.session_state.last_question = None
        st.session_state.accusation_result = None

        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🕵️ WHO IS THE MOLE?</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Facility Investigation • Case #047</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="researcher-card">
        <strong>🔬 Researcher:</strong>
        {game.player_name}
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <strong>📍 Status:</strong>
        Investigation active
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TOP METRICS
# ============================================================

actions_used = MAX_ACTIONS - game.actions_left
rooms_searched = len(game.investigated_rooms)
evidence_count = len(game.clues)

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Actions Remaining
            </div>
            <div class="metric-value">
                {game.actions_left}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Actions Used
            </div>
            <div class="metric-value">
                {actions_used}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Rooms Searched
            </div>
            <div class="metric-value">
                {rooms_searched}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">
                Evidence
            </div>
            <div class="metric-value">
                {evidence_count}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# GAME OVER
# ============================================================

if game.game_over:

    if game.accusation == MOLE:

        st.markdown(
            f"""
            <div class="win-card">
                <h2>🎉 CASE SOLVED</h2>
                <p>
                    Excellent work,
                    <strong>{game.player_name}</strong>.
                </p>
                <p>
                    Your accusation of
                    <strong>{game.accusation}</strong>
                    was correct.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="lose-card">
                <h2>❌ INVESTIGATION FAILED</h2>
                <p>
                    Your accusation of
                    <strong>{game.accusation}</strong>
                    was incorrect.
                </p>
                <p>
                    The Mole was
                    <strong>{MOLE}</strong>.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("## 📊 Investigation Statistics")

    s1, s2, s3 = st.columns(3)

    with s1:
        st.metric(
            "Actions Used",
            actions_used
        )

    with s2:
        st.metric(
            "Rooms Investigated",
            rooms_searched
        )

    with s3:
        st.metric(
            "Questions Asked",
            len(game.questioned_characters)
        )

    st.markdown("---")

    st.markdown("## 🧾 Final Evidence Board")

    clues = game.get_clues()

    if clues:

        for index, clue in enumerate(
            clues,
            1
        ):

            room_name = clue.get(
                "room",
                "Unknown"
            )

            data = clue.get(
                "data",
                {}
            )

            st.markdown(
                f"""
                <div class="evidence-card">
                    <strong>
                        Evidence #{index}
                    </strong>
                    <br>
                    <span style="color:#9da8ba;">
                        📍 {room_name}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            clue_type = data.get("type")

            if clue_type == "lab_note":

                st.markdown(
                    f"### {data.get('title', 'Incident Report')}"
                )

                if data.get("date"):
                    st.caption(
                        data["date"]
                    )

                for time, text in data.get(
                    "lines",
                    []
                ):

                    st.write(
                        f"**{time}** — {text}"
                    )

                if data.get("note"):
                    st.info(
                        data["note"]
                    )

                if data.get("signature"):
                    st.caption(
                        data["signature"]
                    )

            elif clue_type == "riddle":

                st.markdown(
                    f"### {data.get('title', 'Storage Note')}"
                )

                if data.get("text"):
                    st.code(
                        data["text"],
                        language="text"
                    )

                if data.get("hint"):
                    st.info(
                        data["hint"]
                    )

                if data.get("entries"):

                    st.markdown(
                        "#### Access / Movement Log"
                    )

                    for entry in data["entries"]:
                        st.write(entry)

                if data.get("note"):
                    st.info(
                        data["note"]
                    )

            elif clue_type == "vending":

                st.markdown(
                    f"### {data.get('title', 'Supply Unit')}"
                )

                if data.get("instruction"):
                    st.write(
                        data["instruction"]
                    )

                if data.get("survivors") is not None:
                    st.write(
                        f"**Survivors:** "
                        f"{data['survivors']}"
                    )

                if data.get("pin"):
                    st.write(
                        f"**PIN entered:** "
                        f"{data['pin']}"
                    )

                if data.get("terminal_id"):
                    st.write(
                        f"**Terminal ID:** "
                        f"{data['terminal_id']}"
                    )

                if data.get("note"):
                    st.info(
                        data["note"]
                    )

            else:

                for key, value in data.items():

                    if key == "type":
                        continue

                    if isinstance(value, list):

                        for item in value:
                            st.write(item)

                    else:

                        st.write(
                            f"**{key.replace('_', ' ').title()}:** "
                            f"{value}"
                        )

    else:

        st.info(
            "No evidence was collected."
        )

    st.markdown("---")

    if st.button(
        "🔄 PLAY AGAIN",
        use_container_width=True
    ):

        st.session_state.game = Game(
            player_name=st.session_state.player_name
        )

        st.session_state.last_room_result = None
        st.session_state.last_question = None
        st.session_state.accusation_result = None

        st.rerun()

    st.stop()


# ============================================================
# MAIN TABS
# ============================================================

tab_rooms, tab_questions, tab_evidence, tab_accuse = st.tabs(
    [
        "🔎 INVESTIGATE ROOMS",
        "💬 QUESTION SURVIVORS",
        "🧾 EVIDENCE BOARD",
        "⚖️ ACCUSE"
    ]
)


# ============================================================
# INVESTIGATE ROOMS
# ============================================================

with tab_rooms:

    st.markdown(
        '<h2 class="section-title">🔎 Investigate Rooms</h2>',
        unsafe_allow_html=True
    )

    st.write(
        "Search the facility for physical evidence and records."
    )

    for room_name, room in ROOMS.items():

        # ----------------------------------------------------
        # ROOM CARD
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="room-card">

                <div class="room-title">
                    {room.get("icon", "📍")} {room_name}
                </div>

                <div class="room-description">
                    {room.get("description", "")}
                </div>

                <p style="color:#d5dbe5;">
                    <strong>Object:</strong>
                    {room.get("object", "")}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # ALREADY INVESTIGATED
        # ----------------------------------------------------

        if room_name in game.investigated_rooms:

            st.success(
                f"✓ {room_name} already investigated."
            )

        else:

            if st.button(
                f"🔍 Investigate {room_name}",
                key=f"investigate_{room_name}",
                use_container_width=True,
                disabled=game.actions_left <= 0
            ):

                result = game.investigate_room(
                    room_name
                )

                st.session_state.last_room_result = result

                st.rerun()


    # ========================================================
    # RECENT FINDING
    # ========================================================

    if st.session_state.last_room_result:

        st.markdown("---")

        st.markdown("## 🧩 Recent Finding")

        st.info(
            st.session_state.last_room_result
        )

        if game.clues:

            latest = game.clues[-1]

            data = latest.get(
                "data",
                {}
            )

            st.markdown(
                f"""
                <div class="clue-card">
                    <strong>
                        {data.get(
                            "title",
                            "Evidence recovered"
                        )}
                    </strong>
                </div>
                """,
                unsafe_allow_html=True
            )

            clue_type = data.get("type")

            # ------------------------------------------------
            # LABORATORY
            # ------------------------------------------------

            if clue_type == "lab_note":

                if data.get("date"):

                    st.caption(
                        data["date"]
                    )

                for time, text in data.get(
                    "lines",
                    []
                ):

                    st.write(
                        f"**{time}** — {text}"
                    )

                if data.get("note"):

                    st.info(
                        data["note"]
                    )

                if data.get("signature"):

                    st.caption(
                        data["signature"]
                    )

            # ------------------------------------------------
            # STORAGE
            # ------------------------------------------------

            elif clue_type == "riddle":

                if data.get("text"):

                    st.code(
                        data["text"],
                        language="text"
                    )

                if data.get("hint"):

                    st.info(
                        data["hint"]
                    )

                if data.get("entries"):

                    st.markdown(
                        "### Access / Movement Log"
                    )

                    for entry in data["entries"]:

                        st.write(
                            entry
                        )

                if data.get("note"):

                    st.info(
                        data["note"]
                    )

            # ------------------------------------------------
            # CAFETERIA
            # ------------------------------------------------

            elif clue_type == "vending":

                if data.get("instruction"):

                    st.write(
                        data["instruction"]
                    )

                if data.get("survivors") is not None:

                    st.write(
                        f"**Survivors:** "
                        f"{data['survivors']}"
                    )

                if data.get("pin"):

                    st.write(
                        f"**PIN entered:** "
                        f"{data['pin']}"
                    )

                if data.get("terminal_id"):

                    st.write(
                        f"**Terminal ID:** "
                        f"{data['terminal_id']}"
                    )

                if data.get("note"):

                    st.info(
                        data["note"]
                    )

            # ------------------------------------------------
            # GENERIC CLUE
            # ------------------------------------------------

            else:

                for key, value in data.items():

                    if key == "type":
                        continue

                    if isinstance(value, list):

                        for item in value:
                            st.write(item)

                    else:

                        st.write(
                            f"**{key.replace('_', ' ').title()}:** "
                            f"{value}"
                        )


# ============================================================
# QUESTION SURVIVORS
# ============================================================

with tab_questions:

    st.markdown(
        '<h2 class="section-title">💬 Question Survivors</h2>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask survivors about the incident. "
        "Compare their answers with the physical evidence."
    )

    selected_character = st.selectbox(
        "Choose a survivor",
        CHARACTERS,
        key="selected_character"
    )

    selected_question = st.selectbox(
        "Choose a question",
        QUESTIONS,
        key="selected_question"
    )

    already_questioned = (
        selected_character
        in game.questioned_characters
    )

    if already_questioned:

        st.warning(
            f"You have already questioned "
            f"{selected_character}."
        )

    if st.button(
        "💬 Ask Question",
        use_container_width=True,
        disabled=(
            game.actions_left <= 0
            or already_questioned
        )
    ):

        response = game.question_character(
            selected_character,
            selected_question
        )

        st.session_state.last_question = {
            "character": selected_character,
            "question": selected_question,
            "response": response
        }

        st.rerun()


    if st.session_state.last_question:

        st.markdown("---")

        question_data = (
            st.session_state.last_question
        )

        st.markdown(
            f"""
            <div class="evidence-card">

                <strong>
                    💬 {question_data["character"]}
                </strong>

                <p style="color:#9da8ba;">
                    Question:
                    {question_data["question"]}
                </p>

                <p>
                    {question_data["response"]}
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# EVIDENCE BOARD
# ============================================================

with tab_evidence:

    st.markdown(
        '<h2 class="section-title">🧾 Evidence Board</h2>',
        unsafe_allow_html=True
    )

    clues = game.get_clues()

    if not clues:

        st.info(
            "No evidence collected yet. "
            "Investigate a room to begin."
        )

    else:

        for index, clue in enumerate(
            clues,
            1
        ):

            room_name = clue.get(
                "room",
                "Unknown"
            )

            data = clue.get(
                "data",
                {}
            )

            st.markdown(
                f"""
                <div class="evidence-card">

                    <strong>
                        Evidence #{index}
                    </strong>

                    <br>

                    <span style="color:#9da8ba;">
                        📍 {room_name}
                    </span>

                </div>
                """,
                unsafe_allow_html=True
            )

            clue_type = data.get("type")

            # ------------------------------------------------
            # LAB
            # ------------------------------------------------

            if clue_type == "lab_note":

                st.markdown(
                    f"### {data.get('title', 'Incident Report')}"
                )

                if data.get("date"):

                    st.caption(
                        data["date"]
                    )

                for time, text in data.get(
                    "lines",
                    []
                ):

                    st.write(
                        f"**{time}** — {text}"
                    )

                if data.get("note"):

                    st.info(
                        data["note"]
                    )

                if data.get("signature"):

                    st.caption(
                        data["signature"]
                    )

            # ------------------------------------------------
            # STORAGE
            # ------------------------------------------------

            elif clue_type == "riddle":

                st.markdown(
                    f"### {data.get('title', 'Storage Note')}"
                )

                if data.get("text"):

                    st.code(
                        data["text"],
                        language="text"
                    )

                if data.get("hint"):

                    st.info(
                        data["hint"]
                    )

                if data.get("entries"):

                    st.markdown(
                        "#### Access / Movement Log"
                    )

                    for entry in data["entries"]:

                        st.write(
                            entry
                        )

                if data.get("note"):

                    st.info(
                        data["note"]
                    )

            # ------------------------------------------------
            # CAFETERIA
            # ------------------------------------------------

            elif clue_type == "vending":

                st.markdown(
                    f"### {data.get('title', 'Supply Unit')}"
                )

                if data.get("instruction"):

                    st.write(
                        data["instruction"]
                    )

                if data.get("survivors") is not None:

                    st.write(
                        f"**Survivors:** "
                        f"{data['survivors']}"
                    )

                if data.get("pin"):

                    st.write(
                        f"**PIN entered:** "
                        f"{data['pin']}"
                    )

                if data.get("terminal_id"):

                    st.write(
                        f"**Terminal ID:** "
                        f"{data['terminal_id']}"
                    )

                if data.get("note"):

                    st.info(
                        data["note"]
                    )

            # ------------------------------------------------
            # GENERIC
            # ------------------------------------------------

            else:

                for key, value in data.items():

                    if key == "type":
                        continue

                    if isinstance(value, list):

                        for item in value:
                            st.write(item)

                    else:

                        st.write(
                            f"**{key.replace('_', ' ').title()}:** "
                            f"{value}"
                        )


# ============================================================
# ACCUSATION
# ============================================================

with tab_accuse:

    st.markdown(
        '<h2 class="section-title">⚖️ Make Your Accusation</h2>',
        unsafe_allow_html=True
    )

    st.write(
        "Choose carefully. Once you accuse someone, "
        "the investigation ends."
    )

    st.warning(
        "⚠️ Make sure you have cross-referenced "
        "the evidence before accusing."
    )

    accusation = st.selectbox(
        "Who do you believe is the Mole?",
        CHARACTERS,
        key="accusation_character"
    )

    if st.button(
        "⚖️ ACCUSE",
        use_container_width=True,
        disabled=game.actions_left <= 0
    ):

        result = game.accuse(
            accusation
        )

        st.session_state.accusation_result = result

        st.rerun()

    if st.session_state.accusation_result:

        st.markdown("---")

        if accusation == MOLE:

            st.success(
                st.session_state.accusation_result
            )

        else:

            st.error(
                st.session_state.accusation_result
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "🕵️ Case #047 • Trust the evidence, not the stories."
)
