import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os
import json
from streamlit_js import st_js_blocking

# =========================================================
# BACKEND PATH
# =========================================================

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from fuzzy_logic import calculate_quality
from ai_analyzer import generate_ai_analysis


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NetSense AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Palette
INK = "#f4f5f9"
SOFT = "#c5c8d4"
MUTED = "#8a8fa3"
CYAN = "#22d3ee"
VIOLET = "#8b5cf6"
PINK = "#f472b6"
GOOD = "#34d399"
AVG = "#fbbf24"
POOR = "#fb7185"
GRID = "rgba(255,255,255,0.08)"
FONT = "Inter, sans-serif"


# =========================================================
# CSS  (fully self-contained: does not depend on Streamlit theme)
# =========================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@500;700&display=swap');

:root {
    --ink:#f4f5f9; --soft:#c5c8d4; --muted:#8a8fa3;
    --line: rgba(255,255,255,0.09); --panel: rgba(255,255,255,0.04);
    --cyan:#22d3ee; --violet:#8b5cf6; --pink:#f472b6;
    --good:#34d399; --avg:#fbbf24; --poor:#fb7185;
}

/* ---------- BASE ---------- */
.stApp {
    color: var(--ink) !important; color-scheme: dark;
    background:
        radial-gradient(900px 520px at 10% -8%, rgba(34,211,238,0.13), transparent 60%),
        radial-gradient(900px 560px at 96% 0%, rgba(139,92,246,0.20), transparent 60%),
        radial-gradient(800px 500px at 50% 112%, rgba(244,114,182,0.10), transparent 60%),
        #05060b !important;
    background-attachment: fixed !important;
}
.stApp, .stApp [data-testid="stMarkdownContainer"], .stApp button, .stApp input,
.stApp textarea, .stApp [data-baseweb="select"], .stApp [data-baseweb="tab"] {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }
.block-container { max-width: 1180px; padding-top: 1.4rem; padding-bottom: 3rem; }

/* readable text no matter which theme Streamlit picked */
:where(.stApp) :where(h1,h2,h3,h4,h5,h6,p,li,strong,b,em,label,small,span) { color: var(--soft); }
:where(.stApp) :where(h1,h2,h3,h4,h5,h6,strong,b) { color: var(--ink); }
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] * { color: var(--muted) !important; }
label, .stSelectbox label, .stTextInput label { color: var(--soft) !important; font-weight: 600 !important; }

/* ---------- NAV ---------- */
.nav { display:flex; align-items:center; justify-content:space-between; padding: 2px 4px 22px 4px; }
.brand { display:flex; align-items:center; gap:10px; font-family:'Space Grotesk',sans-serif;
    font-weight:700; font-size:20px; letter-spacing:-0.4px; color: var(--ink); }
.logo { width:30px; height:30px; border-radius:9px; position:relative;
    background: linear-gradient(135deg, var(--cyan), var(--violet)); box-shadow: 0 0 24px rgba(34,211,238,0.45); }
.logo::after { content:""; position:absolute; inset:8px; border-radius:50%; border:2px solid rgba(255,255,255,0.9); border-top-color: transparent; }
.brand i { font-style:normal; background: linear-gradient(90deg,var(--cyan),var(--violet)); -webkit-background-clip:text;
    background-clip:text; -webkit-text-fill-color: transparent; }
.chips { display:flex; gap:8px; align-items:center; }
.chip { font-size:12px; font-weight:600; color: var(--soft); background: var(--panel); border:1px solid var(--line);
    padding:7px 13px; border-radius:999px; }
.live { display:inline-block; width:7px; height:7px; border-radius:50%; background: var(--good);
    box-shadow:0 0 10px var(--good); margin-right:7px; animation: blink 2s infinite; }
@keyframes blink { 50% { opacity:.35; } }

/* ---------- HERO ---------- */
.hero { position:relative; overflow:hidden; border-radius:30px; padding:62px 56px; border:1px solid var(--line);
    background: linear-gradient(135deg, rgba(139,92,246,0.24), rgba(34,211,238,0.07) 55%, rgba(255,255,255,0.02)), #090a11;
    display:grid; grid-template-columns: 1.25fr 0.75fr; gap:20px; align-items:center; }
