# streamlit_korean_baseball_pro_plus.py
# 완전판: 한국 야구선수 도감 + 강화된 비교 + 시즌 스탯 연동 + 팀 테마/로고 + 애니메이션 UI + 대량 업로드(CSV/JSON) + 능력치 자동추정
# 실행: streamlit run streamlit_korean_baseball_pro_plus.py

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
# 스타일 (CSS) — 페이지 꾸미기
# -------------------------
st.markdown("""
<style>
/* 배경 그라데이션과 글꼴 */
body {
  background: linear-gradient(135deg, #0f172a 0%, #0b1220 50%, #071029 100%);
  color: #e6eef8;
}
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

# helper: load image (URL or uploaded file)
def load_image(u):
    try:
        if hasattr(u, 'getvalue'):
            return Image.open(BytesIO(u.getvalue())).convert('RGBA')
        resp = requests.get(u, timeout=6)
        return Image.open(BytesIO(resp.content)).convert('RGBA')
    except Exception:
        return None

# helper: image -> datauri
def img_to_datauri(img, fmt='PNG'):
    buffered = BytesIO()
    img.save(buffered, format=fmt)
    b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{fmt.lower()};base64,{b64}"

# radar chart for comparison
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

# default team theme mapping (색상 + 로고 url). 사용자 커스터마이즈 가능.
DEFAULT_TEAM_THEMES = {
    '두산 베어스': {'color':'#c8102e', 'logo':'https://upload.wikimedia.org/wikipedia/commons/5/55/Doosan_Bears_logo.png'},
    '키움 히어로즈': {'color':'#ff5b00', 'logo':'https://upload.wikimedia.org/wikipedia/commons/9/9b/KT_Wiz_logo.png'},
    'KIA 타이거즈': {'color':'#f15a24', 'logo':'https://upload.wikimedia.org/wikipedia/commons/4/4a/KIA_Tigers_logo.png'},
    '한화 이글스': {'color':'#ffd200', 'logo':'https://upload.wikimedia.org/wikipedia/commons/1/1a/Hanwha_Eagles_logo.png'},
    '키움': {'color':'#ff5b00','logo':''},
    '롯데 자이언츠': {'color':'#d40000','logo':'https://upload.wikimedia.org/wikipedia/commons/1/1a/Lotte_Giants_logo.png'},
    'KIA': {'color':'#f15a24','logo':''},
    'SSG 랜더스': {'color':'#e4002b','logo':'https://upload.wikimedia.org/wikipedia/commons/3/30/SSG_Landers_logo.png'},
    'KT 위즈': {'color':'#ff4d00','logo':'https://upload.wikimedia.org/wikipedia/commons/2/2b/KT_Wiz_logo.png'},
    'LG 트윈스': {'color':'#1b458f','logo':'https://upload.wikimedia.org/wikipedia/commons/1/15/LG_Twins_logo.png'},
    # add more as needed
}

# -------------------------
# 초기 선수 목록 (Top10 포함) — 이름 키로 저장
# -------------------------
INITIAL_PLAYERS = {
    '류현진': dict(name='류현진', team='한화 이글스', age=38, position='투수', records='MLB에서 활약한 대표 좌완. 꾸준한 성적과 제구력.',
                hobby='요리, 반려견 산책', images=['https://upload.wikimedia.org/wikipedia/commons/6/60/Hyun-jin_Ryu_2019.jpg'],
                stats={'Contact':45,'Power':50,'Speed':40,'Defense':85,'Arm':90,'Clutch':80}),
    '김하성': dict(name='김하성', team='샌디에이고 파드리스', age=30, position='유격수/내야수', records='다재다능한 수비형 내야수.',
                hobby='게임, 음악', images=['https://upload.wikimedia.org/wikipedia/commons/5/5d/Ha-seong_Kim_2023.jpg'],
                stats={'Contact':70,'Power':65,'Speed':80,'Defense':85,'Arm':75,'Clutch':70}),
    '추신수': dict(name='추신수', team='은퇴', age=43, position='외야수', records='MLB 장기 활약, 높은 출루 능력.', hobby='낚시, 골프',
                images=['https://upload.wikimedia.org/wikipedia/commons/1/12/Choo_Shin-soo_2013.jpg'], stats={'Contact':80,'Power':70,'Speed':50,'Defense':60,'Arm':65,'Clutch':85}),
    '이승엽': dict(name='이승엽', team='은퇴', age=47, position='지명타자/1루수', records='KBO 대표 슬러거, 다수 홈런 기록.', hobby='골프',
                images=['https://upload.wikimedia.org/wikipedia/commons/8/87/Lee_Seung-yeop.jpg'], stats={'Contact':75,'Power':95,'Speed':35,'Defense':40,'Arm':55,'Clutch':90}),
    '양의지': dict(name='양의지', team='두산 베어스', age=38, position='포수', records='리드와 수비가 뛰어난 완성형 포수.', hobby='낚시, 커피 수집',
                images=['https://upload.wikimedia.org/wikipedia/commons/2/29/Yang_Eui-ji.jpg'], stats={'Contact':75,'Power':60,'Speed':40,'Defense':90,'Arm':70,'Clutch':85}),
    '박병호': dict(name='박병호', team='키움 히어로즈', age=36, position='1루수/지명타자', records='강력한 장타자, 홈런왕 출신.', hobby='피트니스',
                images=['https://upload.wikimedia.org/wikipedia/commons/6/6f/Park_Byung-ho.jpg'], stats={'Contact':65,'Power':95,'Speed':45,'Defense':50,'Arm':60,'Clutch':80}),
    '최형우': dict(name='최형우', team='KIA 타이거즈', age=41, position='외야수', records='꾸준한 성적의 베테랑.', hobby='골프',
                images=['https://upload.wikimedia.org/wikipedia/commons/4/4a/Choi_Hyung-woo.jpg'], stats={'Contact':78,'Power':70,'Speed':50,'Defense':68,'Arm':62,'Clutch':88}),
    '김광현': dict(name='김광현', team='SSG 랜더스', age=37, position='투수', records='제구 중심의 베테랑 좌완.', hobby='등산',
                images=['https://upload.wikimedia.org/wikipedia/commons/3/3f/Kim_Kwang-hyun.jpg'], stats={'Contact':40,'Power':35,'Speed':30,'Defense':88,'Arm':88,'Clutch':75}),
    '배지환': dict(name='배지환', team='두산 베어스', age=24, position='내야수', records='젊은 유망주.', hobby='게임, 드라이브',
                images=['https://example.com/bae1.jpg'], stats={'Contact':68,'Power':55,'Speed':72,'Defense':70,'Arm':66,'Clutch':60}),
    '안현민': dict(name='안현민', team='KT 위즈', age=27, position='외야수', records='빠른 발과 컨택 능력.', hobby='음악, 운동',
                images=['https://example.com/ahn1.jpg'], stats={'Contact':70,'Power':60,'Speed':85,'Defense':65,'Arm':60,'Clutch':65}),
}

# session state init
if 'players' not in st.session_state:
    st.session_state.players = INITIAL_PLAYERS.copy()
if 'team_themes' not in st.session_state:
    st.session_state.team_themes = DEFAULT_TEAM_THEMES.copy()

# -------------------------
# 유저 인터페이스: 상단 헤더
# -------------------------
col1, col2 = st.columns([3,1])
with col1:
    st.markdown('<div class="big-title">한국 야구선수 도감 — PRO</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Top10 · 도감 검색 · 게임처럼 비교 · 시즌 스탯 연동 · 팀 테마 · 대량 업로드</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="logo-row"><div class="badge animate-pulse">프로 모드</div></div>', unsafe_allow_html=True)

st.markdown('---')

# -------------------------
# 사이드바: 업로드 / 팀 테마 설정 / 검색·비교 컨트롤
# -------------------------
st.sidebar.header('관리 패널')
# 팀 테마 편집
with st.sidebar.expander('팀 색상·로고 설정'):
    team_to_edit = st.selectbox('팀 선택(직접 입력 가능)', options=list(st.session_state.team_themes.keys()))
    new_color = st.color_picker('팀 색상', value=st.session_state.team_themes[team_to_edit]['color'])
    new_logo = st.text_input('팀 로고 URL', value=st.session_state.team_themes[team_to_edit].get('logo',''))
    if st.button('저장 (팀 테마)'):
        st.session_state.team_themes[team_to_edit] = {'color':new_color, 'logo':new_logo}
        st.success('팀 테마 저장됨')

st.sidebar.markdown('---')
# 대량 업로드
with st.sidebar.expander('대량 업로드 (CSV 또는 JSON)'):
    bulk_file = st.file_uploader('CSV/JSON 파일 업로드 (columns: name,team,age,position,records,hobby,avg,hr,sb,war,era,images)', type=['csv','json'])
    if st.button('대량 등록 실행') and bulk_file is not None:
        try:
            if bulk_file.type == 'application/json' or bulk_file.name.lower().endswith('.json'):
                raw = json.load(bulk_file)
                rows = raw if isinstance(raw, list) else [raw]
            else:
                df = pd.read_csv(bulk_file)
                rows = df.to_dict(orient='records')
            added = 0
            for r in rows:
                name = r.get('name') or r.get('이름')
                if not name: continue
                images = []
                if r.get('images'):
                    if isinstance(r.get('images'), str):
                        images = r.get('images').split('|')
                    else:
                        images = r.get('images')
                # auto estimate stats if season numbers provided
                stats = None
                if any(k in r for k in ('avg','AVG','hr','HR','sb','SB','war','WAR','era','ERA')):
                    stats = estimate_stats_from_season(r)
                st.session_state.players[name] = dict(
                    name=name,
                    team=r.get('team', r.get('팀','')),
                    age=int(r.get('age', r.get('나이',25))) if r.get('age') else 25,
                    position=r.get('position', r.get('포지션','')),
                    records=r.get('records', r.get('업적','')),
                    hobby=r.get('hobby',''),
                    images=images,
                    stats=stats if stats else {'Contact':50,'Power':50,'Speed':50,'Defense':50,'Arm':50,'Clutch':50}
                )
                added += 1
            st.success(f'대량 등록 완료: {added}명 추가/업데이트')
        except Exception as e:
            st.error(f'대량 등록 실패: {e}')

st.sidebar.markdown('---')
search_q = st.sidebar.text_input('도감 검색 (이름/팀/포지션)')
min_age, max_age = st.sidebar.slider('나이 범위', 15, 60, (15,60))
position_filter = st.sidebar.multiselect('포지션 필터', options=list({p['position'] for p in st.session_state.players.values()}))
comp_names = st.sidebar.multiselect('비교할 선수 선택 (최대 4명)', options=list(st.session_state.players.keys()))

# -------------------------
# 시즌 스탯 → 능력치 자동 추정 함수
# (간단한 휴리스틱: 정규화 후 가중치 매핑)
# -------------------------

def normalize(val, minv, maxv):
    try:
        v = float(val)
    except:
        return 0.0
    return max(0.0, min(1.0, (v - minv) / (maxv - minv) if maxv>minv else 0.0))

@st.cache_data
def estimate_stats_from_season(row):
    # row: dict-like with possible keys avg/AVG, hr/HR, sb/SB, war/WAR, era/ERA
    avg = row.get('avg') or row.get('AVG') or row.get('타율') or 0
    hr = row.get('hr') or row.get('HR') or 0
    sb = row.get('sb') or row.get('SB') or 0
    war = row.get('war') or row.get('WAR') or 0
    era = row.get('era') or row.get('ERA') or 999

    # Normalize to 0-1 using typical boundaries (customize as needed)
    n_avg = normalize(float(avg) if avg else 0, 0.18, 0.35) # 타율
    n_hr = normalize(float(hr) if hr else 0, 0, 60)
    n_sb = normalize(float(sb) if sb else 0, 0, 60)
    n_war = normalize(float(war) if war else 0, -1, 10)
    n_era = 1 - normalize(float(era) if era else 999, 0.5, 7.0) # 낮을수록 좋음

    # Map to game stats 0-100
    contact = int(40 + n_avg * 60)
    power = int(20 + n_hr * 80)
    speed = int(30 + n_sb * 70)
    defense = int(40 + n_war * 60)
    arm = int(30 + n_war * 60)
    clutch = int(40 + n_war * 60)
    return {'Contact':contact,'Power':power,'Speed':speed,'Defense':defense,'Arm':arm,'Clutch':clutch}

# -------------------------
# 메인 화면: Top10 그리드 (카드 스타일)
# -------------------------
st.header('🏅 오늘의 Top10')
players = list(st.session_state.players.values())
# sort by a simple overall score (sum of stats)
def overall_score(p):
    s = p.get('stats',{})
    return sum([s.get(k,50) for k in ['Contact','Power','Speed','Defense','Arm','Clutch']])
players_sorted = sorted(players, key=lambda x: overall_score(x), reverse=True)

top10 = players_sorted[:10]

st.markdown('<div class="card-grid">', unsafe_allow_html=True)
for i, p in enumerate(top10):
    # theme color
    team = p.get('team','')
    theme = st.session_state.team_themes.get(team, {'color':'#2b6cb0','logo':''})
    color = theme['color']
    logo = theme.get('logo','')
    # build card html
    img = None
    if p.get('images'):
        img = load_image(p['images'][0])
    card_html = f"""
    <div class='player-card'>
        <div style='display:flex;gap:10px;align-items:center'>
            <div style='width:72px;height:52px;overflow:hidden;border-radius:8px'>"""
    if img:
        try:
            datauri = img_to_datauri(ImageOps.fit(img, (300,200)))
            card_html += f"<img src='{datauri}' style='width:100%;height:100%;object-fit:cover;border-radius:8px'/>"
        except:
            card_html += ""
    card_html += f"""</div>
            <div style='flex:1'>
                <div style='font-weight:700;color:{color}'>#{i+1} {p['name']}</div>
                <div class='small-muted'>{p.get('team','')} • {p.get('position','')}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('---')

# -------------------------
# 도감 검색 결과 리스트
# -------------------------
filtered = []
for p in players:
    if search_q:
        if search_q.lower() not in p['name'].lower() and search_q.lower() not in p.get('team','').lower() and search_q.lower() not in p.get('position','').lower():
            continue
    if not (min_age <= int(p.get('age',0)) <= max_age):
        continue
    if position_filter and p.get('position') not in position_filter:
        continue
    filtered.append(p)

st.header(f'📚 도감 검색 결과 — {len(filtered)}명')
for p in filtered:
    with st.expander(f"{p['name']} — {p.get('team','')} ({p.get('position','')}, 나이 {p.get('age','-')})"):
        left, right = st.columns([1,2])
        with left:
            if p.get('images'):
                img = load_image(p['images'][0])
                if img:
                    st.image(ImageOps.fit(img,(360,240)), caption=p['name'])
            st.markdown(f"**팀:** {p.get('team','')}  
**포지션:** {p.get('position','')}  
**나이:** {p.get('age','')}  ")
            st.markdown(f"**취미:** {p.get('hobby','-')}  
**업적:** {p.get('records','-')}")
            prof_txt = textwrap.dedent(f"""
                이름: {p.get('name')}
                팀: {p.get('team')}
                포지션: {p.get('position')}
                나이: {p.get('age')}
                업적: {p.get('records')}
                취미: {p.get('hobby')}
            """)
            st.download_button('프로필 다운로드', data=prof_txt.encode('utf-8'), file_name=f"{p.get('name')}_profile.txt")
        with right:
            # gallery
            imgs = p.get('images', [])
            if imgs:
                cols = st.columns(3)
                for i,u in enumerate(imgs):
                    img2 = load_image(u)
                    if img2:
                        cols[i%3].image(img2, use_column_width=True)
            # radar preview
            labels = ['Contact','Power','Speed','Defense','Arm','Clutch']
            stats = [p.get('stats',{}).get(l,50) for l in labels]
            fig = radar_chart([stats], labels, [p.get('name')], title=f"{p.get('name')} 능력치")
            st.pyplot(fig)
            plt.close(fig)

st.markdown('---')

# -------------------------
# 비교 섹션
# -------------------------
st.header('⚔️ 선수 비교 (게임 스타일)')
if comp_names and len(comp_names) >= 2:
    comp_players = [st.session_state.players[n] for n in comp_names if n in st.session_state.players]
    labels = ['Contact','Power','Speed','Defense','Arm','Clutch']
    stats_list = [[p.get('stats',{}).get(l,50) for l in labels] for p in comp_players]
    fig = radar_chart(stats_list, labels, [p['name'] for p in comp_players], title='선수 능력치 비교')
    st.pyplot(fig)
    plt.close(fig)
    st.subheader('능력치별 바 차트')
    df_comp = pd.DataFrame({p['name']:[p.get('stats',{}).get(l,50) for l in labels] for p in comp_players}, index=labels)
    st.bar_chart(df_comp)
    comp_table = []
    for p in comp_players:
        row = {'이름':p['name'],'팀':p.get('team',''),'포지션':p.get('position',''),'나이':p.get('age','')}
        row.update({k:p.get('stats',{}).get(k,50) for k in labels})
        comp_table.append(row)
    st.table(pd.DataFrame(comp_table))
else:
    st.info('사이드바에서 비교할 선수 2명 이상을 선택하세요 (최대 4명).')

st.markdown('---')

# -------------------------
# 선수 직접 추가/편집 (하단 폼)
# -------------------------
st.header('✍️ 선수 추가 / 편집')
with st.form('add_edit'):
    aname = st.text_input('이름')
    ateam = st.text_input('팀')
    aage = st.number_input('나이', 15, 60, 25)
    apos = st.text_input('포지션')
    arec = st.text_area('업적/설명')
    ahobby = st.text_input('취미')
    aimg = st.text_input('이미지 URL (여러개는 | 로 구분)')
    aavg = st.text_input('시즌 타율(선택)')
    ahr = st.text_input('시즌 HR(선택)')
    asb = st.text_input('시즌 도루(선택)')
    awar = st.text_input('시즌 WAR(선택)')
    aera = st.text_input('시즌 ERA(선택, 투수일 경우)')
    submitted = st.form_submit_button('저장')
    if submitted and aname:
        images = [s.strip() for s in aimg.split('|')] if aimg else []
        row = {'avg':aavg or None, 'hr':ahr or None, 'sb':asb or None, 'war':awar or None, 'era':aera or None}
        maybe_stats = estimate_stats_from_season(row)
        st.session_state.players[aname] = dict(name=aname, team=ateam, age=aage, position=apos, records=arec, hobby=ahobby, images=images, stats=maybe_stats)
        st.success(f"선수 {aname} 저장됨")

st.markdown('---')

# -------------------------
# 마무리 도움말
# -------------------------
st.subheader('도움말 & 다음 단계')
st.write('- 페이지가 심심하다면 배경 SVG, 선수 애니메이션 GIF, 또는 팀 로고를 더 추가해드릴게요.
- 시즌별 시계열 그래프(연도별 AVG/HR/WAR 등)도 연결 가능 — 원하시면 예시 CSV 양식 제공.
- 더 원하는 스타일(카드 애니메이션, 글꼴, 테마 색상)을 말해주면 바로 반영합니다.')

st.sidebar.subheader('필요 패키지')
st.sidebar.code('''
streamlit
pandas
Pillow
requests
matplotlib
numpy
''')

# 끝
