import streamlit as st
from datetime import datetime
from html import escape

from collector.news_collector import fetch_news
from processing.news_processor import process_news
from database.db import save_news_articles, create_tables
from portfolio.portfolio_manager import (
    add_token,
    delete_token,
    get_portfolio
)
from portfolio.relevance_engine import get_relevant_news
from intelligence.insight_generator import generate_insight
from wallet.wallet_connector import connect_wallet


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="ArthaSutra | Crypto Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

create_tables()


# =========================================================
# SESSION STATE
# =========================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Home"


# =========================================================
# DESIGN SYSTEM
# Palette: Pearl #FBFAFF · Ink #1A1545 · Violet #5B3FD6
#          Saffron #E8920F · Mist #EFEBFF
# Type:    Playfair Display (display, serif) + Outfit (interface)
# Motif:   the "sutra" - a thread strung with beads
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,600;0,700;0,800;0,900;1,400;1,500&family=Outfit:wght@400;500;600;700&display=swap');

:root {
    --pearl: #FBFAFF;
    --paper: #FFFFFF;
    --ink: #1A1545;
    --muted: #625E85;
    --violet: #5B3FD6;
    --violet-deep: #3B2A9E;
    --mist: #EFEBFF;
    --saffron: #E8920F;
    --saffron-soft: #FFF3DD;
    --line: rgba(26, 21, 69, 0.10);
    --shadow: 0 1px 2px rgba(26,21,69,.04), 0 12px 32px -12px rgba(59,42,158,.18);
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

html, body, .stApp, .stApp * {
    font-family: 'Outfit', system-ui, sans-serif;
}

.stApp {
    background:
        radial-gradient(900px 500px at 8% -5%, rgba(91,63,214,.10), transparent 60%),
        radial-gradient(800px 480px at 95% 5%, rgba(232,146,15,.10), transparent 60%),
        var(--pearl);
    color: var(--ink);
}

.block-container {
    max-width: 1240px;
    padding-top: 1.4rem;
    padding-bottom: 3rem;
}

/* ---------- TYPOGRAPHY ---------- */

h1, h2, h3, h4 {
    font-family: 'Playfair Display', Georgia, serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.02em;
    font-weight: 600 !important;
}
h1 { font-size: clamp(32px, 4vw, 46px) !important; line-height: 1.1 !important; }
h2, h3 { line-height: 1.2 !important; }

.stMarkdown p, .stMarkdown li, label, .stCaption, [data-testid="stCaptionContainer"] {
    color: var(--muted);
    line-height: 1.7;
}
.stMarkdown p { font-size: 16.5px; }
a { color: var(--violet) !important; text-decoration: none; font-weight: 600; }
a:hover { text-decoration: underline; text-underline-offset: 3px; }

/* ---------- NAVIGATION ---------- */

.brand {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: var(--ink);
    display: flex; align-items: center; gap: 10px;
    padding-top: 2px;
}
.brand .glyph {
    display: inline-grid; place-items: center;
    width: 34px; height: 34px; border-radius: 50%;
    background: linear-gradient(135deg, var(--violet), var(--saffron));
    color: #fff; font-size: 16px;
}

div.stButton > button {
    border-radius: 999px;
    border: 1px solid var(--line);
    background: var(--paper);
    color: var(--ink);
    font-weight: 600;
    padding: 0.45rem 1.1rem;
    transition: border-color .2s, box-shadow .2s, background .2s;
}
div.stButton > button p { color: inherit !important; font-size: 15px; margin: 0; }
div.stButton > button:hover {
    border-color: var(--violet);
    color: var(--violet);
    box-shadow: 0 6px 20px -8px rgba(91,63,214,.45);
}
div.stButton > button:focus-visible { outline: 2px solid var(--saffron); outline-offset: 2px; }

div.stButton > button[kind="primary"],
div.stButton > button[data-testid="stBaseButton-primary"],
div[data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, var(--violet) 0%, var(--violet-deep) 100%);
    border-color: transparent;
    color: #fff;
}
div.stButton > button[kind="primary"]:hover,
div.stButton > button[data-testid="stBaseButton-primary"]:hover {
    color: #fff;
    box-shadow: 0 10px 26px -8px rgba(59,42,158,.6);
}
div[data-testid="stFormSubmitButton"] > button {
    border-radius: 999px;
    background: linear-gradient(135deg, var(--violet) 0%, var(--violet-deep) 100%);
    color: #fff; border-color: transparent;
}
div[data-testid="stFormSubmitButton"] > button p { color: #fff !important; }

/* ---------- THE THREAD (divider motif) ---------- */

.thread {
    position: relative; height: 18px; margin: 34px 0 28px;
}
.thread::before {
    content: ""; position: absolute; left: 0; right: 0; top: 8px; height: 1.5px;
    background: linear-gradient(90deg, transparent, rgba(91,63,214,.35) 20%, rgba(232,146,15,.55) 50%, rgba(91,63,214,.35) 80%, transparent);
}
.thread span {
    position: absolute; left: 50%; top: 3px; width: 12px; height: 12px; margin-left: -6px;
    border-radius: 50%; background: var(--saffron);
    box-shadow: 0 0 0 5px var(--saffron-soft);
}

.eyebrow {
    display: inline-flex; align-items: center; gap: 9px;
    font-size: 14px; font-weight: 700; color: var(--violet);
    margin-bottom: 6px;
}
.eyebrow::before {
    content: ""; width: 9px; height: 9px; border-radius: 50%;
    background: var(--saffron);
}

/* ---------- HERO ---------- */

.hero {
    position: relative; overflow: hidden;
    text-align: center;
    padding: 84px 28px 64px;
    margin: 18px 0 40px;
    border-radius: 32px;
    background:
        radial-gradient(600px 300px at 50% 0%, rgba(91,63,214,.10), transparent 70%),
        linear-gradient(180deg, #FFFFFF 0%, #F6F2FF 100%);
    border: 1px solid var(--line);
    box-shadow: var(--shadow);
}
.hero.compact { padding: 46px 28px 40px; }
.hero-thread {
    position: absolute; inset: 0; width: 100%; height: 100%;
    pointer-events: none; opacity: .9;
}
.hero > *:not(svg) { position: relative; z-index: 1; }

.hero-tag {
    display: inline-block;
    font-size: 14px; font-weight: 600; color: var(--violet-deep);
    background: var(--mist);
    border: 1px solid rgba(91,63,214,.18);
    padding: 7px 18px; border-radius: 999px;
}
.hero-title {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: clamp(54px, 9vw, 112px);
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.045em;
    margin: 26px 0 6px;
    background: linear-gradient(100deg, var(--ink) 20%, var(--violet) 62%, var(--saffron) 100%);
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
    padding-bottom: 8px;
}
.hero.compact .hero-title { font-size: clamp(40px, 6vw, 64px); margin-top: 20px; }

.quote {
    max-width: 680px; margin: 22px auto 0;
    animation: rise 1.1s ease both;
}
.quote-ornament {
    display: flex; align-items: center; justify-content: center; gap: 14px;
    color: var(--saffron); font-size: 15px;
}
.quote-ornament::before, .quote-ornament::after {
    content: ""; height: 1.5px; width: 70px;
}
.quote-ornament::before { background: linear-gradient(90deg, transparent, var(--saffron)); }
.quote-ornament::after  { background: linear-gradient(270deg, transparent, var(--saffron)); }
.quote-text {
    font-family: 'Playfair Display', Georgia, serif;
    font-style: italic; font-weight: 500;
    font-size: clamp(21px, 2.6vw, 30px);
    line-height: 1.45; letter-spacing: -0.01em;
    color: var(--ink);
    margin: 14px 0 10px;
}
.quote-gloss { font-size: 14px; color: var(--muted); }
@keyframes rise {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: none; }
}
@media (prefers-reduced-motion: reduce) { .quote { animation: none; } }

.hero-subtitle {
    font-size: 18px; color: var(--muted);
    max-width: 640px; margin: 28px auto 0; line-height: 1.75;
}
.hero-subtitle strong { color: var(--ink); font-weight: 700; }

/* ---------- CONTENT BLOCKS ---------- */

.pillars {
    display: grid; grid-template-columns: repeat(3, 1fr);
    margin: 26px 0 6px;
}
.pillar { padding: 6px 34px 6px 30px; border-left: 1.5px solid rgba(91,63,214,.22); }
.pillar:first-child { border-left: none; padding-left: 0; }
.pillar .icon {
    font-size: 26px; color: var(--saffron); margin-bottom: 10px;
}
.pillar h3 { font-size: 23px !important; margin: 0 0 8px !important; }
.pillar p { margin: 0; color: var(--muted); line-height: 1.7; font-size: 16px; }
@media (max-width: 800px) {
    .pillars { grid-template-columns: 1fr; gap: 26px; }
    .pillar, .pillar:first-child { border-left: none; padding: 0; }
}

.step {
    position: relative; display: flex; gap: 22px;
    padding: 0 0 30px 0;
}
.step:not(:last-child)::before {
    content: ""; position: absolute; left: 21px; top: 46px; bottom: 2px; width: 1.5px;
    background: linear-gradient(180deg, rgba(91,63,214,.45), rgba(232,146,15,.35));
}
.step .bead {
    flex: 0 0 44px; height: 44px; border-radius: 50%;
    display: grid; place-items: center;
    font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 18px;
    color: var(--violet-deep); background: var(--mist);
    border: 1.5px solid rgba(91,63,214,.35);
}
.step h3 { font-size: 22px !important; margin: 4px 0 4px !important; }
.step p { margin: 0; color: var(--muted); }

.road-item {
    display: flex; gap: 18px; align-items: flex-start;
    background: var(--paper); border: 1px solid var(--line);
    border-radius: 18px; padding: 22px 26px; margin-bottom: 14px;
    box-shadow: var(--shadow);
}
.road-item .mark { color: var(--saffron); font-size: 22px; line-height: 1.3; }
.road-item h3 { font-size: 21px !important; margin: 0 0 4px !important; }
.road-item p { margin: 0; color: var(--muted); }

.setup {
    background: var(--paper); border: 1px solid var(--line);
    border-left: 4px solid var(--saffron);
    border-radius: 16px; padding: 20px 24px; margin: 22px 0 6px;
    box-shadow: var(--shadow);
}
.setup-title {
    font-family: 'Playfair Display', Georgia, serif; font-weight: 600; font-size: 20px;
    color: var(--ink); margin-bottom: 4px;
}
.setup p { margin: 0 0 12px; font-size: 15.5px !important; }
.setup strong { color: var(--ink); }

.metric-card {
    position: relative; overflow: hidden;
    background: var(--paper); border: 1px solid var(--line);
    border-radius: 22px; padding: 24px 26px 22px;
    box-shadow: var(--shadow); min-height: 150px;
}
.metric-card::before {
    content: ""; position: absolute; left: 0; right: 0; top: 0; height: 4px;
    background: linear-gradient(90deg, var(--violet), var(--saffron));
}
.metric-label { font-size: 14px; font-weight: 700; color: var(--violet); }
.metric-value {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 54px; font-weight: 700; line-height: 1.1; color: var(--ink);
    margin: 6px 0 2px;
}
.metric-value.word { font-size: 36px; padding-top: 12px; display: flex; align-items: center; gap: 12px; }
.metric-description { color: var(--muted); font-size: 14.5px; }
.live-dot {
    width: 11px; height: 11px; border-radius: 50%; background: #1FA971;
    box-shadow: 0 0 0 5px rgba(31,169,113,.16);
}

.chip {
    display: inline-block; font-size: 13px; font-weight: 600;
    padding: 4px 12px; border-radius: 999px; margin: 0 8px 6px 0;
    background: var(--mist); color: var(--violet-deep);
}
.chip.source { background: transparent; border: 1px solid var(--line); color: var(--muted); }
.chip.event  { background: var(--saffron-soft); color: #9A5B00; }
.chip.token  { background: var(--ink); color: #fff; }

.holding {
    display: flex; align-items: center; gap: 14px;
    padding: 10px 4px;
}
.holding .sym {
    font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 20px;
    color: var(--ink);
}
.holding .qty { color: var(--muted); }

.footer {
    text-align: center; padding: 8px 10px 30px; margin-top: 30px;
}
.footer .brand { justify-content: center; font-size: 24px; }
.footer p { color: var(--muted); margin: 8px 0 0; font-size: 14.5px; }

/* ---------- STREAMLIT WIDGETS ---------- */

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: var(--line) !important;
    border-radius: 20px !important;
    background: var(--paper);
    box-shadow: var(--shadow);
}
div[data-testid="stForm"] { border: none; padding: 0; }

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
div[data-testid="stNumberInputContainer"] {
    background-color: #fff !important;
    border-radius: 12px !important;
    border-color: var(--line) !important;
}
input, textarea { color: var(--ink) !important; }
div[data-baseweb="input"]:focus-within > div,
div[data-baseweb="select"]:focus-within > div { border-color: var(--violet) !important; }

div[data-testid="stAlert"] {
    border-radius: 14px; border: 1px solid var(--line);
}
div[data-testid="stAlert"] p { color: var(--ink); font-size: 15.5px; }
div[data-testid="stAlertContentInfo"] { color: var(--ink); }

pre, div[data-testid="stCode"] { border-radius: 12px !important; }

/* ---------- FORCE LIGHT WIDGETS (fixes dark boxes / invisible text) ---------- */

:root, .stApp { color-scheme: light; }

[data-testid="stWidgetLabel"] p, label p { color: var(--ink) !important; font-weight: 600; }

div[data-baseweb="input"], div[data-baseweb="base-input"],
div[data-baseweb="input"] > div, div[data-baseweb="base-input"] > div {
    background: #FFFFFF !important;
}
div[data-baseweb="input"] input, div[data-baseweb="base-input"] input, textarea {
    background: #FFFFFF !important;
    color: var(--ink) !important;
    -webkit-text-fill-color: var(--ink) !important;
    caret-color: var(--violet);
}
input::placeholder, textarea::placeholder {
    color: #8A86A8 !important; -webkit-text-fill-color: #8A86A8 !important; opacity: 1 !important;
}
div[data-testid="stNumberInputContainer"] button {
    background: var(--mist) !important; color: var(--ink) !important; border-color: var(--line) !important;
}
div[data-testid="stNumberInputContainer"] button svg { fill: var(--ink) !important; }

div[data-baseweb="select"] * { color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; }
div[data-baseweb="select"] svg { fill: var(--ink) !important; }
div[data-baseweb="popover"], div[data-baseweb="popover"] > div,
ul[role="listbox"], div[data-baseweb="menu"] {
    background: #FFFFFF !important; color: var(--ink) !important;
}
li[role="option"] { background: #FFFFFF !important; color: var(--ink) !important; }
li[role="option"] * { color: var(--ink) !important; }
li[role="option"]:hover, li[role="option"][aria-selected="true"] { background: var(--mist) !important; }

div[data-testid="stAlert"] { background: #F4F1FF !important; }
div[data-testid="stAlert"] p, div[data-testid="stAlert"] div { color: var(--ink) !important; }

div[data-testid="stCode"], div[data-testid="stCode"] pre, div[data-testid="stCode"] code, pre, code {
    background: #F4F1FF !important; color: var(--ink) !important;
}
div[data-testid="stForm"] { background: transparent !important; }

/* ---------- ANIMATION KIT (shared by every page) ---------- */

.block-container { position: relative; z-index: 1; }
.bgx { position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none; }

.bgx .orb { position: absolute; border-radius: 50%; filter: blur(70px); opacity: .55;
    animation: orbdrift 24s ease-in-out infinite alternate; }
.bgx .orb.v { background: radial-gradient(circle, rgba(91,63,214,.42), transparent 70%); }
.bgx .orb.s { background: radial-gradient(circle, rgba(232,146,15,.38), transparent 70%); }
.bgx .orb.l { background: radial-gradient(circle, rgba(139,115,240,.38), transparent 70%); }

/* Home: spinning rings, aurora ribbons, twinkling stars */
.bgx .ring { position: absolute; left: 50%; top: 440px; border-radius: 50%; }
.bgx .ring.a { width: 1000px; height: 1000px;
    background: conic-gradient(from 0deg, rgba(91,63,214,0), rgba(91,63,214,.75), rgba(232,146,15,.85), rgba(91,63,214,0) 70%);
    -webkit-mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px));
    mask: radial-gradient(farthest-side, transparent calc(100% - 3px), #000 calc(100% - 2px));
    animation: spin 38s linear infinite; }
.bgx .ring.b { width: 760px; height: 760px; border: 1.5px dashed rgba(91,63,214,.35);
    animation: spinrev 60s linear infinite; }
.bgx .ring.c { width: 1260px; height: 1260px; border: 2px dotted rgba(232,146,15,.38);
    animation: spin 110s linear infinite; }
.bgx .ribbon { position: absolute; left: -10%; width: 120%; height: 170px; filter: blur(38px); opacity: .55;
    background: linear-gradient(90deg, transparent, rgba(91,63,214,.38), rgba(232,146,15,.32), transparent);
    animation: wave 16s ease-in-out infinite alternate; }
.bgx .ribbon.alt { animation-direction: alternate-reverse; animation-duration: 21s;
    background: linear-gradient(90deg, transparent, rgba(232,146,15,.30), rgba(91,63,214,.34), transparent); }
.bgx .spark { position: absolute; color: var(--saffron); opacity: .1; animation: twinkle 4s ease-in-out infinite; }

/* About: data streams, packets, sonar pulses */
.bgx .stream { position: absolute; left: 0; right: 0; height: 2px; opacity: .55;
    background: repeating-linear-gradient(90deg, rgba(91,63,214,.6) 0 8px, transparent 8px 28px);
    animation: slide linear infinite; }
.bgx .stream.s { background: repeating-linear-gradient(90deg, rgba(232,146,15,.7) 0 8px, transparent 8px 28px); }
.bgx .packet { position: absolute; left: -30px; top: -5px; width: 12px; height: 12px; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFD08A, var(--saffron));
    box-shadow: 0 0 16px rgba(232,146,15,.8); animation: packet linear infinite; }
.bgx .pulse { position: absolute; width: 340px; height: 340px; border-radius: 50%;
    border: 2px solid rgba(91,63,214,.45); animation: pulse 7s ease-out infinite; }
.bgx .pulse.s { border-color: rgba(232,146,15,.5); }

/* Connect: market bars, drawing sparklines, flipping coins */
.bgx .eq { position: absolute; left: 0; right: 0; bottom: 0; height: 36vh; display: flex;
    align-items: flex-end; gap: 6px; padding: 0 8px; opacity: .3; }
.bgx .eq b { flex: 1; height: 100%; border-radius: 8px 8px 0 0; transform-origin: bottom; transform: scaleY(.15);
    background: linear-gradient(180deg, rgba(232,146,15,.7), rgba(91,63,214,.5));
    animation: eq ease-in-out infinite alternate; }
.bgx svg.lines { position: absolute; inset: 0; width: 100%; height: 100%; }
.bgx svg.lines path { fill: none; stroke-width: 2; stroke-linecap: round;
    stroke-dasharray: 1000; animation: draw 11s ease-in-out infinite; }
.bgx .coin { position: absolute; width: 48px; height: 48px; border-radius: 50%;
    display: grid; place-items: center; font-size: 20px; color: #fff;
    background: radial-gradient(circle at 35% 30%, #FFD08A, var(--saffron));
    border: 3px solid #FFE2AE; box-shadow: 0 8px 24px rgba(232,146,15,.4);
    animation: coin 7s ease-in-out infinite; }
.bgx .coin.v { background: radial-gradient(circle at 35% 30%, #A78BFA, var(--violet)); border-color: #D9CEFF; box-shadow: 0 8px 24px rgba(91,63,214,.4); }

@keyframes orbdrift { to { transform: translate(var(--dx, 140px), var(--dy, 100px)) scale(1.15); } }
@keyframes spin    { from { transform: translate(-50%,-50%) rotate(0); }  to { transform: translate(-50%,-50%) rotate(360deg); } }
@keyframes spinrev { from { transform: translate(-50%,-50%) rotate(0); }  to { transform: translate(-50%,-50%) rotate(-360deg); } }
@keyframes wave { from { transform: translateX(-8%) rotate(-6deg); } to { transform: translateX(8%) translateY(50px) rotate(-2deg); } }
@keyframes twinkle { 0%,100% { opacity: .08; transform: scale(.6) rotate(0); } 50% { opacity: .95; transform: scale(1.25) rotate(45deg); } }
@keyframes slide { to { background-position: 280px 0; } }
@keyframes packet { to { transform: translateX(112vw); } }
@keyframes pulse { from { transform: scale(.15); opacity: .85; } to { transform: scale(2.6); opacity: 0; } }
@keyframes eq { to { transform: scaleY(var(--h, .8)); } }
@keyframes draw { 0% { stroke-dashoffset: 1000; opacity: 0; } 15% { opacity: 1; } 60%,100% { stroke-dashoffset: 0; opacity: .0; } }
@keyframes coin { 0%,100% { transform: translateY(0) rotateY(0); } 50% { transform: translateY(-46px) rotateY(180deg); } }


/* ---------- STRONGER VISIBILITY RULES ---------- */
div[data-testid="stAlert"], div[data-testid="stAlertContainer"], div[data-baseweb="notification"] {
    background: #F4F1FF !important;
    border: 1px solid rgba(91,63,214,.22) !important;
    border-left: 4px solid var(--saffron) !important;
    border-radius: 14px !important;
}
div[data-testid="stAlert"] *, div[data-baseweb="notification"] * {
    color: #1A1545 !important; -webkit-text-fill-color: #1A1545 !important;
    background-color: transparent !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
div[data-baseweb="select"] > div, div[data-baseweb="select"] div {
    background-color: #FFFFFF !important;
}
div[data-testid="stSelectbox"] *, div[data-baseweb="select"] span, div[data-baseweb="select"] input {
    color: #1A1545 !important; -webkit-text-fill-color: #1A1545 !important;
}
.notice {
    background: #F4F1FF; border: 1px solid rgba(91,63,214,.22); border-left: 4px solid #E8920F;
    border-radius: 14px; padding: 16px 20px; margin: 10px 0;
    color: #1A1545 !important; font-size: 16px; font-weight: 500; line-height: 1.6;
}

/* ---------- HOME: livelier motion ---------- */
.bgx.home .orb { animation-duration: 18s; }
.bgx.home .ring.a { animation-duration: 28s; }
.bgx.home .ring.b { animation-duration: 45s; }
.bgx.home .ring.c { animation-duration: 80s; }
.bgx.home .ribbon { animation-duration: 13s; opacity: .4; }
.bgx.home .ribbon.alt { animation-duration: 17s; }
.bgx.home .spark { animation-duration: 3.6s; }
.bgx .rise { position: absolute; bottom: -20px; border-radius: 50%; opacity: 0;
    background: radial-gradient(circle at 35% 35%, #FFD08A, var(--saffron));
    box-shadow: 0 0 12px rgba(232,146,15,.55); animation: riseup linear infinite; }
.bgx .rise.v { background: radial-gradient(circle at 35% 35%, #A78BFA, var(--violet)); box-shadow: 0 0 12px rgba(91,63,214,.5); }
@keyframes riseup {
    0% { transform: translate(0,0); opacity: 0; }
    10% { opacity: .85; }
    50% { transform: translate(28px,-52vh); }
    90% { opacity: .5; }
    100% { transform: translate(-20px,-108vh); opacity: 0; }
}

/* ---------- ABOUT: ripples with travelling beads ---------- */
.bgx .rip { position: absolute; width: 0; height: 0; }
.bgx .rip .pulse { left: -170px; top: -170px; animation-duration: 12s; border-color: rgba(91,63,214,.26); }
.bgx .rip .pulse.s { border-color: rgba(232,146,15,.3); }
.bgx .rip .arm { position: absolute; left: 0; top: 0; width: 0; height: 0; transform: rotate(var(--a)); }
.bgx .rip .rbead { position: absolute; left: 0; top: -5px; width: 10px; height: 10px; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFD08A, var(--saffron));
    box-shadow: 0 0 14px rgba(232,146,15,.85); animation: beadout 8s ease-out infinite; }
.bgx .rip .rbead.v { background: radial-gradient(circle at 35% 35%, #A78BFA, var(--violet)); box-shadow: 0 0 14px rgba(91,63,214,.7); }
@keyframes beadout { from { transform: translateX(25px) scale(1); opacity: .95; } to { transform: translateX(442px) scale(.6); opacity: 0; } }


/* ---------- NEW ANIMATION SET (Home / About / Connect) ---------- */
.bgx.edge {
    -webkit-mask-image: linear-gradient(90deg, #000 0%, rgba(0,0,0,.4) 24%, rgba(0,0,0,.4) 76%, #000 100%);
    mask-image: linear-gradient(90deg, #000 0%, rgba(0,0,0,.4) 24%, rgba(0,0,0,.4) 76%, #000 100%);
}

/* Home: orbit system, comets, morphing blobs */
.bgx .sys { position: absolute; left: 50%; top: 46%; width: 0; height: 0; }
.bgx .oring { position: absolute; border-radius: 50%; border: 1px dashed rgba(91,63,214,.34); animation: rot linear infinite; }
.bgx .oring.s { border-color: rgba(232,146,15,.4); border-style: dotted; }
.bgx .planet { position: absolute; left: 50%; top: -8px; margin-left: -8px; width: 16px; height: 16px; border-radius: 50%;
    background: radial-gradient(circle at 35% 35%, #FFD08A, var(--saffron)); box-shadow: 0 0 20px rgba(232,146,15,.85); }
.bgx .planet.v { background: radial-gradient(circle at 35% 35%, #A78BFA, var(--violet)); box-shadow: 0 0 20px rgba(91,63,214,.75); }
.bgx .planet.b { top: auto; bottom: -8px; width: 10px; height: 10px; margin-left: -5px; }
.bgx .comet { position: absolute; left: -300px; width: 260px; height: 2px; border-radius: 2px; opacity: 0;
    background: linear-gradient(90deg, transparent, rgba(232,146,15,.95)); box-shadow: 0 0 12px rgba(232,146,15,.7);
    animation: comet linear infinite; }
.bgx .comet.v { background: linear-gradient(90deg, transparent, rgba(91,63,214,.95)); box-shadow: 0 0 12px rgba(91,63,214,.6); }
.bgx .blob { position: absolute; filter: blur(28px); opacity: .42;
    animation: morph 13s ease-in-out infinite alternate, blobmove 20s ease-in-out infinite alternate; }
.bgx .blob.v { background: linear-gradient(135deg, rgba(91,63,214,.85), rgba(139,115,240,.5)); }
.bgx .blob.s { background: linear-gradient(135deg, rgba(232,146,15,.85), rgba(255,208,138,.5)); }

/* About: living network graph */
.bgx svg.net { position: absolute; inset: 0; width: 100%; height: 100%; }
.bgx .net .e { stroke: rgba(91,63,214,.2); stroke-width: 1.2; fill: none; }
.bgx .net .f { fill: none; stroke: #E8920F; stroke-width: 5; stroke-linecap: round;
    stroke-dasharray: 0.1 89.9; animation: netflow linear infinite; opacity: .85; }
.bgx .net .f.v { stroke: #5B3FD6; }
.bgx .net .n { fill: #fff; stroke: #5B3FD6; stroke-width: 2; transform-box: fill-box; transform-origin: center;
    animation: nodepulse ease-in-out infinite; }
.bgx .net .n.s { stroke: #E8920F; }
.bgx .scan { position: absolute; top: 0; bottom: 0; left: -300px; width: 260px;
    background: linear-gradient(90deg, transparent, rgba(91,63,214,.14), rgba(232,146,15,.2), transparent);
    animation: scan 11s linear infinite; }

/* Connect: marquee tickers, waves, candlesticks */
.bgx .marq { position: absolute; left: 0; white-space: nowrap; line-height: 1;
    font-family: 'Playfair Display', Georgia, serif; font-weight: 800; font-size: clamp(90px, 11vw, 150px);
    color: transparent; -webkit-text-stroke: 1.5px rgba(91,63,214,.3); animation: marq linear infinite; }
.bgx .marq.s { -webkit-text-stroke-color: rgba(232,146,15,.4); }
.bgx .wave { position: absolute; left: 0; bottom: 0; width: 200%; animation: wavex linear infinite; }
.bgx .wave svg { display: block; width: 100%; height: 100%; }
.bgx .candles { position: absolute; bottom: 7%; display: flex; align-items: flex-end; gap: 9px; height: 36vh; }
.bgx .candles i { position: relative; display: block; width: 11px; height: 100%; border-radius: 3px;
    transform-origin: bottom; transform: scaleY(.3); animation: cdl ease-in-out infinite alternate; }
.bgx .candles i.u { background: linear-gradient(180deg, rgba(232,146,15,.9), rgba(232,146,15,.5)); }
.bgx .candles i.d { background: linear-gradient(180deg, rgba(91,63,214,.85), rgba(91,63,214,.45)); }
.bgx .candles i::before { content: ""; position: absolute; left: 50%; top: -14px; bottom: -14px; width: 2px;
    margin-left: -1px; background: inherit; opacity: .7; }
.bgx .tick { position: absolute; bottom: -50px; padding: 6px 14px; border-radius: 999px; font-weight: 700; font-size: 14px;
    border: 1px solid rgba(91,63,214,.35); background: rgba(255,255,255,.75); color: var(--violet-deep);
    box-shadow: 0 6px 18px -6px rgba(91,63,214,.4); opacity: 0; animation: riseup linear infinite; }
.bgx .tick.s { border-color: rgba(232,146,15,.5); color: #9A5B00; }

@keyframes rot { to { transform: rotate(360deg); } }
@keyframes comet {
    0% { transform: translate(0,0) rotate(22deg); opacity: 0; }
    5% { opacity: 1; }
    30% { opacity: 1; }
    38%, 100% { transform: translate(135vw, 62vh) rotate(22deg); opacity: 0; }
}
@keyframes morph {
    0% { border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
    50% { border-radius: 30% 60% 70% 40% / 50% 60% 30% 60%; }
    100% { border-radius: 50% 50% 60% 40% / 40% 70% 40% 60%; }
}
@keyframes blobmove { to { transform: translate(var(--dx, 120px), var(--dy, 90px)) rotate(50deg) scale(1.25); } }
@keyframes netflow { to { stroke-dashoffset: -900; } }
@keyframes nodepulse { 0%,100% { transform: scale(1); opacity: .65; } 50% { transform: scale(2); opacity: 1; } }
@keyframes scan { to { transform: translateX(calc(100vw + 640px)); } }
@keyframes marq { to { transform: translateX(-50%); } }
@keyframes wavex { to { transform: translateX(-50%); } }
@keyframes cdl { to { transform: scaleY(var(--h, .9)); } }


/* ---------- DARK BOXES: empty-state notices + category filter ---------- */
.notice {
    background: #1A1545 !important;
    border: 1px solid rgba(255,255,255,.12) !important;
    border-left: 4px solid #E8920F !important;
    color: #FFFFFF !important;
}
div[data-testid="stSelectbox"] div[data-baseweb="select"] div { background-color: #1A1545 !important; }
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div { border-color: rgba(255,255,255,.16) !important; }
div[data-testid="stSelectbox"] *, div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
div[data-testid="stSelectbox"] div[data-baseweb="select"] input {
    color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important;
}
div[data-testid="stSelectbox"] svg { fill: #FFFFFF !important; }
div[data-testid="stSelectbox"] label p { color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; }
div[data-baseweb="popover"] > div, div[data-baseweb="popover"] ul[role="listbox"], div[data-baseweb="menu"] {
    background: #1A1545 !important;
}
ul[role="listbox"] li[role="option"] { background: #1A1545 !important; color: #FFFFFF !important; }
ul[role="listbox"] li[role="option"] * { color: #FFFFFF !important; -webkit-text-fill-color: #FFFFFF !important; }
ul[role="listbox"] li[role="option"]:hover,
ul[role="listbox"] li[role="option"][aria-selected="true"] { background: #3B2A9E !important; }


/* ---------- TYPE TUNING (Playfair Display + Outfit) ---------- */
h1, h2, h3, h4 { letter-spacing: -0.01em; }
.hero-title { letter-spacing: -0.02em; font-weight: 800; }
.brand { letter-spacing: -0.01em; }
.quote-text { font-size: clamp(20px, 2.4vw, 27px); line-height: 1.5; }

@media (prefers-reduced-motion: reduce) { .bgx, .bgx * { animation: none !important; } }
hr { display: none; }
</style>
""", unsafe_allow_html=True)


def html(markup: str):
    """Render HTML; strip indentation so Markdown never treats it as code."""
    cleaned = "\n".join(line.strip() for line in markup.strip().splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)


def thread():
    html('<div class="thread"><span></span></div>')


def eyebrow(text):
    html(f'<div class="eyebrow">{text}</div>')


def navigate(page):
    st.session_state.current_page = page
    st.rerun()



def home_bg():
    """Orbit system with planets, shooting comets, morphing blobs, twinkling stars."""
    rings = ""
    for i, (radius, secs, tone) in enumerate([(230, 14, ""), (350, 22, " s"), (480, 31, ""), (620, 44, " s"), (780, 62, "")]):
        direction = "reverse" if i % 2 else "normal"
        planet2 = '<span class="planet v b"></span>' if i % 2 == 0 else '<span class="planet b"></span>'
        planet_main = '<span class="planet v"></span>' if i % 2 else '<span class="planet"></span>'
        rings += (
            f'<div class="oring{tone}" style="width:{radius*2}px;height:{radius*2}px;left:-{radius}px;top:-{radius}px;'
            f'animation-duration:{secs}s;animation-direction:{direction};">{planet_main}{planet2}</div>'
        )
    comets = "".join(
        f'<div class="comet{" v" if i % 2 else ""}" style="top:{(i*17)%55}%;animation-duration:{8 + (i*3)%6}s;'
        f'animation-delay:-{(i*2.7)%9:.1f}s;"></div>'
        for i in range(6)
    )
    sparks = "".join(
        f'<span class="spark" style="left:{(i*53)%100}%;top:{(i*29+7)%92}%;font-size:{10+(i*7)%16}px;'
        f'animation-delay:-{(i*0.9)%6:.1f}s;animation-duration:{3+(i*5)%4}s;'
        f'{"color:#5B3FD6;" if i%3==0 else ""}">✦</span>'
        for i in range(30)
    )
    html(f"""
    <div class="bgx edge">
    <div class="blob v" style="width:420px;height:420px;left:-6%;top:8%;--dx:220px;--dy:160px"></div>
    <div class="blob s" style="width:380px;height:380px;right:-5%;top:48%;--dx:-240px;--dy:-120px;animation-delay:-6s"></div>
    <div class="blob v" style="width:320px;height:320px;right:12%;top:-6%;--dx:-160px;--dy:200px;animation-delay:-3s"></div>
    <div class="sys">{rings}</div>
    {comets}
    {sparks}
    </div>
    """)


def about_bg():
    rows = ""
    for i in range(9):
        top = 6 + i * 11
        cls = "stream s" if i % 3 == 1 else "stream"
        direction = "reverse" if i % 2 else "normal"
        rows += (
            f'<div class="{cls}" style="top:{top}%;animation-duration:{5 + (i*3)%7}s;animation-direction:{direction};">'
            f'<span class="packet" style="animation-duration:{9 + (i*5)%9}s;animation-delay:-{(i*2.3)%10:.1f}s;'
            f'animation-direction:{direction};"></span></div>'
        )
    html(f"""
    <div class="bgx">
    <div class="orb v" style="width:520px;height:520px;right:-8%;top:-6%;--dx:-160px;--dy:140px"></div>
    <div class="orb s" style="width:460px;height:460px;left:-8%;bottom:4%;--dx:170px;--dy:-100px"></div>
    {rows}
    <div class="pulse" style="left:6%;top:62%"></div>
    <div class="pulse s" style="left:6%;top:62%;animation-delay:-2.3s"></div>
    <div class="pulse" style="left:6%;top:62%;animation-delay:-4.6s"></div>
    <div class="pulse s" style="right:4%;top:8%;animation-delay:-1s"></div>
    <div class="pulse" style="right:4%;top:8%;animation-delay:-3.4s"></div>
    </div>
    """)


def connect_bg():
    bars = "".join(
        f'<b style="--h:{0.25 + ((i*37) % 70) / 100:.2f};animation-duration:{2.2 + (i*7) % 30 / 10:.1f}s;'
        f'animation-delay:-{(i*0.37) % 4:.1f}s;"></b>'
        for i in range(52)
    )
    coins = "".join(
        f'<div class="coin{" v" if i % 2 else ""}" style="left:{8 + i*15}%;top:{18 + (i*23) % 55}%;'
        f'animation-delay:-{i*1.3:.1f}s;animation-duration:{6 + i % 3}s;">{g}</div>'
        for i, g in enumerate(["✦", "◈", "⌁", "✦", "◈", "⌁"])
    )
    html(f"""
    <div class="bgx">
    <div class="orb s" style="width:520px;height:520px;left:-8%;top:10%;--dx:180px;--dy:90px"></div>
    <div class="orb v" style="width:500px;height:500px;right:-8%;top:40%;--dx:-170px;--dy:-110px"></div>
    <svg class="lines" viewBox="0 0 1200 800" preserveAspectRatio="none" aria-hidden="true">
    <defs><linearGradient id="cg" x1="0" x2="1"><stop offset="0" stop-color="#5B3FD6"/><stop offset="1" stop-color="#E8920F"/></linearGradient></defs>
    <path pathLength="1000" stroke="url(#cg)" d="M0 560 L120 500 L220 540 L340 420 L450 470 L580 330 L700 390 L820 250 L940 300 L1060 160 L1200 210"/>
    <path pathLength="1000" stroke="url(#cg)" style="animation-delay:-4s" d="M0 640 L140 610 L260 650 L380 560 L500 600 L640 500 L760 540 L900 430 L1020 470 L1200 360"/>
    <path pathLength="1000" stroke="#5B3FD6" style="animation-delay:-7s" d="M0 420 L160 380 L300 430 L420 330 L560 380 L700 260 L840 320 L980 200 L1200 250"/>
    </svg>
    <div class="eq">{bars}</div>
    {coins}
    </div>
    """)


# =========================================================
# NAVIGATION BAR
# =========================================================

nav_col, home_col, about_col, future_col, connect_col = (
    st.columns([2.4, 1, 1, 1.6, 1.6])
)

with nav_col:
    html('<div class="brand"><span class="glyph">✦</span>ArthaSutra</div>')

with home_col:
    if st.button(
        "Home",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "Home" else "secondary"
    ):
        navigate("Home")

with about_col:
    if st.button(
        "About Us",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "About Us" else "secondary"
    ):
        navigate("About Us")

with future_col:
    if st.button(
        "Future Developments",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "Future Developments" else "secondary"
    ):
        navigate("Future Developments")

with connect_col:
    if st.button(
        "Connect / Enter",
        use_container_width=True,
        type="primary" if st.session_state.current_page == "Connect" else "secondary"
    ):
        navigate("Connect")


# =========================================================
# QUOTES
# =========================================================

quotes = [
    "Knowledge becomes valuable when it reveals what matters.",
    "The right information can change the way you invest.",
    "In a world full of noise, discover the signals that matter.",
    "Understand the ecosystem. Understand your investments.",
    "Intelligence is knowing what deserves your attention.",
    "Make informed decisions through meaningful insights."
]

quote_index = int(datetime.now().timestamp() // 15) % len(quotes)
current_quote = quotes[quote_index]

HERO_THREAD = """
<svg class="hero-thread" viewBox="0 0 1200 420" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
<defs>
<linearGradient id="tg" x1="0" x2="1">
<stop offset="0" stop-color="#5B3FD6" stop-opacity="0"/>
<stop offset="0.35" stop-color="#5B3FD6" stop-opacity=".55"/>
<stop offset="0.7" stop-color="#E8920F" stop-opacity=".8"/>
<stop offset="1" stop-color="#E8920F" stop-opacity="0"/>
</linearGradient>
</defs>
<path d="M-20 330 C 220 110, 420 400, 640 230 S 1020 60, 1230 190" fill="none" stroke="url(#tg)" stroke-width="1.6"/>
<path d="M-20 330 C 220 110, 420 400, 640 230 S 1020 60, 1230 190" fill="none" stroke="url(#tg)" stroke-width="7" stroke-linecap="round" stroke-dasharray="0.1 34"/>
</svg>
"""


# =========================================================
# HOME PAGE
# =========================================================

if st.session_state.current_page == "Home":

    home_bg()

    html(f"""
    <div class="hero">
    {HERO_THREAD}
    <div class="hero-tag">Your personalized crypto intelligence platform</div>
    <div class="hero-title">ArthaSutra</div>
    <div class="quote">
    <div class="quote-ornament">✦</div>
    <div class="quote-text">“{current_quote}”</div>
    <div class="quote-gloss">Artha: wealth and meaning. Sutra: the thread that ties them together.</div>
    </div>
    <div class="hero-subtitle">
    <strong>Understand Crypto. Discover What Matters.</strong><br><br>
    An intelligent platform that connects your cryptocurrency portfolio with the news, developments and insights that matter to you.
    </div>
    </div>
    """)

    eyebrow("Why ArthaSutra?")
    st.title("Information That Matters.")

    st.write(
        "The crypto world produces thousands of updates every day. "
        "Finding information relevant to your investments can be difficult. "
        "ArthaSutra helps you focus on what matters to your portfolio."
    )

    html("""
    <div class="pillars">
    <div class="pillar"><div class="icon">◈</div><h3>Portfolio Awareness</h3>
    <p>Keep track of your cryptocurrency holdings and focus on the assets you care about.</p></div>
    <div class="pillar"><div class="icon">⌁</div><h3>Intelligent News</h3>
    <p>Collect, categorize and filter crypto news from multiple sources.</p></div>
    <div class="pillar"><div class="icon">✦</div><h3>Personalized Insights</h3>
    <p>Understand why an article is relevant to your portfolio.</p></div>
    </div>
    """)

    thread()

    eyebrow("Get started")
    st.title("Your Crypto Intelligence Starts Here.")

    st.write(
        "Connect your wallet or manually enter your cryptocurrency holdings "
        "to explore personalized crypto intelligence."
    )

    if st.button(
        "Explore ArthaSutra →",
        type="primary",
        use_container_width=True
    ):
        navigate("Connect")


# =========================================================
# ABOUT US PAGE
# =========================================================

elif st.session_state.current_page == "About Us":

    about_bg()

    eyebrow("About ArthaSutra")
    st.title("Making Crypto Information Meaningful.")

    st.write(
        "ArthaSutra is a portfolio-aware cryptocurrency intelligence "
        "platform. A Python and Streamlit application runs a news "
        "pipeline (collection, processing, storage), a relevance engine "
        "that matches articles to your holdings, and an insight generator "
        "that explains each match."
    )

    html("""
    <div class="setup">
    <div class="setup-title">Current setup</div>
    <p>ArthaSutra currently runs locally on <strong>localhost</strong>.
    Wallet connection works through browser extensions: <strong>MetaMask</strong> for EVM networks
    and <strong>Phantom</strong> for Solana. The extension must be installed and enabled in the
    browser you use to open the app.</p>
    <span class="chip">Python</span><span class="chip">Streamlit</span>
    <span class="chip">Local database</span><span class="chip">MetaMask</span><span class="chip">Phantom</span>
    </div>
    """)

    thread()

    left, right = st.columns(2, gap="large")

    with left:
        st.subheader("Our Vision")
        st.write(
            "To make cryptocurrency information more meaningful, accessible "
            "and personalized by connecting market developments with "
            "individual portfolio interests."
        )

    with right:
        st.subheader("Our Mission")
        st.write(
            "To collect crypto news from multiple sources, identify "
            "important tokens and events, remove duplicate information "
            "and deliver personalized insights."
        )

    thread()

    st.subheader("How the Pipeline Works")

    steps = [
        ("1", "Collect", "The collector fetches crypto articles from a news API as structured results."),
        ("2", "Process", "The processor detects token mentions, assigns a news category and an event type, and removes duplicate articles."),
        ("3", "Store", "Processed articles and your portfolio holdings are saved in the local database."),
        ("4", "Match", "The relevance engine compares the tokens found in each article with the tokens in your portfolio."),
        ("5", "Explain", "The insight generator writes a short explanation of why each matched article matters to you."),
        ("6", "Connect", "The wallet connector reads your public address and network through the MetaMask or Phantom extension.")
    ]

    st.write("")

    for number, heading, description in steps:
        html(f"""
        <div class="step">
        <div class="bead">{number}</div>
        <div><h3>{heading}</h3><p>{description}</p></div>
        </div>
        """)


# =========================================================
# FUTURE DEVELOPMENTS PAGE
# =========================================================

elif st.session_state.current_page == "Future Developments":

    particles = "".join(
        f'<i style="left:{(i * 37) % 100}%;animation-delay:-{(i * 1.7) % 16:.1f}s;'
        f'animation-duration:{14 + (i * 3) % 10}s;'
        f'width:{4 + (i * 5) % 7}px;height:{4 + (i * 5) % 7}px;"></i>'
        for i in range(22)
    )

    html(f"""
    <style>
    .future-bg {{ position: fixed; inset: 0; z-index: -1; overflow: hidden; pointer-events: none; }}
    .block-container {{ position: relative; z-index: 1; }}
    .future-bg .orb {{ position: absolute; border-radius: 50%; filter: blur(70px); opacity: .55; }}
    .future-bg .o1 {{ width: 520px; height: 520px; left: -8%; top: 5%;
        background: radial-gradient(circle, rgba(91,63,214,.45), transparent 70%);
        animation: drift1 22s ease-in-out infinite alternate; }}
    .future-bg .o2 {{ width: 460px; height: 460px; right: -6%; top: 30%;
        background: radial-gradient(circle, rgba(232,146,15,.40), transparent 70%);
        animation: drift2 26s ease-in-out infinite alternate; }}
    .future-bg .o3 {{ width: 420px; height: 420px; left: 35%; bottom: -12%;
        background: radial-gradient(circle, rgba(139,115,240,.38), transparent 70%);
        animation: drift3 30s ease-in-out infinite alternate; }}
    .future-bg .grid {{
        position: absolute; left: -50%; right: -50%; bottom: -10%; height: 55%;
        background-image:
            linear-gradient(rgba(91,63,214,.16) 1px, transparent 1px),
            linear-gradient(90deg, rgba(91,63,214,.16) 1px, transparent 1px);
        background-size: 56px 56px;
        transform: perspective(500px) rotateX(62deg);
        transform-origin: bottom;
        -webkit-mask-image: linear-gradient(to top, #000 10%, transparent 85%);
        mask-image: linear-gradient(to top, #000 10%, transparent 85%);
        animation: gridflow 6s linear infinite;
    }}
    .future-bg svg {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
    .future-bg .flow {{
        fill: none; stroke: url(#fg); stroke-width: 1.6;
        stroke-dasharray: 8 14; animation: flow 18s linear infinite;
    }}
    .future-bg .flow.b {{ animation-duration: 26s; animation-direction: reverse; opacity: .7; }}
    .future-bg i {{
        position: absolute; bottom: -20px; border-radius: 50%;
        background: radial-gradient(circle at 35% 35%, #FFD08A, var(--saffron));
        box-shadow: 0 0 12px rgba(232,146,15,.55);
        opacity: 0; animation: rise-up linear infinite;
    }}
    @keyframes drift1 {{ to {{ transform: translate(160px, 110px) scale(1.15); }} }}
    @keyframes drift2 {{ to {{ transform: translate(-190px, -90px) scale(1.2); }} }}
    @keyframes drift3 {{ to {{ transform: translate(-120px, -130px) scale(.9); }} }}
    @keyframes gridflow {{ to {{ background-position: 0 56px, 56px 0; }} }}
    @keyframes flow {{ to {{ stroke-dashoffset: -440; }} }}
    @keyframes rise-up {{
        0%   {{ transform: translateY(0); opacity: 0; }}
        12%  {{ opacity: .85; }}
        85%  {{ opacity: .5; }}
        100% {{ transform: translateY(-105vh); opacity: 0; }}
    }}
    .road-item {{ background: rgba(255,255,255,.78); backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }}
    @media (prefers-reduced-motion: reduce) {{
        .future-bg *, .future-bg {{ animation: none !important; }}
    }}
    </style>
    <div class="future-bg">
    <div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
    <div class="grid"></div>
    <svg viewBox="0 0 1200 800" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <defs><linearGradient id="fg" x1="0" x2="1">
    <stop offset="0" stop-color="#5B3FD6" stop-opacity="0"/>
    <stop offset=".5" stop-color="#5B3FD6" stop-opacity=".6"/>
    <stop offset="1" stop-color="#E8920F" stop-opacity=".8"/></linearGradient></defs>
    <path class="flow" d="M-20 520 C 250 300, 450 640, 700 430 S 1050 220, 1230 340"/>
    <path class="flow b" d="M-20 300 C 300 520, 520 120, 760 300 S 1060 560, 1230 420"/>
    </svg>
    {particles}
    </div>
    """)

    eyebrow("The road ahead")
    st.title("Future Developments")

    st.write(
        "ArthaSutra is designed to grow into a more comprehensive "
        "cryptocurrency intelligence platform."
    )

    roadmap = [
        (
            "Login / Sign Up",
            "Personal accounts so every user has a private portfolio and feed that follows them across sessions."
        ),
        (
            "Our Own Database",
            "A dedicated ArthaSutra database for users, portfolios and articles, built for scale and reliability."
        ),
        (
            "Perfect Relevance Engine",
            "Vector embeddings to match news to your holdings by meaning, plus a smarter deduplicator that merges stories covering the same event."
        ),
        (
            "Perfect Category-Based Insights",
            "Sharper, category-aware insights that explain exactly why each article matters for what you hold."
        ),
        (
            "Centralized Wallet Connections",
            "Connect to centralized exchange wallets, in addition to the MetaMask and Phantom extensions."
        )
    ]

    st.write("")

    for title, description in roadmap:
        html(f"""
        <div class="road-item">
        <div class="mark">✦</div>
        <div><h3>{title}</h3><p>{description}</p></div>
        </div>
        """)

    st.info(
        "These are planned developments, not features currently available."
    )


# =========================================================
# CONNECT / MAIN DASHBOARD
# =========================================================

elif st.session_state.current_page == "Connect":

    connect_bg()

    html(f"""
    <div class="hero compact">
    {HERO_THREAD}
    <div class="hero-tag">ArthaSutra Intelligence Center</div>
    <div class="hero-title">Your Crypto Dashboard</div>
    <div class="quote">
    <div class="quote-text" style="font-size:22px;">Manage your portfolio and discover the news that matters.</div>
    </div>
    </div>
    """)


    # -----------------------------------------------------
    # WALLET CONNECTION
    # -----------------------------------------------------

    eyebrow("Wallet integration")

    st.subheader("Connect Your Crypto Wallet")

    st.caption(
        "Connect MetaMask or Phantom to access your public wallet information."
    )

    wallet_result = connect_wallet()
    wallet_data = getattr(wallet_result, "wallet", None)

    if wallet_data:

        wallet_type = wallet_data.get("wallet_type", "Wallet")

        if wallet_data.get("status") == "connected":

            address = wallet_data.get("address")
            chain_id = wallet_data.get("chain_id")

            st.success(f"{wallet_type} connected successfully!")

            if address:
                st.code(address, language=None)

            if wallet_type == "MetaMask" and chain_id:
                st.caption(f"Connected Network ID: {chain_id}")

            elif wallet_type == "Phantom":
                st.caption("Connected Network: Solana")

        elif wallet_data.get("status") == "not_installed":

            st.warning(
                f"{wallet_type} was not detected. "
                "Please install or enable the wallet extension."
            )

        elif wallet_data.get("status") == "error":

            st.error(
                wallet_data.get("message", "Wallet connection failed.")
            )

    thread()


    # -----------------------------------------------------
    # DASHBOARD DATA
    # -----------------------------------------------------

    portfolio = get_portfolio()
    relevant_articles = get_relevant_news()


    # -----------------------------------------------------
    # TOP METRICS
    # -----------------------------------------------------

    eyebrow("Your overview")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        html(f"""
        <div class="metric-card">
        <div class="metric-label">Portfolio assets</div>
        <div class="metric-value">{len(portfolio)}</div>
        <div class="metric-description">Tokens you currently hold</div>
        </div>
        """)

    with col2:
        html(f"""
        <div class="metric-card">
        <div class="metric-label">Personalized news</div>
        <div class="metric-value">{len(relevant_articles)}</div>
        <div class="metric-description">Articles matching your holdings</div>
        </div>
        """)

    with col3:
        html("""
        <div class="metric-card">
        <div class="metric-label">Intelligence status</div>
        <div class="metric-value word"><span class="live-dot"></span>Active</div>
        <div class="metric-description">Portfolio matching enabled</div>
        </div>
        """)

    thread()


    # -----------------------------------------------------
    # NEWS COLLECTION
    # -----------------------------------------------------

    eyebrow("News collection")

    col1, col2 = st.columns([3, 1])

    with col1:

        st.subheader("Discover Latest Crypto News")

        st.caption(
            "Collect and process news from your configured sources."
        )

    with col2:

        st.write("")

        if st.button(
            "↻ Fetch Latest News",
            use_container_width=True,
            type="primary"
        ):

            try:

                with st.spinner("Collecting and processing crypto news..."):

                    data = fetch_news()

                    articles = process_news(
                        data.get("results", [])
                    )

                    save_news_articles(articles)

                st.success(
                    f"Successfully processed {len(articles)} articles!"
                )

                st.rerun()

            except Exception as error:

                st.error(f"News collection failed: {error}")


    # -----------------------------------------------------
    # PORTFOLIO MANAGEMENT
    # -----------------------------------------------------

    thread()

    eyebrow("Portfolio management")

    st.subheader("My Portfolio")

    st.caption(
        "Manage the cryptocurrencies you currently hold."
    )

    with st.container(border=True):

        with st.form("portfolio_form", clear_on_submit=True):

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:

                symbol = st.text_input(
                    "Token Symbol",
                    placeholder="e.g. BTC, ETH, SOL"
                )

            with col2:

                quantity = st.number_input(
                    "Quantity",
                    min_value=0.000001,
                    value=1.0
                )

            with col3:

                st.write("")
                st.write("")

                submitted = st.form_submit_button(
                    "＋ Add Token",
                    use_container_width=True
                )

            if submitted:

                if symbol.strip():

                    add_token(symbol, quantity)

                    st.success(
                        f"{symbol.upper()} saved successfully!"
                    )

                    st.rerun()

                else:

                    st.error("Please enter a token symbol.")


    # -----------------------------------------------------
    # DISPLAY PORTFOLIO
    # -----------------------------------------------------

    portfolio = get_portfolio()

    if portfolio:

        st.write("### Your Holdings")

        for token, amount in portfolio:

            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                html(f'<div class="holding"><span class="sym">{escape(str(token))}</span></div>')

            with col2:
                html(f'<div class="holding"><span class="qty">Quantity: {escape(str(amount))}</span></div>')

            with col3:

                if st.button(
                    "Remove",
                    key=f"delete_{token}",
                    use_container_width=True
                ):

                    delete_token(token)
                    st.rerun()

    else:

        html('<div class="notice">Your portfolio is empty. Add your first cryptocurrency above.</div>')


    # -----------------------------------------------------
    # PERSONALIZED NEWS FEED
    # -----------------------------------------------------

    thread()

    eyebrow("Portfolio intelligence")

    st.subheader("Your Personalized News Feed")

    st.caption(
        "News is matched against the tokens currently in your portfolio."
    )

    # Always refresh the data.
    portfolio = get_portfolio()
    relevant_articles = get_relevant_news()

    all_categories = [
        "Finance",
        "Government & Policy",
        "Technology",
        "Security",
        "Markets & Trading",
        "DeFi",
        "Business & Partnerships",
        "Adoption & Payments",
        "Blockchain Infrastructure",
        "Exchanges & Listings",
        "NFTs & Gaming",
        "Stablecoins",
        "Mining & Energy",
        "General"
    ]

    available_categories = sorted({
        article.get("news_category") or "General"
        for article in relevant_articles
    })

    category_options = ["All"] + sorted(
        set(all_categories + available_categories)
    )

    selected_category = st.selectbox(
        "Filter News by Category",
        category_options
    )

    if selected_category == "All":

        filtered_articles = relevant_articles

    else:

        filtered_articles = [
            article
            for article in relevant_articles
            if (
                article.get("news_category") or "General"
            ) == selected_category
        ]


    if filtered_articles:

        st.success(
            f"{len(filtered_articles)} articles found in this category."
        )

        for article in filtered_articles:

            with st.container(border=True):

                st.markdown(
                    f"### {article.get('title') or 'Untitled Article'}"
                )

                source = article.get("source") or "Unknown Source"

                event_category = (
                    article.get("event_category") or "GENERAL"
                )

                news_category = (
                    article.get("news_category") or "General"
                )

                html(f"""
                <span class="chip source">{escape(str(source))}</span>
                <span class="chip">{escape(str(news_category))}</span>
                <span class="chip event">Event: {escape(str(event_category))}</span>
                """)

                st.write(
                    article.get("description") or "No description available."
                )

                matched_tokens = article.get("matched_tokens") or []

                token_chips = "".join(
                    f'<span class="chip token">{escape(str(t))}</span>'
                    for t in matched_tokens
                )

                html(
                    f'<div style="margin:4px 0 10px;"><strong style="color:#1A1545;">Matched tokens</strong>&nbsp;&nbsp;{token_chips}</div>'
                )

                st.info(generate_insight(article))

                article_url = article.get("url")

                if article_url:

                    st.markdown(
                        f"[Read Full Article ↗]({article_url})"
                    )

    else:

        html('<div class="notice">No matching news found for your portfolio. Add tokens or fetch the latest news.</div>')


# =========================================================
# FOOTER
# =========================================================

thread()

html("""
<div class="footer">
<div class="brand"><span class="glyph">✦</span>ArthaSutra</div>
<p>Portfolio-Aware Crypto Intelligence</p>
<p>Understand Crypto. Discover What Matters.</p>
</div>
""")
