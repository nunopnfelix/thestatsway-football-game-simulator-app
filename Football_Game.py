# streamlit run FMtypegame.py
import base64
import html as html_lib
import io
import json
import random
import re
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import streamlit.components.v1 as components

st.set_page_config(page_title="Liga Portugal Manager", page_icon="⚽", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Sora:wght@400;600;700;800&display=swap');

:root {
    --bg-dark: #0b0b16;
    --bg-darker: #07070d;
    --bg-card: #12121f;
    --accent-pink: #ff2f7b;
    --accent-pink-hover: #e0195f;
    --accent-purple: #4a0f3d;
    --text-light: #f5f5f7;
    --text-muted: #9a9aab;
    --border-soft: rgba(255,255,255,0.12);
}

html, body, [class*="css"], .stApp {
    font-family: 'Sora', sans-serif;
}

.stApp {
    background: var(--bg-dark);
    color: var(--text-light);
}

/* Sidebar styling overrides */
[data-testid="stSidebar"] {
    background-color: var(--accent-pink) !important;
}
[data-testid="stSidebar"] * {
    color: #ffffff !important;
}
[data-testid="stSidebarCollapseButton"] {
    background-color: var(--accent-pink) !important;
    color: #ffffff !important;
    border-radius: 50% !important;
    border: 2px solid rgba(255,255,255,0.5) !important;
}
[data-testid="stSidebarCollapseButton"]:hover {
    background-color: var(--accent-pink-hover) !important;
}

header[data-testid="stHeader"] {
    background-color: transparent !important;
    background: transparent !important;
}

.block-container {
    padding-top: 1.5rem;
}

/* Custom Dark Tables */
table {
    width: 100%;
    color: var(--text-light) !important;
    background-color: var(--bg-card) !important;
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid var(--border-soft) !important;
    margin-bottom: 1rem !important;
}
th {
    background-color: rgba(255, 47, 123, 0.15) !important;
    color: var(--accent-pink) !important;
    font-family: 'Space Mono', monospace !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding: 12px 16px !important;
    border-bottom: 1px solid var(--border-soft) !important;
}
td {
    padding: 12px 16px !important;
    border-bottom: 1px solid var(--border-soft) !important;
    font-size: 0.85rem !important;
    color: var(--text-light) !important;
}
tr:last-child td {
    border-bottom: none !important;
}
tr:hover td {
    background-color: rgba(255, 255, 255, 0.04) !important;
}

/* UI Elements */
div[data-testid="stPopover"] button,
div[data-testid="stPopover"] > button,
button[data-testid="stBaseButton-secondary"],
.stPopover > button {
    background-color: var(--bg-card) !important;
    background: var(--bg-card) !important;
    border: 1px solid var(--border-soft) !important;
    border-radius: 8px !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}

div[data-testid="stPopover"] button p,
button[data-testid="stBaseButton-secondary"] p {
    color: var(--text-light) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
}

div[data-testid="stPopover"] button:hover,
button[data-testid="stBaseButton-secondary"]:hover {
    background-color: rgba(255, 47, 123, 0.15) !important;
    background: rgba(255, 47, 123, 0.15) !important;
    border-color: var(--accent-pink) !important;
}

div[data-baseweb="select"] > div,
div[data-baseweb="base-input"],
div[data-baseweb="input"] > div {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-soft) !important;
    color: var(--text-light) !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] * {
    color: var(--text-light) !important;
}

ul[role="listbox"],
ul[data-baseweb="menu"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-soft) !important;
}

li[role="option"] {
    color: var(--text-light) !important;
    background-color: var(--bg-card) !important;
}

li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
    background-color: rgba(255, 47, 123, 0.18) !important;
    color: var(--accent-pink) !important;
}

.stSelectbox label,
label[data-testid="stWidgetLabel"] p {
    color: var(--text-light) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
}

h1, h2, h3 {
    font-family: 'Sora', sans-serif;
    font-weight: 800;
    color: var(--text-light);
}

