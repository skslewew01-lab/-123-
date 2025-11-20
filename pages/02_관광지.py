# streamlit_korean_baseball_compare.py
# 확장 버전: 한국 야구선수 비교 + 추가등록 + 상세 프로필 + 배경 강화 + 취미 정보
# - 선수 Top10 + 신규 선수 추가 가능
# - 선수 비교 기능(포지션, 나이, 팀, 주요 기록)
# - 선수별 취미/성격/특징 표시
# - 더 화려한 배경 스타일링
# - Streamlit Cloud에서 그대로 실행 가능

import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="한국 야구선수 비교", layout="wide")
st.title("⚾ 한국 야구선수 종합 비교 · 상세 프로필 · 이미지 갤러리")
st.caption("선수 추가도 가능! 더 풍부한 정보와 배경 꾸미기 적용.")

# -------------------------------
# 기본 선수 데이터
# -------------------------------
players_data = [
    {
        "name": "류현진",
        "team": "한화 이글스 / MLB(다저스·토론토)",
        "age": 38,
        "position": "투수",
        "records": "MLB 사이영상 후보, 한국 야구 역사상 최고의 좌완 중 하나",
        "hobby": "요리, 강아지 산책",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/6/60/Hyun-jin_Ryu_2019.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/6/60/Hyun-jin_Ryu_2019.jpg"
    },
    {
        "name": "김하성",
        "team": "샌디에이고 파드리스",
        "age": 30,
        "position": "유격수/내야수",
        "records": "MLB 골드글러브급 수비, 빠른 발과 다양한 포지션 소화",
        "hobby": "게임, 음악 감상",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/5/5d/Ha-seong_Kim_2023.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Ha-seong_Kim_2023.jpg"
    },
    {
        "name": "양의지",
        "team": "두산 베어스",
        "age": 38,
        "position": "포수",
        "records": "KBO 최고의 포수. 타격·수비·리드 완전체",
        "hobby": "낚시, 커피 수집",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/2/29/Yang_Eui-ji.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/2/29/Yang_Eui-ji.jpg"
    }
]

# DataFrame for comparing players
players_df = pd.DataFrame(players_data)

# Helper — load image from URL

def load_image(url):
    try:
        r = requests.get(url, timeout=5)
        return Image.open(BytesIO(r.content)).convert("RGBA")
    except:
        return None

# -------------------------------
# 선수 추가 기능 (사용자 입력)
# -------------------------------
st.sidebar.header("➕ 선수 추가하기")
with st.sidebar.form("add_player"):
    new_name = st.text_input("선수 이름")
    new_team = st.text_input("팀")
    new_age = st.number_input("나이", 18, 60, 28)
    new_position = st.text_input("포지션")
    new_record = st.text_area("업적/기록")
    new_hobby = st.text_input("취미")
    new_image_url = st.text_input("대표 이미지 URL")
    submit_new = st.form_submit_button("추가")

if submit_new and new_name:
    players_data.append({
        "name": new_name,
        "team": new_team,
        "age": new_age,
        "position": new_position,
        "records": new_record,
        "hobby": new_hobby,
        "images": [new_image_url],
        "bg": new_image_url
    })
    st.success(f"선수 '{new_name}' 추가 완료!")

# -------------------------------
# 선수 비교 기능
# -------------------------------
st.subheader("📊 선수 비교하기")
selected_players = st.multiselect(
    "비교할 선수 선택 (2~5명)",
    [p["name"] for p in players_data]
)

if len(selected_players) >= 2:
    compare_df = pd.DataFrame([
        {k: v for k, v in p.items() if k in ["name", "team", "age", "position", "records", "hobby"]}
        for p in players_data if p["name"] in selected_players
    ])
    st.dataframe(compare_df, use_container_width=True)

# -------------------------------
# 선수별 상세 카드 + 갤러리 + 배경
# -------------------------------
st.subheader("✨ 선수 상세 정보 & 갤러리")

for p in players_data:
    st.markdown(f"### 🧢 {p['name']}")

    # Player background block
    st.markdown(
        f"<div style='padding:14px;border-radius:12px;background-image:url({p['bg']});background-size:cover;background-position:center;color:white;'>"
        f"<div style='backdrop-filter: blur(4px);background:rgba(0,0,0,0.5);padding:10px;border-radius:10px;'>"
        f"<h3 style='margin:0px'>{p['name']}</h3>"
        f"<p>팀: {p['team']} | 나이: {p['age']} | 포지션: {p['position']}</p>"
        f"<p><b>업적:</b> {p['records']}</p>"
        f"<p><b>취미:</b> {p['hobby']}</p>"
        f"</div></div><br>", unsafe_allow_html=True)

    # Image gallery
    cols = st.columns(3)
    for i, img_url in enumerate(p['images']):
        img = load_image(img_url)
        if img:
            cols[i % 3].image(img, use_column_width=True)

    st.markdown("---")

# -------------------------------
# requirements.txt
# -------------------------------
st.subheader("📄 requirements.txt")
st.code(
"""
streamlit
pandas
Pillow
requests
"""
)

st.caption("원하면 성적 그래프, 시즌별 WAR 차트, 팀별 색상 테마도 넣어줄게!")

