import streamlit as st
from chatbot_backend import (
    generate_case_file, parse_case_file,
    init_game_memory, ask_suspect, make_accusation
)
from game_state import new_game_state, add_clue, remove_clue, log_exchange

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Murder at Midnight",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS — noir aesthetic ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Crimson+Pro:ital,wght@0,400;0,600;1,400&display=swap');

html, body, [class*="css"] {
    font-family: 'Crimson Pro', Georgia, serif;
}

/* Background */
.stApp {
    background-color: #0d0b08;
    color: #d4c9a8;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #12100d;
    border-right: 1px solid #3a2e1e;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Playfair Display', Georgia, serif;
    color: #e8d5a3;
    letter-spacing: 0.02em;
}

/* The big title */
.murder-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.8rem;
    font-weight: 700;
    color: #e8d5a3;
    text-align: center;
    letter-spacing: 0.05em;
    margin-bottom: 0;
    line-height: 1.1;
}
.murder-subtitle {
    font-family: 'Crimson Pro', Georgia, serif;
    font-style: italic;
    font-size: 1.1rem;
    color: #7a6e58;
    text-align: center;
    margin-bottom: 1.5rem;
    letter-spacing: 0.08em;
}

/* Setting card */
.setting-card {
    background: #1a1610;
    border: 1px solid #3a2e1e;
    border-left: 3px solid #8b6914;
    padding: 0.8rem 1.2rem;
    border-radius: 2px;
    font-style: italic;
    color: #b0a07a;
    margin-bottom: 1rem;
    font-size: 1.05rem;
}

/* Suspect cards */
.suspect-btn {
    width: 100%;
    background: #1a1610;
    border: 1px solid #3a2e1e;
    color: #c8b98a;
    padding: 0.6rem 1rem;
    text-align: left;
    cursor: pointer;
    font-family: 'Crimson Pro', serif;
    font-size: 1rem;
    border-radius: 2px;
    margin-bottom: 0.3rem;
    transition: all 0.2s;
}
.suspect-btn:hover, .suspect-btn.active {
    background: #2a2016;
    border-color: #8b6914;
    color: #e8d5a3;
}

/* Chat bubbles */
.chat-question {
    background: #1e1a12;
    border-left: 2px solid #5a4a2a;
    padding: 0.6rem 1rem;
    margin: 0.5rem 0 0.2rem 0;
    border-radius: 0 4px 4px 0;
    color: #a09070;
    font-style: italic;
}
.chat-question::before {
    content: "You: ";
    font-weight: 600;
    color: #8b6914;
    font-style: normal;
}
.chat-answer {
    background: #161210;
    border-left: 2px solid #8b6914;
    padding: 0.7rem 1rem;
    margin: 0.2rem 0 0.8rem 1rem;
    border-radius: 0 4px 4px 0;
    color: #d4c9a8;
    line-height: 1.6;
}
.suspect-label {
    font-size: 0.75rem;
    color: #6a5a3a;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.2rem;
}

/* Clue notebook */
.clue-item {
    background: #1a1a10;
    border: 1px solid #3a3a20;
    padding: 0.4rem 0.7rem;
    border-radius: 2px;
    margin-bottom: 0.3rem;
    color: #c8b870;
    font-size: 0.95rem;
}

/* Accusation box */
.accusation-box {
    border: 1px solid #8b6914;
    background: #1a1408;
    padding: 1.2rem;
    border-radius: 4px;
    margin-top: 1rem;
}

/* Reveal text */
.reveal-box {
    border: 1px solid #6a2020;
    background: #120a0a;
    padding: 1.2rem;
    border-radius: 4px;
    line-height: 1.7;
    color: #d4c9a8;
    font-size: 1.05rem;
}
.reveal-correct {
    border-color: #2a6a2a;
    background: #0a120a;
}

/* Stats */
.stat-chip {
    display: inline-block;
    background: #1e1a12;
    border: 1px solid #3a2e1e;
    padding: 0.15rem 0.6rem;
    border-radius: 12px;
    font-size: 0.82rem;
    color: #7a6e58;
    margin-right: 0.4rem;
}

/* Input styling */
.stTextInput > div > div > input {
    background-color: #1a1610 !important;
    border: 1px solid #3a2e1e !important;
    color: #d4c9a8 !important;
    border-radius: 2px !important;
    font-family: 'Crimson Pro', serif !important;
    font-size: 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #8b6914 !important;
    box-shadow: 0 0 0 1px #8b691420 !important;
}