.hero-title {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, #0b0b16 0%, #3a0f34 40%, #ff2f7b 120%);
    padding: 40px 36px;
    border-radius: 18px;
    margin-top: 15px;
    margin-bottom: 28px;
    border: 1px solid rgba(255,255,255,0.06);
}
.hero-title h1 {
    font-family: 'Sora', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1.15;
    margin: 0;
    color: #ffffff;
}
.hero-title .accent {
    background: linear-gradient(90deg, #ff2f7b, #ff8fb8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.stButton > button[kind="primary"] {
    background-color: var(--accent-pink) !important;
    color: white !important;
    border: none;
    border-radius: 8px;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    padding: 8px 16px;
}
.stButton > button[kind="primary"]:hover {
    background-color: var(--accent-pink-hover) !important;
}
.stButton > button:disabled {
    background-color: #333344 !important;
    color: #777788 !important;
    cursor: not-allowed;
}

hr { border-color: var(--border-soft) !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# TOP NAVIGATION BAR
# ----------------------------------------------------------------------------
NAV_ITEMS = [
    ("instructions", "ℹ️ Instructions"),
    ("stats", "📈 Player Attributes"),
    ("squad", "🧩 Squad & Tactics"),
    ("play", "▶️ Play Matchday"),
    ("table", "📊 League Table"),
    ("fixtures", "📅 Fixtures & Results"),
    ("awards", "🏆 Season Awards"),
]

if "page" not in st.session_state:
    st.session_state.page = "instructions"

nav_cols = st.columns(len(NAV_ITEMS))
for col, (page_id, label) in zip(nav_cols, NAV_ITEMS):
    with col:
        if st.button(
            label,
            key=f"top_nav_{page_id}",
            use_container_width=True,
            type="primary" if st.session_state.page == page_id else "secondary",
        ):
            st.session_state.page = page_id
            st.rerun()

# --------------------------------------------------------------------------
# 1. Data loading
# --------------------------------------------------------------------------
ATTR_RENAME = {
    "Goal.Scoring": "Goal-Scoring",
    "Assist.Creation": "Assist-Creation",
}
RAW_ATTR_MAX = 19

def _repair_mojibake(value):
    if not isinstance(value, str):
        return value
    try:
        return value.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return value

def _robust_read_csv(path: str) -> pd.DataFrame:
    with open(path, "rb") as f:
        raw = f.read()
    line_sep = b"\r\n" if b"\r\n" in raw else b"\n"
    decoded_lines = []
    for line in raw.split(line_sep):
        try:
            decoded_lines.append(line.decode("utf-8"))
        except UnicodeDecodeError:
            decoded_lines.append(line.decode("latin-1"))
    df = pd.read_csv(io.StringIO("\n".join(decoded_lines)))
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(_repair_mojibake)
    return df

@st.cache_data
def load_data() -> pd.DataFrame:
    df = _robust_read_csv("DATA.csv")
    df = df.rename(columns=ATTR_RENAME)
    df["Player"] = df["Player"].astype(str).str.strip()
    df["Team"] = df["Team"].astype(str).str.strip()

    dup_rank = df.groupby(["Team", "Player"]).cumcount()
    df["Player"] = np.where(
        dup_rank > 0, df["Player"] + " (" + (dup_rank + 1).astype(str) + ")", df["Player"]
    )

    df["OVR"] = df.apply(_overall_rating, axis=1)
    df["PlayerID"] = df["Team"] + " | " + df["Player"]
    return df

@st.cache_data
def load_predictions_data() -> pd.DataFrame:
    try:
        return pd.read_excel("predicted_final_league_position.xlsx")
    except Exception:
        return pd.DataFrame()

@st.cache_data
def get_team_strength_modifiers(df: pd.DataFrame) -> dict:
    modifiers = {}
    if df.empty: return modifiers
    pos_cols = [c for c in df.columns if str(c).isdigit()]
    positions = np.array([int(c) for c in pos_cols])
    
    for idx, row in df.iterrows():
        team = str(row['Team']).strip()
        probs = row[pos_cols].values.astype(float) / 100.0
        # Expected Rank E[Rank] = Sum(Position * Probability)
        exp_rank = np.sum(positions * probs)
        # Center baseline around 9.5 (average rank in an 18-team league)
        multiplier = 1.0 + (9.5 - exp_rank) * 0.015
        modifiers[team] = {
            "exp_rank": round(exp_rank, 2),
            "modifier": round(multiplier, 3)
        }
    return modifiers

PREDICTIONS_DF = load_predictions_data()
TEAM_STRENGTH_DATA = get_team_strength_modifiers(PREDICTIONS_DF)

# --------------------------------------------------------------------------
# 2. Rating model & Tactics
# --------------------------------------------------------------------------
POSITION_ORDER = ["GK", "CB", "FB & WB", "MF", "AM & W", "CF"]

POS_WEIGHTS = {
    "GK":      {"Goalkeeping": 0.60, "Defense": 0.20, "Physical": 0.20},
    "CB":      {"Defense": 0.40, "Physical": 0.25, "Possession": 0.15, "Attack": 0.10, "Dribbling": 0.10},
    "FB & WB": {"Defense": 0.25, "Physical": 0.20, "Possession": 0.20, "Dribbling": 0.20, "Attack": 0.15},
    "MF":      {"Possession": 0.30, "Assist-Creation": 0.20, "Defense": 0.20, "Physical": 0.15, "Attack": 0.15},
    "AM & W":  {"Attack": 0.25, "Assist-Creation": 0.25, "Dribbling": 0.25, "Goal-Scoring": 0.15, "Possession": 0.10},
    "CF":      {"Goal-Scoring": 0.40, "Attack": 0.25, "Dribbling": 0.15, "Physical": 0.10, "Possession": 0.10},
}

def _overall_rating(row) -> float:
    w = POS_WEIGHTS.get(row.get("Position"), POS_WEIGHTS["MF"])
    raw = sum(row.get(k, RAW_ATTR_MAX / 2) * v for k, v in w.items())
    return round(min(99.0, raw * (99.0 / RAW_ATTR_MAX)), 1)

# Every pitch slot has a specific role/side (RCB, RB, DM, LW ...), but the data only
# knows six broad positions. "group" is the data position a slot is filled from.
# The four weights say how much a slot contributes to the team's attack / defence
# down the flanks ("wide") and through the middle ("cent").
def _slot(name, group, att_wide, att_cent, def_wide, def_cent):
    return {"name": name, "group": group, "att_wide": att_wide, "att_cent": att_cent,
            "def_wide": def_wide, "def_cent": def_cent}

SLOT_INFO = {
    "GK":  _slot("Goalkeeper",                    "GK",      0.00, 0.00, 0.00, 0.35),
    "LCB": _slot("Left Centre-Back",              "CB",      0.00, 0.00, 0.15, 1.00),
    "CB":  _slot("Centre-Back",                   "CB",      0.00, 0.00, 0.10, 1.00),
    "RCB": _slot("Right Centre-Back",             "CB",      0.00, 0.00, 0.15, 1.00),
    "LB":  _slot("Left-Back",                     "FB & WB", 0.60, 0.05, 1.00, 0.15),
    "RB":  _slot("Right-Back",                    "FB & WB", 0.60, 0.05, 1.00, 0.15),
    "LWB": _slot("Left Wing-Back",                "FB & WB", 0.85, 0.05, 0.80, 0.10),
    "RWB": _slot("Right Wing-Back",               "FB & WB", 0.85, 0.05, 0.80, 0.10),
    "DM":  _slot("Defensive Midfielder",          "MF",      0.10, 0.15, 0.30, 0.70),
    "LDM": _slot("Left Defensive Midfielder",     "MF",      0.10, 0.15, 0.30, 0.70),
    "RDM": _slot("Right Defensive Midfielder",    "MF",      0.10, 0.15, 0.30, 0.70),
    "LCM": _slot("Left Central Midfielder",       "MF",      0.25, 0.50, 0.20, 0.40),
    "CM":  _slot("Central Midfielder",            "MF",      0.20, 0.55, 0.20, 0.45),
    "RCM": _slot("Right Central Midfielder",      "MF",      0.25, 0.50, 0.20, 0.40),
    "LM":  _slot("Left Midfielder",               "AM & W",  1.00, 0.30, 0.40, 0.05),
    "RM":  _slot("Right Midfielder",              "AM & W",  1.00, 0.30, 0.40, 0.05),
    "LW":  _slot("Left Winger",                   "AM & W",  1.00, 0.30, 0.25, 0.00),
    "RW":  _slot("Right Winger",                  "AM & W",  1.00, 0.30, 0.25, 0.00),
    "AM":  _slot("Attacking Midfielder",          "AM & W",  0.20, 1.00, 0.00, 0.10),
    "LAM": _slot("Left Attacking Midfielder",     "AM & W",  0.50, 0.75, 0.10, 0.05),
    "RAM": _slot("Right Attacking Midfielder",    "AM & W",  0.50, 0.75, 0.10, 0.05),
    "ST":  _slot("Striker",                       "CF",      0.15, 1.00, 0.00, 0.00),
    "LST": _slot("Left Striker",                  "CF",      0.35, 0.85, 0.00, 0.00),
    "RST": _slot("Right Striker",                 "CF",      0.35, 0.85, 0.00, 0.00),
}

# Pitch layout per formation, listed GK -> defence -> midfield -> attack.
# Each slot: (depth, lateral). depth: 0 = own goal, 1 = opponent goal.
# lateral: 0 = the team's left touchline, 1 = its right touchline.
FORMATION_LAYOUT = {
    "4-4-2": {
        "GK":  (0.08, 0.50),
        "LB":  (0.26, 0.12), "LCB": (0.22, 0.36), "RCB": (0.22, 0.64), "RB":  (0.26, 0.88),
        "LM":  (0.54, 0.12), "LCM": (0.46, 0.36), "RCM": (0.46, 0.64), "RM":  (0.54, 0.88),
        "LST": (0.82, 0.36), "RST": (0.82, 0.64),
    },
    "4-3-3": {
        "GK":  (0.08, 0.50),
        "LB":  (0.26, 0.12), "LCB": (0.22, 0.36), "RCB": (0.22, 0.64), "RB":  (0.26, 0.88),
        "DM":  (0.40, 0.50), "LCM": (0.52, 0.28), "RCM": (0.52, 0.72),
        "LW":  (0.74, 0.12), "ST":  (0.86, 0.50), "RW":  (0.74, 0.88),
    },
    "4-2-3-1": {
        "GK":  (0.08, 0.50),
        "LB":  (0.26, 0.12), "LCB": (0.22, 0.36), "RCB": (0.22, 0.64), "RB":  (0.26, 0.88),
        "LDM": (0.42, 0.36), "RDM": (0.42, 0.64),
        "LW":  (0.70, 0.12), "AM":  (0.68, 0.50), "RW":  (0.70, 0.88),
        "ST":  (0.86, 0.50),
    },
    "4-1-3-2": {
        "GK":  (0.08, 0.50),
        "LB":  (0.26, 0.12), "LCB": (0.22, 0.36), "RCB": (0.22, 0.64), "RB":  (0.26, 0.88),
        "DM":  (0.38, 0.50),
        "LM":  (0.58, 0.12), "AM":  (0.62, 0.50), "RM":  (0.58, 0.88),
        "LST": (0.84, 0.38), "RST": (0.84, 0.62),
    },
    "5-3-2": {
        "GK":  (0.08, 0.50),
        "LCB": (0.24, 0.30), "CB":  (0.20, 0.50), "RCB": (0.24, 0.70),
        "LWB": (0.42, 0.08), "RWB": (0.42, 0.92),
        "LCM": (0.52, 0.30), "CM":  (0.46, 0.50), "RCM": (0.52, 0.70),
        "LST": (0.82, 0.36), "RST": (0.82, 0.64),
    },
    "5-2-2-1": {
        "GK":  (0.08, 0.50),
        "LCB": (0.24, 0.30), "CB":  (0.20, 0.50), "RCB": (0.24, 0.70),
        "LWB": (0.44, 0.08), "RWB": (0.44, 0.92),
        "LCM": (0.46, 0.36), "RCM": (0.46, 0.64),
        "LAM": (0.68, 0.30), "RAM": (0.68, 0.70),
        "ST":  (0.86, 0.50),
    },
}
FORMATIONS = {name: list(layout) for name, layout in FORMATION_LAYOUT.items()}

MENTALITIES = ["Very Defensive", "Defensive", "Balanced", "Attacking", "Very Attacking"]
MENTALITY_MOD = {
    "Very Defensive": (-0.20, 0.15),
    "Defensive":       (-0.10, 0.08),
    "Balanced":        (0.00, 0.00),
    "Attacking":       (0.08, -0.10),
    "Very Attacking":  (0.15, -0.20),
} 

TEMPOS = ["Slow", "Normal", "Fast"]
TEMPO_VARIANCE = {"Slow": 0.85, "Normal": 1.0, "Fast": 1.2}

OOP_LINES = ["High line", "Medium-block", "Low defensive line"]
PRESS_TYPES = ["High Press", "Balanced", "Low Press"]

# Attacking preference: which lane the team tries to attack through.
ATTACK_PREFS = ["Balanced", "Focus on Wing Play", "Focus on Middle Play"]
# (share of the attack routed down the wings, share routed through the middle)
ATTACK_PREF_LANE_SPLIT = {"Balanced": (0.5, 0.5), "Focus on Wing Play": (0.75, 0.25), "Focus on Middle Play": (0.25, 0.75)}
# Middle play keeps the ball more; wing play is more direct.
ATTACK_PREF_POSSESSION_SHIFT = {"Balanced": 0.0, "Focus on Wing Play": -2.0, "Focus on Middle Play": 3.0}

SCORER_SLOT_BIAS = {"CF": 3.0, "AM & W": 2.0, "MF": 1.0, "FB & WB": 0.35, "CB": 0.15, "GK": 0.02}
ASSIST_SLOT_BIAS = {"AM & W": 3.0, "MF": 2.5, "CF": 1.5, "FB & WB": 1.5, "CB": 0.2, "GK": 0.01}

def slot_labels(formation: str):
    """[(data position group, slot code), ...] in display order for a formation."""
    return [(SLOT_INFO[code]["group"], code) for code in FORMATIONS[formation]]

def default_role_for(group: str) -> str:
    if group == "GK": return "GK"
    if group in ("CF", "AM & W"): return "Attack"
    if group == "MF": return "Balanced"
    return "Defensive"

def auto_select_xi(squad: pd.DataFrame, formation: str) -> pd.DataFrame:
    slots = slot_labels(formation)
    remaining = squad.copy()
    picks = []
    unfilled = []

    def add(group, code, r, oop):
        picks.append({
            "Slot": group, "Label": code, "Player": r["Player"], "Position": r["Position"],
            "OVR": round(r["OVR"] * 0.85, 1) if oop else r["OVR"], "OOP": oop,
        })

    # Pass 1: the best natural players of each group go into that group's slots.
    for group in POSITION_ORDER:
        group_slots = [code for g, code in slots if g == group]
        if not group_slots:
            continue
        pool = remaining[remaining["Position"] == group].sort_values("OVR", ascending=False)
        chosen = pool.head(len(group_slots))
        for code, (_, r) in zip(group_slots, chosen.iterrows()):
            add(group, code, r, False)
        unfilled += [(group, code) for code in group_slots[len(chosen):]]
        remaining = remaining.drop(chosen.index)

    # Pass 2: cover any shortage with the closest-position players left (out of position).
    # A keeper is never used as an outfielder.
    for group, code in unfilled:
        pool = remaining if group == "GK" else remaining[remaining["Position"] != "GK"]
        if pool.empty:
            continue
        g_idx = POSITION_ORDER.index(group)
        dist = pool["Position"].map(lambda p: abs(POSITION_ORDER.index(p) - g_idx) if p in POSITION_ORDER else 99)
        r = pool.assign(_dist=dist).sort_values(["_dist", "OVR"], ascending=[True, False]).iloc[0]
        add(group, code, r, True)
        remaining = remaining.drop(r.name)

    return pd.DataFrame(picks)

def lineup_from_manual(squad: pd.DataFrame, assignments: dict, formation: str) -> pd.DataFrame:
    labels = slot_labels(formation)
    
    rows = []
    for pos, label in labels:
        key = (pos, label)
        player = assignments.get(key)
        
        # If the user selected a valid player, map them to the pitch
        if player and player != "Select Player":
            r = squad[squad["Player"] == player]
            if not r.empty:
                r = r.iloc[0]
                rows.append({
                    "Slot": pos,
                    "Label": label,
                    "Player": player,
                    "Position": r["Position"],
                    "OVR": r["OVR"] if r["Position"] == pos else round(r["OVR"] * 0.85, 1),
                    "OOP": r["Position"] != pos
                })
                continue
                
        # Otherwise, preserve the empty slot explicitly so the pitch updates correctly
        rows.append({
            "Slot": pos,
            "Label": label,
            "Player": "Select Player",
            "Position": pos,
            "OVR": 50.0,
            "OOP": False
        })
        
    return pd.DataFrame(rows)

# --------------------------------------------------------------------------
# 3. Match engine
# --------------------------------------------------------------------------
def _role_weight(role: str, w: float, phase: str) -> float:
    """Attack-minded players count more going forward and less in defence (and vice versa)."""
    if role == "Attack":
        if phase == "att": return w * 1.35
        if phase == "def": return w * 0.65
    elif role == "Defensive":
        if phase == "def": return w * 1.35
        if phase == "att": return w * 0.65
    return w

def lane_ratings(xi: pd.DataFrame, team_name: str = None) -> dict:
    """Quality of a team's attack and defence down the flanks ("wide") vs through the middle ("cent")."""
    labels = xi["Label"].tolist() if "Label" in xi.columns else [None] * len(xi)
    ovrs = xi["OVR"].tolist()
    roles = xi["Role"].tolist() if "Role" in xi.columns else ["Balanced"] * len(xi)
    out = {}
    for key in ("att_wide", "att_cent", "def_wide", "def_cent"):
        phase = "att" if key.startswith("att") else "def"
        num, den = 0.0, 0.0
        for label, ovr, role in zip(labels, ovrs, roles):
            info = SLOT_INFO.get(label)
            if not info or info[key] <= 0:
                continue
            w = _role_weight(role, info[key], phase)
            num += ovr * w
            den += w
        out[key] = num / den if den else 45.0
    if team_name and team_name in TEAM_STRENGTH_DATA:
        mod = TEAM_STRENGTH_DATA[team_name]["modifier"]
        out = {k: v * mod for k, v in out.items()}
    return out

def style_matchup_bonus(own: dict, opp: dict, style: str) -> float:
    """xG shift from routing the attack through a lane, relative to a balanced approach.
    Positive when the chosen lane is where this team is strong / the opponent is weak."""
    wing_edge = own["att_wide"] - opp["def_wide"]
    mid_edge = own["att_cent"] - opp["def_cent"]
    w_wide, w_cent = ATTACK_PREF_LANE_SPLIT.get(style, ATTACK_PREF_LANE_SPLIT["Balanced"])
    chosen = w_wide * wing_edge + w_cent * mid_edge
    neutral = 0.5 * (wing_edge + mid_edge)
    return (chosen - neutral) / 20

def phase_ratings(xi: pd.DataFrame, mentality: str = "Balanced", team_name: str = None) -> dict:
    slots = xi["Slot"].tolist()
    ovrs = xi["OVR"].tolist()
    roles = xi["Role"].tolist() if "Role" in xi.columns else ["Balanced"] * len(slots)

    def bucket(weights, phase):
        num, den = 0.0, 0.0
        for slot, w in weights.items():
            for s, ovr, role in zip(slots, ovrs, roles):
                if s == slot:
                    adj_w = _role_weight(role, w, phase)
                    num += ovr * adj_w
                    den += adj_w
        return num / den if den else 45.0

    d = bucket({"GK": 0.35, "CB": 1.0, "FB & WB": 0.6, "MF": 0.15}, "def")
    m = bucket({"MF": 1.0, "AM & W": 0.4, "FB & WB": 0.25, "CB": 0.1, "CF": 0.1}, "mid")
    a = bucket({"CF": 1.0, "AM & W": 0.9, "MF": 0.25, "FB & WB": 0.1}, "att")
    
    # Apply Pre-season Matrix Strength Modifier
    if team_name and team_name in TEAM_STRENGTH_DATA:
        mod = TEAM_STRENGTH_DATA[team_name]["modifier"]
        d *= mod
        m *= mod
        a *= mod

    att_mod, def_mod = MENTALITY_MOD[mentality]
    return {"def": d * (1 + def_mod), "mid": m, "att": a * (1 + att_mod),
            "lanes": lane_ratings(xi, team_name)}

# ---- Type of Play (playing philosophy) ---------------------------------------
PLAY_TYPE_NAMES = ["Balanced", "Gegenpress", "Tiki-taka", "Catenaccio", "Counter-attack"]

# All effects are xG changes per match (or multipliers).
#   gain_att / gain_def  scale with how well the XI suits the style ("execution quality" q)
#   cost_att / cost_def  are paid regardless of how well the players suit it
#   favourite            bonus for being the stronger side (negative = better as the underdog)
#   home                 bonus at home, same size penalty away
#   poss                 possession shift in points; fatigue / cards are multipliers
PLAY_TYPES = {
    "Balanced": dict(
        gain_att=0.05, gain_def=0.05, cost_att=-0.04, cost_def=0.04, favourite=0.0, home=0.0, poss=0.0, fatigue=1.0, cards=1.0,
        desc="The all-round approach: small but reliable benefits and no extreme upside or downside. Rewards "
             "well-rounded players, moderate settings (balanced mentality, normal tempo, medium line, balanced "
             "pressing) and balanced roles."),
    "Gegenpress": dict(
        gain_att=0.22, gain_def=0.06, cost_att=-0.10, cost_def=0.15, favourite=0.06, home=0.03, poss=2.0, fatigue=1.8, cards=1.35,
        desc="Win the ball back high up, straight after losing it. Suits fit, aggressive, attacking players "
             "(Physical, Defense, Attack). Tires the team much faster, picks up more cards and leaves space behind "
             "for counter-attacks. Better for the stronger side, and at home."),
    "Tiki-taka": dict(
        gain_att=0.14, gain_def=0.12, cost_att=-0.10, cost_def=0.12, favourite=0.08, home=0.02, poss=7.0, fatigue=1.0, cards=0.85,
        desc="Short passing and long spells of possession, so the opponent rarely has the ball. Suits technical players "
             "(Possession, Dribbling, Assist-Creation). Struggles against a deep block (Catenaccio) and a high press "
             "(Gegenpress), and is vulnerable when the ball is lost."),
    "Catenaccio": dict(
        gain_att=0.0, gain_def=0.30, cost_att=-0.26, cost_def=0.0, favourite=-0.06, home=-0.02, poss=-6.0, fatigue=0.8, cards=1.25,
        desc="Deep, compact and disciplined: concede very little and rely on rare chances. Suits strong defenders and a "
             "good keeper (Defense, Physical, Goalkeeping). Fewer goals at both ends and less possession; best for the "
             "underdog, and it frustrates Tiki-taka."),
    "Counter-attack": dict(
        gain_att=0.20, gain_def=0.10, cost_att=-0.10, cost_def=0.10, favourite=-0.06, home=-0.03, poss=-6.0, fatigue=0.9, cards=1.0,
        desc="Sit back, absorb pressure and break quickly. Suits quick, clinical forwards and wingers (Dribbling, "
             "Goal-Scoring, Attack) behind a solid defence. Thrives against teams that push forward (Gegenpress, "
             "Tiki-taka), as the underdog and away from home; gets nothing against a team that also sits deep."),
}

# How much space the opponent leaves behind them (what a counter-attack feeds on).
PLAY_TYPE_OPENNESS = {"Balanced": 0.6, "Gegenpress": 1.0, "Tiki-taka": 0.9, "Catenaccio": 0.2, "Counter-attack": 0.4}

# Style-vs-style xG bonus for the first team.
PLAY_TYPE_MATCHUP = {
    "Gegenpress":     {"Tiki-taka": 0.10, "Catenaccio": -0.05, "Counter-attack": -0.08},
    "Tiki-taka":      {"Gegenpress": -0.08, "Catenaccio": -0.10, "Counter-attack": 0.03},
    "Catenaccio":     {"Tiki-taka": 0.03},
    "Counter-attack": {"Gegenpress": 0.12, "Tiki-taka": 0.08, "Catenaccio": -0.08},
}

# Which players a style runs through (scorer / assist weight multipliers by position group).
PLAY_TYPE_SCORER_TILT = {
    "Gegenpress":     {"MF": 1.25, "AM & W": 1.15},
    "Tiki-taka":      {"MF": 1.25, "AM & W": 1.10, "CF": 0.95},
    "Catenaccio":     {"CB": 1.8, "CF": 0.90},
    "Counter-attack": {"CF": 1.15, "AM & W": 1.25, "MF": 0.85},
}
PLAY_TYPE_ASSIST_TILT = {
    "Gegenpress":     {"MF": 1.15, "AM & W": 1.15},
    "Tiki-taka":      {"MF": 1.30, "FB & WB": 0.90},
    "Counter-attack": {"AM & W": 1.25, "MF": 1.10},
}

# What each style asks of the players: (position groups, {attribute: weight}, component weight).
_OUTFIELD = ("CB", "FB & WB", "MF", "AM & W", "CF")
PLAY_TYPE_PROFILE = {
    "Balanced": [
        (_OUTFIELD, {"Attack": 1 / 7, "Assist-Creation": 1 / 7, "Goal-Scoring": 1 / 7, "Physical": 1 / 7,
                     "Defense": 1 / 7, "Possession": 1 / 7, "Dribbling": 1 / 7}, 0.8),
        (("GK",), {"Goalkeeping": 1.0}, 0.2),
    ],
    "Gegenpress": [(_OUTFIELD, {"Physical": 0.45, "Defense": 0.25, "Attack": 0.30}, 1.0)],
    "Tiki-taka": [
        (("FB & WB", "MF", "AM & W", "CF"), {"Possession": 0.50, "Dribbling": 0.20, "Assist-Creation": 0.30}, 0.7),
        (("CB",), {"Possession": 1.0}, 0.3),
    ],
    "Catenaccio": [
        (("CB", "FB & WB", "MF"), {"Defense": 0.65, "Physical": 0.35}, 0.75),
        (("GK",), {"Goalkeeping": 1.0}, 0.25),
    ],
    "Counter-attack": [
        (("AM & W", "CF"), {"Dribbling": 0.30, "Goal-Scoring": 0.30, "Attack": 0.40}, 0.55),
        (("CB", "FB & WB", "MF"), {"Defense": 0.60, "Physical": 0.40}, 0.30),
        (("MF",), {"Assist-Creation": 1.0}, 0.15),
    ],
}

def _play_type_raw(play_type: str, xi: pd.DataFrame, attrs: pd.DataFrame):
    """Average attribute quality (raw 1-19 scale) of the XI for what this style asks of its players."""
    comps = PLAY_TYPE_PROFILE.get(play_type)
    if not comps:
        return None
    players, slots = xi["Player"].tolist(), xi["Slot"].tolist()
    known = set(attrs.index)
    total, wsum = 0.0, 0.0
    for groups, attr_w, comp_w in comps:
        names = [p for p, s in zip(players, slots) if s in groups and p in known]
        if not names:
            continue
        sub = attrs.loc[names]
        score = np.zeros(len(names))
        for attr, w in attr_w.items():
            col = sub[attr].to_numpy(dtype=float) if attr in sub.columns else np.full(len(names), RAW_ATTR_MAX / 2)
            score += w * col
        total += comp_w * float(score.mean())
        wsum += comp_w
    return total / wsum if wsum else None

@st.cache_data(show_spinner=False)
def _cached_play_type_raw(team: str, assignment: tuple, play_type: str):
    """_play_type_raw for a club's XI, cached by (club, who plays where, style) so season sims stay fast."""
    xi = pd.DataFrame(list(assignment), columns=["Slot", "Player"])
    return _play_type_raw(play_type, xi, DF[DF["Team"] == team].set_index("Player"))

@st.cache_data
def compute_play_type_baseline(_df: pd.DataFrame) -> dict:
    """Mean / std of each style's requirement score across every club's best XI: the yardstick for 'fit'."""
    raws = {t: [] for t in PLAY_TYPE_PROFILE}
    for _, squad in _df.groupby("Team"):
        xi = auto_select_xi(squad, "4-3-3")
        attrs = squad.set_index("Player")
        for t in raws:
            v = _play_type_raw(t, xi, attrs)
            if v is not None:
                raws[t].append(v)
    return {t: (float(np.mean(v)), float(np.std(v))) for t, v in raws.items() if v}

def play_type_player_fit(play_type: str, xi: pd.DataFrame, team: str) -> float:
    """0-1: how well this XI's players suit the style compared with the other clubs (0.5 = league average)."""
    if play_type not in PLAY_TYPE_BASELINE:
        return 0.5
    valid = xi[xi["Player"] != "Select Player"]
    raw = _cached_play_type_raw(team, tuple(zip(valid["Slot"].tolist(), valid["Player"].tolist())), play_type)
    mean, std = PLAY_TYPE_BASELINE[play_type]
    if raw is None or std < 1e-9:
        return 0.5
    return float(np.clip(0.5 + 0.25 * (raw - mean) / std, 0.0, 1.0))

# ---- Squad fit = players + tactical settings + player roles -------------------
FIT_WEIGHT_PLAYERS, FIT_WEIGHT_TACTICS, FIT_WEIGHT_ROLES = 0.50, 0.30, 0.20

# How well each tactical setting suits a Type of Play: +1 ideal, 0 neutral, -1 works against it.
PLAY_TYPE_SETTING_FIT = {
    "Balanced": {
        "formation": {"4-4-2": 0.8, "4-3-3": 0.8, "4-2-3-1": 1.0, "4-1-3-2": 0.6, "5-3-2": 0.2, "5-2-2-1": 0.0},
        "mentality": {"Very Defensive": -0.6, "Defensive": 0.4, "Balanced": 1.0, "Attacking": 0.4, "Very Attacking": -0.6},
        "tempo":     {"Slow": 0.1, "Normal": 1.0, "Fast": 0.1},
        "line":      {"High line": 0.1, "Medium-block": 1.0, "Low defensive line": 0.1},
        "pressing":  {"High Press": 0.1, "Balanced": 1.0, "Low Press": 0.1},
        "attack":    {"Balanced": 1.0, "Focus on Wing Play": 0.2, "Focus on Middle Play": 0.2},
    },
    "Gegenpress": {
        "formation": {"4-3-3": 1.0, "4-2-3-1": 0.8, "4-1-3-2": 0.7, "4-4-2": 0.5, "5-3-2": -0.4, "5-2-2-1": -0.6},
        "mentality": {"Very Defensive": -1.0, "Defensive": -0.6, "Balanced": 0.2, "Attacking": 1.0, "Very Attacking": 0.8},
        "tempo":     {"Slow": -1.0, "Normal": 0.2, "Fast": 1.0},
        "line":      {"High line": 1.0, "Medium-block": 0.2, "Low defensive line": -1.0},
        "pressing":  {"High Press": 1.0, "Balanced": 0.0, "Low Press": -1.0},
        "attack":    {"Balanced": 0.0, "Focus on Wing Play": 0.2, "Focus on Middle Play": 0.2},
    },
    "Tiki-taka": {
        "formation": {"4-3-3": 1.0, "4-2-3-1": 0.8, "4-1-3-2": 0.4, "4-4-2": -0.2, "5-3-2": -0.6, "5-2-2-1": -0.3},
        "mentality": {"Very Defensive": -0.8, "Defensive": -0.4, "Balanced": 0.6, "Attacking": 1.0, "Very Attacking": 0.2},
        "tempo":     {"Slow": 1.0, "Normal": 0.6, "Fast": -0.6},
        "line":      {"High line": 1.0, "Medium-block": 0.5, "Low defensive line": -0.8},
        "pressing":  {"High Press": 0.5, "Balanced": 0.4, "Low Press": -0.8},
        "attack":    {"Balanced": 0.3, "Focus on Wing Play": -0.5, "Focus on Middle Play": 1.0},
    },
    "Catenaccio": {
        "formation": {"5-3-2": 1.0, "5-2-2-1": 1.0, "4-4-2": 0.3, "4-1-3-2": 0.2, "4-2-3-1": 0.0, "4-3-3": -0.6},
        "mentality": {"Very Defensive": 1.0, "Defensive": 1.0, "Balanced": 0.0, "Attacking": -0.8, "Very Attacking": -1.0},
        "tempo":     {"Slow": 1.0, "Normal": 0.3, "Fast": -0.7},
        "line":      {"Low defensive line": 1.0, "Medium-block": 0.4, "High line": -1.0},
        "pressing":  {"Low Press": 1.0, "Balanced": 0.3, "High Press": -1.0},
        "attack":    {"Balanced": 0.2, "Focus on Middle Play": 0.2, "Focus on Wing Play": -0.2},
    },
    "Counter-attack": {
        "formation": {"4-1-3-2": 0.9, "4-4-2": 1.0, "4-2-3-1": 0.8, "5-3-2": 0.7, "5-2-2-1": 0.6, "4-3-3": 0.5},
        "mentality": {"Very Defensive": 0.3, "Defensive": 1.0, "Balanced": 0.8, "Attacking": -0.4, "Very Attacking": -0.8},
        "tempo":     {"Slow": -0.8, "Normal": 0.4, "Fast": 1.0},
        "line":      {"Low defensive line": 1.0, "Medium-block": 0.5, "High line": -0.8},
        "pressing":  {"Low Press": 0.9, "Balanced": 0.4, "High Press": -0.7},
        "attack":    {"Focus on Wing Play": 0.8, "Focus on Middle Play": 0.3, "Balanced": 0.2},
    },
}
# How much each setting counts towards the tactics score.
PLAY_TYPE_SETTING_WEIGHT = {"formation": 1.0, "mentality": 1.2, "tempo": 0.8, "line": 1.0, "pressing": 1.0, "attack": 0.5}
PLAY_TYPE_SETTING_LABEL = {"formation": "Formation", "mentality": "Mentality", "tempo": "Tempo",
                           "line": "Defensive line", "pressing": "Pressing", "attack": "Attacking preference"}

# The stance each style wants from each position group: -1 = Defensive, 0 = Balanced, +1 = Attack.
ROLE_VALUE = {"Attack": 1.0, "Balanced": 0.0, "Defensive": -1.0}
PLAY_TYPE_ROLE_TARGET = {
    "Balanced":       {"CB": 0.0,  "FB & WB": 0.0,  "MF": 0.0,  "AM & W": 0.0, "CF": 0.0},
    "Gegenpress":     {"CB": 0.0,  "FB & WB": 0.5,  "MF": 0.4,  "AM & W": 1.0, "CF": 1.0},
    "Tiki-taka":      {"CB": 0.0,  "FB & WB": 0.0,  "MF": 0.0,  "AM & W": 0.5, "CF": 0.3},
    "Catenaccio":     {"CB": -1.0, "FB & WB": -1.0, "MF": -0.7, "AM & W": -0.5, "CF": 0.0},
    "Counter-attack": {"CB": -0.6, "FB & WB": -0.3, "MF": -0.2, "AM & W": 1.0, "CF": 1.0},
}

def _verdict(score: float) -> str:
    return "good" if score >= 0.5 else "poor" if score <= -0.3 else "ok"

def play_type_squad_fit(play_type: str, xi: pd.DataFrame, team: str, formation: str, mentality: str,
                        tempo: str, line: str, pressing: str, attack_pref: str) -> dict:
    """Squad fit (0-1) for a Type of Play. It combines
       - the players' attributes (50%),
       - how well every tactical setting you picked suits the style (30%),
       - how well each outfield player's role (Attack / Balanced / Defensive) suits it (20%).
    Balanced rewards well-rounded players, moderate settings and balanced roles."""
    if play_type not in PLAY_TYPE_SETTING_FIT:
        return {"fit": 0.5, "players": 0.5, "tactics": 0.5, "roles": 0.5, "details": []}

    players = play_type_player_fit(play_type, xi, team)

    chosen = {"formation": formation, "mentality": mentality, "tempo": tempo,
              "line": line, "pressing": pressing, "attack": attack_pref}
    table = PLAY_TYPE_SETTING_FIT[play_type]
    scores = {k: table[k].get(v, 0.0) for k, v in chosen.items()}
    wsum = sum(PLAY_TYPE_SETTING_WEIGHT.values())
    c_set = sum(PLAY_TYPE_SETTING_WEIGHT[k] * s for k, s in scores.items()) / wsum
    details = [(PLAY_TYPE_SETTING_LABEL[k], chosen[k], _verdict(scores[k])) for k in chosen]

    targets = PLAY_TYPE_ROLE_TARGET[play_type]
    vals = []
    roles = xi["Role"].tolist() if "Role" in xi.columns else ["Balanced"] * len(xi)
    for slot, player, role in zip(xi["Slot"].tolist(), xi["Player"].tolist(), roles):
        if slot == "GK" or player == "Select Player":
            continue
        vals.append(1.0 - abs(ROLE_VALUE.get(role, 0.0) - targets.get(slot, 0.0)))
    c_role = float(np.mean(vals)) if vals else 0.0
    details.append(("Player roles", "", _verdict(c_role)))

    tactics, roles = (c_set + 1) / 2, (c_role + 1) / 2
    fit = FIT_WEIGHT_PLAYERS * players + FIT_WEIGHT_TACTICS * tactics + FIT_WEIGHT_ROLES * roles
    return {"fit": float(np.clip(fit, 0.0, 1.0)), "players": players, "tactics": tactics, "roles": roles, "details": details}

def play_type_quality(fit: float) -> float:
    """Execution quality: 1.0 for an average fit, 1.75 for a perfect one, 0.25 for a terrible one."""
    return 0.25 + 1.5 * fit

def play_type_xg_effect(own: str, own_fit: float, opp: str, opp_fit: float,
                        own_strength: float, opp_strength: float, is_home: bool) -> float:
    """xG change for `own` from both sides' Type of Play: the style itself, how well the players suit it,
    the matchup against the opponent's style, who is the favourite, and home / away."""
    p, o = PLAY_TYPES[own], PLAY_TYPES[opp]
    q, oq = play_type_quality(own_fit), play_type_quality(opp_fit)
    gain_att = p["gain_att"] * q
    if own == "Counter-attack":
        gain_att *= PLAY_TYPE_OPENNESS.get(opp, 0.6)
    gap = float(np.clip((own_strength - opp_strength) / 8.0, -1.0, 1.0))
    bonus = (gain_att + p["cost_att"]
             + PLAY_TYPE_MATCHUP.get(own, {}).get(opp, 0.0)
             + p["favourite"] * gap + p["home"] * (1 if is_home else -1)
             - o["gain_def"] * oq + o["cost_def"])
    return float(np.clip(bonus, -0.6, 0.6))

def play_type_possession_shift(play_type: str, fit: float) -> float:
    return PLAY_TYPES[play_type]["poss"] * float(np.clip(play_type_quality(fit), 0.5, 1.5))

def generate_team_stats(xg: float, goals: int, possession: float, press: str, rng, card_mult: float = 1.0) -> dict:
    """Box-score numbers for one team, kept consistent with the simulated xG, goals and possession."""
    shots = max(goals, int(rng.poisson(xg / 0.11)))
    on_target = max(goals, int(rng.binomial(shots, 0.36)))
    shots = max(shots, on_target)
    corners = int(rng.poisson(shots * 0.35))

    card_rate = {"High Press": 1.85, "Balanced": 1.5, "Low Press": 1.35}.get(press, 1.5) * card_mult
    return {
        "xg": round(float(xg), 2), "possession": int(round(possession)),
        "shots": shots, "on_target": on_target, "corners": corners,
        "yellow_cards": int(rng.poisson(card_rate)),
    }

def get_match_rating(base_xg, goals, is_cs, rng, is_scorer):
    rating = 6.0 + rng.normal(0, 0.5) + (base_xg * 0.2)
    if is_scorer:
        rating += 1.5
    if is_cs:
        rating += 0.8
    return round(min(10.0, max(3.0, rating)), 1)

# ---- Scoring model -------------------------------------------------------------
# Expected goals are built in log space and measured in standard deviations of the league's own spread of
# attack / midfield / defence ratings, so results stay realistic whatever scale the player data uses, and no
# stack of tactical effects can push the chances to zero (or to absurd levels).
XG_BASE = 1.17                                  # xG of an average side against an average side
XG_ATT_SLOPE, XG_MID_SLOPE = 0.20, 0.07         # log-xG per standard deviation of attack-vs-defence / midfield gap
XG_HOME_LOG_PER_ADV = 0.50                      # home_adv (in xG) -> log-xG, +for the home side and - for the away side
MENTALITY_LOG_SCALE = 0.9                       # MENTALITY_MOD (rating %) -> log-xG
TACTIC_LOG_CAP, XG_REF = 0.40, 1.25             # style + Type of Play can change a side's xG by at most about +-33%
TACTIC_TOTAL_CAP = 0.50                         # ALL tactical choices together (mentality, line, tempo, style, Type of Play)
XG_MIN, XG_MAX = 0.30, 3.8
LINE_ATT_MOD = {"High line": 0.05, "Medium-block": 0.0, "Low defensive line": -0.05}
LINE_DEF_MOD = {"High line": -0.05, "Medium-block": 0.0, "Low defensive line": 0.05}

@st.cache_data
def compute_phase_baseline(_df: pd.DataFrame) -> dict:
    """Mean / std of attack, midfield and defence ratings across every club's best XI (with the pre-season
    strength modifier): the yardstick that turns a rating gap into scoring chances."""
    vals = {"att": [], "mid": [], "def": []}
    for team, squad in _df.groupby("Team"):
        xi = auto_select_xi(squad, "4-3-3")
        xi["Role"] = xi["Slot"].apply(default_role_for)
        r = phase_ratings(xi, "Balanced", team_name=team)
        for k in vals:
            vals[k].append(r[k])
    return {k: (float(np.mean(v)), max(float(np.std(v)), 1.0)) for k, v in vals.items()}

def simulate_match(home_xi, away_xi, 
                   home_mentality="Balanced", away_mentality="Balanced",
                   home_tempo="Normal", away_tempo="Normal",
                   home_line="Medium-block", away_line="Medium-block",
                   home_press="Balanced", away_press="Balanced",
                   home_pref="Balanced", away_pref="Balanced",
                   home_type="Balanced", away_type="Balanced", home_fit=0.5, away_fit=0.5,
                   home_adv=0.28, rng=None, home_team=None, away_team=None):
    rng = rng or np.random.default_rng()
    
    # Ratings without mentality; mentality and the defensive line enter as bounded log-xG terms below
    h = phase_ratings(home_xi, "Balanced", team_name=home_team)
    a = phase_ratings(away_xi, "Balanced", team_name=away_team)
    zh = {k: (h[k] - PHASE_BASELINE[k][0]) / PHASE_BASELINE[k][1] for k in ("att", "mid", "def")}
    za = {k: (a[k] - PHASE_BASELINE[k][0]) / PHASE_BASELINE[k][1] for k in ("att", "mid", "def")}

    style_home = style_matchup_bonus(h["lanes"], a["lanes"], home_pref)
    style_away = style_matchup_bonus(a["lanes"], h["lanes"], away_pref)

    # overall strength in standard deviations (x6 = the rating-point scale Type of Play's favourite term expects)
    home_strength = 6.0 * (zh["att"] + zh["mid"] + zh["def"]) / 3
    away_strength = 6.0 * (za["att"] + za["mid"] + za["def"]) / 3
    type_home = play_type_xg_effect(home_type, home_fit, away_type, away_fit, home_strength, away_strength, True)
    type_away = play_type_xg_effect(away_type, away_fit, home_type, home_fit, away_strength, home_strength, False)

    def tactic_log(xg_delta):
        return TACTIC_LOG_CAP * float(np.tanh(xg_delta / XG_REF / TACTIC_LOG_CAP))

    h_att_m, h_def_m = MENTALITY_MOD[home_mentality]
    a_att_m, a_def_m = MENTALITY_MOD[away_mentality]
    def all_tactics_log(att_mod, opp_def_mod, line, opp_line, style_and_type, tempo):
        """Every tactical choice summed, then softly capped so no stack of choices can wipe out (or inflate) chances."""
        total = (MENTALITY_LOG_SCALE * (att_mod - opp_def_mod) + LINE_ATT_MOD[line] - LINE_DEF_MOD[opp_line]
                 + tactic_log(style_and_type) + np.log(TEMPO_VARIANCE[tempo]))
        return TACTIC_TOTAL_CAP * float(np.tanh(total / TACTIC_TOTAL_CAP))

    log_home = (np.log(XG_BASE) + XG_HOME_LOG_PER_ADV * home_adv
                + XG_ATT_SLOPE * (zh["att"] - za["def"]) + XG_MID_SLOPE * (zh["mid"] - za["mid"])
                + all_tactics_log(h_att_m, a_def_m, home_line, away_line, style_home + type_home, home_tempo))
    log_away = (np.log(XG_BASE) - XG_HOME_LOG_PER_ADV * home_adv
                + XG_ATT_SLOPE * (za["att"] - zh["def"]) + XG_MID_SLOPE * (za["mid"] - zh["mid"])
                + all_tactics_log(a_att_m, h_def_m, away_line, home_line, style_away + type_away, away_tempo))
    xg_home = float(np.clip(np.exp(log_home), XG_MIN, XG_MAX))
    xg_away = float(np.clip(np.exp(log_away), XG_MIN, XG_MAX))

    hg = int(rng.poisson(xg_home))
    ag = int(rng.poisson(xg_away))

    press_mod = {"High Press": 0.06, "Balanced": 0.0, "Low Press": -0.04}
    base_possession_home = 50 + np.clip((zh["mid"] - za["mid"]) * 6.0, -22, 22)
    press_poss_shift = (press_mod[home_press] - press_mod[away_press]) * 50
    style_poss_shift = ATTACK_PREF_POSSESSION_SHIFT[home_pref] - ATTACK_PREF_POSSESSION_SHIFT[away_pref]
    type_poss_shift = play_type_possession_shift(home_type, home_fit) - play_type_possession_shift(away_type, away_fit)
    possession_home = np.clip(base_possession_home + press_poss_shift + style_poss_shift + type_poss_shift, 20, 80)
    
    return {
        "home_goals": hg, "away_goals": ag,
        "xg_home": round(xg_home, 2), "xg_away": round(xg_away, 2),
        "possession_home": round(possession_home, 1),
        "play_type_bonus_home": round(type_home, 3), "play_type_bonus_away": round(type_away, 3),
        "stats_home": generate_team_stats(xg_home, hg, possession_home, home_press, rng, PLAY_TYPES[home_type]["cards"]),
        "stats_away": generate_team_stats(xg_away, ag, 100 - possession_home, away_press, rng, PLAY_TYPES[away_type]["cards"]),
    }

# ---- Bench & substitutions ------------------------------------------------
BENCH_SIZE = 7
SUB_COUNT_WEIGHTS = {3: 0.20, 4: 0.30, 5: 0.50}          # substitutions used per match
MAX_SUB_MOMENTS = 3                                       # a team may only change players at 3 separate moments
SUB_MOMENT_WEIGHTS = {1: 0.10, 2: 0.35, 3: 0.55}          # how many of those moments a team actually uses
SUB_OFF_GROUP_WEIGHT = {"CF": 1.3, "AM & W": 1.3, "MF": 1.1, "FB & WB": 1.0, "CB": 0.6}
FATIGUE_START, FATIGUE_SPAN, FATIGUE_MAX_DROP = 55, 35, 0.12   # -12% by minute 90 on the pitch

def _group_distance(pos_a: str, pos_b: str) -> int:
    if pos_a not in POSITION_ORDER or pos_b not in POSITION_ORDER:
        return 99
    return abs(POSITION_ORDER.index(pos_a) - POSITION_ORDER.index(pos_b))

def auto_select_bench(squad: pd.DataFrame, starters, size: int = BENCH_SIZE) -> pd.DataFrame:
    """A sensible bench: a keeper, then the best cover for each outfield group, then the best of the rest."""
    remaining = squad[~squad["Player"].isin(list(starters))].sort_values("OVR", ascending=False)
    picks = []
    for group in ["GK", "CB", "FB & WB", "MF", "AM & W", "CF"]:
        pool = remaining[remaining["Position"] == group]
        if not pool.empty:
            picks.append(pool.index[0])
            remaining = remaining.drop(pool.index[0])
    for idx in remaining[remaining["Position"] != "GK"].index:
        if len(picks) >= size:
            break
        picks.append(idx)
    return squad.loc[picks[:size]]

def _fatigue(minutes_on_pitch, mult: float = 1.0):
    """Performance multiplier after N minutes on the pitch (1.0 while fresh). `mult` scales how fast a style tires players."""
    return 1.0 - FATIGUE_MAX_DROP * mult * np.clip((np.asarray(minutes_on_pitch, dtype=float) - FATIGUE_START) / FATIGUE_SPAN, 0, 1)

_FATIGUE_MEAN_90 = float(_fatigue(np.arange(90)).mean())

def plan_substitutions(xi: pd.DataFrame, bench: pd.DataFrame, rng) -> list:
    """Decide who comes off, when, and who replaces them. Tired / weaker / attacking players go off first;
    the replacement is the best bench player for that position (closest position if there is none)."""
    starters = xi[(xi["Player"] != "Select Player") & (xi["Slot"] != "GK")]
    if bench is None or len(bench) == 0:
        return []
    outfield_bench = bench[bench["Position"] != "GK"]
    if starters.empty or outfield_bench.empty:
        return []
    s_player, s_label, s_slot = starters["Player"].tolist(), starters["Label"].tolist(), starters["Slot"].tolist()
    s_role = starters["Role"].tolist() if "Role" in starters.columns else ["Balanced"] * len(s_player)
    s_ovr = starters["OVR"].to_numpy(dtype=float)
    b_player, b_pos = outfield_bench["Player"].tolist(), outfield_bench["Position"].tolist()
    b_ovr = outfield_bench["OVR"].astype(float).tolist()

    n = int(rng.choice(list(SUB_COUNT_WEIGHTS), p=list(SUB_COUNT_WEIGHTS.values())))
    n = min(n, len(s_player), len(b_player))
    w = (np.clip(110 - s_ovr, 5, None) / 50) * np.array([SUB_OFF_GROUP_WEIGHT.get(g, 1.0) for g in s_slot])
    off_idx = rng.choice(len(s_player), size=n, replace=False, p=w / w.sum())

    # Substitutions happen in at most MAX_SUB_MOMENTS separate moments (half-time counts as one); several players
    # can change at the same moment. Every moment used has at least one substitution.
    k = int(rng.choice(list(SUB_MOMENT_WEIGHTS), p=list(SUB_MOMENT_WEIGHTS.values())))
    k = max(1, min(k, MAX_SUB_MOMENTS, n))
    moments = np.sort(rng.choice(np.arange(46, 86), size=k, replace=False))
    moment_of = list(range(k)) + [int(m) for m in rng.integers(0, k, size=n - k)]
    plan = sorted(((int(moments[m]), int(i)) for m, i in zip(moment_of, off_idx)), key=lambda t: t[0])

    available = list(range(len(b_player)))
    subs = []
    for minute, i in plan:
        j = min(available, key=lambda k: (_group_distance(b_pos[k], s_slot[i]), -b_ovr[k], k))
        natural = b_pos[j] == s_slot[i]
        subs.append({
            "minute": int(minute), "label": s_label[i], "slot": s_slot[i], "role": s_role[i],
            "off": s_player[i], "on": b_player[j], "on_position": b_pos[j],
            "on_ovr": b_ovr[j] if natural else round(b_ovr[j] * 0.85, 1),
        })
        available.remove(j)
    return subs

def build_roster(xi: pd.DataFrame, subs: list) -> pd.DataFrame:
    """Starters + substitutes, each with the minute they came on / went off."""
    roster = xi.copy()
    roster["on_min"] = 0
    roster["off_min"] = 91          # 91 = still on the pitch at full time
    extra = []
    for s in subs:
        roster.loc[roster["Label"] == s["label"], "off_min"] = s["minute"]
        extra.append({
            "Slot": s["slot"], "Label": s["label"], "Player": s["on"], "Position": s["on_position"],
            "OVR": s["on_ovr"], "OOP": s["on_position"] != s["slot"], "Role": s["role"],
            "on_min": s["minute"], "off_min": 91,
        })
    if extra:
        roster = pd.concat([roster, pd.DataFrame(extra)], ignore_index=True)
    return roster

def effective_xi(roster: pd.DataFrame, fatigue_mult: float = 1.0) -> pd.DataFrame:
    """One row per slot whose OVR is the minutes-weighted, fatigue-adjusted rating of whoever played there.
    A starter who plays all 90 minutes keeps exactly his own OVR; fresh legs help late on."""
    totals = {}
    for label, ovr, on, off in zip(roster["Label"].tolist(), roster["OVR"].tolist(),
                                   roster["on_min"].tolist(), roster["off_min"].tolist()):
        on, off = int(on), min(int(off), 90)
        if off <= on:
            continue
        share = float(_fatigue(np.arange(on, off) - on, fatigue_mult).sum()) / (90 * _FATIGUE_MEAN_90)
        totals[label] = totals.get(label, 0.0) + float(ovr) * share
    base = roster[roster["on_min"] == 0].copy()
    base["OVR"] = base["Label"].map(totals).fillna(base["OVR"])
    return base.drop(columns=["on_min", "off_min"])

def _style_assist_mult(label: str, style: str) -> float:
    """Wing play routes chances through wide players, middle play through central ones."""
    info = SLOT_INFO.get(label)
    if not info or style == "Balanced":
        return 1.0
    lane = info["att_wide"] if style == "Focus on Wing Play" else info["att_cent"]
    return 1.0 + 0.5 * lane

def pick_goal_events(xi: pd.DataFrame, n_goals: int, rng=None, style: str = "Balanced", play_type: str = "Balanced"):
    """Scorers and assisters are drawn from the players on the pitch at the minute of the goal.
    `xi` may be a roster with on_min / off_min columns (starters + substitutes)."""
    valid_xi = xi[xi["Player"] != "Select Player"].copy()
    if n_goals <= 0 or valid_xi.empty:
        return []
    rng = rng or np.random.default_rng()
    if "on_min" not in valid_xi:
        valid_xi["on_min"], valid_xi["off_min"] = 0, 91

    valid_xi["w_score"] = (valid_xi["Slot"].map(SCORER_SLOT_BIAS).fillna(0.5) * (valid_xi["OVR"] / 50.0)).clip(lower=0.01)
    valid_xi["w_assist"] = (valid_xi["Slot"].map(ASSIST_SLOT_BIAS).fillna(0.5) * (valid_xi["OVR"] / 50.0)).clip(lower=0.01)
    valid_xi["w_assist"] *= valid_xi["Label"].map(lambda c: _style_assist_mult(c, style))
    valid_xi["w_score"] *= valid_xi["Slot"].map(lambda g: PLAY_TYPE_SCORER_TILT.get(play_type, {}).get(g, 1.0))
    valid_xi["w_assist"] *= valid_xi["Slot"].map(lambda g: PLAY_TYPE_ASSIST_TILT.get(play_type, {}).get(g, 1.0))

    events = []
    for _ in range(n_goals):
        minute = int(rng.integers(1, 91))
        on_pitch = valid_xi[(valid_xi["on_min"] <= minute) & (minute < valid_xi["off_min"])]
        if on_pitch.empty:
            on_pitch = valid_xi
        scorer = rng.choice(on_pitch["Player"].to_numpy(), p=(on_pitch["w_score"] / on_pitch["w_score"].sum()).to_numpy())

        assister = None
        if len(on_pitch) > 1 and rng.random() < 0.75:
            assist_pool = on_pitch[on_pitch["Player"] != scorer]
            if not assist_pool.empty:
                assister = rng.choice(assist_pool["Player"].to_numpy(),
                                      p=(assist_pool["w_assist"] / assist_pool["w_assist"].sum()).to_numpy())

        events.append({"minute": minute, "scorer": scorer, "assist": assister})

    events.sort(key=lambda x: x["minute"])
    return events

CARD_SLOT_WEIGHT = {"GK": 0.15, "CB": 1.2, "FB & WB": 1.3, "MF": 1.6, "AM & W": 0.9, "CF": 0.9}
CARD_REASONS = [("Foul", 0.45), ("Tactical foul", 0.15), ("Dissent", 0.10), ("Time wasting", 0.10),
                ("Simulation", 0.07), ("Unsporting behaviour", 0.07), ("Handball", 0.06)]

def pick_card_events(xi: pd.DataFrame, n_cards: int, rng=None):
    """Yellow cards: different players, more likely for midfielders and full-backs, and only while on the pitch."""
    valid_xi = xi[xi["Player"] != "Select Player"].reset_index(drop=True)
    n = min(int(n_cards), len(valid_xi))
    if n <= 0:
        return []
    rng = rng or np.random.default_rng()
    on_min = valid_xi["on_min"] if "on_min" in valid_xi else pd.Series(0, index=valid_xi.index)
    off_min = valid_xi["off_min"] if "off_min" in valid_xi else pd.Series(91, index=valid_xi.index)
    played = (off_min.clip(upper=90) - on_min).clip(lower=1) / 90.0
    w = (valid_xi["Slot"].map(CARD_SLOT_WEIGHT).fillna(1.0) * played).to_numpy(dtype=float)
    picked = rng.choice(len(valid_xi), size=n, replace=False, p=w / w.sum())
    names = [r for r, _ in CARD_REASONS]
    probs = np.array([p for _, p in CARD_REASONS])
    events = []
    for i in picked:
        lo = max(3, int(on_min.iloc[i]))
        hi = min(90, int(off_min.iloc[i]) - 1)
        minute = int(rng.integers(lo, hi + 1)) if hi >= lo else lo
        events.append({"minute": minute, "player": valid_xi.iloc[i]["Player"],
                       "reason": str(rng.choice(names, p=probs / probs.sum()))})
    events.sort(key=lambda e: e["minute"])
    return events

def build_match_report(home, away, round_no, result, home_events, away_events, home_cards, away_cards,
                       home_subs=(), away_subs=(), home_tactics="", away_tactics="") -> dict:
    """One timeline (goals with running score, cards and substitutions) plus the box-score stats."""
    events = []
    for side, subs in (("home", home_subs), ("away", away_subs)):
        for s in subs:
            events.append({"minute": s["minute"], "side": side, "type": "sub", "player": s["on"], "off": s["off"]})
    for side, goals in (("home", home_events), ("away", away_events)):
        for e in goals:
            events.append({"minute": e["minute"], "side": side, "type": "goal",
                           "player": e["scorer"], "assist": e.get("assist")})
    for side, cards in (("home", home_cards), ("away", away_cards)):
        for e in cards:
            events.append({"minute": e["minute"], "side": side, "type": "card",
                           "player": e["player"], "reason": e["reason"]})
    events.sort(key=lambda e: (e["minute"], {"goal": 0, "card": 1, "sub": 2}[e["type"]]))
    hs = as_ = 0
    for e in events:
        if e["type"] == "goal":
            if e["side"] == "home": hs += 1
            else: as_ += 1
            e["score"] = (hs, as_)
    return {
        "home": home, "away": away, "round": round_no, "home_tactics": home_tactics, "away_tactics": away_tactics,
        "hg": result["home_goals"], "ag": result["away_goals"],
        "stats_home": result["stats_home"], "stats_away": result["stats_away"],
        "events": events,
    }

MR_HOME_COLOR, MR_AWAY_COLOR, MR_MUTED_COLOR = "#ff2f7b", "#3b82f6", "#4b5563"

MATCH_REPORT_CSS = """
<style>
.mr-wrap { max-width: 780px; margin: 0 auto 1rem auto; font-family: 'Sora', sans-serif; }
.mr-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 18px 22px; margin-bottom: 14px;
    background: linear-gradient(115deg, #12121f 0%, #3a0f34 100%); border: 1px solid var(--border-soft); border-radius: 12px; }
.mr-team { flex: 1; font-weight: 800; font-size: 1.05rem; color: #fff; }
.mr-team.away { text-align: right; }
.mr-score { font-family: 'Space Mono', monospace; font-size: 2rem; font-weight: 700; color: #fff; white-space: nowrap; }
.mr-tactics { display: flex; justify-content: space-between; gap: 12px; margin: -6px 4px 10px 4px; color: var(--text-muted);
    font-family: 'Space Mono', monospace; font-size: 0.68rem; }
.mr-sub { text-align: center; color: var(--text-muted); font-size: 0.7rem; font-family: 'Space Mono', monospace; margin: -6px 0 12px 0; }
.mr-card { background: var(--bg-card); border: 1px solid var(--border-soft); border-radius: 12px; overflow: hidden; margin-bottom: 14px; }
.mr-title { background: rgba(255,255,255,0.06); text-align: center; padding: 10px; color: var(--text-muted);
    font-family: 'Space Mono', monospace; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.14em; }
.mr-stat { padding: 12px 20px 6px 20px; }
.mr-stat-top { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; font-size: 0.85rem; color: var(--text-light); }
.mr-val { min-width: 110px; font-weight: 700; }
.mr-val.r { text-align: right; }
.mr-val small { color: var(--text-muted); font-weight: 400; font-size: 0.7rem; }
.mr-label { flex: 1; text-align: center; font-weight: 600; }
.mr-bars { display: flex; gap: 4px; margin-top: 6px; }
.mr-track { flex: 1; height: 7px; background: rgba(255,255,255,0.08); border-radius: 4px; display: flex; }
.mr-track.l { justify-content: flex-end; }
.mr-fill { height: 100%; border-radius: 4px; }
.mr-half { display: flex; justify-content: space-between; padding: 9px 18px; background: rgba(255,255,255,0.06);
    color: var(--text-muted); font-family: 'Space Mono', monospace; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.12em; }
.mr-ev { display: flex; align-items: center; gap: 10px; padding: 9px 18px; border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.82rem; color: var(--text-light); }
.mr-ev.away { flex-direction: row-reverse; }
.mr-ev:last-child { border-bottom: none; }
.mr-min { min-width: 34px; font-family: 'Space Mono', monospace; font-weight: 700; color: var(--text-muted); }
.mr-ev.away .mr-min { text-align: right; }
.mr-main { flex: 1; }
.mr-ev.away .mr-main { text-align: right; }
.mr-main i { color: var(--text-muted); font-style: normal; }
.mr-chip { display: inline-flex; align-items: center; gap: 6px; padding: 3px 9px; border-radius: 8px; white-space: nowrap;
    background: rgba(255,255,255,0.05); border: 1px solid var(--border-soft); font-family: 'Space Mono', monospace; font-size: 0.75rem; font-weight: 700; }
.mr-in { color: #22c55e; font-size: 0.7rem; }
.mr-out { color: #ef4444; font-size: 0.7rem; }
.mr-yc { display: inline-block; width: 10px; height: 14px; border-radius: 2px; background: #ffd400; }
.mr-empty { padding: 12px 18px; color: var(--text-muted); font-size: 0.8rem; }
</style>
"""

def _report_name(name) -> str:
    return html_lib.escape(re.sub(r"\s*\(\d+\)$", "", str(name)).strip())

def match_report_html(rep: dict) -> str:
    sh, sa = rep["stats_home"], rep["stats_away"]

    def bar_colors(h, a):
        if h > a: return MR_HOME_COLOR, MR_MUTED_COLOR
        if a > h: return MR_MUTED_COLOR, MR_AWAY_COLOR
        return MR_HOME_COLOR, MR_AWAY_COLOR

    def stat_row(label, h, a, h_txt=None, a_txt=None):
        total = h + a
        hw = 100 * h / total if total else 0
        aw = 100 * a / total if total else 0
        hc, ac = bar_colors(h, a)
        return (
            '<div class="mr-stat"><div class="mr-stat-top">'
            f'<span class="mr-val">{h_txt if h_txt is not None else h}</span>'
            f'<span class="mr-label">{label}</span>'
            f'<span class="mr-val r">{a_txt if a_txt is not None else a}</span></div>'
            '<div class="mr-bars">'
            f'<div class="mr-track l"><div class="mr-fill" style="width:{hw:.1f}%;background:{hc}"></div></div>'
            f'<div class="mr-track"><div class="mr-fill" style="width:{aw:.1f}%;background:{ac}"></div></div>'
            '</div></div>'
        )

    stats_html = "".join([
        stat_row("Expected goals (xG)", sh["xg"], sa["xg"], f'{sh["xg"]:.2f}', f'{sa["xg"]:.2f}'),
        stat_row("Ball possession", sh["possession"], sa["possession"], f'{sh["possession"]}%', f'{sa["possession"]}%'),
        stat_row("Total shots", sh["shots"], sa["shots"]),
        stat_row("Shots on target", sh["on_target"], sa["on_target"]),
        stat_row("Corners", sh["corners"], sa["corners"]),
        stat_row("Yellow cards", sh["yellow_cards"], sa["yellow_cards"]),
    ])

    def event_row(e):
        side = e["side"]
        if e["type"] == "goal":
            score = f'{e["score"][0]} · {e["score"][1]}'
            chip = f'⚽ {score}' if side == "home" else f'{score} ⚽'
            assist = f' <i>({_report_name(e["assist"])})</i>' if e.get("assist") else ""
            main = (f'<b>{_report_name(e["player"])}</b>{assist}' if side == "home"
                    else (f'<i>({_report_name(e["assist"])})</i> ' if e.get("assist") else "") + f'<b>{_report_name(e["player"])}</b>')
            chip_html = f'<span class="mr-chip">{chip}</span>'
        elif e["type"] == "sub":
            on_n, off_n = _report_name(e["player"]), _report_name(e["off"])
            main = f'<b>{on_n}</b> <i>{off_n}</i>' if side == "home" else f'<i>{off_n}</i> <b>{on_n}</b>'
            chip_html = '<span class="mr-chip"><span class="mr-in">&#9650;</span><span class="mr-out">&#9660;</span></span>'
        else:
            main = f'<b>{_report_name(e["player"])}</b> <i>({html_lib.escape(e["reason"])})</i>'
            chip_html = '<span class="mr-chip"><span class="mr-yc"></span></span>'
        return (f'<div class="mr-ev {side}"><span class="mr-min">{e["minute"]}\'</span>'
                f'{chip_html}<span class="mr-main">{main}</span></div>')

    def half_block(title, evs):
        hg = sum(1 for e in evs if e["type"] == "goal" and e["side"] == "home")
        ag = sum(1 for e in evs if e["type"] == "goal" and e["side"] == "away")
        body = "".join(event_row(e) for e in evs) or '<div class="mr-empty">No goals, cards or substitutions.</div>'
        return f'<div class="mr-half"><span>{title}</span><span>{hg} · {ag}</span></div>{body}'

    first = [e for e in rep["events"] if e["minute"] <= 45]
    second = [e for e in rep["events"] if e["minute"] > 45]

    return (
        MATCH_REPORT_CSS
        + '<div class="mr-wrap">'
        + f'<div class="mr-head"><span class="mr-team">{html_lib.escape(rep["home"])}</span>'
        + f'<span class="mr-score">{rep["hg"]} - {rep["ag"]}</span>'
        + f'<span class="mr-team away">{html_lib.escape(rep["away"])}</span></div>'
        + f'<div class="mr-tactics"><span>{html_lib.escape(rep.get("home_tactics", ""))}</span>'
        + f'<span>{html_lib.escape(rep.get("away_tactics", ""))}</span></div>'
        + f'<div class="mr-sub">MATCHDAY {rep["round"]} · FULL TIME</div>'
        + f'<div class="mr-card"><div class="mr-title">KEY STATS</div>{stats_html}</div>'
        + f'<div class="mr-card">{half_block("1ST HALF", first)}{half_block("2ND HALF", second)}</div>'
        + '</div>'
    )

# --------------------------------------------------------------------------
# 4. Season / schedule
# --------------------------------------------------------------------------
def round_robin_schedule(teams: list) -> list:
    teams = teams[:]
    if len(teams) % 2: teams.append(None)
    n = len(teams)
    rounds = []
    for r in range(n - 1):
        pairs = []
        for i in range(n // 2):
            t1, t2 = teams[i], teams[n - 1 - i]
            if t1 is not None and t2 is not None:
                pairs.append((t1, t2) if r % 2 == 0 else (t2, t1))
        rounds.append(pairs)
        teams.insert(1, teams.pop())
    second_leg = [[(b, a) for (a, b) in rnd] for rnd in rounds]
    return rounds + second_leg

def empty_table_row():
    return {"P": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0}

def update_table(table: dict, home: str, away: str, hg: int, ag: int):
    for t in (home, away): table[t]["P"] += 1
    table[home]["GF"] += hg; table[home]["GA"] += ag
    table[away]["GF"] += ag; table[away]["GA"] += hg
    if hg > ag:
        table[home]["W"] += 1; table[home]["Pts"] += 3; table[away]["L"] += 1
    elif hg < ag:
        table[away]["W"] += 1; table[away]["Pts"] += 3; table[home]["L"] += 1
    else:
        table[home]["D"] += 1; table[away]["D"] += 1
        table[home]["Pts"] += 1; table[away]["Pts"] += 1
    table[home]["GD"] = table[home]["GF"] - table[home]["GA"]
    table[away]["GD"] = table[away]["GF"] - table[away]["GA"]

def table_dataframe(table: dict) -> pd.DataFrame:
    df = pd.DataFrame(table).T
    df.index.name = "Team"
    df = df.reset_index()
    df = df.sort_values(["Pts", "GD", "GF"], ascending=False).reset_index(drop=True)
    df.index = df.index + 1
    df.index.name = "Pos"
    return df[["Team", "P", "W", "D", "L", "GF", "GA", "GD", "Pts"]]

# --------------------------------------------------------------------------
# 5. Streamlit app session
# --------------------------------------------------------------------------

DF = load_data()
PLAY_TYPE_BASELINE = compute_play_type_baseline(DF)
PHASE_BASELINE = compute_phase_baseline(DF)
ALL_TEAMS = sorted(DF["Team"].unique().tolist())

def init_session():
    ss = st.session_state
    ss.setdefault("season_started", False)
    ss.setdefault("user_team", None)
    ss.setdefault("formation", "4-3-3")
    ss.setdefault("mentality", "Balanced")
    ss.setdefault("tempo", "Normal")
    ss.setdefault("oop_line", "Medium-block")
    ss.setdefault("pressing", "Balanced")
    ss.setdefault("attack_pref", "Balanced")
    ss.setdefault("play_type", "Balanced")
    ss.setdefault("manual_lineup", {})   
    ss.setdefault("bench", [])
    ss.setdefault("player_roles", {})    
    ss.setdefault("locked_signature", None)
    ss.setdefault("schedule", [])
    ss.setdefault("matchday", 0)         
    ss.setdefault("table", {})
    ss.setdefault("scorers", {})
    ss.setdefault("assists", {})
    ss.setdefault("history", [])         
    ss.setdefault("last_commentary", None)
    ss.setdefault("player_ratings_sum", {})
    ss.setdefault("player_ratings_count", {})
    ss.setdefault("recent_match_ratings", [])
    ss.setdefault("last_match_viz", None)
    ss.setdefault("last_match_report", None)

init_session()
ss = st.session_state

def start_new_season(team: str):
    ss.user_team = team
    ss.season_started = True
    ss.formation = "4-3-3"
    ss.mentality = "Balanced"
    ss.tempo = "Normal"
    ss.oop_line = "Medium-block"
    ss.pressing = "Balanced"
    ss.attack_pref = "Balanced"
    ss.play_type = "Balanced"
    for attr in ("attack_pref", "play_type", "mentality", "tempo", "oop_line", "pressing"):
        ss.pop(f"{attr}_choice", None)
    ss.manual_lineup = {}
    ss.bench = []
    ss.pop("bench_select", None)
    ss.player_roles = {}
    ss.locked_signature = None
    teams = ALL_TEAMS[:]
    random.shuffle(teams)
    ss.schedule = round_robin_schedule(teams)
    ss.matchday = 0
    ss.table = {t: empty_table_row() for t in ALL_TEAMS}
    ss.scorers = {}
    ss.assists = {}
    ss.history = []
    ss.last_commentary = None
    ss.player_ratings_sum = {}
    ss.player_ratings_count = {}
    ss.recent_match_ratings = []
    ss.last_match_viz = None
    ss.last_match_report = None

def reset_all():
    keep_page = ss.get("page", "instructions")
    for key in list(ss.keys()): del ss[key]
    init_session()
    ss.page = keep_page

def get_user_squad():
    return DF[DF["Team"] == ss.user_team].copy()

def current_user_xi():
    squad = get_user_squad()
    xi = lineup_from_manual(squad, ss.manual_lineup, ss.formation)
    
    roles_list = []
    for _, row in xi.iterrows():
        key = (row["Slot"], row["Label"])
        roles_list.append(ss.player_roles.get(key, default_role_for(row["Slot"])))
    xi["Role"] = roles_list
    return xi

def sync_manual_lineup():
    labels = slot_labels(ss.formation)
    expected_keys = set(labels)
    if not ss.manual_lineup or set(ss.manual_lineup.keys()) != expected_keys:
        new_lineup = {}
        new_roles = {}
        for pos, label in labels:
            key = (pos, label)
            new_lineup[key] = "Select Player"
            new_roles[key] = default_role_for(pos)
        ss.manual_lineup = new_lineup
        ss.player_roles = new_roles

def current_tactics_signature():
    return (
        ss.formation, ss.mentality, ss.tempo, ss.oop_line, ss.pressing, ss.attack_pref, ss.play_type,
        tuple(sorted(ss.manual_lineup.items())), tuple(sorted(ss.bench)),
        tuple(sorted(ss.player_roles.items())),
    )

def tactic_select(label: str, options: list, attr: str, **kwargs):
    """A tactics dropdown with a stable widget key. Without a key Streamlit treats the dropdown as a new widget
    whenever its `index` changes, which can swallow a second change to the same dropdown."""
    key = f"{attr}_choice"
    if key not in ss:
        ss[key] = ss[attr]
    ss[attr] = st.selectbox(label, options, key=key, **kwargs)

def slot_widget_key(code: str) -> str:
    # Formation is part of the key so a formation change never reuses a stale widget value.
    return f"slot_{ss.formation}_{code}"

def role_widget_key(code: str) -> str:
    return f"role_{ss.formation}_{code}"

def apply_auto_pick():
    """Button callback: fill the XI with the best available players.

    The slot dropdowns are keyed widgets, so Streamlit keeps their value in session
    state and ignores `index=` after the first render. The dropdowns' own state has
    to be updated too, otherwise they keep saying "Select Player" and the selection
    loop overwrites the picks straight away.
    """
    auto_xi = auto_select_xi(get_user_squad(), ss.formation)
    for _, code in slot_labels(ss.formation):
        ss[slot_widget_key(code)] = "Select Player"
    for key in list(ss.manual_lineup):
        ss.manual_lineup[key] = "Select Player"
    for _, r in auto_xi.iterrows():
        ss.manual_lineup[(r["Slot"], r["Label"])] = r["Player"]
        ss[slot_widget_key(r["Label"])] = r["Player"]

def user_bench(xi: pd.DataFrame) -> pd.DataFrame:
    """The user's chosen bench; if none is chosen (or it is stale) the assistant manager picks one."""
    squad = get_user_squad()
    starters = set(xi["Player"])
    chosen = squad[squad["Player"].isin(ss.bench) & ~squad["Player"].isin(starters)]
    return chosen if not chosen.empty else auto_select_bench(squad, starters)

def apply_auto_bench():
    """Button callback (same keyed-widget rule as apply_auto_pick: set the widget's own state)."""
    starters = {p for p in ss.manual_lineup.values() if p and p != "Select Player"}
    ss["bench_select"] = auto_select_bench(get_user_squad(), starters)["Player"].tolist()

def is_team_locked() -> bool:
    sig = ss.get("locked_signature")
    return sig is not None and sig == current_tactics_signature()

@st.cache_data(show_spinner=False)
def cached_auto_xi(team: str, formation: str) -> pd.DataFrame:
    """A club's best XI for a formation (with default roles). Deterministic, so it is cached."""
    xi = auto_select_xi(DF[DF["Team"] == team], formation)
    xi["Role"] = xi["Slot"].apply(default_role_for)
    return xi

@st.cache_data(show_spinner=False)
def cached_auto_bench(team: str, starters: tuple) -> pd.DataFrame:
    return auto_select_bench(DF[DF["Team"] == team], list(starters))

def ai_lineup_for(team: str):
    formation = random.choice(["4-3-3", "4-4-2", "4-2-3-1", "4-1-3-2", "5-2-2-1"])
    mentality = random.choice(["Defensive", "Balanced", "Balanced", "Attacking"])
    tempo = random.choice(TEMPOS)
    line = random.choice(OOP_LINES)
    press = random.choice(PRESS_TYPES)
    style = random.choice(ATTACK_PREFS)
    xi = cached_auto_xi(team, formation)
    # Clubs lean towards the Type of Play their players suit best
    fits = [play_type_squad_fit(t, xi, team, formation, mentality, tempo, line, press, style)["fit"] for t in PLAY_TYPE_NAMES]
    play_type = random.choices(PLAY_TYPE_NAMES, weights=[float(np.exp(4 * (f - 0.5))) for f in fits])[0]
    return xi, mentality, tempo, line, press, formation, style, play_type

def play_fixture(home, away, rng):
    if home == ss.user_team:
        home_xi, home_ment, home_tempo, home_line, home_press, home_formation, home_pref, home_type = current_user_xi(), ss.mentality, ss.tempo, ss.oop_line, ss.pressing, ss.formation, ss.attack_pref, ss.play_type
    else:
        home_xi, home_ment, home_tempo, home_line, home_press, home_formation, home_pref, home_type = ai_lineup_for(home)
        
    if away == ss.user_team:
        away_xi, away_ment, away_tempo, away_line, away_press, away_formation, away_pref, away_type = current_user_xi(), ss.mentality, ss.tempo, ss.oop_line, ss.pressing, ss.formation, ss.attack_pref, ss.play_type
    else:
        away_xi, away_ment, away_tempo, away_line, away_press, away_formation, away_pref, away_type = ai_lineup_for(away)

    # Bench + substitutions are decided up front, so they shape the result (fresh legs, weaker cover)
    home_bench = user_bench(home_xi) if home == ss.user_team else cached_auto_bench(home, tuple(home_xi["Player"]))
    away_bench = user_bench(away_xi) if away == ss.user_team else cached_auto_bench(away, tuple(away_xi["Player"]))
    home_subs = plan_substitutions(home_xi, home_bench, rng)
    away_subs = plan_substitutions(away_xi, away_bench, rng)
    home_roster = build_roster(home_xi, home_subs)
    away_roster = build_roster(away_xi, away_subs)
    home_fit = play_type_squad_fit(home_type, home_xi, home, home_formation, home_ment, home_tempo,
                                   home_line, home_press, home_pref)["fit"]
    away_fit = play_type_squad_fit(away_type, away_xi, away, away_formation, away_ment, away_tempo,
                                   away_line, away_press, away_pref)["fit"]

    result = simulate_match(
        effective_xi(home_roster, PLAY_TYPES[home_type]["fatigue"]),
        effective_xi(away_roster, PLAY_TYPES[away_type]["fatigue"]), 
        home_ment, away_ment, 
        home_tempo, away_tempo, 
        home_line, away_line, 
        home_press, away_press, 
        home_pref=home_pref, away_pref=away_pref,
        home_type=home_type, away_type=away_type, home_fit=home_fit, away_fit=away_fit,
        rng=rng,
        home_team=home,
        away_team=away
    )
    
    home_events = pick_goal_events(home_roster, result["home_goals"], rng, style=home_pref, play_type=home_type)
    away_events = pick_goal_events(away_roster, result["away_goals"], rng, style=away_pref, play_type=away_type)

    for e in home_events + away_events:
        if e.get("scorer"):
            ss.scorers[e["scorer"]] = ss.scorers.get(e["scorer"], 0) + 1
        if e.get("assist"):
            ss.assists[e["assist"]] = ss.assists.get(e["assist"], 0) + 1

    update_table(ss.table, home, away, result["home_goals"], result["away_goals"])
    
    home_cs = result["away_goals"] == 0
    away_cs = result["home_goals"] == 0

    def process_player_stats(xi, goal_events, cs, xg, team_goals):
        stats = []
        scorers = [e["scorer"] for e in goal_events]
        assisters = [e["assist"] for e in goal_events if e["assist"]]
        for _, p in xi.iterrows():
            player_name = p["Player"]
            if player_name == "Select Player":
                continue
            minutes = int(min(p["off_min"], 90) - p["on_min"])
            g_count = scorers.count(player_name)
            a_count = assisters.count(player_name)
            is_scorer = g_count > 0
            r = get_match_rating(xg, team_goals, cs, rng, is_scorer)
            if minutes < 90:   # short cameos stay closer to a neutral 6.0
                r = round(6.0 + (r - 6.0) * (0.6 + 0.4 * minutes / 90), 1)
            if a_count > 0:
                r = round(min(10.0, r + 0.5 * a_count), 1)

            ss.player_ratings_sum[player_name] = ss.player_ratings_sum.get(player_name, 0) + r
            ss.player_ratings_count[player_name] = ss.player_ratings_count.get(player_name, 0) + 1

            stats.append({
                "Player": player_name,
                "Minutes Played": minutes,
                "Sub": f"▲ {int(p['on_min'])}'" if p["on_min"] > 0 else (f"▼ {int(p['off_min'])}'" if p["off_min"] <= 90 else ""),
                "Goal": g_count,
                "Assist": a_count,
                "Rating": r
            })
        return stats

    h_stats = process_player_stats(home_roster, home_events, home_cs, result["xg_home"], result["home_goals"])
    a_stats = process_player_stats(away_roster, away_events, away_cs, result["xg_away"], result["away_goals"])

    if home == ss.user_team:
        ss.recent_match_ratings = h_stats
    elif away == ss.user_team:
        ss.recent_match_ratings = a_stats

    if ss.user_team in (home, away):
        # Snapshot exactly what was actually selected/simulated for this
        # fixture, so the 2D viewer can mirror the real formations, tactics
        # and player roles instead of a generic placeholder shape.
        keep_cols = ["Slot", "Label", "Player", "Position", "OVR", "Role"]
        ss.last_match_viz = {
            "home_team": home, "away_team": away,
            "home_formation": home_formation, "home_mentality": home_ment,
            "home_tempo": home_tempo, "home_line": home_line, "home_press": home_press, "home_pref": home_pref, "home_type": home_type,
            "away_formation": away_formation, "away_mentality": away_ment,
            "away_tempo": away_tempo, "away_line": away_line, "away_press": away_press, "away_pref": away_pref, "away_type": away_type,
            "home_xi": home_xi[keep_cols].to_dict("records"),
            "away_xi": away_xi[keep_cols].to_dict("records"),
        }

    if ss.user_team in (home, away):
        home_cards = pick_card_events(home_roster, result["stats_home"]["yellow_cards"], rng)
        away_cards = pick_card_events(away_roster, result["stats_away"]["yellow_cards"], rng)
        def tactics_label(ptype, fit, pref):
            label = f"{ptype} · {round(fit * 100)}% fit"
            return label if pref == "Balanced" else f"{label} · {pref.replace('Focus on ', '')}"
        ss.last_match_report = build_match_report(
            home, away, ss.matchday + 1, result, home_events, away_events, home_cards, away_cards,
            home_subs, away_subs,
            tactics_label(home_type, home_fit, home_pref), tactics_label(away_type, away_fit, away_pref)
        )

    ss.history.append({
        "round": ss.matchday + 1, "home": home, "away": away,
        "hg": result["home_goals"], "ag": result["away_goals"],
        "is_user": ss.user_team in (home, away),
        "home_events": home_events, "away_events": away_events,
    })
    return result, home_events, away_events

def play_next_matchday():
    if ss.matchday >= len(ss.schedule): return None
    rng = np.random.default_rng()
    round_fixtures = ss.schedule[ss.matchday]
    user_result = None
    for home, away in round_fixtures:
        result, he, ae = play_fixture(home, away, rng)
        if ss.user_team in (home, away):
            user_result = (home, away, result, he, ae)
            
    if user_result:
        home, away, result, he, ae = user_result
        lines = [f"Full time at {home}'s ground: {home} {result['home_goals']}-{result['away_goals']} {away}."]
        lines.append(f"Expected Goals: {result['xg_home']} - {result['xg_away']} | Possession: {result['possession_home']}% - {100-result['possession_home']}%")
        
        events = [(e["minute"], "home", e["scorer"], e["assist"]) for e in he] + \
                 [(e["minute"], "away", e["scorer"], e["assist"]) for e in ae]
        events.sort(key=lambda x: x[0])

        for min_, side, scorer, assister in events:
            team_name = home if side == "home" else away
            assist_str = f" (Assist: {assister})" if assister else ""
            lines.append(f"⚽ GOAL! {min_}' - {scorer} ({team_name}){assist_str}")
        ss.last_commentary = lines
    else:
        ss.last_commentary = None
    ss.matchday += 1

def simulate_to_end():
    while ss.matchday < len(ss.schedule):
        play_next_matchday()

# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.title("⚽ Liga Portugal Manager")
    st.caption("Liga Portugal 2026/27")

    if ss.season_started:
        st.metric("Managing", ss.user_team)
        st.metric("Matchday", f"{min(ss.matchday + 1, len(ss.schedule))} / {len(ss.schedule)}")
        st.divider()
        if st.button("🔄 Restart Game", use_container_width=True):
            reset_all()
            st.rerun()

# --------------------------------------------------------------------------
# Main area View Renders
# --------------------------------------------------------------------------

def style_player_attributes(df: pd.DataFrame):
    exclude_cols = ["OVR", "P", "W", "D", "L", "GF", "GA", "GD", "Pts", "round", "Season"]
    num_cols = [c for c in df.select_dtypes(include=np.number).columns if c not in exclude_cols]
    
    if not num_cols:
        return df

    def color_scale(val):
        if not isinstance(val, (int, float)) or pd.isna(val):
            return ''
        if val <= 3:
            return 'background-color: rgba(255, 75, 75, 0.4);'
        elif val <= 7:
            return 'background-color: rgba(255, 150, 50, 0.4);'
        elif val <= 11:
            return 'background-color: rgba(220, 220, 50, 0.3);'
        elif val <= 15:
            return 'background-color: rgba(100, 220, 100, 0.3);'
        else:
            return 'background-color: rgba(50, 180, 50, 0.5);'
            
    styler = df.style
    if hasattr(styler, "map"):
        styler = styler.map(color_scale, subset=num_cols)
    else:
        styler = styler.applymap(color_scale, subset=num_cols)
        
    return styler.format("{:.0f}", subset=num_cols)


def render_instructions():
    st.markdown(
        """
<div class="hero-title">
<h1>⚽ Welcome to <span class="accent">Liga Portugal Manager</span></h1>
<p>A Football-Manager-style game built on real Liga Portugal squads.
No transfer market — you manage exactly the players your club already has.</p>
</div>
""",
        unsafe_allow_html=True,
    )

    if not ss.season_started:
        st.subheader("🏁 Start Your Career")
        st.markdown("Select a club below to begin managing.")
        
        teams = ALL_TEAMS[:]
        for i in range(0, len(teams), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(teams):
                    t = teams[i+j]
                    if cols[j].button(t, use_container_width=True, key=f"btn_start_{t}"):
                        start_new_season(t)
                        ss.page = "squad"
                        st.rerun()

def render_need_season_prompt():
    st.info("👋 Go to **ℹ️ Instructions** to pick a club and start the season.")

def squad_fit_header_html(formation: str, play_type: str, fit_info) -> str:
    """Heading above the pitch: the formation, and a box with the squad fit for the chosen Type of Play.
    `fit_info` is play_type_squad_fit(...) or None while the XI is incomplete."""
    head_css = "display:flex;align-items:center;justify-content:space-between;gap:12px;margin:0 0 8px 0;"
    title = f'<span style="font-size:1.05rem;font-weight:700;">🏟️ {html_lib.escape(formation)} Shape</span>'
    box_base = ("display:inline-flex;flex-direction:column;gap:3px;min-width:190px;padding:6px 12px;border-radius:10px;"
                "background:var(--bg-card);border:1px solid {border};")
    label_css = ("font-family:'Space Mono',monospace;font-size:0.6rem;letter-spacing:0.08em;"
                 "text-transform:uppercase;color:var(--text-muted);")
    muted = "font-size:0.8rem;color:var(--text-muted);"

    if fit_info is None:
        box = (f'<span style="{box_base.format(border="var(--border-soft)")}">'
               f'<span style="{label_css}">Squad fit · {html_lib.escape(play_type)}</span>'
               f'<span style="{muted}">Pick your full XI</span></span>')
    else:
        pct = round(fit_info["fit"] * 100)
        color, verdict = (("#22c55e", "Good fit") if pct >= 60 else ("#f59e0b", "Average fit") if pct >= 40 else ("#ef4444", "Poor fit"))
        tip_lines = [f'{label}{": " + value if value else ""} ({v})' for label, value, v in fit_info["details"]]
        tip = html_lib.escape("&#10;".join(tip_lines), quote=True).replace("&amp;#10;", "&#10;")
        parts = (f'Players {round(fit_info["players"] * 100)}% · Tactics {round(fit_info["tactics"] * 100)}% · '
                 f'Roles {round(fit_info["roles"] * 100)}%')
        box = (f'<span title="{tip}" style="{box_base.format(border=color)}">'
               f'<span style="{label_css}">Squad fit · {html_lib.escape(play_type)}</span>'
               f'<span style="display:flex;align-items:baseline;gap:8px;">'
               f'<b style="font-size:1.35rem;line-height:1;color:{color};">{pct}%</b>'
               f'<span style="font-size:0.72rem;color:var(--text-muted);">{verdict}</span></span>'
               f'<span style="display:block;height:4px;border-radius:2px;background:rgba(255,255,255,0.1);">'
               f'<span style="display:block;height:4px;border-radius:2px;width:{pct}%;background:{color};"></span></span>'
               f'<span style="font-size:0.62rem;color:var(--text-muted);">{parts}</span></span>')
    return f'<div style="{head_css}">{title}{box}</div>'

def generate_pitch_html(xi_df: pd.DataFrame, avg_ratings: dict, formation: str, show_roles: bool = True) -> str:
    layout = FORMATION_LAYOUT.get(formation, FORMATION_LAYOUT["4-3-3"])
    by_label = {r["Label"]: r for _, r in xi_df.iterrows()}

    html = """
<style>
.pitch-container {
    background: #1c4924;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    width: 100%;
    height: 700px;
    position: relative;
    background-image: repeating-linear-gradient(0deg, transparent, transparent 10%, rgba(0,0,0,0.08) 10%, rgba(0,0,0,0.08) 20%);
    overflow: hidden;
}
.pitch-halfway { position: absolute; top: 50%; left: 0; width: 100%; height: 2px; background: rgba(255,255,255,0.25); transform: translateY(-50%); z-index: 1; }
.pitch-center-circle { position: absolute; top: 50%; left: 50%; width: 110px; height: 110px; border: 2px solid rgba(255,255,255,0.25); border-radius: 50%; transform: translate(-50%, -50%); z-index: 1; }
.pitch-box-top { position: absolute; top: 0; left: 20%; width: 60%; height: 15%; border: 2px solid rgba(255,255,255,0.25); border-top: none; z-index: 1; }
.pitch-box-bottom { position: absolute; bottom: 0; left: 20%; width: 60%; height: 15%; border: 2px solid rgba(255,255,255,0.25); border-bottom: none; z-index: 1; }
.pitch-goal-top { position: absolute; top: 0; left: 38%; width: 24%; height: 5%; border: 2px solid rgba(255,255,255,0.25); border-top: none; background: rgba(255,255,255,0.05); z-index: 1; }
.pitch-goal-bottom { position: absolute; bottom: 0; left: 38%; width: 24%; height: 5%; border: 2px solid rgba(255,255,255,0.25); border-bottom: none; background: rgba(255,255,255,0.05); z-index: 1; }

.pitch-node {
    position: absolute;
    transform: translate(-50%, -50%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 5;
}
.pitch-pos {
    font-size: 0.65rem;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 4px;
    font-family: 'Space Mono', monospace;
    font-weight: bold;
    text-shadow: 1px 1px 2px black;
}
.pitch-dot {
    background-color: var(--bg-card);
    border: 3px solid var(--accent-pink);
    border-radius: 50%;
    width: 20px;
    height: 20px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    position: relative;
}
.pitch-dot-empty { background-color: transparent; border-color: rgba(255,255,255,0.3); border-style: dashed; box-shadow: none; }
.pitch-rating-badge {
    background-color: #ffd700;
    color: #000;
    font-size: 0.6rem;
    font-weight: 800;
    padding: 2px 5px;
    border-radius: 6px;
    position: absolute;
    top: -8px;
    right: -25px;
    border: 1px solid rgba(0,0,0,0.4);
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
}
.pitch-name {
    background-color: rgba(0,0,0,0.75);
    color: #f5f5f7;
    font-size: 0.65rem;
    padding: 3px 8px;
    border-radius: 4px;
    margin-top: 4px;
    text-align: center;
    white-space: nowrap;
    border: 1px solid rgba(255,255,255,0.1);
}
.pitch-name-empty { background-color: transparent; border: none; color: rgba(255,255,255,0.5); }
.pitch-role {
    font-size: 0.5rem;
    margin-top: 4px;
    padding: 2px 6px;
    border-radius: 12px;
    font-family: 'Space Mono', monospace;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.role-attack { background-color: var(--accent-pink); color: white; }
.role-balanced { background-color: #3b82f6; color: white; }
.role-defensive { background-color: #4b5563; color: white; }
</style>
<div class="pitch-container">
    <div class="pitch-halfway"></div>
    <div class="pitch-center-circle"></div>
    <div class="pitch-box-top"></div>
    <div class="pitch-box-bottom"></div>
    <div class="pitch-goal-top"></div>
    <div class="pitch-goal-bottom"></div>
"""
    for code, (depth, lateral) in layout.items():
        pos_style = f"left:{lateral * 100:.1f}%; top:{(1 - depth) * 100:.1f}%;"
        p = by_label.get(code)
        if p is None or p["Player"] == "Select Player":
            html += (f'<div class="pitch-node" style="{pos_style}"><div class="pitch-pos">{code}</div>'
                     f'<div class="pitch-dot pitch-dot-empty"></div>'
                     f'<div class="pitch-name pitch-name-empty">Empty</div></div>\n')
            continue

        name_parts = p["Player"].split()
        short_name = html_lib.escape(name_parts[-1] if len(name_parts) > 1 else p["Player"])
        avg = avg_ratings.get(p["Player"])
        badge_html = f'<div class="pitch-rating-badge">{avg:.1f}</div>' if avg else ''

        role_html = ""
        if not show_roles:
            if p.get("Team"):
                team = html_lib.escape(str(p["Team"]))
                role_html = (f'<div class="pitch-role role-defensive" style="max-width:84px;overflow:hidden;'
                             f'text-overflow:ellipsis;white-space:nowrap">{team}</div>')
        elif p["Slot"] != "GK":
            role = p.get("Role", "Balanced")
            role_class = "role-attack" if role == "Attack" else "role-balanced" if role == "Balanced" else "role-defensive"
            role_html = f'<div class="pitch-role {role_class}">{role}</div>'

        html += (f'<div class="pitch-node" style="{pos_style}"><div class="pitch-pos">{code}</div>'
                 f'<div class="pitch-dot">{badge_html}</div><div class="pitch-name">{short_name}</div>{role_html}</div>\n')
    html += '</div>'
    return html

RADAR_ATTRS = ["Attack", "Assist-Creation", "Goal-Scoring", "Physical",
               "Defense", "Possession", "Dribbling"]

def build_radar_chart(p1_row: pd.Series, p2_row: pd.Series):
    categories = RADAR_ATTRS
    v1 = [float(p1_row.get(c, 0)) for c in categories]
    v2 = [float(p2_row.get(c, 0)) for c in categories]
    cats_closed = categories + [categories[0]]
    v1_closed = v1 + [v1[0]]
    v2_closed = v2 + [v2[0]]

    name1, name2 = str(p1_row["Player"]), str(p2_row["Player"])

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=v1_closed, theta=cats_closed, name=name1,
        line=dict(color="#3b82f6", width=2),
        marker=dict(color="#3b82f6", size=7),
        fill="toself", fillcolor="rgba(59, 130, 246, 0.35)",
    ))
    fig.add_trace(go.Scatterpolar(
        r=v2_closed, theta=cats_closed, name=name2,
        line=dict(color="#ff2f2f", width=2),
        marker=dict(color="#ff2f2f", size=7),
        fill="toself", fillcolor="rgba(255, 47, 47, 0.35)",
    ))

    fig.update_layout(
        title=dict(text=f"{name1} vs {name2} Performance Radar", x=0, xanchor="left",
                    font=dict(size=16, color="#f5f5f7", family="Sora, sans-serif")),
        polar=dict(
            bgcolor="rgba(255,255,255,0.02)",
            radialaxis=dict(visible=True, range=[0, 20], tickvals=[0, 4, 8, 12, 16, 20],
                             gridcolor="rgba(255,255,255,0.15)", linecolor="rgba(255,255,255,0.2)",
                             tickfont=dict(color="#9a9aab", size=10)),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.15)", linecolor="rgba(255,255,255,0.2)",
                              tickfont=dict(color="#f5f5f7", size=12)),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#f5f5f7", family="Sora, sans-serif"),
        legend=dict(bgcolor="rgba(255,255,255,0.04)", bordercolor="rgba(255,255,255,0.12)",
                    borderwidth=1, font=dict(color="#f5f5f7"), x=1.02, y=1),
        margin=dict(l=40, r=140, t=60, b=40),
        height=430,
    )
    return fig

def render_squad_tactics():
    if not ss.season_started:
        render_need_season_prompt()
        return

    st.subheader(f"{ss.user_team} — Squad & Tactics")

    if ss.user_team in TEAM_STRENGTH_DATA:
        info = TEAM_STRENGTH_DATA[ss.user_team]
        mod_pct = f"{'+' if info['modifier'] >= 1.0 else ''}{round((info['modifier'] - 1.0) * 100, 1)}%"
        st.caption(f"📊 **Expected Finish:** #{info['exp_rank']} | **Strength Modifier:** {info['modifier']}x ({mod_pct} Rating Factor)")
        
    squad = get_user_squad()

    # Pre-populate empty manual lineup dict if missing or formation changed
    sync_manual_lineup()

    st.markdown("##### 👥 Full Squad Attributes")
    filtered_squad = squad.copy()
    squad_positions = st.multiselect("Filter by Position", POSITION_ORDER, key="squad_pos_filter")
    if squad_positions:
        filtered_squad = filtered_squad[filtered_squad["Position"].isin(squad_positions)]

    squad_display = filtered_squad.drop(
        columns=["PlayerID", "Team", "OVR", "Season", "League", "season", "league"], 
        errors="ignore"
    )
    st.dataframe(style_player_attributes(squad_display), use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("##### 📡 Compare Two Players")

    available_positions = sorted(squad["Position"].dropna().unique())

    selected_position = st.selectbox(
        "Select Position to Compare",
        options=available_positions,
        index=0,
        help="Select a single position to filter the available player options."
    )

    filtered_df = squad[squad["Position"] == selected_position]
    available_players = sorted(filtered_df["Player"].unique())

    compare_pool = available_players if len(available_players) >= 2 else squad["Player"].tolist()
    if len(compare_pool) >= 2:
        cc1, cc2 = st.columns(2)
        with cc1:
            p1_name = st.selectbox("Player A", compare_pool, index=0, key="radar_p1")
        with cc2:
            p2_default_idx = next((i for i, p in enumerate(compare_pool) if p != p1_name), 0)
            p2_name = st.selectbox("Player B", compare_pool, index=p2_default_idx, key="radar_p2")

        if p1_name == p2_name:
            st.caption("Pick two different players to compare.")
        else:
            p1_row = squad[squad["Player"] == p1_name].iloc[0]
            p2_row = squad[squad["Player"] == p2_name].iloc[0]
            st.plotly_chart(build_radar_chart(p1_row, p2_row), use_container_width=True)
    else:
        st.caption("Need at least two players in the squad to compare.")

    st.divider()

    col_tac, col_pitch, col_sel = st.columns([1.2, 2.5, 2.0], gap="medium")
    with col_tac:
        st.markdown("##### 📋 Tactical Style")
        new_formation = st.selectbox("Formation", list(FORMATIONS.keys()), index=list(FORMATIONS.keys()).index(ss.formation))
        if new_formation != ss.formation:
            ss.formation = new_formation
            ss.manual_lineup = {}
            ss.player_roles = {}
            st.rerun()

        if "play_type_choice" not in ss:
            ss["play_type_choice"] = ss.play_type
        ss.play_type = st.selectbox(
            "Type of Play", PLAY_TYPE_NAMES, key="play_type_choice",
            help="Your playing philosophy. Each style suits different players (their Physical, Defense, Possession, "
                 "Dribbling... attributes), tires the team differently, and works better or worse depending on the "
                 "opponent's style, which side is the favourite and whether you play at home. The squad fit shown above "
                 "the pitch combines your players, how well your tactical settings (formation, mentality, tempo, "
                 "defensive line, pressing, attacking preference) suit the style, and your player roles.",
        )
        st.caption(PLAY_TYPES[ss.play_type]["desc"])

        tactic_select("Mentality", MENTALITIES, "mentality")
        tactic_select("Tempo", TEMPOS, "tempo")
        tactic_select("Defensive Line", OOP_LINES, "oop_line")
        tactic_select("Pressing Type", PRESS_TYPES, "pressing")
        if "attack_pref_choice" not in ss:
            ss["attack_pref_choice"] = ss.attack_pref
        ss.attack_pref = st.selectbox(
            "Attacking Preference", ATTACK_PREFS, key="attack_pref_choice",
            help="Which lane you attack through. Wing play leans on your wingers, wide midfielders and "
                 "full-backs against their flank defence; middle play leans on your central midfielders, "
                 "attacking midfielders and strikers against their central defence. "
                 "It pays off when your strength matches their weakness.",
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.button("⚡ Auto-Pick Best XI", use_container_width=True, on_click=apply_auto_pick)

        all_selected = all(p != "Select Player" for p in ss.manual_lineup.values())
        
        if is_team_locked():
            st.success("✅ Team locked in")
            if st.button("🔁 Unlock & edit tactics", use_container_width=True):
                ss.locked_signature = None
                st.rerun()
        else:
            if not all_selected:
                st.warning("⚠️ Select 11 players to lock your team.")
                st.button("🔒 Lock Team & Go to Matchday", type="primary", use_container_width=True, disabled=True)
            else:
                st.caption("Set your formation, roles and starting XI, then lock your team to play.")
                if st.button("🔒 Lock Team & Go to Matchday", type="primary", use_container_width=True):
                    ss.locked_signature = current_tactics_signature()
                    ss.page = "play"
                    st.rerun()

    labels = slot_labels(ss.formation)

    with col_sel:
        st.markdown("##### 👕 Starting XI & Roles")
        
        changed = False
        
        for pos, label in labels:
            key = (pos, label)
            current_val = ss.manual_lineup.get(key, "Select Player")
            
            # Natural position candidates
            pos_players = squad[squad["Position"] == pos]["Player"].tolist()
            
            # Find players already assigned to OTHER slots
            other_selected = {p for k, p in ss.manual_lineup.items() if k != key and p and p != "Select Player"}
            
            # Filter out already selected players
            avail_nat = [p for p in pos_players if p not in other_selected]
            
            avail = ["Select Player"] + avail_nat
            
            # Ensure the currently selected player remains visible even if filters change
            if current_val != "Select Player" and current_val not in avail:
                avail.append(current_val)
                
            idx = avail.index(current_val) if current_val in avail else 0
            
            col_p, col_r = st.columns([6, 4])
            with col_p:
                selected = st.selectbox(
                    f"{label} · {SLOT_INFO[label]['name']}", avail, index=idx, key=slot_widget_key(label),
                    help=f"Filled from {pos} players",
                )
                if ss.manual_lineup.get(key) != selected:
                    ss.manual_lineup[key] = selected
                    changed = True

            with col_r:
                if pos == "GK":
                    st.selectbox("Role", ["GK"], disabled=True, key=role_widget_key(label))
                elif pos == "CB":
                    current_role = ss.player_roles.get(key, "Defensive")
                    if current_role not in ["Balanced", "Defensive"]: current_role = "Defensive"
                    role = st.selectbox("Role", ["Balanced", "Defensive"], index=["Balanced", "Defensive"].index(current_role), key=role_widget_key(label))
                    if ss.player_roles.get(key) != role:
                        ss.player_roles[key] = role
                        changed = True
                else:
                    current_role = ss.player_roles.get(key, default_role_for(pos))
                    role = st.selectbox("Role", ["Attack", "Balanced", "Defensive"], index=["Attack", "Balanced", "Defensive"].index(current_role), key=role_widget_key(label))
                    if ss.player_roles.get(key) != role:
                        ss.player_roles[key] = role
                        changed = True

        if changed:
            st.rerun()

        st.markdown("##### 🪑 Substitutes")
        starters_now = {p for p in ss.manual_lineup.values() if p and p != "Select Player"}
        bench_pool = squad[~squad["Player"].isin(starters_now)].copy()
        bench_pool["_g"] = bench_pool["Position"].map(lambda p: POSITION_ORDER.index(p) if p in POSITION_ORDER else 99)
        bench_pool = bench_pool.sort_values(["_g", "OVR"], ascending=[True, False])
        bench_info = {r["Player"]: f'{r["Player"]} · {r["Position"]} · {r["OVR"]:.0f}' for _, r in bench_pool.iterrows()}
        # keep the widget's own state valid (a player promoted into the XI must leave the bench)
        ss["bench_select"] = [p for p in ss.get("bench_select", []) if p in bench_info][:BENCH_SIZE]
        ss.bench = st.multiselect(
            f"Bench (up to {BENCH_SIZE})", list(bench_info), key="bench_select", max_selections=BENCH_SIZE,
            format_func=lambda p: bench_info.get(p, p),
            help="Substitutes are used automatically during the match, in up to 3 separate moments from the 46th "
                 "minute (several players can change at once): tired or weaker players come off, replaced by the best "
                 "bench player for that position. Deeper cover helps late in games.",
        )
        st.button("⚡ Auto-Pick Bench", use_container_width=True, on_click=apply_auto_bench)
        if not ss.bench:
            st.caption("No bench chosen: your assistant manager will pick one for match days.")

    current_xi_df = current_user_xi()

    with col_pitch:
        fit_info = None
        if (current_xi_df["Player"] != "Select Player").sum() >= 11:
            fit_info = play_type_squad_fit(ss.play_type, current_xi_df, ss.user_team, ss.formation, ss.mentality,
                                           ss.tempo, ss.oop_line, ss.pressing, ss.attack_pref)
        st.markdown(squad_fit_header_html(ss.formation, ss.play_type, fit_info), unsafe_allow_html=True)
        avg_ratings = {k: ss.player_ratings_sum[k]/ss.player_ratings_count[k] for k in ss.player_ratings_sum if ss.player_ratings_count.get(k, 0) > 0}
        st.markdown(generate_pitch_html(current_xi_df, avg_ratings, ss.formation), unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 2D ENGINE RENDER FUNCTION
# --------------------------------------------------------------------------
LINE_X_MOD = {"High line": 0.05, "Medium-block": 0.0, "Low defensive line": -0.05}
MENTALITY_X_MOD = {"Very Defensive": -0.05, "Defensive": -0.025, "Balanced": 0.0, "Attacking": 0.025, "Very Attacking": 0.05}
ROLE_X_OFFSET = {"Attack": 0.03, "Balanced": 0.0, "Defensive": -0.03, "GK": 0.0}
VIZ_CATEGORY = {"GK": "gk", "CB": "df", "FB & WB": "df", "MF": "mf", "AM & W": "am", "CF": "fw"}
VIZ_TEMPO_MULT = {"Slow": 0.9, "Normal": 1.0, "Fast": 1.12}
VIZ_PRESS_LEVEL = {"High Press": 1.35, "Balanced": 1.0, "Low Press": 0.72}
VIZ_ATTACK_SCALE = {"Very Defensive": 0.55, "Defensive": 0.8, "Balanced": 1.0, "Attacking": 1.25, "Very Attacking": 1.5}
VIZ_DEFEND_SCALE = {"Very Defensive": 1.5, "Defensive": 1.2, "Balanced": 1.0, "Attacking": 0.8, "Very Attacking": 0.55}

def _formation_slot_coords(formation: str, oop_line: str, mentality: str) -> dict:
    """slot code -> (x, y) for a team attacking left-to-right.
    x: 0 = own goal, 1 = opponent goal. y: 0 = the team's left touchline, 1 = its right."""
    layout = FORMATION_LAYOUT.get(formation, FORMATION_LAYOUT["4-3-3"])
    coords = {}
    for code, (depth, lateral) in layout.items():
        group = SLOT_INFO[code]["group"]
        x = depth
        if group in ("CB", "FB & WB"):
            x += LINE_X_MOD.get(oop_line, 0.0)
        if group != "GK":
            x += MENTALITY_X_MOD.get(mentality, 0.0) * (0.55 if group == "CF" else 1.0)
        coords[code] = (min(max(x, 0.05), 0.90), lateral)
    return coords

def _short_surname(full_name: str) -> str:
    name = re.sub(r"\s*\(\d+\)$", "", str(full_name)).strip()
    parts = name.split()
    return parts[-1] if parts else name

def _build_team_players(xi_records: list, team_idx: int, formation: str, mentality: str, oop_line: str) -> list:
    coords = _formation_slot_coords(formation, oop_line, mentality)
    valid = [r for r in xi_records if r.get("Player") and r["Player"] != "Select Player"]
    valid.sort(key=lambda r: (
        POSITION_ORDER.index(r["Slot"]) if r["Slot"] in POSITION_ORDER else 99,
        str(r.get("Label", "")),
    ))
    out = []
    for num, r in enumerate(valid, start=1):
        pos = r["Slot"]
        x, y = coords.get(r.get("Label"), (0.5, 0.5))
        role = r.get("Role", "Balanced")
        if pos != "GK":
            x = min(max(x + ROLE_X_OFFSET.get(role, 0.0), 0.05), 0.92)
        if team_idx == 1:
            x, y = 1 - x, 1 - y  # away side defends the right-hand goal, so its left/right flip too
        try:
            ovr = float(r.get("OVR", 60))
        except (TypeError, ValueError):
            ovr = 60.0
        out.append({
            "x": round(x, 4), "y": round(y, 4), "cat": VIZ_CATEGORY.get(pos, "mf"),
            "team": team_idx, "num": num, "role": role, "ovr": ovr,
            "name": _short_surname(r["Player"]),
        })
    return out

def _team_viz_tactics(mentality: str, tempo: str, press: str) -> dict:
    return {
        "tempoMult": VIZ_TEMPO_MULT.get(tempo, 1.0),
        "pressLevel": VIZ_PRESS_LEVEL.get(press, 1.0),
        "attackScale": VIZ_ATTACK_SCALE.get(mentality, 1.0),
        "defendScale": VIZ_DEFEND_SCALE.get(mentality, 1.0),
    }

def render_play():
    if not ss.season_started:
        render_need_season_prompt()
        return
    
    st.subheader("▶️ Play Matchday")
    if ss.matchday >= len(ss.schedule):
        st.success("🎉 The season is over! Check the final league table and the season awards.")
        if st.button("🏆 See the Team of the Season", key="goto_awards"):
            ss.page = "awards"
            st.rerun()
        if ss.recent_match_ratings:
            st.markdown("#### 📊 Final Match Ratings")
            ratings_df = pd.DataFrame(ss.recent_match_ratings)
            st.dataframe(ratings_df, use_container_width=True, hide_index=True)
        return

    st.markdown(f"**Matchday {ss.matchday + 1} of {len(ss.schedule)}**")

    if not is_team_locked():
        st.warning("🔒 Lock your team in **Squad & Tactics** before you can play or simulate a matchday.")
        if st.button("Go to Squad & Tactics", type="primary", use_container_width=True):
            ss.page = "squad"
            st.rerun()
        return

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Next Matchday", type="primary", use_container_width=True):
            play_next_matchday()
            st.rerun()
    with col2:
        if st.button("⏩ Simulate Rest of Season", use_container_width=True):
            simulate_to_end()
            st.rerun()

    if ss.last_commentary:
        st.divider()

        # Feed the exact formation/tactics/lineup snapshot from the match
        # that was just played to the 2D engine, not a generic placeholder.
      
        st.markdown("### 🎙️ Latest Match Report")
        if ss.last_match_report:
            st.markdown(match_report_html(ss.last_match_report), unsafe_allow_html=True)
        with st.expander("📝 Text commentary"):
            for line in ss.last_commentary: st.markdown(f"> {line}")
            
    st.divider()
    st.markdown("### Recent Results")
    recent = [h for h in ss.history if h["round"] == ss.matchday]
    if recent:
        recent_df = pd.DataFrame([
            {
                "Home Team": r["home"],
                "Home Goals": r["hg"],
                "Away Goals": r["ag"],
                "Away Team": r["away"],
            }
            for r in recent
        ])
        st.dataframe(recent_df, use_container_width=True, hide_index=True)
            
    if ss.recent_match_ratings:
        st.markdown("#### 📊 Your Match Ratings")
        ratings_df = pd.DataFrame(ss.recent_match_ratings)
        st.dataframe(ratings_df, use_container_width=True, hide_index=True)

def render_table():
    if not ss.season_started:
        render_need_season_prompt()
        return
    st.subheader("📊 League Table")
    st.dataframe(table_dataframe(ss.table), use_container_width=True)
    
    st.divider()
    st.subheader("🥇 Player Statistics")
    
    stats_df = DF[['Player', 'Team', 'Position']].copy()
    stats_df['Goals'] = stats_df['Player'].map(ss.scorers).fillna(0).astype(int)
    stats_df['Assists'] = stats_df['Player'].map(ss.assists).fillna(0).astype(int)
    
    def get_avg(p):
        cnt = ss.player_ratings_count.get(p, 0)
        return round(ss.player_ratings_sum[p] / cnt, 2) if cnt > 0 else 0.0
        
    stats_df['Average Rating'] = stats_df['Player'].apply(get_avg)
    
    col1, col2 = st.columns(2)
    with col1:
        team_filter = st.multiselect("Filter by Team", ALL_TEAMS, key="stat_team_filter")
    with col2:
        pos_filter = st.multiselect("Filter by Position", POSITION_ORDER, key="stat_pos_filter")
        
    if team_filter:
        stats_df = stats_df[stats_df['Team'].isin(team_filter)]
    if pos_filter:
        stats_df = stats_df[stats_df['Position'].isin(pos_filter)]
        
    stats_df = stats_df[stats_df['Average Rating'] > 0]
    stats_df = stats_df.sort_values(by=['Goals', 'Assists', 'Average Rating'], ascending=[False, False, False])

    if stats_df.empty:
        st.info("No player statistics available yet. Play some matches first!")
    else:
        st.dataframe(stats_df, use_container_width=True, hide_index=True)


def render_fixtures():
    if not ss.season_started:
        render_need_season_prompt()
        return
    st.subheader("📅 Fixtures & Results")
    if not ss.history:
        st.info("No matches played yet.")
    else:
        history_df = pd.DataFrame(ss.history)
        user_history = history_df[history_df["is_user"]].copy()
        user_history["Result"] = user_history["home"] + " " + user_history["hg"].astype(str) + " - " + user_history["ag"].astype(str) + " " + user_history["away"]
        st.dataframe(
            user_history[["round", "Result"]].rename(columns={"round": "Round"}),
            use_container_width=True,
            hide_index=True,
        )
        
    st.divider()
    st.subheader("🔀 Results Matrix")
    
    teams = sorted(ALL_TEAMS)
    matrix = pd.DataFrame(index=teams, columns=teams).fillna("-")
    for h in ss.history:
        matrix.at[h["home"], h["away"]] = f"{h['hg']}-{h['ag']}"
    
    st.dataframe(matrix.rename_axis("Home \\ Away").reset_index(), use_container_width=True, hide_index=True)

def render_player_stats():
    st.subheader("📈 Player Attributes & Scouting")
    df = DF.copy()
    
    search = st.text_input("🔍 Search Player by Name")
    if search:
        df = df[df["Player"].str.contains(search, case=False, na=False)]
        
    col1, col2, col3 = st.columns(3)
    with col1:
        teams = st.multiselect("Filter by Team", ALL_TEAMS)
        if teams: df = df[df["Team"].isin(teams)]
    with col2:
        positions = st.multiselect("Filter by Position", POSITION_ORDER)
        if positions: df = df[df["Position"].isin(positions)]
    with col3:
        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        num_cols = [c for c in num_cols if c not in ["PlayerID", "OVR"]]
        if num_cols and not df.empty:
            attr = st.selectbox("Attribute Filter", ["None"] + sorted(num_cols))
            if attr != "None":
                min_val = float(df[attr].min())
                max_val = float(df[attr].max())
                min_filter = st.number_input(f"Min {attr}", min_value=min_val, max_value=max_val, value=min_val)
                df = df[df[attr] >= min_filter]

    if df.empty:
        st.warning("No players found matching the selected criteria.")
        return

    df_display = df.drop(
        columns=["PlayerID", "OVR", "Season", "League", "season", "league"], 
        errors="ignore"
    )
    st.dataframe(style_player_attributes(df_display), use_container_width=True, hide_index=True)

# --------------------------------------------------------------------------
# Season awards: Team of the Season + best performing player of each club
# --------------------------------------------------------------------------
def season_player_table() -> pd.DataFrame:
    """One row per player who has played, with appearances, goals, assists and average match rating."""
    df = DF[["Player", "Team", "Position"]].copy()
    df["Apps"] = df["Player"].map(ss.player_ratings_count).fillna(0).astype(int)
    df["Goals"] = df["Player"].map(ss.scorers).fillna(0).astype(int)
    df["Assists"] = df["Player"].map(ss.assists).fillna(0).astype(int)
    df["Rating"] = [
        round(ss.player_ratings_sum[p] / ss.player_ratings_count[p], 2) if ss.player_ratings_count.get(p, 0) > 0 else 0.0
        for p in df["Player"]
    ]
    df["G+A"] = df["Goals"] + df["Assists"]
    return df[df["Apps"] > 0].reset_index(drop=True)

def _rank_by_performance(df: pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(["Rating", "G+A", "Apps"], ascending=False)

def pick_team_of_season(players: pd.DataFrame, formation: str, min_apps: int) -> pd.DataFrame:
    """Best XI of the league for a formation: the top-rated players of each position group fill that group's slots.
    Players need `min_apps` appearances; if a group lacks enough of them the best of the rest fill in."""
    slots = slot_labels(formation)
    rows = []
    for group in POSITION_ORDER:
        group_slots = [code for g, code in slots if g == group]
        if not group_slots:
            continue
        pool = players[players["Position"] == group]
        ranked = _rank_by_performance(pool[pool["Apps"] >= min_apps])
        if len(ranked) < len(group_slots):
            ranked = pd.concat([ranked, _rank_by_performance(pool.drop(ranked.index))])
        for code, (_, r) in zip(group_slots, ranked.head(len(group_slots)).iterrows()):
            rows.append({"Slot": group, "Label": code, "Player": r["Player"], "Team": r["Team"], "Position": group,
                         "Apps": int(r["Apps"]), "Goals": int(r["Goals"]), "Assists": int(r["Assists"]), "Rating": float(r["Rating"])})
    order = {code: i for i, code in enumerate(FORMATIONS[formation])}
    return pd.DataFrame(rows).sort_values("Label", key=lambda s: s.map(order)).reset_index(drop=True)

def best_player_per_team(players: pd.DataFrame, min_apps: int) -> pd.DataFrame:
    """Each club's best performer (highest average rating), listed in league-table order."""
    eligible = players[players["Apps"] >= min_apps]
    standings = table_dataframe(ss.table)
    rows = []
    for pos, team in zip(standings.index, standings["Team"]):
        pool = eligible[eligible["Team"] == team]
        if pool.empty:
            pool = players[players["Team"] == team]
        if pool.empty:
            continue
        best = _rank_by_performance(pool).iloc[0]
        rows.append({"Pos": int(pos), "Team": team, "Player": best["Player"], "Position": best["Position"],
                     "Apps": int(best["Apps"]), "Goals": int(best["Goals"]), "Assists": int(best["Assists"]),
                     "Rating": float(best["Rating"])})
    return pd.DataFrame(rows)

def render_awards():
    if not ss.season_started:
        render_need_season_prompt()
        return
    st.subheader("🏆 Season Awards")

    players = season_player_table()
    if players.empty:
        st.info("No player statistics yet. Play some matches first!")
        return

    total = len(ss.schedule)
    season_over = ss.matchday >= total
    min_apps = max(1, round(0.45 * ss.matchday))
    if season_over:
        st.success("🎉 The season is over. These are the final awards.")
    else:
        st.info(f"Provisional awards after matchday {ss.matchday} of {total}. The final awards are decided when the season ends.")
    st.caption(f"Eligible players: at least {min_apps} appearances. If a position or club has no eligible player, "
               "the best of the rest is used.")

    eligible = players[players["Apps"] >= min_apps]
    if eligible.empty:
        eligible = players

    potm = _rank_by_performance(eligible).iloc[0]
    boot = eligible.sort_values(["Goals", "Assists", "Rating"], ascending=False).iloc[0]
    playmaker = eligible.sort_values(["Assists", "Goals", "Rating"], ascending=False).iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("🏅 Player of the Season", potm["Player"])
    c1.caption(f'{potm["Team"]} · {potm["Rating"]:.2f} avg rating')
    c2.metric("👟 Top Scorer", boot["Player"])
    c2.caption(f'{boot["Team"]} · {boot["Goals"]} goals')
    c3.metric("🎯 Top Assister", playmaker["Player"])
    c3.caption(f'{playmaker["Team"]} · {playmaker["Assists"]} assists')

    st.divider()
    st.markdown("### ⭐ Team of the Season")
    formations = list(FORMATIONS.keys())
    formation = st.selectbox("Formation", formations, index=formations.index("4-3-3"), key="awards_formation")
    tos = pick_team_of_season(players, formation, min_apps)

    col_pitch, col_tbl = st.columns([2.2, 2.3], gap="medium")
    with col_pitch:
        st.markdown(generate_pitch_html(tos, dict(zip(tos["Player"], tos["Rating"])), formation, show_roles=False),
                    unsafe_allow_html=True)
    with col_tbl:
        st.dataframe(
            tos[["Label", "Player", "Team", "Apps", "Goals", "Assists", "Rating"]].rename(columns={"Label": "Pos"}),
            hide_index=True, use_container_width=True,
        )
        st.caption(f"Average rating of the XI: **{tos['Rating'].mean():.2f}** · "
                   f"{int((tos['Team'] == ss.user_team).sum())} player(s) from {ss.user_team}")

    st.divider()
    st.markdown("### 🌟 Best Performing Player of Each Team")
    st.caption("Highest average match rating at each club, in league-table order. Your club is highlighted.")
    best_df = best_player_per_team(players, min_apps)

    def highlight_user(row):
        return ["background-color: rgba(255, 47, 123, 0.18); font-weight: 700" if row["Team"] == ss.user_team else ""
                for _ in row]

    st.dataframe(best_df.style.apply(highlight_user, axis=1).format({"Rating": "{:.2f}"}),
                 hide_index=True, use_container_width=True)

# --------------------------------------------------------------------------
# Main Page Router
# --------------------------------------------------------------------------
if ss.page == "instructions": render_instructions()
elif ss.page == "stats": render_player_stats()
elif ss.page == "squad": render_squad_tactics()
elif ss.page == "play": render_play()
elif ss.page == "table": render_table()
elif ss.page == "fixtures": render_fixtures()
elif ss.page == "awards": render_awards()