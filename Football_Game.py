# streamlit run FMtypegame.py
import base64
import io
import random
import numpy as np
import pandas as pd
import streamlit as st

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
]

if "page" not in st.session_state:
    st.session_state.page = "instructions"

nav_cols = st.columns(len(NAV_ITEMS))
for col, (page_id, label) in zip(nav_cols, NAV_ITEMS):
    with col:
        if st.button(
            label,
            key=f"top_nav_{page_id}",
            width="stretch",
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
    w = POS_WEIGHTS[row.get("Position", "MF")]
    raw = sum(row.get(k, RAW_ATTR_MAX / 2) * v for k, v in w.items())
    return round(min(99.0, raw * (99.0 / RAW_ATTR_MAX)), 1)

FORMATIONS = {
    "4-4-2":   {"GK": 1, "CB": 2, "FB & WB": 2, "MF": 2, "AM & W": 2, "CF": 2},
    "4-3-3":   {"GK": 1, "CB": 2, "FB & WB": 2, "MF": 3, "AM & W": 2, "CF": 1},
    "4-2-3-1": {"GK": 1, "CB": 2, "FB & WB": 2, "MF": 2, "AM & W": 3, "CF": 1},
    "5-3-2":   {"GK": 1, "CB": 3, "FB & WB": 2, "MF": 3, "AM & W": 0, "CF": 2},
    "5-2-2-1": {"GK": 1, "CB": 3, "FB & WB": 2, "MF": 2, "AM & W": 2, "CF": 1},
}

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

SCORER_SLOT_BIAS = {"CF": 3.0, "AM & W": 2.0, "MF": 1.0, "FB & WB": 0.35, "CB": 0.15, "GK": 0.02}
ASSIST_SLOT_BIAS = {"AM & W": 3.0, "MF": 2.5, "CF": 1.5, "FB & WB": 1.5, "CB": 0.2, "GK": 0.01}

def slot_labels(formation: str):
    labels = []
    for pos in POSITION_ORDER:
        n = FORMATIONS[formation].get(pos, 0)
        for i in range(1, n + 1):
            labels.append((pos, f"{pos} #{i}" if n > 1 else pos))
    return labels

def auto_select_xi(squad: pd.DataFrame, formation: str) -> pd.DataFrame:
    reqs = FORMATIONS[formation]
    remaining = squad.copy()
    picks = []
    
    for pos, n in reqs.items():
        if n == 0: continue
        pool = remaining[remaining["Position"] == pos].sort_values("OVR", ascending=False)
        chosen = pool.head(n)
        for i, (_, r) in enumerate(chosen.iterrows()):
            label = f"{pos} #{i+1}" if n > 1 else pos
            picks.append({"Slot": pos, "Label": label, "Player": r["Player"], "Position": r["Position"], "OVR": r["OVR"], "OOP": False})
        remaining = remaining.drop(chosen.index)

    filled = {pos: sum(1 for p in picks if p["Slot"] == pos) for pos in reqs}
    for pos, n in reqs.items():
        short = n - filled.get(pos, 0)
        if short > 0 and len(remaining):
            pool = remaining.sort_values("OVR", ascending=False).head(short)
            for i, (_, r) in enumerate(pool.iterrows()):
                idx = filled.get(pos, 0) + i + 1
                label = f"{pos} #{idx}" if n > 1 else pos
                picks.append({"Slot": pos, "Label": label, "Player": r["Player"], "Position": r["Position"], "OVR": round(r["OVR"] * 0.85, 1), "OOP": True})
            remaining = remaining.drop(pool.index)
            
    return pd.DataFrame(picks)

def lineup_from_manual(squad: pd.DataFrame, assignments: dict, formation: str) -> pd.DataFrame:
    assigned_players = set()
    rows = []
    
    for (pos, label), player in assignments.items():
        if player and player != "Select Player":
            assigned_players.add(player)
            r = squad[squad["Player"] == player]
            if not r.empty:
                r = r.iloc[0]
                rows.append({"Slot": pos, "Label": label, "Player": player, "Position": r["Position"], "OVR": r["OVR"], "OOP": r["Position"] != pos})
                
    labels = slot_labels(formation)
    filled_slots = {(r["Slot"], r["Label"]) for r in rows}
    remaining_squad = squad[~squad["Player"].isin(assigned_players)].sort_values("OVR", ascending=False)
    
    for pos, label in labels:
        if (pos, label) in filled_slots:
            continue
        pos_pool = remaining_squad[remaining_squad["Position"] == pos]
        if not pos_pool.empty:
            r = pos_pool.iloc[0]
            is_oop = False
        elif not remaining_squad.empty:
            r = remaining_squad.iloc[0]
            is_oop = True
        else:
            break
            
        rows.append({
            "Slot": pos,
            "Label": label,
            "Player": r["Player"],
            "Position": r["Position"],
            "OVR": round(r["OVR"] * 0.85, 1) if is_oop else r["OVR"],
            "OOP": is_oop
        })
        assigned_players.add(r["Player"])
        remaining_squad = remaining_squad[remaining_squad["Player"] != r["Player"]]
        
    return pd.DataFrame(rows)

# --------------------------------------------------------------------------
# 3. Match engine
# --------------------------------------------------------------------------
def phase_ratings(xi: pd.DataFrame, mentality: str = "Balanced") -> dict:
    def bucket(weights, phase):
        num, den = 0.0, 0.0
        for slot, w in weights.items():
            sub = xi[xi["Slot"] == slot]
            for _, r in sub.iterrows():
                role = r.get("Role", "Balanced")
                adj_w = w
                
                if role == "Attack":
                    if phase == "att": adj_w *= 1.35
                    elif phase == "def": adj_w *= 0.65
                elif role == "Defensive":
                    if phase == "def": adj_w *= 1.35
                    elif phase == "att": adj_w *= 0.65
                    
                num += r["OVR"] * adj_w
                den += adj_w
        return num / den if den else 45.0

    d = bucket({"GK": 0.35, "CB": 1.0, "FB & WB": 0.6, "MF": 0.15}, "def")
    m = bucket({"MF": 1.0, "AM & W": 0.4, "FB & WB": 0.25, "CB": 0.1, "CF": 0.1}, "mid")
    a = bucket({"CF": 1.0, "AM & W": 0.9, "MF": 0.25, "FB & WB": 0.1}, "att")
    
    att_mod, def_mod = MENTALITY_MOD[mentality]
    return {"def": d * (1 + def_mod), "mid": m, "att": a * (1 + att_mod)}

def get_match_rating(base_xg, goals, is_cs, rng, is_scorer):
    rating = 6.0 + rng.normal(0, 0.5) + (base_xg * 0.2)
    if is_scorer:
        rating += 1.5
    if is_cs:
        rating += 0.8
    return round(min(10.0, max(3.0, rating)), 1)

def simulate_match(home_xi, away_xi, 
                   home_mentality="Balanced", away_mentality="Balanced",
                   home_tempo="Normal", away_tempo="Normal",
                   home_line="Medium-block", away_line="Medium-block",
                   home_press="Balanced", away_press="Balanced",
                   home_adv=0.28, rng=None):
    rng = rng or np.random.default_rng()
    h = phase_ratings(home_xi, home_mentality)
    a = phase_ratings(away_xi, away_mentality)
    
    line_att_mod = {"High line": 0.05, "Medium-block": 0.0, "Low defensive line": -0.05}
    line_def_mod = {"High line": -0.05, "Medium-block": 0.0, "Low defensive line": 0.05}
    h["att"] *= (1 + line_att_mod[home_line])
    h["def"] *= (1 + line_def_mod[home_line])
    a["att"] *= (1 + line_att_mod[away_line])
    a["def"] *= (1 + line_def_mod[away_line])

    xg_home = np.clip((1.05 + (h["att"] - a["def"]) / 26 + (h["mid"] - a["mid"]) / 60 + home_adv) * TEMPO_VARIANCE[home_tempo], 0.10, 4.2)
    xg_away = np.clip((1.05 + (a["att"] - h["def"]) / 26 + (a["mid"] - h["mid"]) / 60) * TEMPO_VARIANCE[away_tempo], 0.10, 4.2)
    
    hg = int(rng.poisson(xg_home))
    ag = int(rng.poisson(xg_away))
    
    press_mod = {"High Press": 0.06, "Balanced": 0.0, "Low Press": -0.04}
    base_possession_home = 50 + np.clip((h["mid"] - a["mid"]) * 0.9, -22, 22)
    press_poss_shift = (press_mod[home_press] - press_mod[away_press]) * 50
    possession_home = np.clip(base_possession_home + press_poss_shift, 20, 80)
    
    return {
        "home_goals": hg, "away_goals": ag,
        "xg_home": round(xg_home, 2), "xg_away": round(xg_away, 2),
        "possession_home": round(possession_home, 1),
    }

def pick_goal_events(xi: pd.DataFrame, n_goals: int, rng=None):
    if n_goals <= 0 or xi.empty:
        return []
    rng = rng or np.random.default_rng()

    pool_scorer = xi.copy()
    pool_scorer["w"] = pool_scorer["Slot"].map(SCORER_SLOT_BIAS).fillna(0.5) * (pool_scorer["OVR"] / 50.0)
    pool_scorer["w"] = pool_scorer["w"].clip(lower=0.01)
    scorer_weights = (pool_scorer["w"] / pool_scorer["w"].sum()).to_numpy()

    pool_assist = xi.copy()
    pool_assist["w"] = pool_assist["Slot"].map(ASSIST_SLOT_BIAS).fillna(0.5) * (pool_assist["OVR"] / 50.0)
    pool_assist["w"] = pool_assist["w"].clip(lower=0.01)

    events = []
    for _ in range(n_goals):
        minute = int(rng.integers(1, 91))
        scorer = rng.choice(pool_scorer["Player"].to_numpy(), p=scorer_weights)

        assister = None
        if len(xi) > 1 and rng.random() < 0.75:
            assist_pool = pool_assist[pool_assist["Player"] != scorer]
            if not assist_pool.empty:
                assist_weights = (assist_pool["w"] / assist_pool["w"].sum()).to_numpy()
                assister = rng.choice(assist_pool["Player"].to_numpy(), p=assist_weights)

        events.append({
            "minute": minute,
            "scorer": scorer,
            "assist": assister,
        })

    events.sort(key=lambda x: x["minute"])
    return events

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
    ss.setdefault("manual_lineup", {})   
    ss.setdefault("player_roles", {})    
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
    ss.manual_lineup = {}
    ss.player_roles = {}
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
        default_role = "GK" if row["Slot"] == "GK" else ("Attack" if row["Slot"] in ["CF", "AM & W"] else ("Balanced" if row["Slot"] == "MF" else "Defensive"))
        roles_list.append(ss.player_roles.get(key, default_role))
    xi["Role"] = roles_list
    return xi

def ai_lineup_for(team: str):
    squad = DF[DF["Team"] == team]
    formation = random.choice(["4-3-3", "4-4-2", "4-2-3-1", "5-2-2-1"])
    mentality = random.choice(["Defensive", "Balanced", "Balanced", "Attacking"])
    tempo = random.choice(TEMPOS)
    line = random.choice(OOP_LINES)
    press = random.choice(PRESS_TYPES)
    xi = auto_select_xi(squad, formation)
    
    def default_role(slot):
        if slot in ["CF", "AM & W"]: return "Attack"
        if slot == "MF": return "Balanced"
        if slot in ["CB", "FB & WB"]: return "Defensive"
        return "GK"
        
    xi["Role"] = xi["Slot"].apply(default_role)
    return xi, mentality, tempo, line, press

def play_fixture(home, away, rng):
    if home == ss.user_team:
        home_xi, home_ment, home_tempo, home_line, home_press = current_user_xi(), ss.mentality, ss.tempo, ss.oop_line, ss.pressing
    else:
        home_xi, home_ment, home_tempo, home_line, home_press = ai_lineup_for(home)
        
    if away == ss.user_team:
        away_xi, away_ment, away_tempo, away_line, away_press = current_user_xi(), ss.mentality, ss.tempo, ss.oop_line, ss.pressing
    else:
        away_xi, away_ment, away_tempo, away_line, away_press = ai_lineup_for(away)

    result = simulate_match(home_xi, away_xi, home_ment, away_ment, home_tempo, away_tempo, home_line, away_line, home_press, away_press, rng=rng)
    home_events = pick_goal_events(home_xi, result["home_goals"], rng)
    away_events = pick_goal_events(away_xi, result["away_goals"], rng)

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
            g_count = scorers.count(player_name)
            a_count = assisters.count(player_name)
            is_scorer = g_count > 0
            r = get_match_rating(xg, team_goals, cs, rng, is_scorer)
            if a_count > 0:
                r = round(min(10.0, r + 0.5 * a_count), 1)

            ss.player_ratings_sum[player_name] = ss.player_ratings_sum.get(player_name, 0) + r
            ss.player_ratings_count[player_name] = ss.player_ratings_count.get(player_name, 0) + 1

            stats.append({
                "Player": player_name,
                "Minutes Played": 90,
                "Goal": g_count,
                "Assist": a_count,
                "Rating": r
            })
        return stats

    h_stats = process_player_stats(home_xi, home_events, home_cs, result["xg_home"], result["home_goals"])
    a_stats = process_player_stats(away_xi, away_events, away_cs, result["xg_away"], result["away_goals"])

    if home == ss.user_team:
        ss.recent_match_ratings = h_stats
    elif away == ss.user_team:
        ss.recent_match_ratings = a_stats

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
        if st.button("🔄 Restart Game", width="stretch"):
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
                    if cols[j].button(t, width="stretch", key=f"btn_start_{t}"):
                        start_new_season(t)
                        ss.page = "squad"
                        st.rerun()

def render_need_season_prompt():
    st.info("👋 Go to **ℹ️ Instructions** to pick a club and start the season.")

def generate_pitch_html(xi_df: pd.DataFrame, avg_ratings: dict) -> str:
    lines = {"Attack": [], "AM": [], "Mid": [], "Def": [], "GK": []}
    for _, row in xi_df.iterrows():
        slot = row["Slot"]
        if slot == "CF": lines["Attack"].append(row)
        elif slot == "AM & W": lines["AM"].append(row)
        elif slot == "MF": lines["Mid"].append(row)
        elif slot in ["CB", "FB & WB"]: lines["Def"].append(row)
        elif slot == "GK": lines["GK"].append(row)
            
    fbs = [p for p in lines["Def"] if p["Slot"] == "FB & WB"]
    cbs = [p for p in lines["Def"] if p["Slot"] == "CB"]
    if len(fbs) >= 2: lines["Def"] = [fbs[0]] + cbs + fbs[1:]
    elif len(fbs) == 1: lines["Def"] = [fbs[0]] + cbs
    else: lines["Def"] = cbs

    html = """
<style>
.pitch-container {
    background: #1c4924;
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    width: 100%;
    height: 700px;
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    padding: 10px 0;
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

.pitch-row {
    display: flex;
    justify-content: space-around;
    align-items: center;
    width: 100%;
    min-height: 80px;
    z-index: 2;
}
.pitch-node {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    z-index: 5;
}
.pitch-pos {
    font-size: 0.6rem;
    color: rgba(255, 255, 255, 0.85);
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
    for line_key in ["Attack", "AM", "Mid", "Def", "GK"]:
        players = lines[line_key]
        if not players: continue
        
        html += '<div class="pitch-row">\n'
        for p in players:
            name_parts = p["Player"].split()
            short_name = name_parts[-1] if len(name_parts) > 1 else p["Player"]
            
            avg = avg_ratings.get(p["Player"])
            badge_html = f'<div class="pitch-rating-badge">{avg:.1f}</div>' if avg else ''
            
            if p["Slot"] == "GK":
                html += f'<div class="pitch-node"><div class="pitch-pos">{p["Slot"]}</div><div class="pitch-dot">{badge_html}</div><div class="pitch-name">{short_name}</div></div>\n'
            else:
                role = p.get("Role", "Balanced")
                role_class = "role-attack" if role == "Attack" else "role-balanced" if role == "Balanced" else "role-defensive"
                html += f'<div class="pitch-node"><div class="pitch-pos">{p["Slot"]}</div><div class="pitch-dot">{badge_html}</div><div class="pitch-name">{short_name}</div><div class="pitch-role {role_class}">{role}</div></div>\n'
        html += '</div>\n'
    html += '</div>'
    return html

def render_squad_tactics():
    if not ss.season_started:
        render_need_season_prompt()
        return

    st.subheader(f"{ss.user_team} — Squad & Tactics")
    squad = get_user_squad()

    st.markdown("##### 👥 Full Squad Attributes")
    filtered_squad = squad.copy()
    squad_positions = st.multiselect("Filter by Position", POSITION_ORDER, key="squad_pos_filter")
    if squad_positions:
        filtered_squad = filtered_squad[filtered_squad["Position"].isin(squad_positions)]

    squad_display = filtered_squad.drop(
        columns=["PlayerID", "Team", "OVR", "Season", "League", "season", "league"], 
        errors="ignore"
    )
    st.dataframe(style_player_attributes(squad_display), width="stretch", hide_index=True)
    
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

        ss.mentality = st.selectbox("Mentality", MENTALITIES, index=MENTALITIES.index(ss.mentality))
        ss.tempo = st.selectbox("Tempo", TEMPOS, index=TEMPOS.index(ss.tempo))
        ss.oop_line = st.selectbox("Defensive Line", OOP_LINES, index=OOP_LINES.index(ss.oop_line))
        ss.pressing = st.selectbox("Pressing Type", PRESS_TYPES, index=PRESS_TYPES.index(ss.pressing))
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Auto-Pick XI", width="stretch"):
            ss.manual_lineup = {}
            ss.player_roles = {}
            st.rerun()

    labels = slot_labels(ss.formation)

    with col_sel:
        st.markdown("##### 👕 Starting XI & Roles")
        changed = False
        
        for i, (pos, label) in enumerate(labels):
            key = (pos, label)
            current_val = ss.manual_lineup.get(key, "Select Player")
            
            pos_players = squad[squad["Position"] == pos]["Player"].tolist()
            other_selected = {p for k, p in ss.manual_lineup.items() if k != key and p and p != "Select Player"}
            avail = ["Select Player"] + [p for p in pos_players if p not in other_selected]
            
            if current_val not in avail:
                current_val = "Select Player"
            idx = avail.index(current_val)
            
            col_p, col_r = st.columns([6, 4])
            with col_p:
                selected = st.selectbox(label, avail, index=idx, key=f"slot_{pos}_{label}")
                if ss.manual_lineup.get(key, "Select Player") != selected:
                    ss.manual_lineup[key] = selected
                    changed = True

            with col_r:
                if pos == "GK":
                    st.selectbox("Role", ["GK"], disabled=True, key=f"role_{pos}_{label}")
                elif pos == "CB":
                    current_role = ss.player_roles.get(key, "Defensive")
                    if current_role not in ["Balanced", "Defensive"]: current_role = "Defensive"
                    role = st.selectbox("Role", ["Balanced", "Defensive"], index=["Balanced", "Defensive"].index(current_role), key=f"role_{pos}_{label}")
                    if ss.player_roles.get(key) != role:
                        ss.player_roles[key] = role
                        changed = True
                else:
                    default_role = "Attack" if pos in ["CF", "AM & W"] else "Balanced" if pos == "MF" else "Defensive"
                    current_role = ss.player_roles.get(key, default_role)
                    role = st.selectbox("Role", ["Attack", "Balanced", "Defensive"], index=["Attack", "Balanced", "Defensive"].index(current_role), key=f"role_{pos}_{label}")
                    if ss.player_roles.get(key) != role:
                        ss.player_roles[key] = role
                        changed = True

        if changed:
            st.rerun()

    # Generate current XI AFTER selections have been captured/updated above
    current_xi_df = current_user_xi()

    with col_pitch:
        st.markdown(f"##### 🏟️ {ss.formation} Shape")
        avg_ratings = {k: ss.player_ratings_sum[k]/ss.player_ratings_count[k] for k in ss.player_ratings_sum}
        st.markdown(generate_pitch_html(current_xi_df, avg_ratings), unsafe_allow_html=True)

def render_play():
    if not ss.season_started:
        render_need_season_prompt()
        return
    
    st.subheader("▶️ Play Matchday")
    if ss.matchday >= len(ss.schedule):
        st.success("The season is over! Check the final league table.")
        return

    st.markdown(f"**Matchday {ss.matchday + 1} of {len(ss.schedule)}**")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Next Matchday", type="primary", width="stretch"):
            play_next_matchday()
            st.rerun()
    with col2:
        if st.button("⏩ Simulate Rest of Season", width="stretch"):
            simulate_to_end()
            st.rerun()

    if ss.last_commentary:
        st.divider()
        st.markdown("### 🎙️ Latest Match Report")
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
        st.dataframe(recent_df, width="stretch", hide_index=True)
            
    if ss.recent_match_ratings:
        st.markdown("#### 📊 Your Match Ratings")
        ratings_df = pd.DataFrame(ss.recent_match_ratings)
        st.dataframe(ratings_df, width="stretch", hide_index=True)

def render_table():
    if not ss.season_started:
        render_need_season_prompt()
        return
    st.subheader("📊 League Table")
    st.dataframe(table_dataframe(ss.table), width="stretch")
    
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
        st.dataframe(stats_df, width="stretch", hide_index=True)

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
            width="stretch",
            hide_index=True,
        )
        
    st.divider()
    st.subheader("🔀 Results Matrix")
    
    teams = sorted(ALL_TEAMS)
    matrix = pd.DataFrame(index=teams, columns=teams).fillna("-")
    for h in ss.history:
        matrix.at[h["home"], h["away"]] = f"{h['hg']}-{h['ag']}"
    
    st.dataframe(matrix.rename_axis("Home \\ Away").reset_index(), width="stretch", hide_index=True)

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
        if num_cols:
            attr = st.selectbox("Attribute Filter", ["None"] + sorted(num_cols))
            if attr != "None":
                min_val = float(df[attr].min())
                max_val = float(df[attr].max())
                min_filter = st.number_input(f"Min {attr}", min_value=min_val, max_value=max_val, value=min_val)
                df = df[df[attr] >= min_filter]
                
    df_display = df.drop(
        columns=["PlayerID", "OVR", "Season", "League", "season", "league"], 
        errors="ignore"
    )
    st.dataframe(style_player_attributes(df_display), width="stretch", hide_index=True)

# --------------------------------------------------------------------------
# Main Page Router
# --------------------------------------------------------------------------
if ss.page == "instructions": render_instructions()
elif ss.page == "stats": render_player_stats()
elif ss.page == "squad": render_squad_tactics()
elif ss.page == "play": render_play()
elif ss.page == "table": render_table()
elif ss.page == "fixtures": render_fixtures()