.hero::before { content:""; position:absolute; inset:0;
    background-image: linear-gradient(rgba(255,255,255,0.045) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.045) 1px, transparent 1px);
    background-size: 44px 44px;
    -webkit-mask-image: radial-gradient(ellipse at 75% 35%, #000 15%, transparent 72%);
    mask-image: radial-gradient(ellipse at 75% 35%, #000 15%, transparent 72%); }
.hero > * { position:relative; }
.hero-tag { display:inline-block; font-size:12px; font-weight:700; letter-spacing:.7px; text-transform:uppercase;
    color:#a5f3fc; background: rgba(34,211,238,0.10); border:1px solid rgba(34,211,238,0.30);
    padding:7px 14px; border-radius:999px; margin-bottom:22px; }
.hero h1 { font-family:'Space Grotesk',sans-serif !important; font-size:58px !important; line-height:1.04 !important;
    font-weight:700 !important; letter-spacing:-2.4px !important; margin:0 0 18px 0 !important; padding:0 !important; color:#fff !important; }
.hero h1 em { font-style:normal; background: linear-gradient(90deg,#67e8f9,#a78bfa 55%,#f472b6);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color: transparent; }
.hero p.lead { color:#aeb2c4 !important; font-size:17px; max-width:540px; line-height:1.65; margin:0 0 28px 0; }
.hero-stats { display:flex; gap:36px; flex-wrap:wrap; }
.hero-stats div b { display:block; font-family:'JetBrains Mono',monospace; font-size:24px; color:#fff !important; }
.hero-stats div span { font-size:12px; color:#8a8fa3 !important; font-weight:600; }

.signal { position:relative; width:270px; height:270px; margin:0 auto; }
.signal .ring { position:absolute; inset:0; border-radius:50%; border:1.5px solid rgba(34,211,238,0.45);
    animation: ping 4.2s cubic-bezier(0,0,.2,1) infinite; }
.signal .r2 { animation-delay: 1.4s; } .signal .r3 { animation-delay: 2.8s; }
@keyframes ping { 0% { transform:scale(.25); opacity:.9; } 100% { transform:scale(1.05); opacity:0; } }
.signal .core { position:absolute; inset:98px; border-radius:50%;
    background: radial-gradient(circle at 30% 30%, #67e8f9, #8b5cf6 70%); box-shadow: 0 0 60px rgba(34,211,238,0.6), 0 0 120px rgba(139,92,246,0.4); }
.sig-chip { position:absolute; font-size:11.5px; font-weight:700; color:#e5e7eb !important;
    background: rgba(12,13,20,0.78); border:1px solid var(--line); padding:6px 11px; border-radius:999px;
    backdrop-filter: blur(8px); animation: floaty 5s ease-in-out infinite; }
.sig-chip i { font-style:normal; margin-right:6px; }
.c1 { top:8px; left:-4px; } .c2 { top:110px; right:-18px; animation-delay:1.2s; } .c3 { bottom:6px; left:20px; animation-delay:2.4s; }
@keyframes floaty { 50% { transform: translateY(-8px); } }

/* ---------- CARDS ---------- */
.gcard, div[class*="st-key-card_"] {
    background: var(--panel) !important; border:1px solid var(--line) !important; border-radius:22px !important;
    backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
    box-shadow: 0 20px 50px -30px rgba(0,0,0,0.9);
}
.gcard { padding:24px; height:100%; transition: transform .2s ease, border-color .2s ease; }
.gcard:hover { transform: translateY(-3px); border-color: rgba(34,211,238,0.4); }
div[class*="st-key-card_"] { padding: 20px 22px !important; }
.f-icon { width:44px; height:44px; border-radius:13px; display:flex; align-items:center; justify-content:center; font-size:21px;
    margin-bottom:15px; background: linear-gradient(135deg, rgba(34,211,238,0.22), rgba(139,92,246,0.22)); border:1px solid var(--line); }
.gcard h4 { margin:0 0 6px 0; font-size:16.5px; font-weight:700; color: var(--ink) !important; }
.gcard p { margin:0; color: var(--muted) !important; font-size:14px; line-height:1.55; }

.kicker { font-family:'JetBrains Mono',monospace; font-size:12px; font-weight:700; letter-spacing:1.2px;
    color: var(--cyan) !important; text-transform:uppercase; margin: 52px 0 8px 0; }
.sec { font-family:'Space Grotesk',sans-serif; font-size:32px; font-weight:700; letter-spacing:-1.1px; color: var(--ink) !important; margin:0 0 4px 0; }
.sec-sub { color: var(--muted) !important; font-size:14.5px; margin-bottom:20px; }
.ch-title { font-weight:700; font-size:15.5px; color: var(--ink) !important; margin:2px 0 0 2px; }
.ch-sub { font-size:12.5px; color: var(--muted) !important; margin:0 0 6px 2px; }

/* ---------- PIPELINE ---------- */
.step { display:flex; gap:14px; position:relative; padding-bottom:20px; }
.step:not(:last-child)::after { content:""; position:absolute; left:16px; top:36px; bottom:2px; width:1px;
    background: linear-gradient(var(--line), transparent); }
.step-n { min-width:33px; height:33px; border-radius:10px; display:flex; align-items:center; justify-content:center;
    font-family:'JetBrains Mono',monospace; font-weight:700; font-size:12px; color: var(--cyan) !important;
    background: rgba(34,211,238,0.10); border:1px solid rgba(34,211,238,0.28); }
.step b { display:block; font-size:14.5px; color: var(--ink) !important; }
.step span { color: var(--muted) !important; font-size:13px; }

/* ---------- INPUTS ---------- */
div[data-baseweb="input"], div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.05) !important; border:1px solid var(--line) !important; border-radius:12px !important; }
div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within { border-color: var(--cyan) !important; }
div[data-baseweb="input"] input { color: var(--ink) !important; -webkit-text-fill-color: var(--ink) !important; background: transparent !important; }
div[data-baseweb="select"] *, div[data-baseweb="input"] button { color: var(--ink) !important; }
input::placeholder { color: #6f7488 !important; opacity:1 !important; -webkit-text-fill-color:#6f7488 !important; }
div[data-baseweb="popover"], div[data-baseweb="popover"] > div, div[data-baseweb="popover"] ul, div[data-baseweb="popover"] li {
    background: #12131c !important; color: var(--ink) !important; }
div[data-baseweb="popover"] li:hover { background: rgba(34,211,238,0.12) !important; }
div[data-baseweb="popover"] { border:1px solid var(--line); border-radius:12px; }

/* ---------- BUTTONS ---------- */
div.stButton > button {
    width:100%; height:56px; border:none; border-radius:15px; font-weight:700; font-size:15.5px;
    background: linear-gradient(90deg, #06b6d4, #6366f1 55%, #a855f7);
    box-shadow: 0 14px 34px -12px rgba(99,102,241,0.75); transition: all .2s ease; }
div.stButton > button, div.stButton > button * { color:#fff !important; }
div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 18px 40px -12px rgba(99,102,241,0.95); border:none; filter: brightness(1.08); }
div.stButton > button:active { transform: translateY(0); }
div.stDownloadButton > button { background: var(--panel); border:1px solid var(--line); border-radius:12px; font-weight:700; }
div.stDownloadButton > button, div.stDownloadButton > button * { color: var(--ink) !important; }
div.stDownloadButton > button:hover { border-color: var(--cyan); }

/* ---------- VERDICT ---------- */
.verdict { display:flex; align-items:center; justify-content:space-between; gap:24px; border-radius:26px; padding:30px 34px;
    border:1px solid var(--line); position:relative; overflow:hidden;
    background: radial-gradient(500px 220px at 0% 0%, color-mix(in srgb, var(--c) 30%, transparent), transparent 70%), rgba(255,255,255,0.03); }
.v-kicker { font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:1px; text-transform:uppercase; color: var(--c) !important; font-weight:700; }
.v-title { font-family:'Space Grotesk',sans-serif; font-size:34px; font-weight:700; letter-spacing:-1.2px; color:#fff !important; margin:8px 0 6px 0; line-height:1.1; }
.v-sub { color: var(--soft) !important; font-size:15px; max-width:640px; line-height:1.55; }
.v-ring { min-width:118px; height:118px; border-radius:50%; position:relative; display:flex; align-items:center; justify-content:center;
    background: conic-gradient(var(--c) calc(var(--p) * 1%), rgba(255,255,255,0.09) 0); box-shadow: 0 0 40px color-mix(in srgb, var(--c) 30%, transparent); }
.v-ring::after { content:""; position:absolute; inset:9px; border-radius:50%; background:#0a0b12; }
.v-ring span { position:relative; z-index:2; font-family:'JetBrains Mono',monospace; font-size:27px; font-weight:700; color:#fff !important; }
.v-ring small { position:absolute; z-index:2; bottom:26px; font-size:9.5px; letter-spacing:.8px; color: var(--muted) !important; font-weight:700; }

/* ---------- METRIC TILES ---------- */
.metric { border-radius:20px; padding:20px 22px; height:100%; border:1px solid var(--line); background: var(--panel);
    position:relative; overflow:hidden; }
.metric::after { content:""; position:absolute; right:-40px; top:-40px; width:120px; height:120px; border-radius:50%;
    background: radial-gradient(circle, color-mix(in srgb, var(--c) 28%, transparent), transparent 70%); }
.m-top { display:flex; justify-content:space-between; align-items:center; position:relative; z-index:2; }
.lbl { font-size:11.5px; font-weight:700; color: var(--muted) !important; text-transform:uppercase; letter-spacing:.9px; }
.pill { font-size:11px; font-weight:700; padding:4px 10px; border-radius:999px; }
.pill.good { background: rgba(52,211,153,0.14); color: var(--good) !important; }
.pill.avg  { background: rgba(251,191,36,0.14); color: var(--avg) !important; }
.pill.poor { background: rgba(251,113,133,0.14); color: var(--poor) !important; }
.pill.info { background: rgba(139,92,246,0.16); color:#c4b5fd !important; }
.val { font-family:'JetBrains Mono',monospace; font-size:35px; font-weight:700; color:#fff !important; letter-spacing:-1.5px; margin:12px 0 12px 0; position:relative; z-index:2; }
.unit { font-size:14px; color: var(--muted) !important; margin-left:4px; font-weight:500; letter-spacing:0; }
.mbar { height:6px; border-radius:99px; background: rgba(255,255,255,0.08); overflow:hidden; position:relative; z-index:2; }
.mbar div { height:100%; border-radius:99px; background: var(--c); box-shadow: 0 0 12px var(--c); }
.hint { font-size:12px; color: var(--muted) !important; margin-top:8px; position:relative; z-index:2; }

/* ---------- TABS ---------- */
div[data-baseweb="tab-list"] { gap:8px; background:transparent; }
button[data-baseweb="tab"] { background: var(--panel); border:1px solid var(--line); border-radius:999px; padding:8px 18px; height:auto; }
button[data-baseweb="tab"] p { color: var(--soft) !important; font-weight:700; }
button[data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(90deg, rgba(34,211,238,0.22), rgba(139,92,246,0.28)); border-color: rgba(34,211,238,0.5); }
button[data-baseweb="tab"][aria-selected="true"] p { color:#fff !important; }
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display:none; }

/* ---------- MISC ---------- */
div[data-testid="stAlert"] { border-radius:14px; background: rgba(255,255,255,0.05) !important; border:1px solid var(--line); }
div[data-testid="stAlert"] * { color: var(--ink) !important; }
div[data-testid="stSpinner"] * { color: var(--soft) !important; }
div[data-testid="stCode"], div[data-testid="stCode"] pre { background:#0c0d15 !important; }
div[data-testid="stCode"] * { color: #e5e7eb !important; }
hr { border-color: var(--line) !important; margin: 40px 0 !important; }
.footer { text-align:center; color:#5f6478 !important; font-size:12.5px; padding-top:6px; }
.report p { color: var(--soft) !important; line-height:2.1; font-size:15px; margin:0; }
.report b { color: var(--ink) !important; }

@media (max-width: 860px) {
    .hero { grid-template-columns: 1fr; padding: 36px 24px; border-radius:24px; }
    .signal { display:none; }
    .hero h1 { font-size: 38px !important; letter-spacing:-1.4px !important; }
    .verdict { flex-direction: column; align-items:flex-start; padding:24px; }
    .v-title { font-size: 26px; } .sec { font-size:25px; }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# HELPERS - LOGIC
# =========================================================

# =========================================================
# BROWSER-SIDE NETWORK TEST
# =========================================================
# Streamlit Cloud executes Python on the cloud server. The old
# ping_host() therefore measured the cloud server's network and could
# return 999 ms / 100% loss when ICMP was unavailable.
#
# This test runs JavaScript in the visitor's browser and measures small
# HTTP requests from the browser. It is an HTTP-based estimate, not raw
# ICMP ping, because normal browser JavaScript cannot send ICMP packets.

BROWSER_TEST_JS = """
const probes = 8;
const timeoutMs = 5000;
const targets = [
    "https://www.gstatic.com/generate_204",
    "https://www.google.com/generate_204"
];

const samples = [];

for (let i = 0; i < probes; i++) {
    const target = targets[i % targets.length] +
        "?netsense=" + Date.now() + "-" + i + "-" + Math.random();

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), timeoutMs);
    const start = performance.now();

    try {
        await fetch(target, {
            method: "GET",
            mode: "no-cors",
            cache: "no-store",
            signal: controller.signal
        });

        const elapsed = performance.now() - start;
        samples.push(Number(elapsed.toFixed(2)));
    } catch (error) {
        samples.push(null);
    } finally {
        clearTimeout(timer);
    }
}

const successful = samples.filter(v => typeof v === "number");
const failed = samples.length - successful.length;

let latency = null;
let jitter = null;

if (successful.length > 0) {
    latency = successful.reduce((a, b) => a + b, 0) / successful.length;

    if (successful.length > 1) {
        let totalDiff = 0;
        for (let i = 1; i < successful.length; i++) {
            totalDiff += Math.abs(successful[i] - successful[i - 1]);
        }
        jitter = totalDiff / (successful.length - 1);
    } else {
        jitter = 0;
    }
}

return JSON.stringify({
    success: successful.length > 0,
    latency: latency === null ? null : Number(latency.toFixed(2)),
    jitter: jitter === null ? null : Number(jitter.toFixed(2)),
    packet_loss: Number(((failed / probes) * 100).toFixed(2)),
    successful: successful.length,
    failed: failed,
    probes: probes,
    samples: samples,
    method: "Browser HTTP probes"
});
"""


def measure_browser_connection(test_id):
    """Measure the visitor's connection from their browser."""
    try:
        raw = st_js_blocking(
            code=BROWSER_TEST_JS,
            key=f"netsense_network_test_{test_id}"
        )

        if not raw:
            return {
                "success": False,
                "error": "The browser did not return a network measurement."
            }

        if isinstance(raw, str):
            data = json.loads(raw)
        elif isinstance(raw, dict):
            data = raw
        else:
            data = json.loads(str(raw))

        if not data.get("success"):
            return {
                "success": False,
                "error": "All browser network probes failed.",
                "packet_loss": data.get("packet_loss", 100),
                "method": data.get("method", "Browser HTTP probes")
            }

        return {
            "success": True,
            "latency": float(data["latency"]),
            "jitter": float(data["jitter"]),
            "packet_loss": float(data["packet_loss"]),
            "successful": int(data.get("successful", 0)),
            "failed": int(data.get("failed", 0)),
            "probes": int(data.get("probes", 0)),
            "samples": data.get("samples", []),
            "method": data.get("method", "Browser HTTP probes")
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
            "method": "Browser HTTP probes"
        }


def clip(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, float(x)))


def status(value, good_max, avg_max):
    """Lower is better."""
    if value <= good_max:
        return "good", "Excellent", GOOD
    if value <= avg_max:
        return "avg", "Moderate", AVG
    return "poor", "Needs work", POOR


def quality_css(category):
    return {"Good": "good", "Average": "avg"}.get(category, "poor")


def quality_color(category):
    return {"good": GOOD, "avg": AVG, "poor": POOR}[quality_css(category)]


def health_scores(latency, jitter, loss):
    """Convert raw metrics into 0-100 health values (100 = best)."""
    return {
        "Latency": clip(100 - (float(latency) / 200) * 100),
        "Jitter": clip(100 - (float(jitter) / 50) * 100),
        "Packet Loss": clip(100 - (float(loss) / 10) * 100),
    }


# (excellent_at, breaking_point) per metric for each use case
USE_CASE_LIMITS = {
    "Gaming":          {"lat": (30, 150),  "jit": (5, 40),   "loss": (0.5, 5)},
    "Video Streaming": {"lat": (80, 400),  "jit": (20, 100), "loss": (1, 8)},
    "Video Calling":   {"lat": (60, 250),  "jit": (10, 50),  "loss": (0.5, 5)},
    "Online Classes":  {"lat": (70, 300),  "jit": (15, 60),  "loss": (1, 5)},
    "Web Browsing":    {"lat": (100, 500), "jit": (30, 120), "loss": (2, 10)},
    "File Download":   {"lat": (150, 600), "jit": (50, 150), "loss": (0.5, 4)},
    "General Usage":   {"lat": (80, 300),  "jit": (20, 80),  "loss": (1, 6)},
}


def suitability(latency, jitter, loss):
    out = {}
    for name, lim in USE_CASE_LIMITS.items():
        parts = []
        for val, key in ((latency, "lat"), (jitter, "jit"), (loss, "loss")):
            good, bad = lim[key]
            parts.append(clip((1 - (float(val) - good) / (bad - good)) * 100))
        out[name] = 0.6 * min(parts) + 0.4 * (sum(parts) / len(parts))
    return out


# =========================================================
# HELPERS - HTML
# =========================================================

def feature_card(icon, title, text):
    return (
        f'<div class="gcard"><div class="f-icon">{icon}</div>'
        f'<h4>{title}</h4><p>{text}</p></div>'
    )


def step(num, title, text):
    return (
        f'<div class="step"><div class="step-n">{num}</div>'
        f'<div><b>{title}</b><span>{text}</span></div></div>'
    )


def metric_tile(label, value, unit, good_max, avg_max, health):
    css, txt, color = status(float(value), good_max, avg_max)
    return (
        f'<div class="metric" style="--c:{color}">'
        f'<div class="m-top"><span class="lbl">{label}</span><span class="pill {css}">{txt}</span></div>'
        f'<div class="val">{value}<span class="unit">{unit}</span></div>'
        f'<div class="mbar"><div style="width:{health:.0f}%"></div></div>'
        f'<div class="hint">Health {health:.0f} / 100</div></div>'
    )


def chart_header(title, sub):
    st.markdown(
        f'<div class="ch-title">{title}</div><div class="ch-sub">{sub}</div>',
        unsafe_allow_html=True,
    )


def card(name):
    return st.container(key=f"card_{name}")


def show(fig):
    cfg = {"displayModeBar": False}
    try:
        st.plotly_chart(fig, width="stretch", config=cfg)
    except Exception:
        st.plotly_chart(fig, use_container_width=True, config=cfg)


# =========================================================
# HELPERS - CHARTS (dark)
# =========================================================

def base_layout(fig, height):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=30, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, color=SOFT, size=13),
        showlegend=False,
        hoverlabel=dict(bgcolor="#12131c", bordercolor="rgba(255,255,255,0.15)", font=dict(color="#fff", family=FONT)),
    )
    return fig


def gauge_fig(score, category):
    color = quality_color(category)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=float(score),
            number={"font": {"size": 58, "color": "#ffffff", "family": "JetBrains Mono"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": MUTED, "tickfont": {"size": 11, "color": MUTED}},
                "bar": {"color": color, "thickness": 0.3},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(251,113,133,0.16)"},
                    {"range": [40, 70], "color": "rgba(251,191,36,0.16)"},
                    {"range": [70, 100], "color": "rgba(52,211,153,0.16)"},
                ],
            },
        )
    )
    base_layout(fig, 280)
    fig.update_layout(margin=dict(l=25, r=25, t=25, b=5))
    return fig


def radar_fig(latency, jitter, loss, score):
    h = health_scores(latency, jitter, loss)
    labels = ["Latency", "Jitter", "Packet Loss", "Overall"]
    values = [h["Latency"], h["Jitter"], h["Packet Loss"], clip(score)]
    fig = go.Figure(
        go.Scatterpolar(
            r=values + values[:1],
            theta=labels + labels[:1],
            fill="toself",
            fillcolor="rgba(34,211,238,0.18)",
            line=dict(color=CYAN, width=3),
            marker=dict(size=9, color=VIOLET, line=dict(color="#fff", width=1)),
            hovertemplate="%{theta}: %{r:.0f}/100<extra></extra>",
        )
    )
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(range=[0, 100], gridcolor=GRID, linecolor=GRID, tickfont=dict(size=10, color=MUTED)),
            angularaxis=dict(gridcolor=GRID, linecolor=GRID, tickfont=dict(size=13, color=INK)),
        )
    )
    return base_layout(fig, 340)


def usecase_fig(latency, jitter, loss, selected):
    data = suitability(latency, jitter, loss)
    items = sorted(data.items(), key=lambda kv: kv[1])
    names = [k for k, _ in items]
    vals = [v for _, v in items]
    colors = [CYAN if n == selected else "rgba(139,92,246,0.45)" for n in names]
    fig = go.Figure(
        go.Bar(
            x=vals, y=names, orientation="h",
            marker=dict(color=colors),
            text=[f"{v:.0f}%" for v in vals],
            textposition="outside", cliponaxis=False,
            textfont=dict(color=INK),
            hovertemplate="%{y}: %{x:.0f}%<extra></extra>",
        )
    )
    fig.update_xaxes(range=[0, 118], showgrid=True, gridcolor=GRID, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, tickfont=dict(size=13, color=INK))
    fig.update_layout(bargap=0.36)
    return base_layout(fig, 340)


def health_fig(latency, jitter, loss):
    h = health_scores(latency, jitter, loss)
    names, vals = list(h.keys()), list(h.values())
    colors = [GOOD if v >= 70 else AVG if v >= 40 else POOR for v in vals]
    fig = go.Figure(
        go.Bar(
            x=names, y=vals, marker=dict(color=colors),
            text=[f"{v:.0f}" for v in vals], textposition="outside", cliponaxis=False,
            textfont=dict(color=INK, size=14),
            hovertemplate="%{x}: %{y:.0f}/100<extra></extra>",
        )
    )
    fig.update_yaxes(range=[0, 118], gridcolor=GRID, zeroline=False, tickfont=dict(size=11, color=MUTED))
    fig.update_xaxes(tickfont=dict(size=13, color=INK))
    fig.update_layout(bargap=0.5)
    return base_layout(fig, 320)


def limit_fig(latency, jitter, loss, use_case):
    lim = USE_CASE_LIMITS[use_case]
    rows = [
        ("Latency", float(latency), lim["lat"], "ms"),
        ("Jitter", float(jitter), lim["jit"], "ms"),
        ("Packet Loss", float(loss), lim["loss"], "%"),
    ][::-1]
    names, pct, colors, texts = [], [], [], []
    for name, val, (good, bad), unit in rows:
        names.append(name)
        pct.append(min(val / bad * 100, 135))
        colors.append(GOOD if val <= good else AVG if val <= (good + bad) / 2 else POOR)
        texts.append(f"{val:g} {unit}  /  limit {bad:g} {unit}")
    fig = go.Figure(
        go.Bar(
            x=pct, y=names, orientation="h", marker=dict(color=colors),
            text=texts, textposition="outside", cliponaxis=False, textfont=dict(color=SOFT, size=12),
            hovertemplate="%{y}: %{x:.0f}% of breaking point<extra></extra>",
        )
    )
    fig.add_vline(x=100, line=dict(color=POOR, width=2, dash="dash"),
                  annotation_text="Breaking point", annotation_font=dict(color=POOR, size=11),
                  annotation_position="top")
    fig.update_xaxes(range=[0, 190], gridcolor=GRID, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, tickfont=dict(size=13, color=INK))
    fig.update_layout(bargap=0.5)
    return base_layout(fig, 320)


def fuzzy_fig(membership):
    titles = [("latency", "Latency"), ("jitter", "Jitter"), ("packet_loss", "Packet Loss")]
    palette = [CYAN, VIOLET, PINK, "#38bdf8", AVG]
    fig = make_subplots(rows=1, cols=3, subplot_titles=[t for _, t in titles], horizontal_spacing=0.08)
    for i, (key, _) in enumerate(titles, start=1):
        values = membership.get(key, {})
        labels = [str(k).title() for k in values.keys()]
        vals = [float(v) for v in values.values()]
        fig.add_trace(
            go.Bar(
                x=labels, y=vals, marker=dict(color=palette[: len(vals)]),
                text=[f"{v:.2f}" for v in vals], textposition="outside", cliponaxis=False,
                textfont=dict(color=INK),
                hovertemplate="%{x}: %{y:.2f}<extra></extra>",
            ),
            row=1, col=i,
        )
        fig.update_yaxes(range=[0, 1.25], gridcolor=GRID, zeroline=False, tickfont=dict(size=10, color=MUTED), row=1, col=i)
        fig.update_xaxes(tickfont=dict(size=12, color=INK), row=1, col=i)
    fig.update_annotations(font=dict(size=14, family=FONT, color=INK))
    fig.update_layout(bargap=0.4)
    return base_layout(fig, 340)


# =========================================================
# NAV + HERO
# =========================================================

st.markdown(
    '<div class="nav"><div class="brand"><span class="logo"></span>Net<i>Sense</i> AI</div>'
    '<div class="chips"><span class="chip"><span class="live"></span>Fuzzy Logic</span>'
    '<span class="chip">Gemini</span></div></div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="hero"><div>'
    '<div class="hero-tag">✦ Network intelligence</div>'
    '<h1>See what your<br>connection <em>really</em> feels like.</h1>'
    '<p class="lead">We measure latency, jitter and packet loss, score them with fuzzy logic, '
    'chart the results and let Gemini explain what it means for you.</p>'
    '<div class="hero-stats">'
    '<div><b>3</b><span>Core metrics</span></div>'
    '<div><b>8</b><span>Fuzzy rules</span></div>'
    '<div><b>5</b><span>Live graphs</span></div></div></div>'
    '<div class="signal"><div class="ring"></div><div class="ring r2"></div><div class="ring r3"></div>'
    '<div class="core"></div>'
    '<span class="sig-chip c1"><i style="color:#22d3ee">●</i>Latency</span>'
    '<span class="sig-chip c2"><i style="color:#a78bfa">●</i>Jitter</span>'
    '<span class="sig-chip c3"><i style="color:#f472b6">●</i>Packet loss</span></div></div>',
    unsafe_allow_html=True,
)

st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3, gap="medium")
with f1:
    st.markdown(feature_card("⚡", "Network Test", "Browser-based latency, jitter and request-loss measurements."), unsafe_allow_html=True)
with f2:
    st.markdown(feature_card("🧠", "Fuzzy Scoring", "Eight rules turn raw numbers into a 0-100 quality score."), unsafe_allow_html=True)
with f3:
    st.markdown(feature_card("🤖", "AI Explanation", "Gemini explains what the numbers mean for how you use the internet."), unsafe_allow_html=True)


# =========================================================
# INPUT
# =========================================================

st.markdown('<div class="kicker">01 — Analyze</div><div class="sec">Run a connection test</div>'
            '<div class="sec-sub">Pick your main use case and start the analysis.</div>', unsafe_allow_html=True)

secret_key = None
try:
    secret_key = st.secrets.get("GEMINI_API_KEY", None)
except Exception:
    secret_key = None

left, right = st.columns([1.3, 1], gap="large")

with left:
    with card("input"):
        if secret_key:
            api_key = secret_key
            st.success("Gemini API key loaded securely from server settings.")
        else:
            api_key = st.text_input("Gemini API Key", type="password", placeholder="Paste your Gemini API key")

        use_case_input = st.selectbox("What do you mainly use your internet for?", list(USE_CASE_LIMITS.keys()))
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        analyze_button = st.button("⚡ Analyze Connection")

with right:
    st.markdown(
        '<div class="gcard">'
        + step("01", "Measure", "Latency • Jitter • Packet loss")
        + step("02", "Score", "8 fuzzy rules → quality score")
        + step("03", "Visualize", "Gauge, radar, readiness and limit charts")
        + step("04", "Explain", "Gemini gives tailored recommendations")
        + "</div>",
        unsafe_allow_html=True,
    )


# =========================================================
# RUN ANALYSIS
# IMPORTANT:
# st_js_blocking() can trigger a Streamlit rerun while waiting
# for browser-side JavaScript. We therefore store the user's
# request in session_state before starting the measurement.
# =========================================================

if analyze_button:
    if not api_key:
        st.error("Please enter your Gemini API key.")
    else:
        st.session_state["analysis_requested"] = True
        st.session_state["analysis_api_key"] = api_key
        st.session_state["analysis_use_case"] = use_case_input

        test_id = st.session_state.get("network_test_id", 0) + 1
        st.session_state["network_test_id"] = test_id

        # Clear the previous result so the new test becomes the active one.
        st.session_state.pop("res", None)


# Continue the analysis after the rerun triggered by st_js_blocking().
if st.session_state.get("analysis_requested", False):

    api_key_run = st.session_state.get("analysis_api_key", "")
    use_case_run = st.session_state.get(
        "analysis_use_case",
        "General Usage"
    )
    test_id = st.session_state.get("network_test_id", 1)

    try:
        with st.spinner("Testing your connection..."):

            # -------------------------------------------------
            # 1. Measure from the visitor's browser
            # -------------------------------------------------
            network = measure_browser_connection(test_id)

            if not network.get("success"):
                st.error(
                    "Unable to measure the connection from your browser. "
                    "Please check your internet connection and try again."
                )
                st.info(
                    network.get(
                        "error",
                        "The browser network test did not return usable measurements."
                    )
                )
                st.session_state["analysis_requested"] = False

            else:
                # -------------------------------------------------
                # 2. Get the measured network values
                # -------------------------------------------------
                latency = network["latency"]
                jitter = network["jitter"]
                packet_loss = network["packet_loss"]

                # -------------------------------------------------
                # 3. Fuzzy Logic scoring
                # -------------------------------------------------
                fuzzy = calculate_quality(
                    latency,
                    jitter,
                    packet_loss
                )

                # -------------------------------------------------
                # 4. LangChain + Gemini explanation
                # -------------------------------------------------
                ai = generate_ai_analysis(
                    api_key=api_key_run,
                    latency=latency,
                    jitter=jitter,
                    packet_loss=packet_loss,
                    quality_score=fuzzy["score"],
                    category=fuzzy["category"],
                    use_case=use_case_run,
                )

                # -------------------------------------------------
                # 5. Save everything so results survive reruns
                # -------------------------------------------------
                st.session_state["res"] = {
                    "latency": latency,
                    "jitter": jitter,
                    "packet_loss": packet_loss,
                    "network_method": network.get(
                        "method",
                        "Browser HTTP probes"
                    ),
                    "successful_probes": network.get(
                        "successful",
                        0
                    ),
                    "failed_probes": network.get(
                        "failed",
                        0
                    ),
                    "total_probes": network.get(
                        "probes",
                        0
                    ),
                    "fuzzy": fuzzy,
                    "ai": ai,
                    "use_case": use_case_run,
                }

                st.session_state["analysis_requested"] = False

    except Exception as error:
        st.error("Something went wrong during analysis.")
        st.exception(error)
        st.session_state["analysis_requested"] = False


# =========================================================
# RESULTS
# =========================================================

res = st.session_state.get("res")

if res:
    latency = res["latency"]
    jitter = res["jitter"]
    packet_loss = res["packet_loss"]
    network_method = res.get("network_method", "Browser HTTP probes")
    successful_probes = res.get("successful_probes", 0)
    failed_probes = res.get("failed_probes", 0)
    total_probes = res.get("total_probes", 0)
    fuzzy = res["fuzzy"]
    ai = res["ai"]
    use_case = res["use_case"]
    score = fuzzy["score"]
    category = fuzzy["category"]

    css = quality_css(category)
    color = quality_color(category)
    health = health_scores(latency, jitter, packet_loss)
    ready = suitability(latency, jitter, packet_loss)[use_case]
    weakest = min(health, key=health.get)

    if ready >= 75:
        headline = f"Great for {use_case}."
    elif ready >= 50:
        headline = f"Workable for {use_case}, with hiccups."
    else:
        headline = f"Struggling for {use_case}."

    st.markdown('<div class="kicker">02 — Results</div><div class="sec">Your connection report</div>'
                f'<div class="sec-sub">Analysis tailored for <b>{use_case}</b></div>', unsafe_allow_html=True)

    # ---------- VERDICT BANNER ----------
    st.markdown(
        f'<div class="verdict" style="--c:{color};--p:{ready:.0f}">'
        f'<div><div class="v-kicker">● {str(category).upper()} CONNECTION</div>'
        f'<div class="v-title">{headline}</div>'
        f'<div class="v-sub">Overall quality is {str(category).lower()} at {score}/100. '
        f'Your weakest link right now is <b style="color:#fff">{weakest.lower()}</b>.</div></div>'
        f'<div class="v-ring"><span>{ready:.0f}%</span><small>READY</small></div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    # ---------- GAUGE + TILES ----------
    g_col, m_col = st.columns([1, 1.45], gap="large")

    with g_col:
        with card("gauge"):
            chart_header("Overall quality", "Fuzzy logic score out of 100")
            show(gauge_fig(score, category))

    with m_col:
        a, b = st.columns(2, gap="medium")
        with a:
            st.markdown(metric_tile("Latency", latency, "ms", 50, 100, health["Latency"]), unsafe_allow_html=True)
        with b:
            st.markdown(metric_tile("Jitter", jitter, "ms", 10, 30, health["Jitter"]), unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        c, d = st.columns(2, gap="medium")
        with c:
            st.markdown(metric_tile("Packet Loss", packet_loss, "%", 1, 3, health["Packet Loss"]), unsafe_allow_html=True)
        with d:
            st.markdown(
                f'<div class="metric" style="--c:{VIOLET}">'
                f'<div class="m-top"><span class="lbl">Fuzzy rules</span><span class="pill info">Engine</span></div>'
                f'<div class="val">{fuzzy.get("rules_count", "-")}<span class="unit">fired</span></div>'
                f'<div class="mbar"><div style="width:{clip(score):.0f}%"></div></div>'
                f'<div class="hint">Score {score} / 100</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:26px'></div>", unsafe_allow_html=True)

    # ---------- TABS ----------
    tab_graphs, tab_fuzzy, tab_ai, tab_report = st.tabs(
        ["📊 Graphs", "🧠 Fuzzy engine", "🤖 AI insights", "📋 Report"]
    )

    with tab_graphs:
        p1, p2 = st.columns(2, gap="medium")
        with p1:
            with card("radar"):
                chart_header("Connection profile", "Radar view - bigger and wider is better")
                show(radar_fig(latency, jitter, packet_loss, score))
        with p2:
            with card("usecase"):
                chart_header("Use-case readiness", f"How suitable your connection is for each activity ({use_case} highlighted)")
                show(usecase_fig(latency, jitter, packet_loss, use_case))

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        p3, p4 = st.columns(2, gap="medium")
        with p3:
            with card("health"):
                chart_header("Metric health", "Each metric converted to a 0-100 health score")
                show(health_fig(latency, jitter, packet_loss))
        with p4:
            with card("limit"):
                chart_header("Distance to breaking point", f"How close each metric is to being a problem for {use_case}")
                show(limit_fig(latency, jitter, packet_loss, use_case))

        st.caption(
            "Measurements are collected in your browser using HTTP probes. "
            "They estimate browser-to-internet latency, jitter and request loss; "
            "they are not raw ICMP ping measurements. "
            f"Successful probes: {successful_probes}/{total_probes}."
        )
        st.caption("Health, readiness and breaking-point values are estimates based on typical thresholds for each activity.")

    with tab_fuzzy:
        membership = fuzzy.get("membership", {})
        with card("fuzzy"):
            chart_header("Membership degrees", "How strongly each measurement belongs to each fuzzy set")
            if membership:
                show(fuzzy_fig(membership))
            else:
                st.info("No membership data returned by the fuzzy engine.")
        st.caption("A value near 1.0 means the measurement fits that fuzzy set almost completely.")

    with tab_ai:
        with card("ai"):
            if ai.get("success"):
                st.markdown(ai.get("analysis", "No AI analysis returned."))
            else:
                st.error("AI analysis failed.")
                st.code(ai.get("message", "Unknown Gemini error."))

    with tab_report:
        report = (
            "NetSense AI Report\n"
            f"Use case: {use_case}\n"
            f"Connection quality: {category}\n"
            f"Fuzzy score: {score}/100\n"
            f"Latency: {latency} ms\n"
            f"Jitter: {jitter} ms\n"
            f"Packet loss: {packet_loss}%\n"
            f"Measurement method: {network_method}\n"
            f"Successful probes: {successful_probes}/{total_probes}\n"
            f"Readiness for {use_case}: {ready:.0f}%\n"
        )
        with card("report"):
            st.markdown(
                '<div class="report">'
                f'<p><b>Use case:</b> {use_case}</p>'
                f'<p><b>Connection quality:</b> {category}</p>'
                f'<p><b>Fuzzy score:</b> {score}/100</p>'
                f'<p><b>Latency:</b> {latency} ms</p>'
                f'<p><b>Jitter:</b> {jitter} ms</p>'
                f'<p><b>Packet loss:</b> {packet_loss}%</p>'
                f'<p><b>Measurement method:</b> {network_method}</p>'
                f'<p><b>Successful probes:</b> {successful_probes}/{total_probes}</p>'
                f'<p><b>Readiness for {use_case}:</b> {ready:.0f}%</p></div>',
                unsafe_allow_html=True,
            )
            st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
            st.download_button("⬇ Download report", report, file_name="netsense_report.txt")


# =========================================================
# FOOTER
# =========================================================

st.divider()
st.markdown(
    '<div class="footer">NetSense AI • AI + Fuzzy Logic Internet Connection Quality Analyzer</div>',
    unsafe_allow_html=True,
)