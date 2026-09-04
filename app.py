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
    page_title="WHO IS THE MOLE?",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .stApp {
        background-color: #0b0d10;
        color: #eeeeee;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #11151a;
        border-right: 1px solid #292e35;
    }


    /* -------------------------------------------------------
       MAIN TITLE
    ------------------------------------------------------- */

    .main-title {
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        line-height: 1;
        margin-bottom: 0.3rem;
    }

    .subtitle {
        color: #8d96a3;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }


    /* -------------------------------------------------------
       CARDS
    ------------------------------------------------------- */

    .case-box {
        background-color: #13171c;
        border: 1px solid #292f37;
        border-radius: 12px;
        padding: 24px;
        margin: 12px 0;
    }

    .room-card {
        background-color: #13171c;
        border: 1px solid #292f37;
        border-radius: 12px;
        padding: 20px;
        min-height: 230px;
    }

    .suspect-card {
        background-color: #13171c;
        border: 1px solid #292f37;
        border-radius: 12px;
        padding: 18px;
    }


    /* -------------------------------------------------------
       CLUES
    ------------------------------------------------------- */

    .clue-box {
        background-color: #151a20;
        border-left: 4px solid #d6a84f;
        border-radius: 8px;
        padding: 20px;
        margin: 14px 0;
    }

    .warning-box {
        background-color: #21191a;
        border-left: 4px solid #c95757;
        border-radius: 8px;
        padding: 20px;
        margin: 14px 0;
    }

    .success-box {
        background-color: #142019;
        border-left: 4px solid #56a56a;
        border-radius: 8px;
        padding: 20px;
        margin: 14px 0;
    }


    /* -------------------------------------------------------
       LABELS
    ------------------------------------------------------- */

    .small-label {
        color: #7d8794;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.72rem;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .room-icon {
        font-size: 2.4rem;
    }

    .room-name {
        font-size: 1.45rem;
        font-weight: 800;
        margin-top: 5px;
    }

    .evidence-title {
        font-size: 1.2rem;
        font-weight: 800;
        margin-bottom: 10px;
    }

    .quote {
        color: #c8cdd4;
        font-style: italic;
        border-left: 2px solid #555d67;
        padding-left: 14px;
        margin: 10px 0;
    }


    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    div.stButton > button {
        border-radius: 8px;
        font-weight: 700;
        min-height: 42px;
    }


    /* -------------------------------------------------------
       METRICS
    ------------------------------------------------------- */

    [data-testid="stMetric"] {
        background-color: #151a20;
        border: 1px solid #292f37;
        padding: 12px;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
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
# HELPER FUNCTIONS
# ============================================================

def restart_game():
    """Start a completely new investigation."""

    st.session_state.game = Game()
    st.session_state.started = True
    st.session_state.last_room_result = None
    st.session_state.last_response = None

    st.rerun()


def get_clue_data(clue):
    """
    Safely extract the actual clue data.

    Game stores clues like:

        {
            "room": "Storage",
            "data": {...}
        }
    """

    if not isinstance(clue, dict):
        return {}

    data = clue.get("data", clue)

    if not isinstance(data, dict):
        return {}

    return data


def render_clue(clue):
    """
    Render one piece of evidence.

    This function deliberately uses Streamlit markdown with
    unsafe_allow_html=True so HTML is rendered instead of
    displayed as literal text.
    """

    data = get_clue_data(clue)

    clue_type = data.get(
        "type",
        clue.get("type", "")
        if isinstance(clue, dict)
        else "",
    )


    # ========================================================
    # LABORATORY
    # ========================================================

    if clue_type in ("lab_report", "lab_note"):

        st.markdown(
            f"""
            <div class="clue-box">

                <div class="small-label">
                    LABORATORY EVIDENCE
                </div>

                <div class="evidence-title">
                    {data.get("title", "INCIDENT REPORT")}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        date = data.get("date")

        if date:
            st.markdown(f"**Date:** {date}")

        events = data.get(
            "events",
            data.get("lines", []),
        )

        if events:

            st.markdown("#### Incident Timeline")

            for event in events:

                if isinstance(event, (tuple, list)) and len(event) >= 2:

                    time = event[0]
                    description = event[1]

                    st.markdown(
                        f"**{time}** — {description}"
                    )

                else:

                    st.markdown(
                        f"• {event}"
                    )

        maintenance = data.get(
            "maintenance",
            data.get("maintenance_note"),
        )

        if maintenance:

            st.markdown("#### Maintenance Note")

            st.markdown(
                f"""
                <div class="quote">
                    {maintenance}
                </div>
                """,
                unsafe_allow_html=True,
            )

        note = data.get("note")

        if note:
            st.markdown(
                f"**Investigator note:** {note}"
            )

        signature = data.get("signature")

        if signature:
            st.markdown(
                f"*{signature}*"
            )


    # ========================================================
    # STORAGE
    # ========================================================

    elif clue_type == "storage_log":

        st.markdown(
            f"""
            <div class="clue-box">

                <div class="small-label">
                    STORAGE EVIDENCE
                </div>

                <div class="evidence-title">
                    {data.get(
                        "title",
                        "RESTRICTED STORAGE ACCESS LOG"
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        entries = data.get(
            "entries",
            [],
        )

        if entries:

            st.markdown("#### Access Log")

            for entry in entries:
                st.markdown(
                    f"• **{entry}**"
                )

        note = data.get("note")

        if note:

            st.markdown(
                f"**Note:** {note}"
            )

        handwritten = data.get(
            "handwritten",
            data.get("secondary_note"),
        )

        if handwritten:

            st.markdown("#### Handwritten Note")

            st.markdown(
                f"""
                <div class="quote">
                    {handwritten}
                </div>
                """,
                unsafe_allow_html=True,
            )


    # ========================================================
    # CAFETERIA
    # ========================================================

    elif clue_type in (
        "cafeteria_log",
        "vending",
    ):

        st.markdown(
            f"""
            <div class="clue-box">

                <div class="small-label">
                    CAFETERIA EVIDENCE
                </div>

                <div class="evidence-title">
                    {data.get(
                        "title",
                        "CAFETERIA SECURITY LOG"
                    )}
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        instruction = data.get(
            "instruction"
        )

        if instruction:

            st.markdown(
                f"**System instruction:** {instruction}"
            )

        survivors = data.get(
            "survivors"
        )

        if survivors is not None:

            st.markdown(
                f"**Registered survivors:** {survivors}"
            )

        terminal_id = data.get(
            "terminal_id"
        )

        if terminal_id:

            st.markdown(
                f"**Terminal ID:** `{terminal_id}`"
            )

        system_log = data.get(
            "system_log"
        )

        if system_log:

            st.markdown("#### System Log")

            if isinstance(system_log, list):

                system_log = "\n".join(
                    str(line)
                    for line in system_log
                )

            st.code(
                str(system_log),
                language="text",
            )

        note = data.get("note")

        if note:

            st.markdown(
                f"**Note:** {note}"
            )


    # ========================================================
    # PARTIAL / DAMAGED EVIDENCE
    # ========================================================

    elif clue_type == "partial":

        message = (
            data.get("message")
            or data.get("note")
            or "Part of the evidence is missing."
        )

        st.markdown(
            f"""
            <div class="warning-box">

                <div class="small-label">
                    PARTIAL EVIDENCE
                </div>

                <p>
                    {message}
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # ========================================================
    # FALLBACK
    # ========================================================

    else:

        st.markdown(
            """
            <div class="clue-box">

                <div class="small-label">
                    EVIDENCE
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

        for key, value in data.items():

            if key == "type":
                continue

            label = key.replace(
                "_",
                " ",
            ).title()

            if isinstance(value, list):

                st.markdown(
                    f"**{label}**"
                )

                for item in value:
                    st.markdown(
                        f"• {item}"
                    )

            else:

                st.markdown(
                    f"**{label}:** {value}"
                )


def render_interview(
    character,
    question,
    response,
):

    st.markdown(
        f"""
        <div class="case-box">

            <div class="small-label">
                INTERVIEW RECORD
            </div>

            <div class="evidence-title">
                {character}
            </div>

            <p>
                <strong>Question:</strong>
                {question}
            </p>

            <div class="quote">
                "{response}"
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# START SCREEN
# ============================================================

if not st.session_state.started:

    st.markdown(
        '<div class="main-title">WHO IS THE MOLE?</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="subtitle">
            A closed-room investigation in 12 moves.
        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # CASE INTRODUCTION
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="case-box">

            <div class="small-label">
                CASE FILE #047
            </div>

            <h2>
                Someone inside the team sabotaged the facility.
            </h2>

            <p>
                At 23:40, the facility suffered a power fluctuation.
                Three minutes later, the security alarm activated.
            </p>

            <p>
                By 23:50, restricted storage had been accessed,
                emergency systems had been used, and the cafeteria
                security cameras were offline.
            </p>

            <p>
                Five people were inside.
                One of them is lying.
            </p>

            <p>
                Your job is not to find a confession.
                Your job is to find the contradictions.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # RULES
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="case-box">

            <div class="small-label">
                INVESTIGATOR'S NOTE
            </div>

            <h3>How to play</h3>

            <p>
                You have a limited number of actions.
            </p>

            <ul>
                <li>Search locations for physical evidence.</li>
                <li>Question suspects.</li>
                <li>Compare their answers with the evidence.</li>
                <li>Look for contradictions.</li>
                <li>Accuse the person you believe is the Mole.</li>
            </ul>

            <p>
                No single clue is intended to solve the case.
                Connect the evidence.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    if st.button(
        "🔎 START INVESTIGATION",
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

    st.markdown("## 🕵️ INVESTIGATION")

    st.metric(
        "Actions Remaining",
        game.actions_left,
    )

    progress = (
        game.actions_left / MAX_ACTIONS
        if MAX_ACTIONS > 0
        else 0
    )

    st.progress(
        max(
            0,
            min(
                progress,
                1,
            ),
        )
    )

    st.caption(
        f"{game.actions_left} of {MAX_ACTIONS} actions remaining"
    )

    st.divider()

    # --------------------------------------------------------
    # INVESTIGATION STATUS
    # --------------------------------------------------------

    st.markdown("### Investigation Status")

    st.write(
        f"🧪 Locations: "
        f"**{len(game.investigated_rooms)} / {len(ROOMS)}**"
    )

    st.write(
        f"🗣️ Interviews: "
        f"**{len(game.questioned_characters)} / "
        f"{len(CHARACTERS)}**"
    )

    st.write(
        f"📁 Evidence: "
        f"**{len(game.clues)}**"
    )

    # --------------------------------------------------------
    # SEARCHED ROOMS
    # --------------------------------------------------------

    if game.investigated_rooms:

        st.divider()

        st.markdown("### Locations Searched")

        for room in game.investigated_rooms:

            icon = ROOMS.get(
                room,
                {}
            ).get(
                "icon",
                "📍",
            )

            st.write(
                f"✓ {icon} {room}"
            )

    # --------------------------------------------------------
    # QUESTIONED PEOPLE
    # --------------------------------------------------------

    if game.questioned_characters:

        st.divider()

        st.markdown("### People Questioned")

        for character in game.questioned_characters:

            st.write(
                f"✓ {character}"
            )

    st.divider()

    if st.button(
        "🔄 RESTART CASE",
        use_container_width=True,
    ):

        restart_game()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">WHO IS THE MOLE?</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="subtitle">
        Follow the evidence. Trust nobody.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GAME OVER
# ============================================================

if game.game_over:

    st.divider()

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    if game.last_accusation_correct:

        st.markdown(
            """
            <div class="success-box">

                <div class="small-label">
                    INVESTIGATION COMPLETE
                </div>

                <h2>
                    CASE SOLVED
                </h2>

                <p>
                    Your accusation was correct.
                    The evidence led you to the Mole.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
            """
            <div class="warning-box">

                <div class="small-label">
                    INVESTIGATION COMPLETE
                </div>

                <h2>
                    WRONG ACCUSATION
                </h2>

                <p>
                    Your conclusion was incorrect.
                    The evidence was not enough to support
                    the accusation you made.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # RESULT TEXT
    # --------------------------------------------------------

    if game.result:

        st.markdown(
            f"""
            <div class="case-box">
                <h3>Final Verdict</h3>
                <p>{game.result}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # COLLECTED EVIDENCE
    # --------------------------------------------------------

    st.header("📁 Evidence Collected")

    if game.clues:

        for index, clue in enumerate(
            game.clues,
            start=1,
        ):

            room_name = clue.get(
                "room",
                "Unknown location",
            )

            st.markdown(
                f"### Evidence #{index} — {room_name}"
            )

            render_clue(clue)

    else:

        st.info(
            "You collected no physical evidence."
        )


    st.divider()

    if st.button(
        "🔁 PLAY AGAIN",
        use_container_width=True,
    ):

        restart_game()

    st.stop()


# ============================================================
# MAIN TABS
# ============================================================

tab_investigate, tab_question, tab_evidence, tab_accuse = st.tabs(
    [
        "🧪 INVESTIGATE",
        "🗣️ QUESTION",
        "📁 EVIDENCE",
        "⚖️ ACCUSE",
    ]
)


# ============================================================
# INVESTIGATE TAB
# ============================================================

with tab_investigate:

    st.header("Investigate Locations")

    st.caption(
        "Searching a location costs one action. "
        "Read the details carefully — small connections matter."
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

            st.markdown(
                f"""
                <div class="room-card">

                    <div class="room-icon">
                        {room.get("icon", "📍")}
                    </div>

                    <div class="room-name">
                        {room_name}
                    </div>

                    <p>
                        {room.get("description", "")}
                    </p>

                </div>
                """,
                unsafe_allow_html=True,
            )

            st.write("")

            already_investigated = (
                room_name in game.investigated_rooms
            )

            if already_investigated:

                st.success(
                    "✓ Already investigated"
                )

            else:

                if st.button(
                    f"Search {room_name}",
                    key=f"search_{room_name}",
                    disabled=game.actions_left <= 0,
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
    # LATEST ROOM RESULT
    # --------------------------------------------------------

    if st.session_state.last_room_result:

        st.divider()

        st.subheader("Latest Investigation")

        room_name, result = (
            st.session_state.last_room_result
        )

        st.info(result)

        latest_clues = game.get_room_clues(
            room_name
        )

        if latest_clues:

            render_clue(
                latest_clues[-1]
            )


# ============================================================
# QUESTION TAB
# ============================================================

with tab_question:

    st.header("Question The Suspects")

    st.caption(
        "Each person can only be questioned once. "
        "Choose your question carefully."
    )

    for character in CHARACTERS:

        already_questioned = (
            character in game.questioned_characters
        )

        with st.expander(
            (
                f"✓ {character}"
                if already_questioned
                else character
            )
        ):

            if already_questioned:

                st.info(
                    "You have already questioned this person."
                )

            else:

                question = st.selectbox(
                    "Choose a question",
                    QUESTIONS,
                    key=f"question_select_{character}",
                )

                if st.button(
                    f"Question {character}",
                    key=f"question_button_{character}",
                    disabled=game.actions_left <= 0,
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
    # LATEST INTERVIEW
    # --------------------------------------------------------

    if st.session_state.last_response:

        st.divider()

        st.subheader("Latest Interview")

        character, question, response = (
            st.session_state.last_response
        )

        render_interview(
            character,
            question,
            response,
        )


# ============================================================
# EVIDENCE TAB
# ============================================================

with tab_evidence:

    st.header("📁 Evidence Board")

    if not game.clues:

        st.info(
            "Your evidence board is empty."
        )

        st.markdown(
            """
            <div class="case-box">

                <h3>Start looking around.</h3>

                <p>
                    Search the Laboratory, Storage, and Cafeteria.
                    Then compare what you find with what the
                    suspects tell you.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.caption(
            f"{len(game.clues)} piece(s) of physical evidence collected."
        )

        for index, clue in enumerate(
            game.clues,
            start=1,
        ):

            room_name = clue.get(
                "room",
                "Unknown",
            )

            st.markdown(
                f"### Evidence #{index} — {room_name}"
            )

            render_clue(
                clue
            )


    # --------------------------------------------------------
    # INVESTIGATOR TIPS
    # --------------------------------------------------------

    st.divider()

    st.markdown(
        """
        <div class="case-box">

            <div class="small-label">
                INVESTIGATOR'S METHOD
            </div>

            <h3>Don't look for a confession.</h3>

            <p>
                Look for things that should not be possible
                at the same time.
            </p>

            <ul>
                <li>
                    Compare timestamps.
                </li>

                <li>
                    Compare access records.
                </li>

                <li>
                    Compare someone's story with the physical evidence.
                </li>

                <li>
                    Look for repeated identifiers.
                </li>

                <li>
                    Ask yourself who would realistically have
                    access to the systems involved.
                </li>
            </ul>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ACCUSATION TAB
# ============================================================

with tab_accuse:

    st.header("⚖️ Make Your Accusation")

    st.warning(
        "Accusing ends the investigation. "
        "It does not consume an action."
    )

    st.markdown(
        """
        <div class="case-box">

            <div class="small-label">
                FINAL DECISION
            </div>

            <h3>Who is the Mole?</h3>

            <p>
                Before making your accusation, make sure you
                can explain the chain of evidence.
            </p>

            <p>
                A good accusation should connect physical evidence,
                system records, and testimony.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )


    accusation = st.selectbox(
        "Select a suspect",
        ["Select a suspect..."] + CHARACTERS,
        key="final_accusation",
    )


    if accusation != "Select a suspect...":

        st.markdown(
            f"""
            <div class="warning-box">

                <div class="small-label">
                    SELECTED SUSPECT
                </div>

                <h3>
                    {accusation}
                </h3>

                <p>
                    This will end the investigation.
                </p>

            </div>
            """,
            unsafe_allow_html=True,
        )


    if st.button(
        "⚖️ MAKE FINAL ACCUSATION",
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

st.markdown(
    """
    <div style="text-align:center; color:#666f7a;">
        CASE FILE #047 • Trust the evidence, not the story.
    </div>
    """,
    unsafe_allow_html=True,
)