/* Buttons */
.stButton > button {
    background: #1a1610;
    border: 1px solid #8b6914;
    color: #e8d5a3;
    font-family: 'Playfair Display', serif;
    letter-spacing: 0.05em;
    border-radius: 2px;
    font-size: 0.95rem;
}
.stButton > button:hover {
    background: #2a2016;
    border-color: #c8a030;
    color: #f0e0b0;
}

/* Selectbox */
.stSelectbox > div > div {
    background-color: #1a1610 !important;
    border: 1px solid #3a2e1e !important;
    color: #d4c9a8 !important;
}

/* Divider */
hr {
    border-color: #2a2016;
    margin: 1rem 0;
}

/* Scrollable chat area */
.chat-scroll {
    max-height: 420px;
    overflow-y: auto;
    padding-right: 0.5rem;
}

/* Loading spinner text */
.stSpinner > div {
    color: #8b6914 !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab-list"] {
    background: #12100d;
    border-bottom: 1px solid #3a2e1e;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Crimson Pro', serif;
    color: #7a6e58;
}
.stTabs [aria-selected="true"] {
    color: #e8d5a3 !important;
    border-bottom-color: #8b6914 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state bootstrap ──────────────────────────────────────────────────
if "gs" not in st.session_state:
    st.session_state.gs = new_game_state()


gs = st.session_state.gs


# ── SIDEBAR — Clue Notebook + Stats ─────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🕵️ Detective's Notebook")
    st.markdown("---")

    if gs["phase"] != "loading" and gs["case_data"]:
        cd = gs["case_data"]
        st.markdown(f"**Setting:** *{cd.get('setting', '—')}*")
        st.markdown(f"**Victim:** {cd.get('victim', '—')}")
        st.markdown(f"**Questions asked:** {gs['questions_asked']}")
        st.markdown("---")

    st.markdown("**📋 Your clues**")

    if not gs["clues_collected"]:
        st.markdown("*No clues noted yet. Save answers that seem important.*")
    else:
        for i, clue in enumerate(gs["clues_collected"]):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f'<div class="clue-item">🔍 {clue}</div>', unsafe_allow_html=True)
            with col2:
                if st.button("✕", key=f"del_clue_{i}", help="Remove clue"):
                    remove_clue(gs, i)
                    st.rerun()

    st.markdown("---")

    if gs["phase"] == "playing":
        st.markdown("*Tip: Ask about alibis, relationships with the victim, and where they were that night.*")

    if gs["phase"] in ("playing", "accused"):
        st.markdown("---")
        if st.button("🔄 New Mystery", use_container_width=True):
            st.session_state.gs = new_game_state()
            st.rerun()


# ── MAIN AREA ────────────────────────────────────────────────────────────────
st.markdown('<div class="murder-title">🔪 Murder at Midnight</div>', unsafe_allow_html=True)
st.markdown('<div class="murder-subtitle">A Detective Mystery — Question suspects. Uncover the truth.</div>', unsafe_allow_html=True)


# ── PHASE: LOADING (start screen) ───────────────────────────────────────────
if gs["phase"] == "loading":
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.markdown("""
        <div style='text-align:center; color:#7a6e58; font-style:italic; font-size:1.1rem; margin-bottom:2rem;'>
        A murder has been committed.<br>Four suspects. One killer.<br>Can you solve the case?
        </div>
        """, unsafe_allow_html=True)

        if st.button("🕵️ Begin New Investigation", use_container_width=True):
            with st.spinner("Generating your mystery..."):
                case_text = generate_case_file()
                case_data = parse_case_file(case_text)
                memory = init_game_memory(case_text)

                gs["case_file_text"] = case_text
                gs["case_data"] = case_data
                gs["memory"] = memory
                gs["current_suspect"] = case_data["suspects"][0] if case_data["suspects"] else None
                gs["phase"] = "playing"
            st.rerun()


