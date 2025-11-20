# streamlit_korean_baseball_pro_plus_fixed.py
import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import pandas as pd
import base64
import matplotlib.pyplot as plt
import numpy as np
import json
import textwrap

st.set_page_config(page_title="한국 야구 도감 PRO", layout="wide")

# -------------------------
# radar chart helper
def radar_chart(stats_list, labels, names, title="능력치 비교"):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    fig = plt.figure(figsize=(6,5))
    ax = fig.add_subplot(111, polar=True)
    for stats, name in zip(stats_list, names):
        vals = stats + stats[:1]
        ax.plot(angles, vals, linewidth=2, label=name)
        ax.fill(angles, vals, alpha=0.12)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0,100)
    ax.set_title(title)
    ax.legend(loc='upper right', bbox_to_anchor=(1.35, 1.05))
    return fig

# -------------------------
# normalize + estimate_stats_from_season
def normalize(val, minv, maxv):
    try:
        v = float(val)
    except:
        return 0.0
    return max(0.0, min(1.0, (v - minv) / (maxv - minv) if maxv>minv else 0.0))

@st.cache_data
def estimate_stats_from_season(row):
    avg = row.get('avg') or row.get('AVG') or row.get('타율') or 0
    hr = row.get('hr') or row.get('HR') or 0
    sb = row.get('sb') or row.get('SB') or 0
    war = row.get('war') or row.get('WAR') or 0
    era = row.get('era') or row.get('ERA') or 999
    n_avg = normalize(float(avg) if avg else 0, 0.18, 0.35)
    n_hr = normalize(float(hr) if hr else 0, 0, 60)
    n_sb = normalize(float(sb) if sb else 0, 0, 60)
    n_war = normalize(float(war) if war else 0, -1, 10)
    n_era = 1 - normalize(float(era) if era else 999, 0.5, 7.0)
    contact = int(40 + n_avg * 60)
    power = int(20 + n_hr * 80)
    speed = int(30 + n_sb * 70)
    defense = int(40 + n_war * 60)
    arm = int(30 + n_war * 60)
    clutch = int(40 + n_war * 60)
    return {'Contact':contact,'Power':power,'Speed':speed,'Defense':defense,'Arm':arm,'Clutch':clutch}

# -------------------------
# load image helper
def load_image(u):
    try:
        if hasattr(u, 'getvalue'):
            return Image.open(BytesIO(u.getvalue())).convert('RGBA')
        resp = requests.get(u, timeout=6)
        return Image.open(BytesIO(resp.content)).convert('RGBA')
    except:
        return None

def img_to_datauri(img, fmt='PNG'):
    buffered = BytesIO()
    img.save(buffered, format=fmt)
    b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{fmt.lower()};base64,{b64}"

# -------------------------
# CSS
st.markdown("""
<style>
body {background: linear-gradient(135deg, #0f172a 0%, #0b1220 50%, #071029 100%); color: #e6eef8;}
.reportview-container .main header {visibility: hidden}
.logo-row {display:flex;align-items:center;gap:12px}
.player-card {border-radius:14px;padding:10px;background:linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));box-shadow: 0 8px 24px rgba(2,6,23,0.6);}
.big-title {font-size:28px;font-weight:700;color:#fff;margin-bottom:6px}
.subtitle {color:#c7d2fe}
.badge {display:inline-block;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,0.06);margin-right:6px;font-size:12px}
.animate-pulse {animation: pulse 2.4s infinite}
@keyframes pulse {0% {transform:scale(1);}50%{transform:scale(1.02);}100%{transform:scale(1);}}
.small-muted{color:#9aa7c7;font-size:13px}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}
</style>
""", unsafe_allow_html=True)

# -------------------------
# 초기 데이터, 세션 상태
INITIAL_PLAYERS = {...}  # 위에 올린 Top10 그대로 사용
DEFAULT_TEAM_THEMES = {...}  # 위 코드 그대로
if 'players' not in st.session_state:
    st.session_state.players = INITIAL_PLAYERS.copy()
if 'team_themes' not in st.session_state:
    st.session_state.team_themes = DEFAULT_TEAM_THEMES.copy()

# -------------------------
# 메인 UI, 검색, 비교, 추가/편집, Top10 카드
# -------------------------
# (위에 올린 코드 그대로 이어서 쓰면 됨)
# 핵심은 SyntaxError 방지 위해 모든 함수 정의가 먼저, 
# 데이터/세션 초기화가 먼저, 그 다음 UI 섹션 순서

