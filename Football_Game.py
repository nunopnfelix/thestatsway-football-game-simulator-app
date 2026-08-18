#streamlit run Football_Game.py
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from collections import Counter
from sklearn.ensemble import RandomForestRegressor
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

st.set_page_config(page_title="Football Club Manager", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background-color: #E7D9B4;
        color: #2F2A1E;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    [data-testid="stSidebar"] { display: none; }

    .stat-card {
        background-color: #F2E7C9;
        border-radius: 8px;
        padding: 18px 12px;
        text-align: center;
        border: 1px solid #C9B989;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.12);
        margin-bottom: 20px;
    }
    .stat-label {
        color: #7A6F52;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 6px;
    }
    .stat-value { color: #2F2A1E; font-size: 1.45rem; font-weight: 800; }

    div[data-baseweb="select"] > div {
        background-color: #F2E7C9 !important;
        color: #2F2A1E !important;
        border-color: #C9B989 !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #2F2A1E; }

    [data-testid="stDataFrame"] { background-color: #F2E7C9; }

    .roster-header {
        font-size: 0.72rem;
        font-weight: 700;
        color: #7A6F52;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .metric-badge {
        border-radius: 4px;
        text-align: center;
        padding: 2px 8px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
        min-width: 26px;
    }
    .match-score { font-size: 1.6rem; font-weight: 800; color: #2F2A1E; }

    /* Modern HTML tables (no white background) */
    .table-scroll { overflow-x: auto; margin-bottom: 1.2rem; border-radius: 10px; }
    table.modern-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #F2E7C9;
        border-radius: 10px;
        overflow: hidden;
    }
    table.modern-table thead tr { background-color: #3B3324; }
    table.modern-table th {
        color: #F2E7C9;
        text-transform: uppercase;
        font-size: 0.68rem;
        letter-spacing: 0.05em;
        padding: 9px 12px;
        text-align: left;
        white-space: nowrap;
    }
    table.modern-table td {
        padding: 7px 12px;
        border-bottom: 1px solid #DCCB9E;
        font-size: 0.85rem;
        color: #2F2A1E;
        white-space: nowrap;
    }
    table.modern-table tbody tr:nth-child(even) { background-color: #EADFC0; }
    table.modern-table tbody tr:hover { background-color: #DCCB9E; }
    table.modern-table tr.row-highlight { background-color: #C9B989 !important; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

OUTFIELD_METRICS = ['Goal-Scoring', 'Assist-Creation', 'Attack', 'Dribbling', 'Possession', 'Defense', 'Physical']
ABILITY_METRICS = OUTFIELD_METRICS + ['Goalkeeping']

METRIC_ABBR = {
    'Goal-Scoring': 'GS', 'Assist-Creation': 'AC', 'Attack': 'ATT', 'Dribbling': 'DRB',
    'Possession': 'POS', 'Defense': 'DEF', 'Physical': 'PHY', 'Goalkeeping': 'GK'
}

LEAGUE_LEVELS = {
    'Liga Portugal': 1,
    'Liga 2': 2,
    'Liga 3': 3,
    'Campeonato de Portugal': 4,
}

ordered_positions = ["GK", "CB", "FB & WB", "MF", "AM & W", "CF"]

SLOT_TO_POS_MAP = {
    'GK': 'GK',
    'CB': 'CB', 'CB1': 'CB', 'CB2': 'CB', 'CB3': 'CB',
    'LB': 'FB & WB', 'RB': 'FB & WB', 'LWB': 'FB & WB', 'RWB': 'FB & WB',
    'CM': 'MF', 'CM1': 'MF', 'CM2': 'MF', 'DM': 'MF', 'DM1': 'MF', 'DM2': 'MF', 'LM': 'MF', 'RM': 'MF',
    'LW': 'AM & W', 'RW': 'AM & W', 'LAM': 'AM & W', 'CAM': 'AM & W', 'RAM': 'AM & W',
    'ST': 'CF', 'ST1': 'CF', 'ST2': 'CF'
}

FORMATIONS = {
    "4-3-3": {
        'GK': (50, 10),
        'LB': (15, 28), 'CB1': (38, 26), 'CB2': (62, 26), 'RB': (85, 28),
        'CM1': (30, 52), 'DM': (50, 44), 'CM2': (70, 52),
        'LW': (20, 78), 'ST': (50, 83), 'RW': (80, 78)
    },
    "4-4-2": {
        'GK': (50, 10),
        'LB': (15, 28), 'CB1': (38, 26), 'CB2': (62, 26), 'RB': (85, 28),
        'LM': (18, 55), 'CM1': (38, 52), 'CM2': (62, 52), 'RM': (82, 55),
        'ST1': (38, 83), 'ST2': (62, 83)
    },
    "3-5-2": {
        'GK': (50, 10),
        'CB1': (25, 25), 'CB2': (50, 23), 'CB3': (75, 25),
        'LWB': (12, 52), 'CM1': (35, 48), 'DM': (50, 42), 'CM2': (65, 48), 'RWB': (88, 52),
        'ST1': (38, 83), 'ST2': (62, 83)
    },
    "4-2-3-1": {
        'GK': (50, 10),
        'LB': (15, 28), 'CB1': (38, 26), 'CB2': (62, 26), 'RB': (85, 28),
        'DM1': (38, 45), 'DM2': (62, 45),
        'LAM': (22, 68), 'CAM': (50, 68), 'RAM': (78, 68),
        'ST': (50, 85)
    }
}

DEFENSIVE_STYLES = ["High Press", "Middle Block", "Low Block"]
BUILDUP_STYLES = ["Slow Construction", "Direct Play", "Not Specific"]
FOCUS_STYLES = ["Focus through Middle", "Focus through Wings"]

ROLE_MATRIX = {
    'CB': ['Defensive CB', 'Ball-Playing CB', 'Wide Progressor CB'],
    'FB & WB': ['Defensive FB', 'Attacking FB', 'Playmaker FB'],
    'MF': ['Defensive MF', 'Ball Winner MF', 'Box-to-Box', 'Deep Lying Playmaker', 'Advanced Playmaker', 'Box Crasher'],
    'AM & W': ['Playmaker', 'Winger', 'Inside Forward'],
    'CF': ['Poacher', 'Pressing CF', 'False 9', 'Second Striker', 'Link-Up Forward'],
}

ROLE_METRIC_WEIGHTS = {
    'Defensive CB': {'Defense': 0.5, 'Physical': 0.3, 'Possession': 0.2},
    'Ball-Playing CB': {'Possession': 0.4, 'Defense': 0.35, 'Attack': 0.15, 'Dribbling': 0.1},
    'Wide Progressor CB': {'Possession': 0.3, 'Dribbling': 0.25, 'Defense': 0.25, 'Physical': 0.2},

    'Defensive FB': {'Defense': 0.5, 'Physical': 0.3, 'Possession': 0.2},
    'Attacking FB': {'Attack': 0.3, 'Dribbling': 0.25, 'Assist-Creation': 0.25, 'Physical': 0.2},
    'Playmaker FB': {'Possession': 0.35, 'Assist-Creation': 0.3, 'Dribbling': 0.2, 'Defense': 0.15},

    'Defensive MF': {'Defense': 0.45, 'Physical': 0.3, 'Possession': 0.25},
    'Ball Winner MF': {'Defense': 0.5, 'Physical': 0.35, 'Possession': 0.15},
    'Box-to-Box': {'Physical': 0.25, 'Defense': 0.2, 'Attack': 0.2, 'Possession': 0.2, 'Dribbling': 0.15},
    'Deep Lying Playmaker': {'Possession': 0.4, 'Assist-Creation': 0.3, 'Defense': 0.15, 'Dribbling': 0.15},
    'Advanced Playmaker': {'Assist-Creation': 0.4, 'Possession': 0.25, 'Dribbling': 0.2, 'Attack': 0.15},
    'Box Crasher': {'Attack': 0.35, 'Goal-Scoring': 0.3, 'Physical': 0.2, 'Dribbling': 0.15},

    'Playmaker': {'Assist-Creation': 0.4, 'Possession': 0.3, 'Dribbling': 0.3},
    'Winger': {'Dribbling': 0.4, 'Attack': 0.3, 'Physical': 0.15, 'Assist-Creation': 0.15},
    'Inside Forward': {'Attack': 0.35, 'Goal-Scoring': 0.35, 'Dribbling': 0.3},

    'Poacher': {'Goal-Scoring': 0.6, 'Attack': 0.25, 'Physical': 0.15},
    'Pressing CF': {'Physical': 0.35, 'Defense': 0.25, 'Attack': 0.25, 'Goal-Scoring': 0.15},
    'False 9': {'Assist-Creation': 0.35, 'Possession': 0.35, 'Goal-Scoring': 0.3},
    'Second Striker': {'Goal-Scoring': 0.35, 'Assist-Creation': 0.3, 'Dribbling': 0.2, 'Attack': 0.15},
    'Link-Up Forward': {'Possession': 0.35, 'Assist-Creation': 0.3, 'Attack': 0.2, 'Physical': 0.15},
}

ROLE_TEAM_EFFECT = {
    'Defensive CB': (-0.02, 0.05), 'Ball-Playing CB': (0.02, 0.02), 'Wide Progressor CB': (0.04, 0.0),
    'Defensive FB': (-0.02, 0.04), 'Attacking FB': (0.05, -0.02), 'Playmaker FB': (0.03, 0.0),
    'Defensive MF': (-0.02, 0.05), 'Ball Winner MF': (-0.01, 0.05), 'Box-to-Box': (0.02, 0.02),
    'Deep Lying Playmaker': (0.03, 0.01), 'Advanced Playmaker': (0.05, -0.01), 'Box Crasher': (0.05, -0.02),
    'Playmaker': (0.05, -0.01), 'Winger': (0.05, -0.02), 'Inside Forward': (0.06, -0.02),
    'Poacher': (0.06, -0.02), 'Pressing CF': (0.03, 0.02), 'False 9': (0.04, 0.0),
    'Second Striker': (0.05, -0.01), 'Link-Up Forward': (0.03, 0.0),
}

MAX_SUBS_PER_GAME = 5
ASSIST_PROBABILITY = 0.75


def format_eur(value):
    if pd.isna(value):
        return "—"
    if value >= 1_000_000:
        return f"€{value / 1_000_000:.2f}M"
    if value >= 1_000:
        return f"€{value / 1_000:.0f}K"
    return f"€{value:.0f}"


def relevant_metrics(position):
    if position == 'GK':
        return ['Goalkeeping']
    return OUTFIELD_METRICS


def prepare_metrics_display(df):
    df = df.copy()
    is_gk = df['Position'] == 'GK'
    for m in OUTFIELD_METRICS:
        df.loc[is_gk, m] = np.nan
    df.loc[~is_gk, 'Goalkeeping'] = np.nan
    return df


def get_metric_color(value):
    """0-100 quality scale: red -> orange -> yellow -> light green -> dark green."""
    if value < 20:
        return '#E74C3C', '#FFFFFF'
    elif value < 40:
        return '#E67E22', '#FFFFFF'
    elif value < 60:
        return '#F1C40F', '#2F2A1E'
    elif value < 80:
        return '#8BC34A', '#1B3B0F'
    else:
        return '#2E7D32', '#FFFFFF'


def get_rating_color(value):
    """0-10 match rating scale, centered so ~6.0 reads as an 'average' yellow/green."""
    if value < 5:
        return '#E74C3C', '#FFFFFF'
    elif value < 6:
        return '#E67E22', '#FFFFFF'
    elif value < 7:
        return '#F1C40F', '#2F2A1E'
    elif value < 8:
        return '#8BC34A', '#1B3B0F'
    else:
        return '#2E7D32', '#FFFFFF'


def df_to_html_table(df, badge_cols=None, badge_color_func=get_metric_color, highlight_col=None, highlight_val=None):
    """Renders a DataFrame as a modern, non-white HTML table. badge_cols is a dict of
    {column_name: decimal_places} for columns that should render as colored badges."""
    badge_cols = badge_cols or {}
    html = "<div class='table-scroll'><table class='modern-table'><thead><tr>"
    for col in df.columns:
        html += f"<th>{col}</th>"
    html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        row_cls = "row-highlight" if highlight_col and row.get(highlight_col) == highlight_val else ""
        html += f"<tr class='{row_cls}'>"
        for col in df.columns:
            val = row[col]
            if col in badge_cols and pd.notna(val):
                try:
                    fv = float(val)
                    bg, fg = badge_color_func(fv)
                    dec = badge_cols[col]
                    html += f"<td><span class='metric-badge' style='background:{bg};color:{fg};'>{fv:.{dec}f}</span></td>"
                    continue
                except (ValueError, TypeError):
                    pass
            html += f"<td>{val}</td>"
        html += "</tr>"
    html += "</tbody></table></div>"
    st.markdown(html, unsafe_allow_html=True)


def adjust_ratings_for_league_step(player, destination_league):
    """
    Discounts a signed player's ability metrics by 15% per league level stepped up
    (compounding), since a rating earned in a weaker league overstates true ability
    at a higher level. Liga Revelação U23 is not part of this tiering.
    """
    adjusted = dict(player)
    origin_level = LEAGUE_LEVELS.get(player.get('League'))
    dest_level = LEAGUE_LEVELS.get(destination_league)

    if origin_level is not None and dest_level is not None and origin_level > dest_level:
        levels_stepped = origin_level - dest_level
        multiplier = 0.85 ** levels_stepped
        for metric in ABILITY_METRICS:
            if metric in adjusted and pd.notna(adjusted[metric]):
                adjusted[metric] = adjusted[metric] * multiplier

    return adjusted


def get_tactic_modifiers():
    defensive = st.session_state.get('tactic_defensive', 'Middle Block')
    buildup = st.session_state.get('tactic_buildup', 'Not Specific')

    attack_mod = 0.0
    defense_mod = 0.0

    if defensive == 'High Press':
        attack_mod += 0.10
        defense_mod -= 0.05
    elif defensive == 'Low Block':
        attack_mod -= 0.05
        defense_mod += 0.15

    if buildup == 'Direct Play':
        attack_mod += 0.10
    elif buildup == 'Slow Construction':
        attack_mod -= 0.03
        defense_mod += 0.03

    return attack_mod, defense_mod


def get_role_modifiers():
    roles = st.session_state.get('starting_roles', {})
    if not roles:
        return 0.0, 0.0

    attack_total, defense_total, n = 0.0, 0.0, 0
    for role in roles.values():
        eff = ROLE_TEAM_EFFECT.get(role)
        if eff is None:
            continue
        attack_total += eff[0]
        defense_total += eff[1]
        n += 1

    if n == 0:
        return 0.0, 0.0
    return attack_total / n, defense_total / n


def compute_player_rating(player, team_gf, team_ga, role=None):
    """Synthetic match rating (3.0-10.0). Centered so that an average-quality
    player (50/100) in a drawn match scores ~6.0."""
    if player.get('Position') == 'GK':
        quality = player.get('Goalkeeping', 50)
        quality = 50 if pd.isna(quality) else quality
    else:
        weights = ROLE_METRIC_WEIGHTS.get(role)
        if weights:
            weighted_sum, total_w = 0.0, 0.0
            for metric, w in weights.items():
                val = player.get(metric)
                if pd.notna(val):
                    weighted_sum += val * w
                    total_w += w
            quality = (weighted_sum / total_w) if total_w > 0 else 50.0
        else:
            vals = [player.get(m) for m in OUTFIELD_METRICS if pd.notna(player.get(m))]
            quality = float(np.mean(vals)) if vals else 50.0

    base = 6.0 + (quality - 50.0) * 0.04 

    if team_gf > team_ga:
        result_adj = np.random.uniform(0.2, 0.6)
    elif team_gf < team_ga:
        result_adj = -np.random.uniform(0.2, 0.6)
    else:
        result_adj = np.random.uniform(-0.1, 0.1)

    noise = np.random.normal(0, 0.3)
    rating = float(np.clip(base + result_adj + noise, 3.0, 10.0))
    return round(rating, 1)


def get_xi_players():
    result = []
    for slot, pname in st.session_state.get('starting_xi', {}).items():
        p = next((pl for pl in st.session_state.active_squad if pl['Display_Name'] == pname), None)
        if p:
            role = st.session_state.get('starting_roles', {}).get(slot)
            result.append((slot, p, role))
    return result


def get_bench_players():
    starters = set(st.session_state.get('starting_xi', {}).values())
    return [p for p in st.session_state.active_squad if p['Display_Name'] not in starters]


def simulate_match_squad(xi_players):
    """Simulates up to MAX_SUBS_PER_GAME substitutions (GKs are never subbed).
    Returns (involved, events) where involved = [(player_dict, role), ...] for
    everyone who featured, and events describe each swap."""
    bench = get_bench_players()
    outfield_idxs = [i for i, (slot, p, role) in enumerate(xi_players) if p.get('Position') != 'GK']
    np.random.shuffle(outfield_idxs)

    max_subs = min(MAX_SUBS_PER_GAME, len(outfield_idxs))
    num_subs = np.random.randint(0, max_subs + 1) if max_subs > 0 else 0

    events = []
    used_bench = set()
    involved = [(p, role) for (slot, p, role) in xi_players]

    subs_done = 0
    for i in outfield_idxs:
        if subs_done >= num_subs:
            break
        slot, starter, role = xi_players[i]
        candidates = [b for b in bench if b.get('Position') == starter.get('Position') and b['Display_Name'] not in used_bench]
        if not candidates:
            continue
        sub_player = candidates[np.random.randint(len(candidates))]
        used_bench.add(sub_player['Display_Name'])
        events.append({'out': starter['Player'], 'in': sub_player['Player']})
        involved.append((sub_player, role))
        subs_done += 1

    return involved, events


def _weighted_pick(candidates_players_roles, metric, exclude_name=None):
    """Weighted-random pick of a player name based on a metric value + role emphasis."""
    names, weights = [], []
    for p, role in candidates_players_roles:
        if exclude_name is not None and p['Player'] == exclude_name:
            continue
        val = p.get(metric, 50)
        val = 50 if pd.isna(val) else val
        role_w = ROLE_METRIC_WEIGHTS.get(role, {}).get(metric, 0.05)
        w = max((role_w + 0.05) * (val / 100.0 + 0.1), 0.01)
        names.append(p['Player'])
        weights.append(w)
    if not names:
        return None
    weights = np.array(weights)
    weights = weights / weights.sum()
    return str(np.random.choice(names, p=weights))


def generate_match_report(gf, ga, involved):
    """Possession / shots / shots on target / goal events (scorer + optional assist)
    for the user's match, based on the quality of everyone who featured."""
    outfield = [(p, role) for p, role in involved if p.get('Position') != 'GK']

    if outfield:
        poss_vals = [p.get('Possession') for p, role in outfield if pd.notna(p.get('Possession'))]
        avg_poss = float(np.mean(poss_vals)) if poss_vals else 50.0

        attack_vals = []
        for p, role in outfield:
            vals = [p.get(m) for m in ['Attack', 'Goal-Scoring', 'Dribbling'] if pd.notna(p.get(m))]
            if vals:
                attack_vals.append(float(np.mean(vals)))
        avg_attack = float(np.mean(attack_vals)) if attack_vals else 50.0
    else:
        avg_poss, avg_attack = 50.0, 50.0

    poss_for = float(np.clip(50 + (avg_poss - 50) * 0.4 + np.random.uniform(-3, 3), 25, 75))
    poss_for = round(poss_for, 1)
    poss_against = round(100 - poss_for, 1)

    shots_for = int(np.random.poisson(max(1.0, 8 + (avg_attack - 50) / 8)))
    shots_for = max(shots_for, gf)
    sot_for = min(shots_for, gf + int(np.random.poisson(2)))
    sot_for = max(sot_for, gf)

    shots_against = int(np.random.poisson(8))
    shots_against = max(shots_against, ga)
    sot_against = min(shots_against, ga + int(np.random.poisson(2)))
    sot_against = max(sot_against, ga)

    goal_events = []
    if gf > 0 and outfield:
        for _ in range(gf):
            scorer = _weighted_pick(outfield, 'Goal-Scoring')
            assist = None
            if scorer and np.random.rand() < ASSIST_PROBABILITY and len(outfield) > 1:
                assist = _weighted_pick(outfield, 'Assist-Creation', exclude_name=scorer)
            goal_events.append({'scorer': scorer, 'assist': assist})

    return {
        'possession_for': poss_for, 'possession_against': poss_against,
        'shots_for': shots_for, 'sot_for': sot_for,
        'shots_against': shots_against, 'sot_against': sot_against,
        'goal_events': goal_events
    }


def simulate_user_match_extras(gf, ga, matchday_num, opponent, is_home):
    """Runs substitutions + match report + player ratings (with goals/assists) for
    the user's team for one matchday, and appends the results to session state."""
    xi_players = get_xi_players()
    if not xi_players:
        return
    involved, sub_events = simulate_match_squad(xi_players)

    report = generate_match_report(gf, ga, involved)
    report.update({
        'Matchday': matchday_num, 'GF': gf, 'GA': ga,
        'opponent': opponent, 'is_home': is_home, 'substitutions': sub_events
    })
    st.session_state.match_reports.append(report)

    goals_count = Counter(g['scorer'] for g in report['goal_events'] if g['scorer'])
    assists_count = Counter(g['assist'] for g in report['goal_events'] if g['assist'])

    for p, role in involved:
        rating = compute_player_rating(p, gf, ga, role=role)
        st.session_state.player_ratings_log.append({
            'Player': p['Player'], 'Position': p['Position'], 'Role': role or '-',
            'Matchday': matchday_num, 'Rating': rating,
            'Goals': goals_count.get(p['Player'], 0),
            'Assists': assists_count.get(p['Player'], 0)
        })


def generate_round_robin(teams):
    """Circle-method double round-robin: every team plays every other team home
    and away. Returns a list of rounds, each a list of (home, away) tuples."""
    teams = list(teams)
    bye = None
    if len(teams) % 2 != 0:
        bye = "__BYE__"
        teams.append(bye)

    n = len(teams)
    rotation = teams.copy()
    first_half = []
    for _ in range(n - 1):
        round_matches = []
        for i in range(n // 2):
            home, away = rotation[i], rotation[n - 1 - i]
            if bye not in (home, away):
                round_matches.append((home, away))
        first_half.append(round_matches)
        rotation = [rotation[0]] + [rotation[-1]] + rotation[1:-1]

    second_half = [[(away, home) for (home, away) in rnd] for rnd in first_half]
    return first_half + second_half


def simulate_matchday_fixtures(df_stand, round_matches, attack_mod, defense_mod, managed_team, md_num):
    """Simulates every fixture in this round as a real home-vs-away match, updating
    both teams' standings rows and the league-wide results log."""
    user_gf, user_ga, user_opponent, user_is_home = None, None, None, None
    base_home, base_away = 1.35, 1.05

    for home, away in round_matches:
        home_is_user = home == managed_team
        away_is_user = away == managed_team

        home_lambda, away_lambda = base_home, base_away
        if home_is_user:
            home_lambda = base_home + attack_mod
            away_lambda = max(0.1, base_away - defense_mod)
        elif away_is_user:
            away_lambda = base_away + attack_mod
            home_lambda = max(0.1, base_home - defense_mod)

        gf_home = int(np.random.poisson(max(0.1, home_lambda)))
        gf_away = int(np.random.poisson(max(0.1, away_lambda)))

        h_idx = df_stand.index[df_stand['Team'] == home]
        a_idx = df_stand.index[df_stand['Team'] == away]
        if len(h_idx) == 0 or len(a_idx) == 0:
            continue
        h_idx, a_idx = h_idx[0], a_idx[0]

        df_stand.loc[h_idx, 'MP'] += 1
        df_stand.loc[a_idx, 'MP'] += 1
        df_stand.loc[h_idx, 'GF'] += gf_home
        df_stand.loc[h_idx, 'GA'] += gf_away
        df_stand.loc[a_idx, 'GF'] += gf_away
        df_stand.loc[a_idx, 'GA'] += gf_home
        df_stand.loc[h_idx, 'GD'] = df_stand.loc[h_idx, 'GF'] - df_stand.loc[h_idx, 'GA']
        df_stand.loc[a_idx, 'GD'] = df_stand.loc[a_idx, 'GF'] - df_stand.loc[a_idx, 'GA']

        if gf_home > gf_away:
            df_stand.loc[h_idx, 'W'] += 1
            df_stand.loc[h_idx, 'Pts'] += 3
            df_stand.loc[a_idx, 'L'] += 1
        elif gf_home < gf_away:
            df_stand.loc[a_idx, 'W'] += 1
            df_stand.loc[a_idx, 'Pts'] += 3
            df_stand.loc[h_idx, 'L'] += 1
        else:
            df_stand.loc[h_idx, 'D'] += 1
            df_stand.loc[h_idx, 'Pts'] += 1
            df_stand.loc[a_idx, 'D'] += 1
            df_stand.loc[a_idx, 'Pts'] += 1

        st.session_state.all_results.append({
            'Matchday': md_num, 'home': home, 'away': away,
            'home_goals': gf_home, 'away_goals': gf_away
        })

        if home_is_user or away_is_user:
            user_is_home = home_is_user
            user_opponent = away if home_is_user else home
            user_gf = gf_home if home_is_user else gf_away
            user_ga = gf_away if home_is_user else gf_home

    return df_stand, user_gf, user_ga, user_opponent, user_is_home


def generate_league_transfers(league, league_teams, managed_team):
    """Simulates a one-off summer transfer market across the selected league:
    players moving between AI-controlled clubs (and up from lower tiers), for
    display only. The user's own club is excluded - those moves are made
    manually in the Scouting & Transfers tab."""
    dest_level = LEAGUE_LEVELS.get(league)
    if dest_level is not None:
        feeder_leagues = [league] + [lg for lg, lvl in LEAGUE_LEVELS.items() if lvl > dest_level]
    else:
        feeder_leagues = [league]

    candidate_pool = df_all[df_all['League'].isin(feeder_leagues)].copy()
    candidate_pool = candidate_pool[candidate_pool['Team'] != managed_team]

    other_teams = [t for t in league_teams if t != managed_team]
    if candidate_pool.empty or len(other_teams) < 2:
        return []

    num_transfers = int(np.random.randint(10, 21))
    transfers = []
    used_players = set()
    attempts = 0

    while len(transfers) < num_transfers and attempts < num_transfers * 6:
        attempts += 1
        player_row = candidate_pool.sample(1).iloc[0]
        if player_row['Player'] in used_players:
            continue
        origin_team = player_row['Team']
        possible_dest = [t for t in other_teams if t != origin_team]
        if not possible_dest:
            continue
        dest_team = str(np.random.choice(possible_dest))

        fee = player_row['Cost']
        origin_level = LEAGUE_LEVELS.get(player_row['League'])
        if origin_level is not None and dest_level is not None and origin_level > dest_level:
            fee = fee * (0.85 ** (origin_level - dest_level))

        transfers.append({
            'Player': player_row['Player'], 'Position': player_row['Position'],
            'From Team': origin_team, 'From League': player_row['League'],
            'To Team': dest_team, 'Fee': fee
        })
        used_players.add(player_row['Player'])

    return transfers


def build_new_season_state(league, teams, managed_team):
    schedule = generate_round_robin(teams)
    total_md = len(schedule)
    standings = pd.DataFrame({
        'Team': teams, 'MP': 0, 'W': 0, 'D': 0, 'L': 0, 'GF': 0, 'GA': 0, 'GD': 0, 'Pts': 0
    })
    transfers = generate_league_transfers(league, teams, managed_team)
    return schedule, total_md, standings, transfers

@st.cache_data
def load_and_value_dataset():
    df = pd.read_csv("DATA_git.csv")

    league_target_means = {
        'Liga Portugal': 3800000.0,
        'Liga 2': 200000.0,
        'Liga 3': 25000.0,
        'Campeonato de Portugal': 10000.0,
        'Liga Revelação U23': 30000.0
    }

    ability_metrics = ABILITY_METRICS

    df['Known_Value'] = df['Cost'].fillna(df['Sale'])

    features = ['Age', 'Position', 'League'] + ability_metrics
    numeric_features = ['Age'] + ability_metrics
    categorical_features = ['Position', 'League']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='constant', fill_value=0), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=2))
    ])

    train_df = df[df['Known_Value'].notna() & (df['Known_Value'] > 0)]
    model.fit(train_df[features], train_df['Known_Value'])

    df['Predicted_Val'] = model.predict(df[features])
    df['Market_Value'] = df['Known_Value'].fillna(df['Predicted_Val'])

    for league, target_mean in league_target_means.items():
        mask = df['League'] == league
        if mask.any():
            curr_mean = df.loc[mask, 'Market_Value'].mean()
            if curr_mean > 0:
                df.loc[mask, 'Market_Value'] *= (target_mean / curr_mean)

    df['Market_Value'] = df['Market_Value'].apply(lambda x: max(x, 5000.0))

    df['Cost'] = df['Market_Value'] * 1.15
    df['Sale'] = df['Market_Value'] * 0.85

    df['Display_Name'] = df.apply(
        lambda row: f"{row['Player']} ({row['Position']} | Age {int(row['Age'])} | {row['Team']})", axis=1
    )
    return df

df_all = load_and_value_dataset()

st.markdown("## ⚽ Football Manager")

col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    leagues = sorted(df_all["League"].dropna().unique().tolist())
    selected_league = st.selectbox("Select League", leagues)

league_df = df_all[df_all["League"] == selected_league]

with col_filter2:
    available_teams = sorted(league_df["Team"].dropna().unique().tolist())
    selected_team = st.selectbox("Managed Club", available_teams)

st.divider()

if 'player_ratings_log' not in st.session_state:
    st.session_state.player_ratings_log = []
if 'match_reports' not in st.session_state:
    st.session_state.match_reports = []
if 'all_results' not in st.session_state:
    st.session_state.all_results = []

if 'current_league' not in st.session_state or st.session_state.current_league != selected_league:
    st.session_state.current_league = selected_league
    schedule, total_md, standings, transfers = build_new_season_state(selected_league, available_teams, selected_team)
    st.session_state.schedule = schedule
    st.session_state.total_matchdays = total_md
    st.session_state.league_standings = standings
    st.session_state.matchday = 1
    st.session_state.all_results = []
    st.session_state.league_transfers = transfers

if 'user_team' not in st.session_state or st.session_state.user_team != selected_team:
    st.session_state.user_team = selected_team
    squad_base = df_all[(df_all['Team'] == selected_team) & (df_all['Season'] == '2025/26')].copy()
    if squad_base.empty:
        squad_base = df_all[df_all['Team'] == selected_team].copy()

    st.session_state.active_squad = squad_base.to_dict('records')
    total_val = sum(p['Market_Value'] for p in st.session_state.active_squad)
    st.session_state.budget = total_val * 0.25
    st.session_state.starting_xi = {}
    st.session_state.starting_roles = {}
    st.session_state.xi_confirmed = False
    st.session_state.player_ratings_log = []
    st.session_state.match_reports = []

    schedule, total_md, standings, transfers = build_new_season_state(selected_league, available_teams, selected_team)
    st.session_state.schedule = schedule
    st.session_state.total_matchdays = total_md
    st.session_state.league_standings = standings
    st.session_state.matchday = 1
    st.session_state.all_results = []
    st.session_state.league_transfers = transfers

squad_df = pd.DataFrame(st.session_state.active_squad)
current_squad_value = squad_df['Market_Value'].sum() if not squad_df.empty else 0

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"""
    <div class="stat-card"><div class="stat-label">MANAGED CLUB</div>
    <div class="stat-value">{selected_team}</div></div>
""", unsafe_allow_html=True)

c2.markdown(f"""
    <div class="stat-card"><div class="stat-label">TRANSFER BUDGET</div>
    <div class="stat-value">€ {st.session_state.budget:,.0f}</div></div>
""", unsafe_allow_html=True)

c3.markdown(f"""
    <div class="stat-card"><div class="stat-label">SQUAD VALUE</div>
    <div class="stat-value">€ {current_squad_value:,.0f}</div></div>
""", unsafe_allow_html=True)

c4.markdown(f"""
    <div class="stat-card"><div class="stat-label">SQUAD SIZE</div>
    <div class="stat-value">{len(squad_df)}</div></div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👥 Squad Roster",
    "📋 Starting XI & Tactics",
    "🔄 Scouting & Transfers",
    "⚽ Matchday Simulation",
    "📊 League Player Stats",
    "💼 League Transfer Market"
])

with tab1:
    st.subheader(f"👥 Roster Management - {selected_team}")

    if not squad_df.empty:
        pos_order_map = {"GK": 1, "CB": 2, "FB & WB": 3, "MF": 4, "AM & W": 5, "CF": 6}
        squad_df['pos_rank'] = squad_df['Position'].map(pos_order_map).fillna(99)
        squad_df = squad_df.sort_values(by=['pos_rank', 'Market_Value'], ascending=[True, False]).reset_index(drop=True)

        col_widths = [0.55, 2.0, 0.5] + [0.55] * len(ABILITY_METRICS) + [1.0, 1.0, 0.8]
        headers = ['Pos', 'Player', 'Age'] + [METRIC_ABBR[m] for m in ABILITY_METRICS] + ['Value', 'Sale', '']

        if len(squad_df) <= 11:
            st.caption("⚠️ Squad is at the 11-player minimum — the sell button is disabled until you sign a replacement.")

        header_cols = st.columns(col_widths)
        for hc, h in zip(header_cols, headers):
            hc.markdown(f"<span class='roster-header'>{h}</span>", unsafe_allow_html=True)

        for idx, row in squad_df.iterrows():
            with st.container(border=True):
                row_cols = st.columns(col_widths)
                row_cols[0].write(row['Position'])
                row_cols[1].write(row['Player'])
                row_cols[2].write(int(row['Age']))

                rel_metrics = relevant_metrics(row['Position'])
                for i, metric in enumerate(ABILITY_METRICS):
                    val = row[metric]
                    if metric in rel_metrics and pd.notna(val):
                        bg, fg = get_metric_color(val)
                        row_cols[3 + i].markdown(
                            f"<div class='metric-badge' style='background:{bg};color:{fg};'>{val:.0f}</div>",
                            unsafe_allow_html=True
                        )
                    else:
                        row_cols[3 + i].markdown(
                            "<div class='metric-badge' style='color:#9a917a;'>—</div>",
                            unsafe_allow_html=True
                        )

                row_cols[3 + len(ABILITY_METRICS)].write(format_eur(row['Market_Value']))
                row_cols[3 + len(ABILITY_METRICS) + 1].write(format_eur(row['Sale']))

                sell_disabled = len(squad_df) <= 11
                if row_cols[3 + len(ABILITY_METRICS) + 2].button("Sell", key=f"sell_{row['Display_Name']}_{idx}", disabled=sell_disabled):
                    st.session_state.active_squad = [
                        p for p in st.session_state.active_squad if p['Display_Name'] != row['Display_Name']
                    ]
                    st.session_state.budget += row['Sale']
                    st.success(f"Successfully sold {row['Player']} for {format_eur(row['Sale'])}!")
                    st.rerun()
    else:
        st.warning("No player data available for this team.")

with tab2:
    st.subheader("📋 Tactical Setup & Pitch Lineup")

    col_t1, col_t2 = st.columns([1, 2])

    with col_t1:
        st.markdown("### ⚙️ Tactical Setup")
        formation_choice = st.selectbox("Select Formation:", list(FORMATIONS.keys()))
        slots = FORMATIONS[formation_choice]

        st.markdown("### 🧠 Team Identity")
        st.selectbox("Defensive Approach:", DEFENSIVE_STYLES, key="tactic_defensive")
        st.selectbox("Build-Up Style:", BUILDUP_STYLES, key="tactic_buildup")
        st.selectbox("Attacking Focus:", FOCUS_STYLES, key="tactic_focus")

        st.markdown("### 🎯 Assign Starting XI & Roles")
        current_xi = {}
        current_roles = {}
        assigned_players = set()

        for slot in slots.keys():
            req_pos = SLOT_TO_POS_MAP[slot]
            eligible_players = [
                p for p in st.session_state.active_squad
                if p['Position'] == req_pos and p['Display_Name'] not in assigned_players
            ]
            options = ["-- Select Player --"] + [p['Display_Name'] for p in eligible_players]

            player_col, role_col = st.columns([1.4, 1])
            selected_player = player_col.selectbox(
                f"{slot} ({req_pos})",
                options=options,
                key=f"slot_select_{formation_choice}_{slot}"
            )

            if selected_player != "-- Select Player --":
                current_xi[slot] = selected_player
                assigned_players.add(selected_player)

            if req_pos in ROLE_MATRIX:
                role_options = ["-- Select Role --"] + ROLE_MATRIX[req_pos]
                selected_role = role_col.selectbox(
                    "Role",
                    options=role_options,
                    key=f"role_select_{formation_choice}_{slot}",
                    label_visibility="hidden" if slot != list(slots.keys())[0] else "visible"
                )
                if selected_role != "-- Select Role --":
                    current_roles[slot] = selected_role

        st.markdown("---")
        if st.button("✅ Confirm Starting XI Lineup", type="primary", use_container_width=True):
            role_slots_needed = [s for s in slots if SLOT_TO_POS_MAP[s] != 'GK']
            missing_roles = [s for s in role_slots_needed if current_roles.get(s) is None]

            if len(current_xi) != len(slots):
                st.error(f"Please assign all {len(slots)} positions before confirming.")
            elif missing_roles:
                st.error(f"Please assign a role for: {', '.join(missing_roles)}")
            else:
                st.session_state.starting_xi = current_xi
                st.session_state.starting_roles = current_roles
                st.session_state.xi_confirmed = True
                st.success("Starting XI Lineup & Roles Confirmed & Saved!")

        if st.session_state.xi_confirmed:
            st.info("🟢 Status: Starting XI Lineup Confirmed (squad locked — transfer market closed)")
        else:
            st.warning("🟠 Status: Lineup Pending Confirmation")

        st.caption(f"During simulation, up to {MAX_SUBS_PER_GAME} substitutions may be made per match "
                   f"from your bench (goalkeepers are not substituted).")

    with col_t2:
        st.markdown(f"### 🏟️ Pitch View - {formation_choice}")

        fig, ax = plt.subplots(figsize=(8, 10))
        fig.patch.set_facecolor('#2e8b57')
        ax.set_facecolor('#2e8b57')

        ax.plot([0, 100, 100, 0, 0], [0, 0, 100, 100, 0], color="white", lw=2)
        ax.plot([0, 100], [50, 50], color="white", lw=2)
        center_circle = patches.Circle((50, 50), 10, color="white", fill=False, lw=2)
        ax.add_patch(center_circle)

        ax.add_patch(patches.Rectangle((22, 0), 56, 18, color="white", fill=False, lw=2))
        ax.add_patch(patches.Rectangle((22, 82), 56, 18, color="white", fill=False, lw=2))

        for slot, (x, y) in slots.items():
            player_name = current_xi.get(slot, "Empty")
            display_str = player_name.split(" (")[0] if " (" in player_name else player_name
            role_str = current_roles.get(slot, "")
            label = f"{display_str}\n{role_str}" if role_str else display_str

            ax.scatter(x, y, color="gold" if player_name != "Empty" else "grey", s=500, zorder=3, edgecolors='black')
            ax.text(x, y, slot, color="black", fontsize=8, weight="bold", ha="center", va="center", zorder=4)
            ax.text(x, y - 4.5, label, color="white", fontsize=7.5, weight="bold", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="black", alpha=0.6))

        ax.set_xlim(-5, 105)
        ax.set_ylim(-5, 105)
        plt.axis("off")
        st.pyplot(fig)

with tab3:
    st.subheader("🔄 Scouting Network & Market")

    active_squad_names = [p['Player'] for p in st.session_state.active_squad]
    pool_full = df_all[~df_all['Player'].isin(active_squad_names)].copy()

    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    s_league = col_f1.selectbox("Filter League:", ["All"] + sorted(pool_full['League'].dropna().unique().tolist()))
    pool = pool_full if s_league == "All" else pool_full[pool_full['League'] == s_league]

    s_team = col_f2.selectbox("Filter Team:", ["All"] + sorted(pool['Team'].dropna().unique().tolist()))
    if s_team != "All":
        pool = pool[pool['Team'] == s_team]

    s_position = col_f3.selectbox("Filter Position:", ["All"] + ordered_positions)
    if s_position != "All":
        pool = pool[pool['Position'] == s_position]

    if not pool_full.empty:
        age_lo, age_hi = int(pool_full['Age'].min()), int(pool_full['Age'].max())
    else:
        age_lo, age_hi = 15, 40
    s_age_range = col_f4.slider("Filter Age:", min_value=age_lo, max_value=age_hi, value=(age_lo, age_hi))
    pool = pool[(pool['Age'] >= s_age_range[0]) & (pool['Age'] <= s_age_range[1])]

    st.markdown("---")
    st.markdown("### 📋 Scouting Pool & Player Values")
    st.caption(
        "Attribute ratings reflect quality relative to each player's own league (first column). "
        "Signing a player from a lower division discounts their ratings by 15% per league level "
        "stepped up, applied once they join your squad."
    )

    if pool.empty:
        st.info("No players found matching current filters.")
    else:
        display_df = prepare_metrics_display(
            pool[['League', 'Position', 'Player', 'Age', 'Team'] + ABILITY_METRICS + ['Market_Value', 'Cost']]
        ).reset_index(drop=True)
        display_df['Market_Value'] = display_df['Market_Value'].apply(format_eur)
        display_df['Cost'] = display_df['Cost'].apply(format_eur)
        display_df = display_df.rename(columns={m: METRIC_ABBR[m] for m in ABILITY_METRICS})
        display_df = display_df.rename(columns={'Market_Value': 'Market Value', 'Cost': 'Transfer Cost'})

        badge_cols = {METRIC_ABBR[m]: 0 for m in ABILITY_METRICS}
        df_to_html_table(display_df, badge_cols=badge_cols, badge_color_func=get_metric_color)

        st.markdown("### 🛒 Sign Player")
        sign_options = pool['Display_Name'].tolist()
        selected_target = st.selectbox("Select Target Player:", [""] + sign_options)

        if selected_target != "":
            target_data = pool[pool['Display_Name'] == selected_target].iloc[0].to_dict()
            cost = target_data['Cost']
            mkt_val = target_data['Market_Value']

            origin_level = LEAGUE_LEVELS.get(target_data.get('League'))
            dest_level = LEAGUE_LEVELS.get(selected_league)
            if origin_level is not None and dest_level is not None and origin_level > dest_level:
                levels_stepped = origin_level - dest_level
                pct_drop = (1 - 0.85 ** levels_stepped) * 100
                st.warning(
                    f"⚠️ This player is moving up from **{target_data.get('League')}** to **{selected_league}** "
                    f"({levels_stepped} level(s) up). Their attribute ratings will be reduced by "
                    f"{pct_drop:.1f}% upon signing to reflect the step up in league quality."
                )

            st.info(f"**Player Market Value:** € {mkt_val:,.0f} | **Required Transfer Fee:** € {cost:,.0f}")

            if st.button("➕ Confirm Signing", type="primary"):
                if st.session_state.budget >= cost:
                    st.session_state.budget -= cost
                    adjusted_player = adjust_ratings_for_league_step(target_data, selected_league)
                    st.session_state.active_squad.append(adjusted_player)
                    st.success(f"Successfully signed {target_data['Player']} for € {cost:,.0f}!")
                    st.rerun()
                else:
                    st.error("Insufficient transfer budget to complete this acquisition!")

with tab4:
    st.subheader(f"⚽ {selected_league} - Matchday Simulation")

    total_md = st.session_state.total_matchdays

    col_m1, col_m2 = st.columns([1, 2])

    with col_m1:
        st.markdown("### 🗓️ Tournament Controls")
        st.write(f"**Current Matchday:** {min(st.session_state.matchday, total_md)} / {total_md}")

        season_over = st.session_state.matchday > total_md
        if season_over:
            st.success("🏁 Season complete!")
        elif not st.session_state.xi_confirmed:
            st.warning("⚠️ Please confirm your Starting XI in Tab 2 before simulating matchdays.")

        play_disabled = (not st.session_state.xi_confirmed) or season_over

        if st.button("▶️ Play Next Matchday", type="primary", disabled=play_disabled):
            round_idx = st.session_state.matchday - 1
            round_matches = st.session_state.schedule[round_idx]
            df_stand = st.session_state.league_standings.copy()
            t_am, t_dm = get_tactic_modifiers()
            r_am, r_dm = get_role_modifiers()
            attack_mod, defense_mod = t_am + r_am, t_dm + r_dm

            df_stand, user_gf, user_ga, opponent, is_home = simulate_matchday_fixtures(
                df_stand, round_matches, attack_mod, defense_mod, selected_team, st.session_state.matchday
            )
            st.session_state.league_standings = df_stand.sort_values(
                by=['Pts', 'GD', 'GF'], ascending=False
            ).reset_index(drop=True)

            if user_gf is not None:
                simulate_user_match_extras(user_gf, user_ga, st.session_state.matchday, opponent, is_home)

            st.session_state.matchday += 1
            st.success(f"Matchday {st.session_state.matchday - 1} completed!")
            st.rerun()

        if st.button("⚡ Fast Forward Entire Season", disabled=play_disabled):
            remaining = total_md - st.session_state.matchday + 1
            if remaining > 0:
                df_stand = st.session_state.league_standings.copy()
                t_am, t_dm = get_tactic_modifiers()
                r_am, r_dm = get_role_modifiers()
                attack_mod, defense_mod = t_am + r_am, t_dm + r_dm
                start_md = st.session_state.matchday

                for step in range(remaining):
                    md_num = start_md + step
                    round_matches = st.session_state.schedule[md_num - 1]
                    df_stand, user_gf, user_ga, opponent, is_home = simulate_matchday_fixtures(
                        df_stand, round_matches, attack_mod, defense_mod, selected_team, md_num
                    )
                    if user_gf is not None:
                        simulate_user_match_extras(user_gf, user_ga, md_num, opponent, is_home)

                st.session_state.league_standings = df_stand.sort_values(
                    by=['Pts', 'GD', 'GF'], ascending=False
                ).reset_index(drop=True)
                st.session_state.matchday = total_md + 1
                st.success("Season finished!")
                st.rerun()

    with col_m2:
        st.markdown("### 🏆 League Standings Table")
        standings_display = st.session_state.league_standings.copy()
        df_to_html_table(standings_display, highlight_col='Team', highlight_val=selected_team)

    st.divider()
    st.markdown("### 🗂️ League Results Matrix (Home vs Away)")
    st.caption("Rows = home team, columns = away team. Shows the score once that fixture has been played.")

    if st.session_state.all_results:
        teams_sorted = sorted(available_teams)
        matrix_df = pd.DataFrame("", index=teams_sorted, columns=teams_sorted)
        for t in teams_sorted:
            matrix_df.loc[t, t] = "—"
        for r in st.session_state.all_results:
            if r['home'] in matrix_df.index and r['away'] in matrix_df.columns:
                matrix_df.loc[r['home'], r['away']] = f"{r['home_goals']}-{r['away_goals']}"
        matrix_df = matrix_df.reset_index().rename(columns={'index': 'Home \\ Away'})
        df_to_html_table(matrix_df, highlight_col='Home \\ Away', highlight_val=selected_team)
    else:
        st.info("Play a matchday to start filling in the results matrix.")

    st.divider()
    st.markdown("### 📰 Match Report")

    match_reports = st.session_state.get('match_reports', [])
    if match_reports:
        available_mds = [r['Matchday'] for r in match_reports]
        selected_md = st.selectbox("View report for matchday:", available_mds, index=len(available_mds) - 1)
        report = next(r for r in match_reports if r['Matchday'] == selected_md)

        venue_tag = "Home" if report['is_home'] else "Away"
        if report['is_home']:
            score_line = f"{selected_team} {report['GF']} - {report['GA']} {report['opponent']}"
        else:
            score_line = f"{report['opponent']} {report['GA']} - {report['GF']} {selected_team}"

        st.markdown(
            f"<div class='match-score'>{score_line}</div>"
            f"<div style='color:#7A6F52;'>Matchday {selected_md} · {venue_tag}</div>",
            unsafe_allow_html=True
        )

        stat_cols = st.columns(3)
        stat_cols[0].metric("Avg. Possession", f"{report['possession_for']:.0f}% - {report['possession_against']:.0f}%")
        stat_cols[1].metric("Shots", f"{report['shots_for']} - {report['shots_against']}")
        stat_cols[2].metric("Shots on Target", f"{report['sot_for']} - {report['sot_against']}")

        if report['goal_events']:
            lines = []
            for g in report['goal_events']:
                if g['assist']:
                    lines.append(f"{g['scorer']} (assist: {g['assist']})")
                else:
                    lines.append(g['scorer'])
            st.write(f"**⚽ Goals:** {', '.join(lines)}")
        else:
            st.write("**⚽ Goals:** No goals scored.")

        if report['substitutions']:
            subs_str = " | ".join(f"{e['out']} ➜ {e['in']}" for e in report['substitutions'])
            st.write(f"**🔄 Substitutions:** {subs_str}")
        else:
            st.write("**🔄 Substitutions:** None made.")

        st.markdown("**Player Ratings — This Match**")
        ratings_df_all = pd.DataFrame(st.session_state.get('player_ratings_log', []))
        if not ratings_df_all.empty:
            this_match_df = ratings_df_all[ratings_df_all['Matchday'] == selected_md].sort_values('Rating', ascending=False)
            this_match_df = this_match_df[['Player', 'Position', 'Role', 'Rating', 'Goals', 'Assists']].reset_index(drop=True)
            df_to_html_table(this_match_df, badge_cols={'Rating': 1}, badge_color_func=get_rating_color)
    else:
        st.info("Play a matchday to generate a match report.")

    st.markdown("### 🌟 Season Average Player Ratings")
    ratings_log = st.session_state.get('player_ratings_log', [])
    if ratings_log:
        ratings_df = pd.DataFrame(ratings_log)
        season_avg = ratings_df.groupby(['Player', 'Position']).agg(
            **{'Avg Rating': ('Rating', 'mean'), 'Appearances': ('Rating', 'count'),
               'Goals': ('Goals', 'sum'), 'Assists': ('Assists', 'sum')}
        ).reset_index()
        season_avg = season_avg.sort_values('Avg Rating', ascending=False).reset_index(drop=True)
        df_to_html_table(season_avg, badge_cols={'Avg Rating': 2}, badge_color_func=get_rating_color)
    else:
        st.info("Player season averages will appear here once matchdays have been played.")

with tab5:
    st.subheader(f"📊 Player Statistics - {selected_league}")
    st.caption(
        "Appearances, goals and assists are tracked for your own squad's players, since they are "
        "the only players individually simulated match-by-match in this league."
    )

    ratings_log = st.session_state.get('player_ratings_log', [])
    if ratings_log:
        stats_df = pd.DataFrame(ratings_log)
        stats_agg = stats_df.groupby(['Player', 'Position']).agg(
            **{'Appearances': ('Rating', 'count'), 'Goals': ('Goals', 'sum'),
               'Assists': ('Assists', 'sum'), 'Avg Rating': ('Rating', 'mean')}
        ).reset_index()

        sort_choice = st.selectbox("Sort by:", ["Goals", "Assists", "Appearances", "Avg Rating"])
        stats_agg = stats_agg.sort_values(sort_choice, ascending=False).reset_index(drop=True)

        df_to_html_table(stats_agg, badge_cols={'Avg Rating': 2}, badge_color_func=get_rating_color)
    else:
        st.info("Play a matchday in the Matchday Simulation tab to start generating player statistics.")

with tab6:
    st.subheader(f"💼 Transfer Market - {selected_league}")

    market_open = (not st.session_state.xi_confirmed) and (st.session_state.matchday == 1)

    if not market_open:
        st.info(
            "🔒 The transfer market is closed. It's only available before you confirm your Starting XI "
            "and before the first matchday is played."
        )
    else:
        st.caption(
            "A simulated summer transfer window across the rest of the league (your own club's transfers "
            "are handled separately, in Scouting & Transfers)."
        )
        transfers = st.session_state.get('league_transfers', [])
        if transfers:
            transfers_df = pd.DataFrame(transfers)[['Player', 'Position', 'From Team', 'From League', 'To Team', 'Fee']].copy()
            transfers_df['Fee'] = transfers_df['Fee'].apply(format_eur)
            df_to_html_table(transfers_df)
        else:
            st.info("No transfers were generated for this league.")