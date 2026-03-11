import streamlit as st
from rag_pipeline import ask

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="ASISSE Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Custom CSS ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #0A0E1A !important;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stMain"] { background: transparent !important; padding: 0 !important; }

.block-container {
    max-width: 860px !important;
    padding: 0 24px 120px !important;
    margin: 0 auto !important;
}

/* ── Hero ── */
.hero {
    text-align: center;
    padding: 52px 0 36px;
}

.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(99,179,237,0.15), rgba(159,122,234,0.15));
    border: 1px solid rgba(99,179,237,0.3);
    color: #90CDF4;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    padding: 6px 16px;
    border-radius: 100px;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2rem, 5vw, 3.2rem);
    line-height: 1.1;
    color: #F7FAFC;
    letter-spacing: -1px;
    margin-bottom: 12px;
}

.hero-title span {
    background: linear-gradient(135deg, #63B3ED, #9F7AEA, #F687B3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-size: 15px;
    color: #718096;
    font-weight: 300;
    letter-spacing: 0.2px;
    line-height: 1.6;
}

/* ── Stats bar ── */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 28px auto;
    max-width: 480px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    overflow: hidden;
}

.stat-item {
    flex: 1;
    text-align: center;
    padding: 14px 12px;
    border-right: 1px solid rgba(255,255,255,0.07);
}
.stat-item:last-child { border-right: none; }

.stat-number {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 18px;
    color: #63B3ED;
    display: block;
}

.stat-label {
    font-size: 10px;
    color: #4A5568;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    font-weight: 500;
    margin-top: 2px;
    display: block;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,179,237,0.2), transparent);
    margin: 8px 0 28px;
}

/* ── Chat messages ── */
.chat-wrapper { display: flex; flex-direction: column; gap: 16px; margin-bottom: 8px; }

.msg-row {
    display: flex;
    gap: 12px;
    animation: fadeSlideIn 0.35s ease both;
}

@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
}

.msg-row.user { flex-direction: row-reverse; }
.msg-row.bot  { flex-direction: row; }

.avatar {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    margin-top: 2px;
}

.avatar.user-av { background: linear-gradient(135deg, #63B3ED, #9F7AEA); }

.avatar.bot-av {
    background: linear-gradient(135deg, #2D3748, #1A202C);
    border: 1px solid rgba(99,179,237,0.25);
}

.bubble {
    max-width: 72%;
    padding: 13px 17px;
    border-radius: 16px;
    font-size: 14.5px;
    line-height: 1.65;
    font-weight: 400;
}

.bubble.user {
    background: linear-gradient(135deg, #2B4A7A, #3B3069);
    color: #EBF4FF;
    border: 1px solid rgba(99,179,237,0.2);
    border-bottom-right-radius: 4px;
}

.bubble.bot {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    color: #CBD5E0;
    border-bottom-left-radius: 4px;
}

.timestamp {
    font-size: 10px;
    color: #4A5568;
    margin-top: 4px;
    display: block;
    text-align: right;
}
.msg-row.bot .timestamp { text-align: left; }

/* ── Suggestions ── */
.suggestions-title {
    font-family: 'Syne', sans-serif;
    font-size: 11px;
    font-weight: 600;
    color: #4A5568;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 10px;
    text-align: center;
}

/* Style suggestion buttons */
div[data-testid="stColumns"] .stButton button {
    background: rgba(99,179,237,0.07) !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    color: #90CDF4 !important;
    font-size: 12.5px !important;
    padding: 7px 14px !important;
    border-radius: 100px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 400 !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

div[data-testid="stColumns"] .stButton button:hover {
    background: rgba(99,179,237,0.15) !important;
    border-color: rgba(99,179,237,0.4) !important;
    transform: translateY(-1px) !important;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 20px 0 32px;
}
.empty-icon {
    font-size: 40px;
    margin-bottom: 12px;
    display: block;
    filter: drop-shadow(0 0 20px rgba(99,179,237,0.3));
}
.empty-text {
    font-size: 14px;
    color: #4A5568;
    font-weight: 300;
    line-height: 1.7;
}

/* ── Input ── */
.input-container {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100%;
    max-width: 860px;
    padding: 16px 24px 24px;
    background: linear-gradient(to top, #0A0E1A 70%, transparent);
    z-index: 100;
}

[data-testid="stChatInput"] {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 14px !important;
    padding: 4px 8px !important;
    backdrop-filter: blur(12px);
}

[data-testid="stChatInput"]:focus-within {
    border-color: rgba(99,179,237,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,179,237,0.08) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #E2E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    caret-color: #63B3ED;
}

[data-testid="stChatInput"] textarea::placeholder { color: #4A5568 !important; }
[data-testid="stChatInputSubmitButton"] svg { fill: #63B3ED !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,179,237,0.2); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_query" not in st.session_state:
    st.session_state.pending_query = None


# ── Hero ──────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">NSO · Government of India</div>
    <div class="hero-title">ASISSE <span>AI Assistant</span></div>
    <div class="hero-sub">Annual Survey of Incorporated Services Sector Enterprises<br>Ask anything about the survey documentation</div>
</div>
<div class="stats-bar">
    <div class="stat-item"><span class="stat-number">5,103</span><span class="stat-label">Q&A Pairs</span></div>
    <div class="stat-item"><span class="stat-number">432</span><span class="stat-label">Pages</span></div>
    <div class="stat-item"><span class="stat-number">RAG</span><span class="stat-label">Powered</span></div>
    <div class="stat-item"><span class="stat-number">Groq</span><span class="stat-label">LLaMA 3.3</span></div>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Suggestion chips ──────────────────────────────────────────────
SUGGESTIONS = [
    "What is the objective of ASISSE?",
    "How is data collected?",
    "What is GVA?",
    "Is participation mandatory?",
    "What is a Financial Year?",
    "How to fill Block 3?",
]

if not st.session_state.messages:
    st.markdown("""
    <div class="empty-state">
        <span class="empty-icon">📊</span>
        <div class="empty-text">Ask me anything about the ASISSE survey.<br>I'll find the answer from the official documentation.</div>
    </div>
    <div class="suggestions-title">Try asking</div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, s in enumerate(SUGGESTIONS):
        with cols[i % 3]:
            if st.button(s, key=f"sug_{i}"):
                st.session_state.pending_query = s
                st.rerun()


# ── Render chat history ───────────────────────────────────────────
if st.session_state.messages:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role    = msg["role"]
        content = msg["content"]
        time_str = msg.get("time", "")

        if role == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div>
                    <div class="bubble user">{content}</div>
                    <span class="timestamp">{time_str}</span>
                </div>
                <div class="avatar user-av">👤</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row bot">
                <div class="avatar bot-av">📊</div>
                <div>
                    <div class="bubble bot">{content}</div>
                    <span class="timestamp">{time_str}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ── Process query ─────────────────────────────────────────────────
def process_query(query: str):
    import datetime
    now = datetime.datetime.now().strftime("%H:%M")
    st.session_state.messages.append({"role": "user", "content": query, "time": now})
    with st.spinner("Searching documentation..."):
        response = ask(query)
    st.session_state.messages.append({"role": "assistant", "content": response, "time": now})


if st.session_state.pending_query:
    q = st.session_state.pending_query
    st.session_state.pending_query = None
    process_query(q)
    st.rerun()


# ── Chat input ────────────────────────────────────────────────────
st.markdown('<div class="input-container">', unsafe_allow_html=True)
user_query = st.chat_input("Ask about ASISSE survey documentation...")
st.markdown('</div>', unsafe_allow_html=True)

if user_query:
    process_query(user_query)
    st.rerun()