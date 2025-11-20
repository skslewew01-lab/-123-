# streamlit_korean_baseball_short.py
import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="한국 야구 도감", layout="wide")

# -------------------------
# 유틸 함수
def load_image(u):
    try:
        resp = requests.get(u, timeout=6)
        return Image.open(BytesIO(resp.content))
    except:
        return None

def radar_chart(stats_list, labels, names, title="능력치 비교"):
    N = len(labels)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]
    fig = plt.figure(figsize=(5,4))
    ax = fig.add_subplot(111, polar=True)
    for stats, name in zip(stats_list, names):
        vals = stats + stats[:1]
        ax.plot(angles, vals, label=name)
        ax.fill(angles, vals, alpha=0.1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    ax.set_ylim(0,100)
    ax.set_title(title)
    ax.legend(loc='upper right')
    return fig

# -------------------------
# 초기 데이터 (Top10)
PLAYERS = {
    '류현진': {'team':'한화','age':38,'position':'투수','stats':{'Contact':45,'Power':50,'Speed':40,'Defense':85,'Arm':90,'Clutch':80},
             'images':['https://upload.wikimedia.org/wikipedia/commons/6/60/Hyun-jin_Ryu_2019.jpg']},
    '김하성': {'team':'샌디에이고','age':30,'position':'유격수','stats':{'Contact':70,'Power':65,'Speed':80,'Defense':85,'Arm':75,'Clutch':70},
             'images':['https://upload.wikimedia.org/wikipedia/commons/5/5d/Ha-seong_Kim_2023.jpg']},
    # 나머지 선수 간략화
}

if 'players' not in st.session_state:
    st.session_state.players = PLAYERS.copy()

# -------------------------
# 상단
st.header("🏅 Top10 한국 야구 선수")
top10 = list(st.session_state.players.values())[:10]
cols = st.columns(3)
for i, p in enumerate(top10):
    with cols[i%3]:
        if p.get('images'):
            img = load_image(p['images'][0])
            if img:
                st.image(ImageOps.fit(img,(250,150)), caption=p.get('team',''))
        st.write(p.get('position',''), p.get('age',''))

# -------------------------
# 검색
search_q = st.text_input("도감 검색 (이름/팀)")
filtered = []
for name, p in st.session_state.players.items():
    if search_q.lower() in name.lower() or search_q.lower() in p.get('team','').lower():
        filtered.append((name,p))

st.subheader(f"검색 결과 {len(filtered)}명")
for name, p in filtered:
    st.write(name, p.get('team',''), p.get('position',''), p.get('age',''))

# -------------------------
# 비교
comp_names = st.multiselect("비교할 선수 선택 (2~4명)", options=list(st.session_state.players.keys()))
if len(comp_names)>=2:
    labels = ['Contact','Power','Speed','Defense','Arm','Clutch']
    stats_list = [[st.session_state.players[n]['stats'][l] for l in labels] for n in comp_names]
    fig = radar_chart(stats_list, labels, comp_names)
    st.pyplot(fig)
    df = pd.DataFrame({n:[st.session_state.players[n]['stats'][l] for l in labels] for n in comp_names}, index=labels)
    st.bar_chart(df)

# -------------------------
# 선수 추가
st.subheader("✍️ 선수 추가 / 편집")
with st.form('add'):
    aname = st.text_input("이름")
    ateam = st.text_input("팀")
    aage = st.number_input("나이",15,60,25)
    apos = st.text_input("포지션")
    aimg = st.text_input("이미지 URL")
    submitted = st.form_submit_button("저장")
    if submitted and aname:
        st.session_state.players[aname] = {'team':ateam,'age':aage,'position':apos,'stats':{'Contact':50,'Power':50,'Speed':50,'Defense':50,'Arm':50,'Clutch':50},'images':[aimg]}
        st.success(f"{aname} 저장됨")
