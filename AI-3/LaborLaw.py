"""
LaborLex PH — Philippine Labor Code RAG Assistant
Streamlit Web Interface (Gemma-only version)
"""

import streamlit as st
import requests

# ─── PAGE CONFIG ──────────────────────────────────────────────
FAVICON_SVG = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
    "%3Crect width='64' height='64' rx='12' fill='%23c9933a'/%3E"
    "%3Ctext x='50%25' y='54%25' dominant-baseline='middle' text-anchor='middle' "
    "font-family='Georgia,serif' font-size='38' font-weight='700' fill='%231a0f08'%3E"
    "L%3C/text%3E%3C/svg%3E"
)

st.set_page_config(
    page_title="LaborLex PH — Labor Code Assistant",
    page_icon=FAVICON_SVG,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --br-950: #1a0f08; --br-900: #2c1a0e; --br-800: #3d2410;
    --br-700: #5c3a1e; --br-600: #7a4f2d; --br-500: #9a6640;
    --br-400: #b8845a; --br-300: #d4a97a; --br-200: #e8cfa8;
    --br-100: #f5e8d4; --br-50:  #fdf6ec;
    --gold: #c9933a; --gold-l: #e8b96a;
    --cream: #faf4ea;
    --border: #d4b896; --shadow: rgba(44,26,14,0.12);
    --font-serif: 'Source Serif 4', Georgia, serif;
    --font-display: 'Playfair Display', Georgia, serif;
    --font-mono: 'JetBrains Mono', 'Courier New', monospace;
}

html, body, [class*="css"] {
    font-family: var(--font-serif);
    background-color: var(--cream);
    color: #111111;
}
.stApp { background: var(--cream); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0.5rem !important; max-width: 1200px; }

[data-testid="collapsedControl"],
[data-testid="collapsedControl"] > div {
    display: none !important;
}

section[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
}

[data-testid="stSidebar"][aria-expanded="false"] {
    transform: none !important;
}

[data-baseweb="tab-highlight"] {
    background-color: #c9933a !important;
}

[data-testid="collapsedControl"],
button[title="Collapse sidebar"],
button[title="Expand sidebar"] {
    display: none !important;
    visibility: hidden !important;
}

[data-testid="stTabs"] { margin: 0 0.25rem; }
[data-baseweb="tab-list"] {
    background: var(--br-50) !important;
    border-radius: 7px !important;
    padding: 0.15rem 0.2rem !important;
    border: 1px solid var(--border) !important;
    gap: 0.15rem !important;
}
[data-baseweb="tab"] {
    font-family: var(--font-serif) !important;
    font-size: 0.88rem !important;
    color: #555555 !important;
    padding: 0.4rem 1.2rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: var(--br-700) !important;
    color: var(--br-100) !important;
    border-radius: 5px !important;
}