# ── PHASE: PLAYING ───────────────────────────────────────────────────────────
elif gs["phase"] == "playing":
    cd = gs["case_data"]

    # Setting banner
    st.markdown(f'<div class="setting-card">📍 {cd.get("setting", "Unknown location")}</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    # Left: suspect selector
    with col_left:
        st.markdown("**Choose a suspect to interrogate:**")
        for suspect in cd.get("suspects", []):
            is_active = gs["current_suspect"] == suspect
            style = "active" if is_active else ""
            if st.button(
                f"{'▶ ' if is_active else '   '}{suspect}",
                key=f"suspect_{suspect}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                gs["current_suspect"] = suspect
                st.rerun()

        st.markdown("---")
        st.markdown("**Scene clues:**")
        for clue in cd.get("clues", []):
            st.markdown(f"🔎 *{clue}*")

    # Right: interrogation area
    with col_right:
        current = gs["current_suspect"]
        st.markdown(f"### Interrogating: {current}")

        # Chat log for this suspect
        suspect_log = [e for e in gs["chat_log"] if e["suspect"] == current]

        if suspect_log:
            with st.container():
                for entry in suspect_log:
                    st.markdown(f'<div class="chat-question">{entry["question"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="suspect-label">{entry["suspect"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-answer">{entry["answer"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="color:#5a4a2a; font-style:italic; margin-bottom:1rem;">'
                       f'You approach {current}. They watch you warily...</div>', unsafe_allow_html=True)

        # Question input
        with st.form(key=f"question_form_{current}", clear_on_submit=True):
            question = st.text_input(
                "Your question:",
                placeholder=f'Ask {current} something...',
                label_visibility="collapsed"
            )
            col_ask, col_save = st.columns([3, 2])
            with col_ask:
                submitted = st.form_submit_button("Ask →", use_container_width=True)

        if submitted and question.strip():
            with st.spinner(f"{current} considers your question..."):
                answer = ask_suspect(question.strip(), current, gs["memory"])
            log_exchange(gs, current, question.strip(), answer)
            st.rerun()

        # Save last answer as clue
        if suspect_log:
            last_answer = suspect_log[-1]["answer"]
            if st.button("📌 Save last answer as clue", key="save_clue"):
                short = last_answer[:120] + "..." if len(last_answer) > 120 else last_answer
                add_clue(gs, f"[{current}] {short}")
                st.rerun()

    # ── Accusation section ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔒 Make Your Accusation")
    st.markdown("*Choose wisely — you only get one shot.*")

    with st.expander("Ready to accuse someone?"):
        st.markdown('<div class="accusation-box">', unsafe_allow_html=True)
        suspects_list = cd.get("suspects", [])

        acc_col1, acc_col2 = st.columns(2)
        with acc_col1:
            accused = st.selectbox("I accuse:", suspects_list, key="accused_person")
            weapon = st.text_input("With:", placeholder="the murder weapon...", key="acc_weapon")
        with acc_col2:
            motive = st.text_input("Because:", placeholder="their motive was...", key="acc_motive")

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("⚖️ Submit Accusation", type="primary"):
            if weapon.strip() and motive.strip():
                with st.spinner("The room falls silent..."):
                    result = make_accusation(accused, weapon.strip(), motive.strip(), gs["memory"], gs["case_file_text"])
                gs["accusation_result"] = result
                gs["phase"] = "accused"
                st.rerun()
            else:
                st.warning("Fill in the weapon and motive fields first.")


# ── PHASE: ACCUSED (reveal shown) ───────────────────────────────────────────
elif gs["phase"] == "accused":
    cd = gs["case_data"]
    st.markdown(f'<div class="setting-card">📍 {cd.get("setting", "")}</div>', unsafe_allow_html=True)

    st.markdown("### 📜 The Verdict")

    result_text = gs["accusation_result"]
    is_correct = any(word in result_text.lower() for word in ["correct", "right", "solved", "congratulations", "indeed"])

    box_class = "reveal-box reveal-correct" if is_correct else "reveal-box"
    st.markdown(f'<div class="{box_class}">{result_text}</div>', unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start a New Mystery", use_container_width=True):
            st.session_state.gs = new_game_state()
            st.rerun()
    with col2:
        if not is_correct:
            if st.button("🔙 Continue Investigating", use_container_width=True):
                gs["phase"] = "playing"
                st.rerun()

    # Show full chat log
    if gs["chat_log"]:
        with st.expander("📖 Review your full case notes"):
            for entry in gs["chat_log"]:
                st.markdown(f'<div class="chat-question">{entry["question"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="suspect-label">{entry["suspect"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="chat-answer">{entry["answer"]}</div>', unsafe_allow_html=True)