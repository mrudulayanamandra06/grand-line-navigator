import datetime as dt
import base64
import os
import random
from typing import Any

import streamlit as st
import frontend.api_client
from frontend.api_client import APIError

st.set_page_config(
    page_title="Grand Line Navigator",
    page_icon="☠️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Final visual system: consistent typography, spacing, surfaces, and responsive behavior.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');
    :root { --display:'Bricolage Grotesque',sans-serif; --body:'Plus Jakarta Sans',sans-serif; --mono:'JetBrains Mono',monospace; }
    [data-testid="stHeader"] { display:block !important; height:3.5rem !important; background:rgba(255,248,231,.88) !important; backdrop-filter:blur(16px); border-bottom:1px solid rgba(20,40,61,.10); }
    [data-testid="stToolbar"] { display:flex !important; }
    [data-testid="stSidebarCollapsedControl"] {
        display:flex !important; position:fixed !important; top:16px !important; left:16px !important; z-index:999999 !important;
    }
    [data-testid="stSidebarCollapsedControl"] button {
        width:42px !important; height:42px !important; border:1px solid rgba(229,181,68,.65) !important;
        border-radius:10px !important; background:#0b3554 !important; color:#fff8e7 !important; box-shadow:0 8px 22px rgba(11,53,84,.22) !important;
    }
    [data-testid="stSidebarCollapseButton"] button { color:#fff8e7 !important; }
    [data-testid="stAppViewContainer"] > .main { background:transparent; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#0b3554 0%,#0e5870 58%,#0a405b 100%) !important; border-right:1px solid rgba(229,181,68,.42) !important; }
    [data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] .menu-label { color:#fff8e7 !important; }
    [data-testid="stSidebar"] .menu-label { color:#e5b544 !important; }
    .sidebar-brand { background:linear-gradient(135deg,#c64038,#8f292d) !important; border:1px solid rgba(229,181,68,.65); }
    .sidebar-status { background:rgba(255,248,231,.09) !important; border-left-color:#e5b544 !important; color:#fff8e7 !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label { background:rgba(255,248,231,.06) !important; border-color:rgba(255,248,231,.08) !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label:hover { background:rgba(229,181,68,.15) !important; border-color:rgba(229,181,68,.38) !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] { background:linear-gradient(90deg,#c64038,#a93235) !important; border-color:#e5b544 !important; }
    .block-container {
        width: min(1480px, calc(100% - 64px)) !important;
        max-width: 1480px !important;
        margin-inline: auto !important;
        padding: 38px 0 80px !important;
    }
    body,p,li,label,input,textarea,button,[data-testid="stMarkdownContainer"] { font-family:var(--body) !important; }
    h1,h2,h3,h4,.hero-title,.section-heading h2,.fruit-name,.faction-title,.sidebar-brand strong { font-family:var(--display) !important; }
    h1,h2,h3,h4 { letter-spacing:-.045em !important; font-weight:700 !important; }
    p,li { line-height:1.72; }
    [data-testid="stVerticalBlock"] { gap:1rem !important; }
    [data-testid="stHorizontalBlock"] { gap:1.25rem !important; align-items:stretch !important; }
    [data-testid="stColumn"] { min-width:0 !important; }

    [data-testid="stSidebar"] { width:300px !important; min-width:300px !important; border-right:1px solid rgba(36,52,71,.12); }
    [data-testid="stSidebar"] > div:first-child { padding:26px 18px 30px; }
    .sidebar-brand { padding:16px; border-radius:16px; box-shadow:0 12px 32px rgba(141,32,41,.18); }
    .sidebar-brand strong { font-size:1.2rem; font-weight:700; letter-spacing:-.02em; }
    .sidebar-brand small { margin-top:3px; font-family:var(--mono) !important; font-size:.61rem; }
    .menu-label,.section-kicker,.eyebrow,.detail-label { font-family:var(--mono) !important; }
    [data-testid="stSidebar"] [role="radiogroup"] { gap:7px !important; }
    [data-testid="stSidebar"] [role="radiogroup"] label { min-height:46px; padding:11px 12px !important; border-radius:10px; box-shadow:none; }
    [data-testid="stSidebar"] [role="radiogroup"] label p { font-size:.86rem; line-height:1.25; }
    .sidebar-status { margin-top:18px; padding:12px 14px; font-family:var(--mono); font-size:.65rem; }

    .brand-lockup { margin-top:4px; font-family:var(--mono); font-size:.82rem; letter-spacing:.14em; }
    .brand-rule { width:54px; margin:10px 0 12px; }
    .subtitle { max-width:780px; margin:0 0 28px; font-size:.98rem; font-weight:500; line-height:1.65; }
    .st-key-main_navigation {
        width: 100% !important;
        margin: 0 0 30px !important;
        overflow: hidden !important;
        background: rgba(255, 248, 231, 0.96) !important;
        border-bottom: 1px solid rgba(20, 40, 61, 0.18) !important;
    }
    .st-key-main_navigation [role="radiogroup"] {
        display: grid !important;
        grid-template-columns: repeat(8, minmax(0, 1fr)) !important;
        width: 100% !important;
        gap: 0 !important;
    }
    .st-key-main_navigation label {
        width: 100% !important;
        min-width: 0 !important;
        min-height: 54px !important;
        margin: 0 !important;
        padding: 14px 8px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        color: #14283d !important;
        cursor: pointer !important;
        transition: color .18s ease, background .18s ease;
    }
    .st-key-main_navigation label:hover {
        background: rgba(229, 181, 68, 0.09) !important;
        color: #14283d !important;
    }
    .st-key-main_navigation label p {
        color: inherit !important;
        font-size: 0.76rem !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        text-align: center !important;
        white-space: nowrap !important;
    }
    .st-key-main_navigation label:has(input:checked) {
        color: #c64038 !important;
        background: rgba(198, 64, 56, 0.06) !important;
        box-shadow: inset 0 -3px 0 #c64038 !important;
    }
    .st-key-main_navigation [data-baseweb="radio"] > div:first-child {
        display: none !important;
    }

    @media (max-width: 1100px) {
        .st-key-main_navigation {
            overflow-x: auto !important;
        }

        .st-key-main_navigation [role="radiogroup"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            width: max-content !important;
            min-width: 100% !important;
        }

        .st-key-main_navigation label {
            flex: 0 0 auto !important;
            width: auto !important;
            min-width: 145px !important;
            padding-inline: 16px !important;
        }
    }
    .hero { min-height:280px; padding:42px 48px; margin:0 0 22px; border-radius:20px; background:linear-gradient(125deg,#fff1c9 0%,#f7d99d 48%,#bfe4e5 100%) !important; border-color:rgba(14,113,135,.28) !important; box-shadow:0 24px 60px rgba(11,53,84,.16); }
    .hero::before { content:''; position:absolute; inset:auto 0 0; height:7px; background:linear-gradient(90deg,#0e7187 0 22%,#e5b544 22% 44%,#c64038 44% 66%,#e87545 66% 82%,#0b3554 82%); opacity:.9; }
    .hero-copy { max-width:720px; }
    .hero-title { max-width:690px; font-size:clamp(2.5rem,5vw,4.65rem); font-weight:700; line-height:.94; letter-spacing:-.065em; }
    .hero-note { max-width:620px; margin-top:18px; font-size:.96rem; line-height:1.72; }
    .hero-svg { width:280px; height:190px; }
    .icon-rail { gap:8px; margin:0 0 54px; }
    .icon-chip { padding:8px 12px; background:rgba(255,250,240,.82); border-color:rgba(14,113,135,.2); font-family:var(--mono); font-size:.68rem; }
    .icon-chip svg { stroke:#0e7187; }

    .section-heading { margin:10px 0 24px; padding-top:22px; border-top:1px solid var(--line); }
    .section-heading h2 { font-size:clamp(1.9rem,3vw,2.75rem) !important; font-weight:700 !important; letter-spacing:-.05em !important; line-height:1.05; }
    .section-heading .ui-icon { width:40px; height:40px; padding:9px; border-radius:12px; }
    .section-kicker { margin-bottom:5px; font-size:.64rem; }

    .card,.fruit-card,.story,.faction-card,.battle-result,.crew-stat-card,.encyclopedia-toolbar,.insight-card,.compare-card,[data-testid="stMetric"],[data-testid="stExpander"] {
        border-color:rgba(20,40,61,.14) !important; box-shadow:0 10px 30px rgba(11,53,84,.09); }
    .card,.fruit-card,.compare-card,.crew-stat-card,[data-testid="stMetric"],[data-testid="stExpander"] { background:linear-gradient(145deg,#fffdf6,#fff5dc) !important; }
    .story { background:linear-gradient(110deg,#fffaf0,#f6e3b4) !important; border-left-color:#c64038 !important; }
    .insight-card,.battle-result { background:linear-gradient(135deg,#f8df9d,#ccebed) !important; }
    .encyclopedia-toolbar { background:rgba(255,250,240,.9) !important; border-top:3px solid #0e7187 !important; }
    .card,.fruit-card,.compare-card { height:100%; padding:22px; border-radius:16px; }
    .card { min-height:150px; }
    .card h4 { margin-bottom:16px; font-family:var(--mono) !important; font-size:.66rem; }
    .value { font-family:var(--display); font-size:1.32rem; font-weight:700; letter-spacing:-.03em; }
    .story { margin-top:4px; margin-bottom:18px; padding:22px 25px; border-radius:14px; }
    .story h3 { font-size:1.35rem; }
    .fruit-card { min-height:0; margin-bottom:18px; }
    .portrait-image { aspect-ratio:1.35; border-radius:10px; margin-bottom:18px; }
    .fruit-name { font-size:1.22rem; letter-spacing:-.03em; }
    .insight-card { min-height:120px; display:flex; flex-direction:column; justify-content:center; }
    .insight-card strong { font-family:var(--display); font-size:2rem; }
    .reward-row { min-height:58px; padding:14px 4px; }
    .reward-ledger { overflow:hidden; border:1px solid var(--line); border-radius:14px; background:rgba(255,255,255,.7); box-shadow:0 10px 30px rgba(48,77,91,.07); }
    .reward-ledger .reward-row { margin:0; padding:15px 18px; }
    .reward-ledger .reward-row:last-child { border-bottom:0; }
    .reward-ledger .reward-row strong { display:flex; align-items:center; gap:10px; color:var(--ink); }
    .reward-ledger .reward-row em { padding:4px 7px; border-radius:999px; background:#fff4dc; color:var(--orange); font-family:var(--mono); font-size:.58rem; font-style:normal; letter-spacing:.05em; }
    .reward-ledger .reward-row.is-claimed { background:rgba(73,167,192,.08); }
    .reward-ledger .reward-row.is-claimed em { background:rgba(73,167,192,.16); color:#2f7d9a; }
    [data-testid="stToggle"] { padding:4px 0 8px; }
    [data-testid="stToggle"] label p { font-size:.78rem; font-weight:700; }

    [data-testid="stMetric"] { min-height:122px; padding:18px 20px; border-radius:14px; }
    [data-testid="stMetricValue"] { font-family:var(--display) !important; font-size:1.8rem !important; font-weight:700; letter-spacing:-.04em; }
    [data-testid="stMetricLabel"] { font-family:var(--mono) !important; font-size:.66rem !important; letter-spacing:.05em; text-transform:uppercase; }
    [data-testid="stTextInput"],[data-testid="stNumberInput"],[data-testid="stSelectbox"],[data-testid="stMultiSelect"],[data-testid="stSlider"] { margin-bottom:8px; }
    [data-baseweb="input"],[data-baseweb="select"] > div { min-height:48px; border-radius:10px !important; }
    [data-baseweb="input"],[data-baseweb="select"] > div { background:#fffdf6 !important; border-color:rgba(14,113,135,.28) !important; }
    .stButton > button { min-height:46px; padding:10px 18px; border-radius:10px; font-size:.84rem; box-shadow:none; background:linear-gradient(135deg,#e5b544,#e87545) !important; border-color:#c64038 !important; color:#14283d !important; }
    .stButton > button:hover { background:linear-gradient(135deg,#f0c85d,#ed8253) !important; border-color:#8f292d !important; }
    [data-testid="stProgressBar"] > div > div,[data-testid="stProgress"] > div > div > div > div { background:linear-gradient(90deg,#0e7187,#e5b544,#c64038) !important; }
    [data-testid="stMetric"] { position:relative; overflow:hidden; }
    [data-testid="stMetric"]::before { content:''; position:absolute; inset:0 auto 0 0; width:4px; background:linear-gradient(#0e7187,#e5b544); }
    [data-testid="stToggle"] button[aria-checked="true"] { background:#0e7187 !important; }
    .reward-ledger { background:rgba(255,250,240,.9) !important; border-color:rgba(14,113,135,.18) !important; }
    .reward-ledger .reward-row.is-claimed { background:rgba(14,113,135,.10) !important; }
    .reward-ledger .reward-row.is-claimed em { background:rgba(14,113,135,.16) !important; color:#0b5870 !important; }
    [data-testid="stDataFrame"],[data-testid="stExpander"] { border-radius:12px !important; overflow:hidden; }

    @media (max-width:900px) {
        .block-container { width:min(1480px, calc(100% - 40px)) !important; margin-inline:auto !important; padding:28px 0 60px !important; }
        .hero { min-height:250px; padding:34px 30px; }
        .hero-svg { width:210px; }
        [data-testid="stHorizontalBlock"] { flex-wrap:wrap !important; }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width:calc(50% - .75rem) !important; flex:1 1 calc(50% - .75rem) !important; }
    }
    @media (max-width:640px) {
        .block-container { width:min(1480px, calc(100% - 28px)) !important; margin-inline:auto !important; padding:22px 0 48px !important; }
        .hero { min-height:0; padding:28px 24px; }
        .hero-title { font-size:2.65rem; }
        .hero-svg { display:none; }
        .icon-rail { margin-bottom:38px; }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { min-width:100% !important; flex:1 1 100% !important; }
        .reward-row { align-items:flex-start; flex-direction:column; gap:5px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');
        :root { --ink:#14283d; --deep:#0b3554; --panel:#fffaf0; --panel-2:#f4e5bd; --gold:#e5b544; --orange:#e87545; --red:#c64038; --red-dark:#8f292d; --cream:#fff8e7; --sea:#0e7187; --sky:#48a9bd; --muted:#5e6f78; --line:rgba(20,40,61,.16); }
        .stApp { background:radial-gradient(circle at 82% 0%,rgba(229,181,68,.20),transparent 30%),radial-gradient(circle at 4% 24%,rgba(14,113,135,.17),transparent 28%),linear-gradient(145deg,#edf7f5 0%,#fff8e7 54%,#f6e8c7 100%); color:var(--ink); font-family:'Nunito Sans',sans-serif; }
        .stApp:before { content:''; position:fixed; inset:0; pointer-events:none; opacity:.24; background-image:linear-gradient(rgba(36,52,71,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(36,52,71,.035) 1px,transparent 1px); background-size:42px 42px; mask-image:linear-gradient(to bottom,black,transparent 75%); }
        [data-testid="stHeader"] { background:transparent; }
        [data-testid="stSidebar"] { background:linear-gradient(180deg,#fffdf7,#eaf5f7); border-right:1px solid rgba(185,43,43,.18); }
        [data-testid="stSidebar"] h2 { font-family:'DM Serif Display',serif; letter-spacing:.01em; }
        h1,h2,h3,h4 { color:var(--ink) !important; font-family:'DM Serif Display',serif; letter-spacing:-.02em; font-weight:400 !important; }
        h1 { font-size:3.15rem !important; margin-bottom:.25rem !important; }
        p,li,label,.stMarkdown { color:var(--ink); font-family:'Manrope',sans-serif; line-height:1.62; }
        .stCaption, [data-testid="stCaptionContainer"] { color:var(--muted) !important; font-family:'Manrope',sans-serif !important; font-size:.82rem !important; letter-spacing:.01em; }
        [data-testid="stTextInput"] label, [data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label, [data-testid="stSlider"] label, [data-testid="stRadio"] label { font-weight:700 !important; letter-spacing:.01em; }
        input,textarea,button,[data-baseweb="select"],[data-testid="stMetricValue"],[data-testid="stMetricLabel"] { font-family:'Manrope',sans-serif !important; }
        .subtitle { color:var(--muted); font-size:1.08rem; font-weight:600; letter-spacing:.01em; margin-top:-6px; margin-bottom:24px; }
        .hero { position:relative; overflow:hidden; display:flex; align-items:center; justify-content:space-between; min-height:190px; padding:28px 34px; margin:0 0 24px; border:1px solid rgba(185,43,43,.18); border-radius:24px; background:linear-gradient(120deg,#fff0d1,#e2f3f7); box-shadow:0 18px 45px rgba(48,77,91,.14); }
        .hero:after { content:''; position:absolute; width:380px; height:380px; right:-110px; top:-120px; border:1px solid rgba(247,189,84,.14); border-radius:50%; box-shadow:0 0 0 26px rgba(247,189,84,.03),0 0 0 52px rgba(247,189,84,.03); }
        .hero-copy { position:relative; z-index:2; max-width:650px; }
        .brand-lockup { display:flex; align-items:center; gap:10px; color:var(--red); font-family:'Bebas Neue',sans-serif; font-size:1.2rem; letter-spacing:.12em; }
        .brand-rule { width:78px; height:2px; margin:9px 0 12px; background:linear-gradient(90deg,var(--gold),transparent); }
        .ui-icon { flex:0 0 auto; }
        .section-heading { display:flex; align-items:center; gap:13px; margin:6px 0 18px; }
        .section-heading h2 { margin:0 !important; font-size:2.15rem !important; letter-spacing:.03em; }
        .section-heading .ui-icon { width:34px; height:34px; padding:7px; border:1px solid rgba(247,189,84,.3); border-radius:10px; background:rgba(247,189,84,.08); }
        .portrait-image { display:block; width:100%; aspect-ratio:1.52; object-fit:cover; border-radius:12px; margin-bottom:13px; border:1px solid rgba(247,189,84,.22); }
        .eyebrow { color:var(--gold); font-size:.75rem; font-weight:700; letter-spacing:.18em; text-transform:uppercase; margin-bottom:10px; }
        .hero-title { font-family:'DM Serif Display',serif; color:var(--ink); font-size:2.45rem; letter-spacing:-.02em; line-height:1.05; margin-bottom:10px; }
        .hero-note { color:var(--muted); max-width:560px; line-height:1.55; }
        .hero-svg { position:relative; z-index:1; width:230px; height:160px; opacity:.96; }
        .menu-label { color:var(--red); font-size:.72rem; font-weight:800; letter-spacing:.18em; text-transform:uppercase; margin:18px 0 10px; }
        .menu-caption { color:var(--muted); font-size:.84rem; line-height:1.55; margin-bottom:14px; }
        .sidebar-brand { display:flex; align-items:center; gap:10px; padding:13px 14px; border-radius:15px; background:linear-gradient(135deg,#b92b2b,#7f1d27); color:#fffdf7; box-shadow:0 8px 18px rgba(185,43,43,.18); }
        .sidebar-brand strong { font-family:'DM Serif Display',serif; font-size:1.22rem; letter-spacing:.01em; font-weight:400; }
        .sidebar-brand small { display:block; opacity:.78; font-family:'Manrope',sans-serif; font-size:.7rem; letter-spacing:.04em; }
        .sidebar-status { padding:9px 12px; margin:12px 0 14px; border-left:3px solid var(--gold); border-radius:8px; background:rgba(255,212,71,.13); color:var(--ink); font-size:.78rem; font-weight:700; }
        [data-testid="stSidebar"] [role="radiogroup"] { gap:4px; }
        [data-testid="stSidebar"] [role="radiogroup"] label { border:1px solid transparent; border-radius:12px; padding:10px 12px; margin:2px 0; background:rgba(255,255,255,.46); transition:all .2s ease; font-size:.9rem; font-weight:700; }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover { background:#fff4dc; border-color:rgba(185,43,43,.22); transform:translateX(2px); }
        [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] { background:linear-gradient(90deg,#b92b2b,#8d2029); color:#fffdf7 !important; border-color:#d99f00; box-shadow:0 5px 14px rgba(185,43,43,.2); }
        [data-testid="stSidebar"] [role="radiogroup"] label[data-checked="true"] p { color:#fffdf7 !important; }
        .icon-rail { display:flex; gap:10px; flex-wrap:wrap; margin:0 0 22px; }
        .icon-chip { display:flex; align-items:center; gap:8px; padding:8px 12px; border:1px solid rgba(185,43,43,.14); border-radius:999px; background:rgba(255,255,255,.72); color:var(--muted); font-size:.82rem; }
        .icon-chip svg { width:18px; height:18px; stroke:var(--gold); fill:none; stroke-width:1.8; }
        .card { background:linear-gradient(145deg,#ffffff,#fff8eb); border:1px solid var(--line); border-radius:18px; padding:19px; min-height:122px; box-shadow:0 10px 28px rgba(48,77,91,.11); transition:transform .2s ease,border-color .2s ease; }
        .card:hover,.fruit-card:hover { transform:translateY(-3px); border-color:rgba(247,189,84,.55); }
        .card h4 { color:var(--gold) !important; font-size:.78rem; letter-spacing:.12em; text-transform:uppercase; margin:0 0 12px; }
        .value { color:var(--ink); font-size:1.18rem; font-weight:700; line-height:1.35; }
        .story { background:linear-gradient(110deg,#ffffff,#fff7e8); border:1px solid var(--line); border-left:4px solid var(--red); border-radius:16px; padding:17px 22px; margin-top:20px; box-shadow:0 8px 24px rgba(48,77,91,.09); }
        .story h3 { font-size:1.05rem; margin-top:0; }
        .fruit-card { background:linear-gradient(145deg,#ffffff,#f4fafb); border:1px solid var(--line); border-radius:18px; padding:18px; min-height:205px; height:100%; box-shadow:0 10px 28px rgba(48,77,91,.11); transition:transform .2s ease,border-color .2s ease; }
        .fruit-detail { margin-top:14px; padding-top:13px; border-top:1px solid var(--line); }
        .detail-label { color:var(--muted); font-size:.7rem; font-weight:800; letter-spacing:.11em; text-transform:uppercase; }
        .detail-text { font-size:.84rem; line-height:1.45; margin:4px 0 10px; }
        .stat-strip { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin:10px 0 4px; }
        .stat-box { background:#fff4dc; border-radius:9px; padding:7px 5px; text-align:center; }
        .stat-box strong { display:block; color:var(--red); font-size:.9rem; }
        .stat-box span { color:var(--muted); font-size:.62rem; text-transform:uppercase; letter-spacing:.05em; }
        .faction-card { display:flex; align-items:center; gap:12px; padding:14px; border:2px solid var(--faction-accent); border-radius:16px; background:#fffdf7; box-shadow:0 8px 22px rgba(48,77,91,.1); }
        .faction-card svg { width:78px; height:62px; flex:0 0 auto; }
        .faction-title { color:var(--ink); font-family:'DM Serif Display',serif; font-size:1.35rem; }
        .battle-result { padding:18px; border-radius:16px; border:1px solid var(--line); background:linear-gradient(135deg,#fff4dc,#e2f3f7); text-align:center; }
        .battle-result strong { display:block; color:var(--red); font-family:'DM Serif Display',serif; font-size:2rem; }
        .reward-row { display:flex; align-items:center; justify-content:space-between; gap:12px; padding:11px 0; border-bottom:1px solid var(--line); }
        .reward-row:last-child { border-bottom:0; }
        .crew-stat-card { padding:14px; border:1px solid var(--line); border-radius:14px; background:#fffdf7; }
        .crew-stat-card h4 { margin:0 0 3px; font-size:1.15rem; }
        .encyclopedia-toolbar { padding:16px; border:1px solid var(--line); border-radius:16px; background:rgba(255,255,255,.72); margin-bottom:16px; }
        .insight-card { padding:16px; border-radius:14px; background:linear-gradient(135deg,#fff4dc,#e2f3f7); border:1px solid var(--line); text-align:center; }
        .insight-card strong { display:block; color:var(--red); font-family:'DM Serif Display',serif; font-size:1.65rem; }
        .insight-card span { color:var(--muted); font-size:.72rem; font-weight:800; letter-spacing:.09em; text-transform:uppercase; }
        .compare-card { padding:15px; border:1px solid rgba(185,43,43,.18); border-top:4px solid var(--red); border-radius:14px; background:#fffdf7; height:100%; }
        .character-card { min-height:0; height:auto; }
        .fruit-name { color:var(--ink); font-family:'Space Grotesk',sans-serif; font-size:1.08rem; font-weight:700; line-height:1.25; }
    .fruit-type { display:inline-flex; align-items:center; gap:5px; color:#14283d; background:#e5b544; border-radius:999px; font-size:.72rem; font-weight:800; letter-spacing:.06em; margin:10px 0; padding:4px 9px 4px 6px; text-transform:uppercase; }
        .fruit-type .ui-icon { width:18px; height:18px; stroke:#243447; }
        .muted { color:var(--muted); font-size:.9rem; }
        .role-label { margin:5px 0 14px; }
        .bounty-line { display:flex; justify-content:space-between; align-items:center; gap:8px; padding-top:11px; border-top:1px solid rgba(247,189,84,.14); font-size:.78rem; color:var(--muted); }
        .bounty-line strong { color:var(--gold); font-size:.82rem; text-align:right; }
        .section-kicker { color:var(--gold); font-size:.76rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }
        .stButton > button { border:1px solid var(--gold); border-radius:10px; background:linear-gradient(135deg,var(--gold),#df861c); color:#24100e; font-weight:700; }
        .stProgress > div > div > div > div { background:linear-gradient(90deg,var(--red),var(--gold)); }
        [data-testid="stMetric"] { background:rgba(255,255,255,.78); border:1px solid var(--line); padding:14px; border-radius:14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Final responsive shell. This deliberately comes after the component styles so
# every page receives the same alignment, type scale, motion, and sidebar rules.
st.markdown(
    """
    <style>
    html { font-size: 15.5px; }
    body, .stApp, p, li, label, input, textarea, button,
    [data-testid="stMarkdownContainer"] {
        font-family: 'Plus Jakarta Sans', 'Manrope', system-ui, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }
    h1, h2, h3, h4, .hero-title, .section-heading h2, .fruit-name,
    .faction-title, .sidebar-brand strong {
        font-family: 'Bricolage Grotesque', 'Space Grotesk', system-ui, sans-serif !important;
        font-weight: 700 !important;
        letter-spacing: -.035em !important;
    }
    p, li, .stMarkdown { font-size: .92rem; line-height: 1.65; }
    h1 { font-size: clamp(2.15rem, 3.2vw, 3.25rem) !important; line-height: 1.05 !important; }
    h2 { font-size: clamp(1.7rem, 2.4vw, 2.4rem) !important; line-height: 1.1 !important; }
    h3 { font-size: clamp(1.2rem, 1.7vw, 1.55rem) !important; line-height: 1.2 !important; }

    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stMain"] { width: 100% !important; }
    .block-container {
        width: calc(100% - 64px) !important;
        max-width: 1400px !important;
        margin: 0 auto !important;
        padding: 1.75rem 0 4.5rem !important;
    }
    [data-testid="stVerticalBlock"] { gap: 1rem !important; }
    [data-testid="stHorizontalBlock"] {
        width: 100% !important;
        gap: 1rem !important;
        align-items: stretch !important;
    }
    [data-testid="stColumn"] {
        min-width: 0 !important;
        padding: 0 !important;
    }

    [data-testid="stHeader"] {
        display: block !important;
        height: 3.5rem !important;
        background: rgba(255,248,231,.9) !important;
        backdrop-filter: blur(16px);
        border-bottom: 1px solid rgba(20,40,61,.1);
    }
    [data-testid="stToolbar"] { display: flex !important; }
    [data-testid="stSidebar"] {
        width: 290px !important;
        min-width: 290px !important;
        background: linear-gradient(180deg,#0b3554 0%,#0e5870 58%,#0a405b 100%) !important;
        box-shadow: 18px 0 50px rgba(11,53,84,.13);
    }
    [data-testid="stSidebar"] > div:first-child { padding: 1.5rem 1.1rem 2rem !important; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .menu-caption { color: #fff8e7 !important; }
    [data-testid="stSidebar"] .menu-label { color: #e5b544 !important; }
    [data-testid="stSidebarCollapsedControl"] {
        display: flex !important;
        top: .4rem !important;
        left: .55rem !important;
        z-index: 1000000 !important;
    }
    [data-testid="stSidebarCollapseButton"] { display: flex !important; }
    [data-testid="stSidebarCollapseButton"] {
        position: absolute !important;
        top: .65rem !important;
        right: .65rem !important;
        z-index: 1000001 !important;
    }
    [data-testid="stSidebarCollapseButton"] button {
        color: #fff8e7 !important;
        background: rgba(255,248,231,.12) !important;
        border: 1px solid rgba(229,181,68,.45) !important;
        border-radius: 9px !important;
    }
    [data-testid="stSidebar"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapseButton"] { display: none !important; }

    .brand-lockup { justify-content: center; margin-top: .35rem; font-size: .86rem; }
    .brand-rule { margin: .75rem auto 1rem; }
    .subtitle { max-width: 820px; margin: 0 auto 1.75rem; text-align: center; font-size: .96rem; }
    .st-key-main_navigation {
        max-width: 1400px !important;
        margin: 0 auto 1.6rem !important;
        border: 1px solid rgba(20,40,61,.14) !important;
        border-radius: 16px !important;
        box-shadow: 0 12px 34px rgba(11,53,84,.08);
    }
    .st-key-main_navigation [role="radiogroup"] {
        display: grid !important;
        grid-template-columns: repeat(8, minmax(0, 1fr)) !important;
        width: 100% !important;
    }
    .st-key-main_navigation > label,
    .st-key-main_navigation > div:first-child > label { display: none !important; }
    .st-key-main_navigation label { min-height: 50px !important; padding: 10px 7px !important; }
    .st-key-main_navigation label p {
        font-size: .7rem !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
    }

    .hero {
        width: 100%;
        min-height: 220px;
        padding: clamp(1.5rem, 2.2vw, 2.25rem);
        margin: 0 auto 1.35rem;
    }
    .hero-copy { max-width: 680px !important; }
    .hero-title { font-size: clamp(2rem, 3vw, 2.9rem) !important; line-height: 1.04 !important; }
    .hero-note { font-size: .96rem; }
    .section-heading { margin: 1.1rem 0 1.3rem; }
    .section-heading h2 { font-size: clamp(1.75rem, 2.5vw, 2.5rem) !important; }
    .card, .fruit-card, .compare-card, .crew-stat-card,
    .story, .faction-card, .battle-result, .encyclopedia-toolbar,
    .insight-card, [data-testid="stMetric"], [data-testid="stExpander"] {
        border-radius: 18px !important;
    }
    .card, .fruit-card, .compare-card { padding: 1.25rem !important; }
    .card { min-height: 150px; }
    .value { font-size: 1.3rem; }
    [data-testid="stMetricValue"] { font-size: 1.75rem !important; }
    .stButton > button { min-height: 46px; font-size: .88rem; }

    @keyframes pageEnter {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes cardEnter {
        from { opacity: 0; transform: translateY(16px) scale(.99); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    .block-container > div { animation: pageEnter .45s ease-out both; }
    .card, .fruit-card, .story, .faction-card, .battle-result,
    .crew-stat-card, .insight-card, .compare-card, [data-testid="stMetric"] {
        animation: cardEnter .42s ease-out both;
        transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease !important;
    }
    .card:hover, .fruit-card:hover, .compare-card:hover, .crew-stat-card:hover {
        transform: translateY(-4px) !important;
        box-shadow: 0 18px 42px rgba(11,53,84,.14) !important;
    }
    @media (prefers-reduced-motion: reduce) {
        *, *::before, *::after { animation: none !important; transition: none !important; }
    }
    @media (max-width: 1100px) {
        .block-container { width: calc(100% - 40px) !important; }
        .st-key-main_navigation [role="radiogroup"] { grid-template-columns: repeat(4, minmax(0, 1fr)) !important; }
    }
    @media (max-width: 760px) {
        html { font-size: 15px; }
        .block-container { width: calc(100% - 28px) !important; padding: 1.35rem 0 3.5rem !important; }
        .st-key-main_navigation [role="radiogroup"] { grid-template-columns: repeat(2, minmax(0, 1fr)) !important; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] { flex: 1 1 100% !important; min-width: 100% !important; }
        .hero { min-height: 0; padding: 2rem 1.5rem; border-radius: 18px; }
        .hero-title { font-size: clamp(1.9rem, 9vw, 2.5rem) !important; }
        .hero-svg { display: none; }
        .brand-lockup, .subtitle { text-align: center; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =============================================================================
# Read-Only Catalog Caching via Backend API (Fallback to local constants)
# =============================================================================
@st.cache_data(show_spinner=False)
def load_arcs():
    try:
        return api_client.get_arcs()
    except APIError:
        return None

@st.cache_data(show_spinner=False)
def load_characters():
    try:
        return api_client.get_characters()
    except APIError:
        return None

@st.cache_data(show_spinner=False)
def load_devil_fruits():
    try:
        return api_client.get_devil_fruits()
    except APIError:
        return None

@st.cache_data(show_spinner=False)
def load_devil_fruit_meta():
    try:
        return api_client.get_devil_fruit_types()
    except APIError:
        return None

@st.cache_data(show_spinner=False)
def load_crew_members():
    try:
        return api_client.get_crew_members()
    except APIError:
        return None

@st.cache_data(show_spinner=False)
def load_quiz_questions():
    try:
        return api_client.get_quiz_questions()
    except APIError:
        return None

@st.cache_data(show_spinner=False)
def load_bounty_rewards():
    try:
        return api_client.get_bounty_rewards()
    except APIError:
        return None

@st.cache_data(show_spinner=False)
def load_factions():
    try:
        return api_client.get_factions()
    except APIError:
        return None

# Local fallbacks if backend is unreachable on initial render
FALLBACK_ARC_DATA: dict[str, dict[str, Any]] = {
    "East Blue": {"episode_range":"Episodes 1–61", "location":"East Blue", "antagonists":"Alvida, Buggy, Arlong, Don Krieg, Kuro", "highlights":["Luffy begins his journey to become the Pirate King.", "The first core Straw Hat members join the adventure.", "The crew defeats Arlong and liberates Nami's village."], "joined":"Zoro, Nami, Usopp, and Sanji"},
    "Alabasta": {"episode_range":"Episodes 62–130", "location":"Arabasta Kingdom", "antagonists":"Crocodile and Baroque Works", "highlights":["The Straw Hats help Princess Vivi stop a civil war.", "Luffy defeats Crocodile.", "Chopper joins the Straw Hat Pirates."], "joined":"Tony Tony Chopper"},
    "Water 7 / Enies Lobby": {"episode_range":"Episodes 229–325", "location":"Water 7 and Enies Lobby", "antagonists":"Rob Lucci, CP9, and the World Government", "highlights":["Robin's tragic past is revealed.", "The Straw Hats declare war on the World Government.", "The Thousand Sunny becomes the crew's new ship."], "joined":"Franky"},
    "Marineford": {"episode_range":"Episodes 457–489", "location":"Marineford", "antagonists":"The Marines and World Government", "highlights":["Luffy and allies attempt to rescue Ace.", "The Whitebeard Pirates clash with the Marines.", "The balance of power in the New World changes."], "joined":"No new permanent Straw Hat member"},
    "Dressrosa": {"episode_range":"Episodes 629–746", "location":"Dressrosa", "antagonists":"Donquixote Doflamingo and his crew", "highlights":["The Straw Hats challenge Doflamingo's control.", "Luffy unveils Gear Fourth.", "The Grand Fleet is formed."], "joined":"No new permanent Straw Hat member"},
    "Wano Country": {"episode_range":"Episodes 890–1085", "location":"Wano Country", "antagonists":"Kaido, Big Mom, and the Beast Pirates", "highlights":["The Alliance rises against Kaido.", "Luffy awakens Gear Fifth.", "Wano is liberated."], "joined":"No new permanent Straw Hat member"},
    "Egghead": {"episode_range":"Episodes 1086–present", "location":"Egghead Island", "antagonists":"The Five Elders, CP0, and the World Government", "highlights":["The crew arrives at Vegapunk's futuristic island.", "Secrets about the Void Century are revealed.", "The Final Saga begins in earnest."], "joined":"No new permanent Straw Hat member"},
}

FALLBACK_CHARACTERS = {
    "Monkey D. Luffy": {"bounty": 3_000_000_000, "role": "Captain", "color": "#e76f51"},
    "Roronoa Zoro": {"bounty": 1_111_000_000, "role": "Swordsman", "color": "#6a994e"},
    "Nami": {"bounty": 366_000_000, "role": "Navigator", "color": "#f4a261"},
    "Usopp": {"bounty": 500_000_000, "role": "Sniper", "color": "#e9c46a"},
    "Vinsmoke Sanji": {"bounty": 1_032_000_000, "role": "Cook", "color": "#457b9d"},
    "Tony Tony Chopper": {"bounty": 1_000, "role": "Doctor", "color": "#e63946"},
    "Nico Robin": {"bounty": 930_000_000, "role": "Archaeologist", "color": "#8d5a97"},
    "Franky": {"bounty": 394_000_000, "role": "Shipwright", "color": "#277da1"},
    "Brook": {"bounty": 383_000_000, "role": "Musician", "color": "#577590"},
    "Jinbe": {"bounty": 1_100_000_000, "role": "Helmsman", "color": "#264653"},
    "Shanks": {"bounty": 4_048_900_000, "role": "Emperor", "color": "#9b2226"},
    "Kaido": {"bounty": 4_611_100_000, "role": "Emperor", "color": "#6d597a"},
}

FALLBACK_DEVIL_FRUITS: list[dict[str, str]] = [
    {"name":"Gomu Gomu no Mi", "type":"Paramecia", "user":"Monkey D. Luffy", "ability":"Grants the body rubber-like properties; later revealed to be the Mythical Zoan Hito Hito no Mi, Model: Nika."},
    {"name":"Mera Mera no Mi", "type":"Logia", "user":"Portgas D. Ace / Sabo", "ability":"Creates, controls, and transforms the user into fire."},
    {"name":"Hito Hito no Mi, Model: Nika", "type":"Mythical Zoan", "user":"Monkey D. Luffy", "ability":"Gives the user extraordinary freedom and rubber-like combat abilities as the Sun God Nika."},
    {"name":"Yami Yami no Mi", "type":"Logia", "user":"Marshall D. Teach", "ability":"Creates darkness and can nullify the powers of other Devil Fruits through contact."},
    {"name":"Gura Gura no Mi", "type":"Paramecia", "user":"Edward Newgate / Marshall D. Teach", "ability":"Produces powerful vibrations capable of generating earthquakes and tsunamis."},
    {"name":"Ope Ope no Mi", "type":"Paramecia", "user":"Trafalgar D. Water Law", "ability":"Creates a ROOM in which the user can manipulate objects, bodies, and spatial positions."},
    {"name":"Uo Uo no Mi, Model: Seiryu", "type":"Mythical Zoan", "user":"Kaido", "ability":"Transforms the user into an eastern dragon with weather and flame-based abilities."},
    {"name":"Tori Tori no Mi, Model: Phoenix", "type":"Mythical Zoan", "user":"Marco", "ability":"Transforms the user into a phoenix and grants regenerative blue flames."},
    {"name":"Suna Suna no Mi", "type":"Logia", "user":"Crocodile", "ability":"Creates, controls, and transforms the user into sand, including the ability to drain moisture."},
    {"name":"Nikyu Nikyu no Mi", "type":"Paramecia", "user":"Bartholomew Kuma", "ability":"Repels virtually anything, including physical attacks, air, and even pain."},
    {"name":"Bara Bara no Mi", "type":"Paramecia", "user":"Buggy", "ability":"Allows the user to split their body into floating pieces and become immune to cutting attacks."},
    {"name":"Neko Neko no Mi, Model: Leopard", "type":"Zoan", "user":"Rob Lucci", "ability":"Transforms the user into a leopard or human-leopard hybrid, greatly increasing physical power."},
]

FALLBACK_DEVIL_FRUIT_TYPE_GUIDE = {
    "Paramecia": "Grants unusual superhuman abilities that alter the user's body, environment, or physical interaction.",
    "Zoan": "Allows transformation into an animal or animal-human hybrid, usually improving strength, speed, and recovery.",
    "Mythical Zoan": "A rare Zoan class based on legendary creatures and often accompanied by supernatural abilities.",
    "Logia": "Allows the user to create, control, and become a natural element or force of nature.",
}

FALLBACK_DEVIL_FRUIT_AWAKENINGS = {
    "Gomu Gomu no Mi": "Awakened as the Hito Hito no Mi, Model: Nika; Luffy can affect his surroundings with rubber-like freedom.",
    "Hito Hito no Mi, Model: Nika": "Awakening is represented by Gear Fifth and the user’s transformation into the legendary Sun God Nika.",
    "Ope Ope no Mi": "Awakening enables K-ROOM and R-ROOM, extending spatial manipulation to objects and targets outside the user's body.",
    "Uo Uo no Mi, Model: Seiryu": "No confirmed awakening has been shown; Kaido's advanced dragon abilities remain distinct from a confirmed awakening.",
    "Yami Yami no Mi": "No confirmed awakening has been shown.",
}

FALLBACK_DEVIL_FRUIT_DETAILS = {
    "Gomu Gomu no Mi": {"profile":"Monkey D. Luffy · Captain · 3,000,000,000 Berries", "strength":"Extreme", "control":"Advanced", "danger":"Yonko", "weakness":"Standard Devil Fruit water and seastone weaknesses; blunt force is less effective than cutting or piercing attacks."},
    "Mera Mera no Mi": {"profile":"Portgas D. Ace / Sabo · Fire Fist users", "strength":"Extreme", "control":"Advanced", "danger":"High", "weakness":"Elemental counters and stronger Haki can overcome its Logia intangibility; water suppresses flames."},
    "Hito Hito no Mi, Model: Nika": {"profile":"Monkey D. Luffy · Gear Fifth user", "strength":"Legendary", "control":"Awakened", "danger":"Mythic", "weakness":"Consumes enormous stamina and still carries standard Devil Fruit and Haki limitations."},
    "Yami Yami no Mi": {"profile":"Marshall D. Teach · Blackbeard Pirates", "strength":"Extreme", "control":"Advanced", "danger":"Yonko", "weakness":"The user cannot phase through attacks and receives amplified pain; contact is needed to nullify powers."},
    "Gura Gura no Mi": {"profile":"Edward Newgate / Marshall D. Teach · Emperors", "strength":"Legendary", "control":"Advanced", "danger":"World-level", "weakness":"Collateral damage is difficult to control; normal Devil Fruit and Haki counters still apply."},
    "Ope Ope no Mi": {"profile":"Trafalgar D. Water Law · Surgeon of Death", "strength":"Extreme", "control":"Expert", "danger":"Very high", "weakness":"Techniques consume stamina and require a ROOM; strong Haki can resist some internal operations."},
    "Uo Uo no Mi, Model: Seiryu": {"profile":"Kaido · Former Emperor of the Sea", "strength":"Legendary", "control":"Awakened-like mastery", "danger":"Yonko", "weakness":"Large form is easier to target; seastone, Haki, and coordinated attacks remain effective."},
    "Tori Tori no Mi, Model: Phoenix": {"profile":"Marco · Former Whitebeard commander", "strength":"Extreme", "control":"Advanced", "danger":"High", "weakness":"Regeneration consumes stamina and does not make the user invincible."},
    "Suna Suna no Mi": {"profile":"Crocodile · Former Warlord", "strength":"High", "control":"Advanced", "danger":"High", "weakness":"Water and liquids can solidify the sand body and reduce Logia evasion."},
}

FALLBACK_CREW_MEMBERS = {
    "Monkey D. Luffy": "Captain",
    "Roronoa Zoro": "Swordsman",
    "Nami": "Navigator",
    "Usopp": "Sniper",
    "Vinsmoke Sanji": "Cook",
    "Tony Tony Chopper": "Doctor",
    "Nico Robin": "Archaeologist",
    "Franky": "Shipwright",
    "Brook": "Musician",
    "Jinbe": "Helmsman",
}

FALLBACK_QUIZ_QUESTIONS = [
    {"id": 1, "question": "Who is known as the Straw Hat captain?", "options": ["Roronoa Zoro", "Monkey D. Luffy", "Trafalgar Law", "Usopp"]},
    {"id": 2, "question": "Which Devil Fruit is associated with fire?", "options": ["Mera Mera no Mi", "Suna Suna no Mi", "Gura Gura no Mi", "Ope Ope no Mi"]},
    {"id": 3, "question": "Who ruled Wano as one of its major antagonists?", "options": ["Crocodile", "Doflamingo", "Kaido", "Arlong"]},
    {"id": 4, "question": "What is the name of the Straw Hats' ship after the Going Merry?", "options": ["Red Force", "Thousand Sunny", "Oro Jackson", "Moby Dick"]},
    {"id": 5, "question": "Which character is famous for using three-sword style?", "options": ["Sanji", "Franky", "Brook", "Roronoa Zoro"]},
    {"id": 6, "question": "Who is the Straw Hat crew's navigator?", "options": ["Nami", "Robin", "Vivi", "Perona"]},
    {"id": 7, "question": "What is the name of Luffy's signature technique category?", "options": ["Gomu Gomu", "Diable Jambe", "Asura", "Room"]},
    {"id": 8, "question": "Which arc features the rescue of Nico Robin at Enies Lobby?", "options": ["Dressrosa", "Water 7 / Enies Lobby", "Egghead", "Alabasta"]},
    {"id": 9, "question": "Who is the Straw Hat crew's doctor?", "options": ["Brook", "Franky", "Tony Tony Chopper", "Jinbe"]},
    {"id": 10, "question": "Which class can transform the user into a natural element?", "options": ["Paramecia", "Zoan", "Logia", "Mythical Zoan"]},
]

FALLBACK_BOUNTY_REWARDS = [
    {"achievement": "Complete an East Blue arc", "reward": 30_000_000},
    {"achievement": "Defeat a Warlord-level opponent", "reward": 150_000_000},
    {"achievement": "Survive a Marineford-scale war", "reward": 300_000_000},
    {"achievement": "Defeat a Yonko commander", "reward": 500_000_000},
    {"achievement": "Liberate a country from a Yonko", "reward": 1_000_000_000},
]

FALLBACK_FACTION_UNITS = {
    "Pirates": [
        {"name": "Straw Hat Captain", "power": 96, "defense": 82, "speed": 94, "special": "Gear Fifth"},
        {"name": "Three-Sword Swordsman", "power": 91, "defense": 88, "speed": 83, "special": "King of Hell"},
        {"name": "Soul King Musician", "power": 76, "defense": 69, "speed": 86, "special": "Soul Solid"},
        {"name": "Helmsman of the Sea", "power": 87, "defense": 93, "speed": 72, "special": "Fish-Man Karate"},
    ],
    "Marines": [
        {"name": "Fleet Admiral", "power": 95, "defense": 91, "speed": 76, "special": "Magma Fist"},
        {"name": "Admiral of Light", "power": 92, "defense": 79, "speed": 99, "special": "Light-Speed Kick"},
        {"name": "Vice Admiral", "power": 80, "defense": 84, "speed": 75, "special": "Haki Barrage"},
        {"name": "Marine Strategist", "power": 73, "defense": 78, "speed": 82, "special": "Tactical Net"},
    ],
}

FACTION_SVG = {
    "Pirates": '<path d="M30 67c18-20 72-20 90 0" fill="none" stroke="#b92b2b" stroke-width="7"/><circle cx="75" cy="47" r="24" fill="#fffdf7" stroke="#243447" stroke-width="4"/><circle cx="66" cy="46" r="5" fill="#243447"/><circle cx="84" cy="46" r="5" fill="#243447"/><path d="M64 58c7 6 15 6 22 0" fill="none" stroke="#243447" stroke-width="3"/><path d="M75 14v15M48 24l27-10 27 10" fill="none" stroke="#b92b2b" stroke-width="5"/>',
    "Marines": '<path d="M75 12 96 25v26c0 20-12 31-21 37-9-6-21-17-21-37V25Z" fill="#fffdf7" stroke="#243447" stroke-width="4"/><path d="m64 48 8 8 15-17" fill="none" stroke="#b92b2b" stroke-width="6" stroke-linecap="round"/><path d="M40 22h70" stroke="#e3a900" stroke-width="5"/>',
}

# Resolve active catalog data (cached from backend or fallback)
ARC_DATA = load_arcs() or FALLBACK_ARC_DATA
CHARACTERS = load_characters() or FALLBACK_CHARACTERS
DEVIL_FRUITS = load_devil_fruits() or FALLBACK_DEVIL_FRUITS

_meta = load_devil_fruit_meta() or {}
DEVIL_FRUIT_TYPE_GUIDE = _meta.get("types", FALLBACK_DEVIL_FRUIT_TYPE_GUIDE)
DEVIL_FRUIT_AWAKENINGS = _meta.get("awakenings", FALLBACK_DEVIL_FRUIT_AWAKENINGS)
DEVIL_FRUIT_DETAILS = _meta.get("details", FALLBACK_DEVIL_FRUIT_DETAILS)

CREW_MEMBERS = load_crew_members() or FALLBACK_CREW_MEMBERS
QUIZ_QUESTIONS = load_quiz_questions() or FALLBACK_QUIZ_QUESTIONS
BOUNTY_REWARDS = load_bounty_rewards() or FALLBACK_BOUNTY_REWARDS
FACTION_UNITS = load_factions() or FALLBACK_FACTION_UNITS


def character_svg_data_uri(name: str, role: str, color: str) -> str:
    """Create a lightweight, always-loading illustrated SVG character portrait."""
    if "Luffy" in name:
        hair = '<path d="M255 145 Q270 70 320 92 Q370 70 385 145 Q350 118 320 130 Q290 118 255 145Z" fill="#5b2b1e"/><path d="M270 112 Q320 64 370 112" fill="none" stroke="#3d1e18" stroke-width="18"/>'
        accessory = '<path d="M245 92 Q320 52 395 92 L380 108 Q320 82 260 108Z" fill="#c92d2d" stroke="#ffd447" stroke-width="5"/>'
        outfit = '<path d="M255 267 Q320 235 385 267 L420 350 H220Z" fill="#c92d2d"/><path d="M282 275 L320 315 358 275" fill="#fff7e6"/>'
    elif "Zoro" in name:
        hair = '<path d="M252 148 Q260 72 320 70 Q380 72 388 148 L360 130 340 96 320 130 292 96 275 140Z" fill="#4d7134"/>'
        accessory = '<path d="M368 185 L430 115" stroke="#e3a900" stroke-width="8"/><path d="M420 105 l18 12-12 18" fill="none" stroke="#c92d2d" stroke-width="5"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#263b45"/><path d="M315 276h10v66h-10z" fill="#e3a900"/>'
    elif "Nami" in name:
        hair = '<path d="M250 165 Q255 75 320 78 Q385 75 390 165 L370 145 Q350 112 320 122 Q285 110 268 145Z" fill="#e3a83a"/><path d="M263 130 Q225 220 270 247" fill="none" stroke="#e3a83a" stroke-width="24"/>'
        accessory = '<circle cx="379" cy="132" r="12" fill="#f7bd54" stroke="#c92d2d" stroke-width="5"/>'
        outfit = '<path d="M255 267 Q320 235 385 267 L420 350 H220Z" fill="#3e9bb0"/><path d="M278 274h84" stroke="#fff7e6" stroke-width="10"/>'
    elif "Sanji" in name:
        hair = '<path d="M252 148 Q270 75 340 86 Q382 95 390 150 L357 122 Q332 100 300 120 L270 160Z" fill="#d4a02c"/>'
        accessory = '<path d="M365 106 Q390 135 360 166" fill="none" stroke="#3d241d" stroke-width="12" stroke-linecap="round"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#283845"/><path d="M320 270v78" stroke="#f7bd54" stroke-width="4"/>'
    elif "Chopper" in name:
        hair = '<path d="M255 147 Q270 95 320 95 Q370 95 385 147Z" fill="#8b5e3c"/><path d="M269 115 L238 75 283 94 M371 115 L402 75 357 94" fill="#8b5e3c" stroke="#fff7e6" stroke-width="5"/>'
        accessory = '<path d="M250 118 Q320 84 390 118" fill="none" stroke="#c92d2d" stroke-width="12"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#c92d2d"/><path d="M280 280h80v58h-80z" fill="#fff7e6"/>'
    elif "Robin" in name:
        hair = '<path d="M245 166 Q250 65 320 75 Q390 65 395 166 L370 130 Q320 106 270 130Z" fill="#211d2d"/><path d="M264 130 Q230 205 270 245" fill="none" stroke="#211d2d" stroke-width="26"/>'
        accessory = '<circle cx="373" cy="142" r="8" fill="#e66f2e"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#8d4a69"/><path d="M280 277h80" stroke="#fff7e6" stroke-width="5"/>'
    elif "Franky" in name:
        hair = '<path d="M255 135 Q320 52 385 135 L360 148 320 95 280 148Z" fill="#4d9ab3"/><path d="M278 164h84" stroke="#8e5a3c" stroke-width="14"/>'
        accessory = '<path d="M270 170h34M336 170h34" stroke="#e3a900" stroke-width="8"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#274c77"/><path d="M270 292h100" stroke="#e3a900" stroke-width="9"/>'
    elif "Brook" in name:
        hair = '<path d="M250 150 Q270 66 320 76 Q370 66 390 150Z" fill="#16151a"/>'
        accessory = '<circle cx="320" cy="178" r="74" fill="#fff7e6" stroke="#243447" stroke-width="5"/><circle cx="292" cy="170" r="12" fill="#243447"/><circle cx="348" cy="170" r="12" fill="#243447"/><path d="M280 215 Q320 250 360 215" fill="none" stroke="#243447" stroke-width="8"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#17151b"/><path d="M320 270v78" stroke="#e3a900" stroke-width="5"/>'
    elif "Jinbe" in name:
        hair = '<path d="M240 150 Q250 60 320 68 Q390 60 400 150 L370 125 350 88 320 120 290 88 270 125Z" fill="#315c75"/>'
        accessory = '<path d="M257 182 Q320 140 383 182" fill="none" stroke="#315c75" stroke-width="18"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#e66f2e"/><path d="M270 290h100" stroke="#fff7e6" stroke-width="7"/>'
    elif "Shanks" in name:
        hair = '<path d="M245 152 Q260 60 320 78 Q380 60 395 152 L365 122 340 90 320 124 292 90 270 140Z" fill="#9d2b2b"/>'
        accessory = '<path d="M372 160 Q392 184 371 205" fill="none" stroke="#7f1d27" stroke-width="8"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#5b1f2b"/><path d="M270 278h100" stroke="#e3a900" stroke-width="5"/>'
    elif "Kaido" in name:
        hair = '<path d="M235 150 Q255 45 320 70 Q385 45 405 150 L370 118 350 70 320 110 290 70 270 118Z" fill="#1f2833"/>'
        accessory = '<path d="M260 112 L230 72 278 96 M380 112 L410 72 362 96" fill="#1f2833" stroke="#fff7e6" stroke-width="5"/>'
        outfit = '<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="#5d315f"/><path d="M270 288h100" stroke="#e3a900" stroke-width="8"/>'
    else:
        hair = '<path d="M250 150 Q260 76 320 78 Q380 76 390 150 L365 125 Q320 100 275 125Z" fill="#3d2b27"/>'
        accessory = '<circle cx="320" cy="86" r="7" fill="#ffd447"/>'
        outfit = f'<path d="M250 267 Q320 235 390 267 L420 350 H220Z" fill="{color}"/>'

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 420">
      <defs><linearGradient id="g" x1="0" x2="1" y1="0" y2="1"><stop stop-color="{color}"/><stop offset="1" stop-color="#243447"/></linearGradient></defs>
      <rect width="640" height="420" rx="28" fill="url(#g)"/>
      <path d="M0 330 Q130 270 250 330 T500 330 T760 330 V420 H0Z" fill="#243447" opacity=".42"/>
      <circle cx="320" cy="180" r="88" fill="#d8956a" stroke="#fff7e6" stroke-width="5"/>
      {hair}{accessory}
      <ellipse cx="289" cy="177" rx="8" ry="12" fill="#243447"/><ellipse cx="351" cy="177" rx="8" ry="12" fill="#243447"/>
      <path d="M300 222 Q320 238 340 222" fill="none" stroke="#7d352d" stroke-width="5" stroke-linecap="round"/>
      {outfit}
      <text x="32" y="48" font-family="DM Sans, sans-serif" font-size="16" letter-spacing="4" fill="#fff7e6">GRAND LINE // PORTRAIT</text>
      <text x="32" y="382" font-family="Space Grotesk, sans-serif" font-size="24" font-weight="700" fill="#fff7e6">{name}</text>
    </svg>'''
    encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


def svg_icon(icon_name: str, size: int = 24, color: str = "#e5b544") -> str:
    """Return a crisp inline SVG icon; avoids emoji rendering differences."""
    paths = {
        "compass": '<circle cx="12" cy="12" r="8"/><path d="m12 4 2.6 8-2.6 8-2.6-8L12 4Z"/>',
        "map": '<path d="m3 6 6-3 6 3 6-3v15l-6 3-6-3-6 3V6Z"/><path d="M9 3v15M15 6v15"/>',
        "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3 2"/>',
        "wanted": '<path d="M5 4h14v16H5z"/><circle cx="12" cy="10" r="2.5"/><path d="M8 17c1.5-2 6.5-2 8 0"/>',
        "fruit": '<path d="M12 7c-4-4-8 1-6 6 1 4 3 7 6 7s5-3 6-7c2-5-2-10-6-6Z"/><path d="M12 7c0-3 2-5 5-5-1 3-2 5-5 5Z"/>',
        "quiz": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 4 2c-1 .7-1.5 1.1-1.5 2.2M12 16.5h.01"/>',
        "bounty": '<path d="M7 4h10v16H7z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
        "crew": '<circle cx="9" cy="9" r="3"/><circle cx="17" cy="10" r="2.5"/><path d="M3.5 20c.5-4 10-4 11 0M14 20c.3-2.5 5.5-2.7 6.5 0"/>',
        "paramecia": '<circle cx="12" cy="12" r="7"/><path d="M12 5v14M5 12h14"/>',
        "zoan": '<path d="M12 3c-4 3-6 6-6 10a6 6 0 0 0 12 0c0-4-2-7-6-10Z"/><path d="M9 14h.01M15 14h.01M10 17c1 .8 3 .8 4 0"/>',
        "mythical": '<path d="M4 17c4-9 12-9 16 0"/><path d="M7 13 5 7l5 3 2-7 2 7 5-3-2 6"/>',
        "logia": '<path d="M12 3c3 4 6 6 6 10a6 6 0 0 1-12 0c0-4 3-6 6-10Z"/><path d="M12 11c1.5 2 2 3 2 4a2 2 0 1 1-4 0c0-1 .5-2 2-4Z"/>',
    }
    shape = paths.get(icon_name, paths["compass"])
    return f'<svg class="ui-icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{shape}</svg>'


def faction_card_svg(faction: str, accent: str) -> str:
    """Render a custom SVG faction emblem card without external images."""
    return f'''<div class="faction-card" style="--faction-accent:{accent};"><svg viewBox="0 0 150 105" role="img" aria-label="{faction} faction emblem">{FACTION_SVG[faction]}</svg><div><div class="faction-title">{faction}</div><div class="muted">Battle faction</div></div></div>'''


def format_bounty(bounty: int | None) -> str:
    return "Unknown" if bounty is None else f"{bounty:,} Berries"

# =============================================================================
# Team Member 2: Header and navigation
# =============================================================================
st.markdown(f'<div class="brand-lockup">{svg_icon("compass", 30)}<span>GRAND LINE NAVIGATOR</span></div>', unsafe_allow_html=True)
st.markdown('<div class="brand-rule"></div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore the seas, catch up on episodes, track legendary bounties, and study Devil Fruits.</p>', unsafe_allow_html=True)
PAGES = ["Arc Explorer", "Catch-Up Calculator", "Character Database", "Devil Fruit Encyclopedia", "Trivia Quiz", "Bounty Rewards", "Crew Management", "Faction Battle Simulator"]
active_page = st.radio(
    "Main navigation",
    PAGES,
    horizontal=True,
    label_visibility="collapsed",
    key="main_navigation",
)
st.markdown(
    '''
    <div class="hero">
      <div class="hero-copy">
        <div class="eyebrow">The New World </div>
        <div class="hero-title">Chart your route. Build your crew. Chase the legend.</div>
        <div class="hero-note">A focused command deck for arc discovery, episode planning, pirate reputations, Devil Fruit lore, and crew strategy.</div>
      </div>
      <svg class="hero-svg" viewBox="0 0 240 170" role="img" aria-label="Compass and ocean waves icon">
        <circle cx="150" cy="75" r="54" fill="none" stroke="#e5b544" stroke-width="2" opacity=".8"/>
        <circle cx="150" cy="75" r="43" fill="none" stroke="#e5b544" stroke-width="1" opacity=".38"/>
        <path d="M150 25 L162 75 L150 126 L138 75 Z" fill="#c64038" opacity=".92"/>
        <path d="M150 25 L162 75 L150 126 L138 75 Z" fill="none" stroke="#f8f3e8" stroke-width="2"/>
        <circle cx="150" cy="75" r="5" fill="#f8f3e8"/>
        <path d="M22 131 C43 113 62 148 84 130 C104 113 124 148 146 130 C166 113 186 148 218 126" fill="none" stroke="#48a9bd" stroke-width="3" stroke-linecap="round"/>
        <path d="M36 148 C58 130 76 163 98 146 C118 130 140 163 162 146 C181 130 201 158 224 143" fill="none" stroke="#0e7187" stroke-width="3" stroke-linecap="round"/>
        <text x="150" y="15" text-anchor="middle" fill="#e5b544" font-size="10" font-family="JetBrains Mono">N</text>
      </svg>
    </div>
    ''',
    unsafe_allow_html=True,
)
st.markdown(
    '''<div class="icon-rail">
      <div class="icon-chip"><svg viewBox="0 0 24 24"><path d="M3 20h18M5 17l7-12 7 12M9 13h6M12 5v-2"/></svg>Routes</div>
      <div class="icon-chip"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="m12 4 2.5 8-2.5 8-2.5-8L12 4Z"/></svg>Navigation</div>
      <div class="icon-chip"><svg viewBox="0 0 24 24"><path d="M4 17c3-5 5 5 8 0s5 5 8 0M4 12c3-5 5 5 8 0s5 5 8 0"/></svg>Sea log</div>
      <div class="icon-chip"><svg viewBox="0 0 24 24"><path d="M12 3 4 7v5c0 5 3.5 8 8 9 4.5-1 8-4 8-9V7l-8-4Z"/><path d="m8 12 2.5 2.5L16 9"/></svg>Archive</div>
    </div>''',
    unsafe_allow_html=True,
)

# =============================================================================
# Page 1: Arc Explorer
# =============================================================================
if active_page == "Arc Explorer":
    st.markdown(f'<div class="section-heading">{svg_icon("map")}<div><div class="section-kicker">Chart room</div><h2>Explore the Grand Line</h2></div></div>', unsafe_allow_html=True)
    selected_arc = st.selectbox("Choose a major One Piece arc", list(ARC_DATA))
    arc = ARC_DATA[selected_arc]
    columns = st.columns(3)
    for column, title, value in zip(columns, ["Episode Range", "Primary Location", "Main Antagonists"], [arc["episode_range"], arc["location"], arc["antagonists"]]):
        with column:
            st.markdown(f'<div class="card"><h4>{title}</h4><div class="value">{value}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="story"><h3>Key Storyline Highlights</h3><ul>{"".join(f"<li>{item}</li>" for item in arc["highlights"])}</ul></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="story"><h3>Straw Hat Crew Members Joined</h3><p>{arc["joined"]}</p></div>', unsafe_allow_html=True)

# =============================================================================
# Page 2: Catch-Up Calculator (Backed by Flask API)
# =============================================================================
if active_page == "Catch-Up Calculator":
    st.markdown(f'<div class="section-heading">{svg_icon("clock")}<div><div class="section-kicker">Voyage planner</div><h2>Calculate Your Catch-Up Journey</h2></div></div>', unsafe_allow_html=True)
    input_column, summary_column = st.columns(2)
    with input_column:
        current_episode = st.number_input("Your Current Episode", min_value=1, max_value=1165, value=1, step=1)
        episodes_per_day = st.number_input("Episodes Watched Per Day", min_value=1, value=3, step=1)

    try:
        calc_result = api_client.calculate_catch_up(int(current_episode), int(episodes_per_day))
        remaining = calc_result["episodes_remaining"]
        days = calc_result["estimated_days"]
        completion_date_str = calc_result["estimated_completion_date"]
        progress = calc_result["completion_percentage"]
    except APIError as e:
        st.error(f"Backend calculation error: {e.message}")
        remaining = max(0, 1165 - int(current_episode))
        days = (remaining + int(episodes_per_day) - 1) // int(episodes_per_day)
        completion_date = dt.date.today() + dt.timedelta(days=days)
        completion_date_str = completion_date.strftime("%d %B %Y")
        progress = min(float(current_episode) / 1165, 1.0)

    with summary_column:
        st.metric("Episodes Remaining", f"{remaining:,}")
        st.metric("Estimated Days Needed", f"{days:,}")
        st.metric("Estimated Completion Date", completion_date_str)
    st.progress(progress, text=f"{progress:.1%} complete")

# =============================================================================
# Page 3: Character Database
# =============================================================================
if active_page == "Character Database":
    st.markdown(f'<div class="section-heading">{svg_icon("wanted")}<div><div class="section-kicker">Wanted archive</div><h2>Character & Bounty Database</h2></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">Local wanted-poster archive // always available</div>', unsafe_allow_html=True)
    characters = [
        {"name": name, **data, "image_url": character_svg_data_uri(name, data["role"], data["color"])}
        for name, data in CHARACTERS.items()
    ]
    query = st.text_input("Search characters", placeholder="Try Luffy, Zoro, Sanji, Shanks, or Kaido").lower().strip()
    filtered = [item for item in characters if not query or query in item["name"].lower()]
    for start in range(0, min(len(filtered), 30), 4):
        row = filtered[start:start + 4]
        columns = st.columns(4)
        for column, character in zip(columns, row):
            with column:
                portrait = character.get("image_url", "")
                card_html = f'''
                <div class="fruit-card character-card">
                    <img class="portrait-image" src="{portrait}" alt="{character["name"]} SVG portrait">
                    <div class="fruit-name">{character["name"]}</div>
                    <div class="muted role-label">{character["role"]}</div>
                    <div class="bounty-line"><span>Bounty</span><strong>{format_bounty(character.get("bounty"))}</strong></div>
                </div>
                '''
                st.markdown(card_html, unsafe_allow_html=True)
    if not filtered:
        st.info("No characters matched your search.")

# =============================================================================
# Page 4: Devil Fruit Encyclopedia (Persisted via SQLite)
# =============================================================================
if active_page == "Devil Fruit Encyclopedia":
    st.markdown(f'<div class="section-heading">{svg_icon("fruit")}<div><div class="section-kicker">Field guide</div><h2>Devil Fruit Encyclopedia</h2></div></div>', unsafe_allow_html=True)
    st.markdown("Search by fruit name, user, ability, weakness, or profile, then narrow the catalog by classification and known user.")

    # Load persisted favorites from backend
    try:
        saved_list = api_client.get_favorites()
        st.session_state["favorite_fruits"] = set(saved_list)
    except APIError as e:
        st.error(f"Failed to fetch saved favorites from database: {e.message}")
        if "favorite_fruits" not in st.session_state:
            st.session_state["favorite_fruits"] = set()

    toolbar_left, toolbar_right = st.columns([3, 1])
    with toolbar_left:
        st.markdown('<div class="encyclopedia-toolbar"><strong>Field guide controls</strong><br><span class="muted">Build a shortlist, compare fruits, or discover one at random.</span></div>', unsafe_allow_html=True)
    with toolbar_right:
        if st.button("Discover random fruit"):
            st.session_state["random_fruit"] = random.choice(DEVIL_FRUITS)["name"]
        show_saved_only = st.toggle(
            "View saved favourites only",
            value=False,
            key="show_saved_fruits_only",
            help="Show only the Devil Fruits you saved.",
        )
    search_column, category_column, user_column = st.columns([2, 1, 1])
    with search_column:
        fruit_query = st.text_input("Search the encyclopedia", placeholder="Try Nika, fire, Kaido, water, or ROOM...").lower().strip()
    categories = ["All Types"] + sorted({fruit["type"] for fruit in DEVIL_FRUITS})
    with category_column:
        selected_category = st.selectbox("Fruit type", categories)
    user_options = ["All Users"] + sorted({fruit["user"] for fruit in DEVIL_FRUITS})
    with user_column:
        selected_user = st.selectbox("Known user", user_options)
    sort_mode = st.selectbox("Sort results", ["Name A–Z", "Type", "Power profile"], key="fruit_sort")
    filtered_fruits = [
        fruit for fruit in DEVIL_FRUITS
        if (selected_category == "All Types" or fruit["type"] == selected_category)
        and (selected_user == "All Users" or selected_user == fruit["user"])
        and (not show_saved_only or fruit["name"] in st.session_state["favorite_fruits"])
        and (not fruit_query or fruit_query in (" ".join(fruit.values()) + " " + str(DEVIL_FRUIT_DETAILS.get(fruit["name"], {}))).lower())
    ]
    if sort_mode == "Name A–Z":
        filtered_fruits.sort(key=lambda fruit: fruit["name"])
    elif sort_mode == "Type":
        filtered_fruits.sort(key=lambda fruit: (fruit["type"], fruit["name"]))
    else:
        strength_order = {"Unknown": 0, "High": 1, "Extreme": 2, "Legendary": 3}
        filtered_fruits.sort(key=lambda fruit: strength_order.get(DEVIL_FRUIT_DETAILS.get(fruit["name"], {}).get("strength", "Unknown"), 0), reverse=True)
    favorite_count = len(st.session_state["favorite_fruits"])
    insight_columns = st.columns(3)
    with insight_columns[0]:
        st.markdown(f'<div class="insight-card"><strong>{len(filtered_fruits)}</strong><span>Matching fruits</span></div>', unsafe_allow_html=True)
    with insight_columns[1]:
        st.markdown(f'<div class="insight-card"><strong>{favorite_count}</strong><span>Saved favorites</span></div>', unsafe_allow_html=True)
    with insight_columns[2]:
        st.markdown(f'<div class="insight-card"><strong>{len(categories) - 1}</strong><span>Fruit classes</span></div>', unsafe_allow_html=True)
    view_label = "saved favourites" if show_saved_only else "catalogued Devil Fruits"
    st.caption(f"Showing {len(filtered_fruits)} {view_label} · {len(DEVIL_FRUITS)} fruits in the full archive")
    comparison_names = st.multiselect("Compare up to three fruits", [fruit["name"] for fruit in DEVIL_FRUITS], max_selections=3, key="fruit_compare")
    if comparison_names:
        st.markdown("### Fruit Comparison")
        comparison_columns = st.columns(len(comparison_names))
        for column, fruit_name in zip(comparison_columns, comparison_names):
            fruit = next(item for item in DEVIL_FRUITS if item["name"] == fruit_name)
            details = DEVIL_FRUIT_DETAILS.get(fruit_name, {"profile":"Profile pending", "strength":"Unknown", "control":"Unknown", "danger":"Unrated", "weakness":"Standard weaknesses apply."})
            with column:
                st.markdown(f'<div class="compare-card"><div class="fruit-name">{fruit_name}</div><p><strong>Type:</strong> {fruit["type"]}</p><p><strong>Power:</strong> {details["strength"]}</p><p><strong>Control:</strong> {details["control"]}</p><p><strong>Threat:</strong> {details["danger"]}</p><p><strong>Weakness:</strong> {details["weakness"]}</p></div>', unsafe_allow_html=True)
    if st.session_state.get("random_fruit"):
        st.info(f"Random discovery: {st.session_state['random_fruit']}")
    if not filtered_fruits:
        if show_saved_only and not st.session_state["favorite_fruits"]:
            st.info("You have not saved any Devil Fruits yet. Turn off the saved view, then use ‘Save to favourites’ on a fruit card.")
        else:
            st.info("No Devil Fruits matched the current saved view, search, and filters.")
    else:
        for start in range(0, len(filtered_fruits), 3):
            row = filtered_fruits[start:start + 3]
            columns = st.columns(3)
            for column, fruit in zip(columns, row):
                with column:
                    icon_key = "mythical" if fruit["type"] == "Mythical Zoan" else fruit["type"].lower()
                    type_icon = svg_icon(icon_key, 20, "#243447")
                    details = DEVIL_FRUIT_DETAILS.get(fruit["name"], {"profile":f"{fruit['user']} · Profile data pending", "strength":"Unknown", "control":"Unknown", "danger":"Unrated", "weakness":"Standard Devil Fruit and seastone weaknesses apply."})
                    is_saved = fruit["name"] in st.session_state["favorite_fruits"]
                    favorite_label = "Saved" if is_saved else "Save to favorites"
                    if st.button(favorite_label, key=f"favorite_{fruit['name']}"):
                        try:
                            if is_saved:
                                api_client.remove_favorite(fruit["name"])
                                st.session_state["favorite_fruits"].remove(fruit["name"])
                            else:
                                api_client.add_favorite(fruit["name"])
                                st.session_state["favorite_fruits"].add(fruit["name"])
                            st.rerun()
                        except APIError as e:
                            st.error(f"Database operation failed: {e.message}")
                    st.markdown(
                        f'''<div class="fruit-card"><div class="fruit-name">{fruit["name"]}</div><div class="fruit-type">{type_icon}<span>{fruit["type"]}</span></div><p>{fruit["ability"]}</p><div class="fruit-detail"><div class="detail-label">Known user profile</div><div class="detail-text">{details["profile"]}</div><div class="stat-strip"><div class="stat-box"><strong>{details["strength"]}</strong><span>Power</span></div><div class="stat-box"><strong>{details["control"]}</strong><span>Control</span></div><div class="stat-box"><strong>{details["danger"]}</strong><span>Threat</span></div></div><div class="detail-label">Weaknesses</div><div class="detail-text">{details["weakness"]}</div></div></div>''',
                        unsafe_allow_html=True,
                    )
                    with st.expander("Type breakdown and awakening"):
                        st.markdown(f"**{fruit['type']} classification**")
                        st.write(DEVIL_FRUIT_TYPE_GUIDE.get(fruit["type"], "Classification details unavailable."))
                        st.markdown("**Awakening status**")
                        st.write(DEVIL_FRUIT_AWAKENINGS.get(fruit["name"], "No confirmed awakening has been shown for this fruit."))

# =============================================================================
# Page 5: Interactive Trivia Quiz (Server-Side Scoring & Leaderboard)
# =============================================================================
if active_page == "Trivia Quiz":
    st.markdown(f'<div class="section-heading">{svg_icon("quiz")}<div><div class="section-kicker">Captain\'s test</div><h2>One Piece Trivia Challenge</h2></div></div>', unsafe_allow_html=True)
    st.markdown("Test your knowledge of the Grand Line. Select an answer for each question and submit when ready.")
    player_name = st.text_input("Pirate name", value="Anonymous Captain", max_chars=24)
    quiz_answers = {}
    for index, question in enumerate(QUIZ_QUESTIONS, start=1):
        q_id = question.get("id", index)
        quiz_answers[q_id] = st.radio(
            f"{index}. {question['question']}",
            question["options"],
            key=f"quiz_question_{index}",
        )
    if st.button("Submit Quiz", type="primary"):
        try:
            result = api_client.submit_quiz(player_name, quiz_answers)
            score = result["score"]
            total = result["total"]
            category = result["category"]
            st.session_state["quiz_last_score"] = score
            st.metric("Your Score", f"{score} / {total}")
            if category == "perfect":
                st.success("Perfect score! You are ready for the New World.")
            elif category == "strong":
                st.info("Strong showing, captain. A little more training and you will conquer the Grand Line.")
            else:
                st.warning("Keep exploring the dashboard and try again to improve your score.")
        except APIError as e:
            st.error(f"Quiz submission failed: {e.message}")

    # Fetch live leaderboard from backend
    try:
        leaderboard_rows = api_client.get_quiz_leaderboard(limit=10)
    except APIError as e:
        st.error(f"Could not load leaderboard from database: {e.message}")
        leaderboard_rows = []

    if leaderboard_rows:
        st.markdown("### Grand Line Leaderboard")
        st.dataframe(leaderboard_rows, use_container_width=True, hide_index=True)

# =============================================================================
# Page 6: Bounty Reward Calculator (Backend Calculation & Persistent Claims)
# =============================================================================
if active_page == "Bounty Rewards":
    st.markdown(f'<div class="section-heading">{svg_icon("bounty")}<div><div class="section-kicker">Reputation ledger</div><h2>Bounty Reward Calculator</h2></div></div>', unsafe_allow_html=True)
    st.markdown("Select completed achievements to calculate your fictional World Government bounty and threat classification.")

    # Load claimed rewards from backend
    try:
        persisted_claimed = set(api_client.get_claimed_rewards())
        st.session_state["claimed_rewards"] = persisted_claimed
    except APIError as e:
        st.error(f"Could not load claimed rewards from database: {e.message}")
        if "claimed_rewards" not in st.session_state:
            st.session_state["claimed_rewards"] = set()

    claimed_rewards = st.session_state["claimed_rewards"]
    achievement_names = [item["achievement"] for item in BOUNTY_REWARDS]
    selected_achievements = st.multiselect("Completed achievements", options=achievement_names, key="bounty_achievements")

    try:
        bounty_calc = api_client.calculate_bounty(selected_achievements)
        reward_total = bounty_calc["total_bounty"]
        maximum_bounty = bounty_calc["maximum_bounty"]
        rank = bounty_calc["threat_classification"]
        next_rank = bounty_calc["next_rank"]
        berries_to_next_rank = bounty_calc["amount_needed_for_next_rank"]
        progress_val = bounty_calc["progress_percentage"]
    except APIError as e:
        st.error(f"Bounty calculation failed: {e.message}")
        reward_total = sum(item["reward"] for item in BOUNTY_REWARDS if item["achievement"] in selected_achievements)
        maximum_bounty = sum(item["reward"] for item in BOUNTY_REWARDS)
        rank = "Rising rookie"
        next_rank = "Notorious pirate"
        berries_to_next_rank = max(0, 150_000_000 - reward_total)
        progress_val = min(reward_total / maximum_bounty, 1.0) if maximum_bounty > 0 else 0.0

    reward_column, rank_column, milestone_column = st.columns(3)
    with reward_column:
        st.metric("Estimated bounty", f"{reward_total:,}", help="Berries")
    with rank_column:
        st.metric("Threat classification", rank)
    with milestone_column:
        st.metric("To next rank", f"{berries_to_next_rank:,}", help=next_rank)

    st.progress(progress_val, text=f"{progress_val:.1%} of the maximum archive bounty")
    action_left, action_right = st.columns([1, 1])
    with action_left:
        if st.button("Claim selected milestones", type="primary", disabled=not selected_achievements, use_container_width=True):
            try:
                claim_res = api_client.claim_rewards(selected_achievements)
                newly_claimed = claim_res.get("newly_claimed_count", 0)
                if newly_claimed > 0:
                    st.success(f"Added {newly_claimed} new milestone(s) to your reputation ledger.")
                else:
                    st.info("Those milestones are already in your reputation ledger.")
                st.rerun()
            except APIError as e:
                st.error(f"Failed to claim milestones in database: {e.message}")
    with action_right:
        if st.button("Reset claimed milestones", disabled=not claimed_rewards, use_container_width=True):
            try:
                api_client.reset_claimed_rewards()
                st.session_state["claimed_rewards"] = set()
                st.rerun()
            except APIError as e:
                st.error(f"Failed to reset claimed milestones in database: {e.message}")

    if not selected_achievements:
        st.info("Choose at least one achievement to calculate a bounty and unlock the claim action.")
    st.markdown("### Reward progression")
    reward_rows = []
    for reward in BOUNTY_REWARDS:
        is_claimed = reward["achievement"] in claimed_rewards
        status = "CLAIMED" if is_claimed else "AVAILABLE"
        reward_rows.append(f'<div class="reward-row {"is-claimed" if is_claimed else ""}"><span>{reward["achievement"]}</span><strong>{reward["reward"]:,} Berries <em>{status}</em></strong></div>')
    st.markdown(f'<div class="reward-ledger">{"".join(reward_rows)}</div>', unsafe_allow_html=True)

# =============================================================================
# Page 7: Crew Management (Persistent Roster & Member Training Stats)
# =============================================================================
if active_page == "Crew Management":
    st.markdown(f'<div class="section-heading">{svg_icon("crew")}<div><div class="section-kicker">Ship manifest</div><h2>Crew Management</h2></div></div>', unsafe_allow_html=True)
    st.markdown("Build your own pirate crew by choosing a name, captain, and up to nine additional specialists.")

    # Load saved crew from backend
    try:
        saved_crew = api_client.get_saved_crew()
    except APIError as e:
        st.error(f"Could not load saved crew from database: {e.message}")
        saved_crew = None

    default_crew_name = saved_crew["crew_name"] if saved_crew else "The Grand Line Crew"
    default_captain = saved_crew["captain"] if (saved_crew and saved_crew.get("captain") in CREW_MEMBERS) else list(CREW_MEMBERS)[0]
    captain_index = list(CREW_MEMBERS).index(default_captain)

    crew_name = st.text_input("Crew name", value=default_crew_name)
    captain_column, member_column = st.columns(2)
    with captain_column:
        captain = st.selectbox("Captain", list(CREW_MEMBERS), index=captain_index)

    available_members = [name for name in CREW_MEMBERS if name != captain]
    default_members = (
        [m for m in saved_crew["members"] if m in available_members]
        if (saved_crew and saved_crew.get("members"))
        else available_members[:4]
    )

    with member_column:
        selected_members = st.multiselect("Crew members", available_members, default=default_members, max_selections=9)
    roster = [captain] + selected_members
    st.metric("Crew Size", f"{len(roster)} / 10")
    roster_columns = st.columns(min(5, len(roster)))
    for column, member in zip(roster_columns * ((len(roster) + len(roster_columns) - 1) // len(roster_columns)), roster):
        with column:
            st.markdown(f'<div class="card"><h4>{member}</h4><div class="value">{CREW_MEMBERS[member]}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="story"><h3>{crew_name}</h3><p>Captain: {captain} · Specialists aboard: {len(selected_members)}</p></div>', unsafe_allow_html=True)

    st.markdown("### Crew Member Stats Tracker")
    tracked_member = st.selectbox("Choose a member to train", roster, key="tracked_member")

    saved_stats = (saved_crew.get("member_stats", {}) if saved_crew else {}).get(tracked_member, {})
    stat_columns = st.columns(4)
    with stat_columns[0]:
        power = st.slider("Power", 0, 100, int(saved_stats.get("power", 75)), key=f"power_{tracked_member}")
    with stat_columns[1]:
        defense = st.slider("Defense", 0, 100, int(saved_stats.get("defense", 70)), key=f"defense_{tracked_member}")
    with stat_columns[2]:
        speed = st.slider("Speed", 0, 100, int(saved_stats.get("speed", 72)), key=f"speed_{tracked_member}")
    with stat_columns[3]:
        loyalty = st.slider("Loyalty", 0, 100, int(saved_stats.get("loyalty", 90)), key=f"loyalty_{tracked_member}")
    readiness = round((power + defense + speed + loyalty) / 4)
    st.progress(readiness / 100, text=f"{tracked_member} readiness · {readiness}%")
    st.markdown(f'<div class="crew-stat-card"><h4>{tracked_member}</h4><p class="muted">{CREW_MEMBERS[tracked_member]} · Training profile updates live as you adjust the sliders.</p></div>', unsafe_allow_html=True)

    # Persistence action for crew manifest
    if st.button("Save crew", type="primary", use_container_width=False):
        try:
            current_member_stats = (saved_crew.get("member_stats", {}) if saved_crew else {}).copy()
            current_member_stats[tracked_member] = {
                "power": int(power),
                "defense": int(defense),
                "speed": int(speed),
                "loyalty": int(loyalty),
            }
            crew_payload = {
                "crew_name": crew_name,
                "captain": captain,
                "members": selected_members,
                "member_stats": current_member_stats,
            }
            api_client.save_crew(crew_payload)
            st.success(f"Crew configuration for '{crew_name}' saved successfully to database!")
        except APIError as e:
            st.error(f"Failed to save crew: {e.message}")

# =============================================================================
# Page 8: Marine vs Pirate Faction Battle Simulator (Authoritative Backend)
# =============================================================================
if active_page == "Faction Battle Simulator":
    st.markdown(f'<div class="section-heading">{svg_icon("bounty")}<div><div class="section-kicker">Grand Line conflict</div><h2>Marine vs Pirate Battle Simulator</h2></div></div>', unsafe_allow_html=True)
    st.markdown("Assemble both sides, compare their combat profiles, and run a lightweight deterministic battle simulation.")
    left, right = st.columns(2)
    with left:
        st.markdown(faction_card_svg("Pirates", "#c64038"), unsafe_allow_html=True)
        pirate_units = st.multiselect("Pirate combatants", [unit["name"] for unit in FACTION_UNITS["Pirates"]], default=[FACTION_UNITS["Pirates"][0]["name"], FACTION_UNITS["Pirates"][1]["name"]], key="pirate_units")
    with right:
        st.markdown(faction_card_svg("Marines", "#0e7187"), unsafe_allow_html=True)
        marine_units = st.multiselect("Marine combatants", [unit["name"] for unit in FACTION_UNITS["Marines"]], default=[FACTION_UNITS["Marines"][0]["name"], FACTION_UNITS["Marines"][1]["name"]], key="marine_units")

    if st.button("Run Battle Simulation", type="primary"):
        try:
            battle_outcome = api_client.simulate_battle(pirate_units, marine_units)
            st.session_state["last_battle"] = {
                "winner": battle_outcome["winner"],
                "pirate_score": battle_outcome["pirate_score"],
                "marine_score": battle_outcome["marine_score"],
            }
        except APIError as e:
            st.error(f"Battle simulation failed: {e.message}")

    if st.session_state.get("last_battle"):
        result = st.session_state["last_battle"]
        result_columns = st.columns(3)
        with result_columns[0]:
            st.metric("Pirate Power", result["pirate_score"])
        with result_columns[1]:
            st.markdown(f'<div class="battle-result"><span>VICTORIOUS FACTION</span><strong>{result["winner"]}</strong></div>', unsafe_allow_html=True)
        with result_columns[2]:
            st.metric("Marine Power", result["marine_score"])