.nav-bar {
    background: linear-gradient(135deg, var(--br-900), var(--br-700));
    padding: 1rem 2rem; display: flex; align-items: center;
    justify-content: space-between;
    border-bottom: 2px solid var(--gold);
    box-shadow: 0 3px 16px var(--shadow);
    margin: -0.5rem -1rem 1.5rem -1rem;
}
.nav-left { display: flex; align-items: center; gap: 0.85rem; }
.nav-monogram {
    width: 2.4rem; height: 2.4rem; border-radius: 6px;
    background: linear-gradient(135deg, var(--gold), var(--br-400));
    display: flex; align-items: center; justify-content: center;
    font-family: var(--font-display); font-size: 1.1rem; font-weight: 700;
    color: var(--br-950); flex-shrink: 0;
}
.nav-title {
    font-family: var(--font-display); font-size: 1.65rem;
    font-weight: 700; color: var(--br-100); line-height: 1.1;
}
.nav-sub {
    font-family: var(--font-serif); font-size: 0.7rem;
    color: var(--br-300); letter-spacing: 0.09em;
    text-transform: uppercase; font-style: italic;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--br-900) 0%, var(--br-950) 100%) !important;
    border-right: 1px solid var(--br-700) !important;
}
[data-testid="stSidebar"] * { color: var(--br-200) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--br-100) !important;
    font-family: var(--font-display) !important;
}
[data-testid="stSidebar"] [data-testid="stSelectbox"] > div > div {
    background: var(--br-800) !important;
    border-color: var(--br-600) !important;
}
[data-testid="stSidebar"] .stTextInput input {
    background: var(--br-800) !important;
    border-color: var(--br-600) !important;
    color: var(--br-100) !important;
    font-family: var(--font-mono) !important;
    font-size: 0.8rem !important;
}
.slabel {
    font-family: var(--font-mono); font-size: 0.6rem;
    letter-spacing: 0.13em; text-transform: uppercase;
    color: var(--gold-l) !important; margin-bottom: 0.3rem; display: block;
}
.sdiv { border-top: 1px solid var(--br-700); margin: 0.9rem 0; padding-top: 0.9rem; }
.mbadge {
    display: inline-block; padding: 0.15rem 0.5rem;
    border-radius: 3px; font-family: var(--font-mono);
    font-size: 0.66rem; margin: 0.1rem 0; line-height: 1.5;
}
.mg { background:rgba(201,147,58,.15); color:#000000; border:1px solid rgba(184,132,90,.25); }

.cmsg { display:flex; gap:0.75rem; margin-bottom:1.1rem; animation:fsi 0.25s ease; }
@keyframes fsi {
    from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)}
}
.cav {
    width:1.9rem; height:1.9rem; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    flex-shrink:0; margin-top:0.15rem;
    font-family:var(--font-mono); font-size:0.58rem; font-weight:600; letter-spacing:0.03em;
}
.cav-u { background:var(--br-200); border:1.5px solid var(--br-400); color:var(--br-800) !important; }
.cav-b { background:linear-gradient(135deg,var(--br-800),var(--br-900)); border:1.5px solid var(--gold); color:var(--gold) !important; }
.cbub {
    flex:1; padding:0.8rem 1.05rem; border-radius:0 10px 10px 10px;
    line-height:1.7; font-size:0.91rem; font-family:var(--font-serif); color:#111111;
}
.cbub-u { background:var(--br-100); border:1px solid var(--border); border-radius:10px 0 10px 10px; }
.cbub-b { background:#ffffff; border:1px solid var(--border); box-shadow:0 2px 10px var(--shadow); }
.cmeta {
    font-family:var(--font-mono); font-size:0.61rem;
    color:#555555; margin-top:0.4rem; display:flex; gap:0.6rem; flex-wrap:wrap;
}
.chip { background:var(--br-50); border:1px solid var(--border); padding:0.06rem 0.4rem; border-radius:3px; }

.src-chunk {
    background:var(--br-50); border-left:3px solid var(--gold);
    padding:0.55rem 0.85rem; margin:0.25rem 0;
    font-family:var(--font-serif); font-size:0.8rem;
    color:#333333; border-radius:0 4px 4px 0; font-style:italic; line-height:1.6;
}

.stTextInput input {
    font-family: var(--font-serif) !important;
    font-size: 0.92rem !important;
    background: var(--br-900) !important;
    color: #ffffff !important;
    border: 1px solid var(--br-600) !important;
    border-radius: 7px !important;
    caret-color: var(--gold) !important;
}
.stTextInput input::placeholder {
    color: var(--br-300) !important;
    opacity: 1 !important;
}

.stButton button {
    background:linear-gradient(135deg,var(--br-700),var(--br-800)) !important;
    color:var(--br-100) !important; border:1px solid var(--br-600) !important;
    font-family:var(--font-serif) !important; font-size:0.88rem !important;
    border-radius:7px !important; transition:all 0.2s !important;
}
.stButton button:hover {
    background:linear-gradient(135deg,var(--br-600),var(--br-700)) !important;
    border-color:var(--gold) !important;
}

.wcard {
    background:#fff; border:1px solid var(--border); border-radius:10px;
    padding:2rem; text-align:center; max-width:560px;
    margin:1.5rem auto; box-shadow:0 4px 20px var(--shadow);
}
.wmonogram {
    width:3rem; height:3rem; border-radius:8px;
    background:linear-gradient(135deg,var(--gold),var(--br-400));
    display:flex; align-items:center; justify-content:center;
    font-family:var(--font-display); font-size:1.3rem; font-weight:700;
    color:var(--br-950); margin:0 auto 0.75rem;
}
.wtitle { font-family:var(--font-display); font-size:1.3rem; font-weight:700; color:#111111; margin-bottom:0.45rem; }
.wbody  { font-family:var(--font-serif); font-size:0.87rem; color:#444444; line-height:1.7; }

.acard {
    background:#fff; border:1px solid var(--border);
    border-left:3px solid var(--gold); border-radius:6px;
    padding:0.85rem 1rem; margin-bottom:0.6rem;
}
.atitle { font-family:var(--font-display); font-size:0.88rem; font-weight:600; color:#111111; margin-bottom:0.4rem; }
.abody  { font-family:var(--font-serif); font-size:0.82rem; color:#333333; line-height:1.65; }

.ditem {
    display:flex; gap:0.65rem; align-items:flex-start;
    margin-bottom:0.6rem; padding:0.55rem 0.85rem;
    background:var(--br-50); border-radius:5px; border-left:3px solid var(--gold);
}
.dmarker {
    font-family:var(--font-mono); font-size:0.6rem; font-weight:600;
    color:var(--gold); flex-shrink:0; margin-top:0.25rem;
    letter-spacing:0.05em; text-transform:uppercase; width:1.8rem;
}
.dtext { font-family:var(--font-serif); font-size:0.85rem; color:#222222; line-height:1.55; }

.gdiv { height:1px; background:linear-gradient(90deg,transparent,var(--gold),transparent); margin:1.2rem 0; }

.ldots { display:flex; gap:0.35rem; align-items:center; padding:0.4rem 0; }
.ldot { width:6px; height:6px; border-radius:50%; background:var(--gold); animation:bounce 1.2s ease-in-out infinite; }
.ldot:nth-child(2){animation-delay:.2s} .ldot:nth-child(3){animation-delay:.4s}
@keyframes bounce {
    0%,80%,100%{transform:scale(.55);opacity:.35} 40%{transform:scale(1);opacity:1}
}

[data-testid="stExpander"] {
    border:1px solid var(--border) !important; border-radius:7px !important;
    background:var(--br-50) !important;
}
[data-testid="stExpander"] summary {
    font-family:var(--font-mono) !important; font-size:0.75rem !important;
    letter-spacing:0.04em !important; color:#333333 !important;
}

::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:var(--br-50)}
::-webkit-scrollbar-thumb{background:var(--br-300);border-radius:3px}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ────────────────────────────────────────────
if "agreed" not in st.session_state:
    st.session_state.agreed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "pending_q" not in st.session_state:
    st.session_state.pending_q = ""
if "auto_submit" not in st.session_state:
    st.session_state.auto_submit = False

# ─── TERMS MODAL ──────────────────────────────────────────────
if not st.session_state.agreed:
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div style="text-align:center;padding:1.5rem 0 1rem">
            <div style="width:3.2rem;height:3.2rem;border-radius:8px;
                background:linear-gradient(135deg,#c9933a,#b8845a);
                display:flex;align-items:center;justify-content:center;
                font-family:'Playfair Display',serif;font-size:1.4rem;
                font-weight:700;color:#1a0f08;margin:0 auto 1rem;">L</div>
            <div style="font-family:'Playfair Display',serif;font-size:1.75rem;
                font-weight:700;color:#111111;line-height:1;">LaborLex PH</div>
            <div style="font-family:'Source Serif 4',serif;font-size:0.72rem;
                color:#555555;letter-spacing:0.09em;text-transform:uppercase;
                font-style:italic;margin-bottom:1.75rem;">
                Philippine Labor Code AI Assistant</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            "<h5 style='color:black;'>Terms and Conditions of Use</h5>",
            unsafe_allow_html=True
        )
        st.markdown("""
        <div class="ditem"><span class="dmarker">01</span>
            <span class="dtext"><strong>Not a lawyer.</strong> This chatbot is not a licensed legal professional and does not provide legal advice.</span></div>
        <div class="ditem"><span class="dmarker">02</span>
            <span class="dtext"><strong>Informational only.</strong> Responses are for general information and must not be used as the basis for legal decisions.</span></div>
        <div class="ditem"><span class="dmarker">03</span>
            <span class="dtext"><strong>Curated sources only.</strong> Answers are retrieved from the Labor Code of the Philippines Renumbered DOLE Edition 2022 PDF.</span></div>
        <div class="ditem"><span class="dmarker">04</span>
            <span class="dtext"><strong>May be incorrect.</strong> AI-generated responses can contain errors or omissions. Always verify with official government sources or a licensed attorney.</span></div>
        <div class="ditem"><span class="dmarker">05</span>
            <span class="dtext"><strong>Academic project only.</strong> This is a student research tool and is not an official government or legal service.</span></div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("I Have Read and Agree to the Terms", use_container_width=True):
            st.session_state.agreed = True
            st.rerun()
    st.stop()

# ─── NAV BAR ──────────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
  <div class="nav-left">
    <div class="nav-monogram">L</div>
    <div>
      <div class="nav-title">LaborLex PH</div>
      <div class="nav-sub">Philippine Labor Code Assistant</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Settings")

    st.markdown('<span class="slabel">Backend URL</span>', unsafe_allow_html=True)
    BACKEND_URL = st.text_input(
        "url", value="http://localhost:8000",
        placeholder="https://your-ngrok-url.ngrok-free.app",
        label_visibility="collapsed",
        help="Copy the ngrok URL printed in your Colab cell and paste it here."
    )
    BACKEND_URL = BACKEND_URL.rstrip("/")

    # ── Health check indicator ──
    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    try:
        hc = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if hc.status_code == 200:
            hdata = hc.json()
            gpu_status = "GPU" if hdata.get("gpu") else "⚠️ CPU only"
            st.success(f"Backend connected — {gpu_status}")
        else:
            st.error(f"Backend returned {hc.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot reach backend")
    except Exception:
        st.warning("⚠️ Backend check failed")

    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown("""
    <span class="mbadge mg">Gemma-2-9B-IT</span>
    <div style="font-family:'JetBrains Mono',monospace;font-size:0.61rem;
        color:#aaaaaa;margin-top:0.4rem;">4-bit quantized · active model</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    st.markdown('<span class="slabel">Top K Chunks</span>', unsafe_allow_html=True)
    top_k = st.slider("top_k", min_value=1, max_value=8, value=4, label_visibility="collapsed")
    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    show_sources = st.toggle("Show Source Chunks", value=True)
    st.markdown('<div class="sdiv"></div>', unsafe_allow_html=True)
    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

# ─── HELPER: send question to backend ────────────────────────
def _send_question(q: str):
    try:
        r = requests.post(
            f"{BACKEND_URL}/ask",
            json={"question": q, "model": "gemma", "top_k": top_k},
            timeout=120,
        )
        r.raise_for_status()
        data = r.json()
        st.session_state.chat_history.append({
            "question": q,
            "mode": "single",
            "model": "Gemma-2-9B",
            "response": data,
        })
        return None
    except requests.exceptions.ConnectionError:
        return "Cannot reach the backend. Make sure your Colab server is running and the ngrok URL is correct."
    except requests.exceptions.Timeout:
        return "Request timed out. The model may still be loading. Try again in a moment."
    except Exception as e:
        return f"Error: {e}"

# ─── TABS ─────────────────────────────────────────────────────
tab_chat, tab_about = st.tabs(["Chat", "About"])

# ══════════════════════════════════════════════════════════════
# ABOUT TAB
# ══════════════════════════════════════════════════════════════
with tab_about:
    st.markdown("""
    <div style="padding:0.5rem 0 1.5rem">
        <div style="font-family:'Playfair Display',serif;font-size:1.6rem;
            font-weight:700;color:#111111;">About LaborLex PH</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="acard">
          <div class="atitle">Overview</div>
          <div class="abody">
            This system uses a Retrieval-Augmented Generation (RAG) pipeline
            powered by Gemma-2-9B to answer questions about the Philippine
            Labor Code (PD 442, as amended), grounding all answers in
            verified statutory text.
          </div>
        </div>
        <div class="acard">
          <div class="atitle">Research Team</div>
          <div class="abody">
            Bautista, Cedric Isaiah D.<br>
            Domingo, Alisandro N.<br>
            Monteon, John Paul Benedict R.
          </div>
        </div>
        <div class="acard">
          <div class="atitle">Data Sources</div>
          <div class="abody">
            Philippine Labor Code (PD 442, as amended)<br>
            Presidential Decree No. 851 (13th Month Pay)<br><br>
            Chunked by article boundary — 800-char max, 150-char overlap.<br>
            Indexed with BAAI/bge-m3 embeddings + BM25.
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="acard">
          <div class="atitle">Model</div>
          <div class="abody">
            <span class="mbadge mg">Gemma-2-9B-IT</span>
            <div style="margin-top:0.6rem;font-family:'Source Serif 4',serif;
                font-size:0.81rem;color:#555555;">
              4-bit quantized · loaded via Unsloth on Google Colab (T4 GPU).
            </div>
          </div>
        </div>
        <div class="acard">
          <div class="atitle">Retrieval Pipeline</div>
          <div class="abody">
            Dense retrieval: BAAI/bge-m3 + FAISS<br>
            Sparse retrieval: BM25 (Okapi)<br>
            Fusion: Reciprocal Rank Fusion (k=60)<br>
            Reranking: bge-reranker-v2-m3 / ms-marco-MiniLM-L-12<br>
            Selection: MMR diversity (&lambda;=0.6, k=4)
          </div>
        </div>
        <div class="acard">
          <div class="atitle">Evaluation Metrics</div>
          <div class="abody">
            Recall@4 &nbsp;&middot;&nbsp; Precision@4 &nbsp;&middot;&nbsp; Faithfulness<br>
            Semantic Similarity &nbsp;&middot;&nbsp; Answer Relevancy<br>
            Citation Accuracy &nbsp;&middot;&nbsp; LLM-as-a-Judge &nbsp;&middot;&nbsp; Latency
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gdiv"></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# CHAT TAB
# ══════════════════════════════════════════════════════════════
with tab_chat:

    # ── Handle auto-submit from preset buttons ──
    if st.session_state.auto_submit and st.session_state.pending_q:
        q = st.session_state.pending_q
        st.session_state.pending_q = ""
        st.session_state.auto_submit = False

        st.markdown(f"""
        <div class="cmsg">
          <div class="cav cav-u">You</div>
          <div class="cbub cbub-u">{q}</div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("Thinking..."):
            error_msg = _send_question(q)

        if error_msg:
            st.error(error_msg)
            st.info("Setup reminder: Run the backend cell in Colab, copy the ngrok URL, and paste it in the sidebar.")
        else:
            st.rerun()

    # ── Welcome card (only when no history) ──
    if not st.session_state.chat_history and not st.session_state.auto_submit:
        st.markdown("""
        <div class="wcard">
          <div class="wmonogram">L</div>
          <div class="wtitle">Ask about Philippine Labor Law</div>
          <div class="wbody">
            Ask any question about the Philippine Labor Code — wages,
            working hours, leave benefits, termination rights, and more.
            Available in English and Filipino/Tagalog.
          </div>
        </div>
        """, unsafe_allow_html=True)

        examples = [
            "What is the night shift differential?",
            "What are just causes for termination?",
            "Ano ang overtime pay?",
            "What is service incentive leave?",
            "Can a pregnant woman be terminated?",
            "What is the cooling off period before a strike?",
        ]
        c1, c2, c3 = st.columns(3)
        for i, ex in enumerate(examples):
            with [c1, c2, c3][i % 3]:
                if st.button(ex, key=f"ex{i}", use_container_width=True):
                    st.session_state.pending_q = ex
                    st.session_state.auto_submit = True
                    st.rerun()

    # ── Render history ──
    for entry in st.session_state.chat_history:
        st.markdown(f"""
        <div class="cmsg">
          <div class="cav cav-u">You</div>
          <div class="cbub cbub-u">{entry['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        resp = entry.get("response", {})
        metrics_html = (
            '<div class="cmeta">'
            f'<span class="chip">{resp.get("latency", 0):.2f}s</span>'
            f'<span class="chip">{resp.get("tokens", 0)} tokens</span>'
            f'<span class="chip">{resp.get("chunks", 0)} chunks</span>'
            f'<span class="chip">Gemma-2-9B</span>'
            '</div>'
        )
        st.markdown(f"""
        <div class="cmsg">
          <div class="cav cav-b">Lex</div>
          <div style="flex:1">
            <div class="cbub cbub-b">{resp.get('answer', '—')}</div>
            {metrics_html}
          </div>
        </div>
        """, unsafe_allow_html=True)

        if show_sources and resp.get("sources"):
            with st.expander(f"View {len(resp['sources'])} retrieved source chunks"):
                for i, s in enumerate(resp["sources"]):
                    st.markdown(f"""
                    <div class="src-chunk">
                      <strong>Chunk {i+1}</strong> &nbsp;&middot;&nbsp; score: {s.get('score', 0):.3f}<br>
                      {s.get('text', '')[:320]}{'…' if len(s.get('text', '')) > 320 else ''}
                    </div>
                    """, unsafe_allow_html=True)

    # ── Input form ──
    st.markdown('<div class="gdiv"></div>', unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        col_in, col_btn = st.columns([5, 1])
        with col_in:
            question = st.text_input(
                "q", value="",
                placeholder="Ask about Philippine labor law — English or Filipino",
                label_visibility="collapsed",
            )
        with col_btn:
            submitted = st.form_submit_button("Ask", use_container_width=True)

    if submitted and question.strip():
        q = question.strip()

        loading_slot = st.empty()
        loading_slot.markdown("""
        <div class="cmsg">
          <div class="cav cav-b">Lex</div>
          <div class="cbub cbub-b">
            <div class="ldots">
              <div class="ldot"></div><div class="ldot"></div><div class="ldot"></div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        error_msg = _send_question(q)
        loading_slot.empty()

        if error_msg:
            st.error(error_msg)
            st.info("Setup reminder: Run the backend cell in Colab, copy the ngrok URL, and paste it in the sidebar Backend URL field.")
        else:
            st.rerun()