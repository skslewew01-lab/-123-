# streamlit_korean_baseball_full.py
# 한국 야구선수 비교 · 추가 · 상세 프로필 · 화려한 배경 · 이미지 업로드 지원
# 실행: streamlit run streamlit_korean_baseball_full.py

import streamlit as st
from PIL import Image, ImageOps
import requests
from io import BytesIO
import pandas as pd
import base64

st.set_page_config(page_title="한국 야구선수 비교·프로필", layout="wide")

# -------------------------
# 유틸리티 함수
# -------------------------

def load_image(url_or_file):
    """URL 또는 업로드된 파일(UploadedFile) 모두 처리"""
    try:
        if hasattr(url_or_file, "getvalue"):
            return Image.open(BytesIO(url_or_file.getvalue())).convert("RGBA")
        else:
            resp = requests.get(url_or_file, timeout=5)
            return Image.open(BytesIO(resp.content)).convert("RGBA")
    except Exception:
        return None


def img_to_datauri(img, fmt='PNG'):
    buffered = BytesIO()
    img.save(buffered, format=fmt)
    b64 = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/{fmt.lower()};base64,{b64}"


def highlight_card_html(name, subtitle, bg_datauri):
    return f'''<div style="border-radius:16px;overflow:hidden;box-shadow:0 6px 18px rgba(0,0,0,0.25);">
        <div style="background-image:url('{bg_datauri}');background-size:cover;background-position:center;padding:18px;">
            <div style="backdrop-filter: blur(4px);background:rgba(0,0,0,0.45);padding:12px;border-radius:10px;color:white;">
                <h3 style="margin:0">{name}</h3>
                <div style="font-size:13px;color:#eee">{subtitle}</div>
            </div>
        </div>
    </div>'''

# -------------------------
# 초기 선수 데이터 (Top10)
# -------------------------
initial_players = [
    dict(name="류현진", team="한화 이글스 / MLB(다저스·토론토)", age=38, position="투수",
         records="MLB 사이영상 후보, KBO·MLB 통산 우수 성적", hobby="요리, 강아지 산책",
         images=["https://upload.wikimedia.org/wikipedia/commons/6/60/Hyun-jin_Ryu_2019.jpg"]),
    dict(name="김하성", team="샌디에이고 파드리스", age=30, position="유격수/내야수",
         records="MLB에서 다재다능한 내야수로 활약", hobby="게임, 음악 감상",
         images=["https://upload.wikimedia.org/wikipedia/commons/5/5d/Ha-seong_Kim_2023.jpg"]),
    dict(name="추신수", team="은퇴 / 역대: 텍사스 등(MLB)", age=43, position="외야수",
         records="긴 MLB 경력, 높은 출루율", hobby="낚시, 골프",
         images=["https://upload.wikimedia.org/wikipedia/commons/1/12/Choo_Shin-soo_2013.jpg"]),
    dict(name="이승엽", team="은퇴 / KBO·NPB", age=47, position="지명타자/1루수",
         records="KBO 대표 슬러거, 다수의 홈런 기록", hobby="가족, 골프",
         images=["https://upload.wikimedia.org/wikipedia/commons/8/87/Lee_Seung-yeop.jpg"]),
    dict(name="양의지", team="두산 베어스", age=38, position="포수",
         records="KBO 최고의 포수, 다수 골든글러브", hobby="낚시, 커피 수집",
         images=["https://upload.wikimedia.org/wikipedia/commons/2/29/Yang_Eui-ji.jpg"]),
    dict(name="안현민", team="KT 위즈", age=27, position="외야수",
         records="빠른 발과 컨택 능력", hobby="음악, 운동",
         images=["https://example.com/ahn1.jpg"]),
    dict(name="김광현", team="SSG 랜더스 / MLB 경력", age=37, position="투수",
         records="KBO·MLB에서 활약한 베테랑 좌완", hobby="낚시, 등산",
         images=["https://upload.wikimedia.org/wikipedia/commons/3/3f/Kim_Kwang-hyun.jpg"]),
    dict(name="박병호", team="키움 히어로즈", age=36, position="1루수/지명타자",
         records="강력한 장타력, KBO 홈런왕 경험", hobby="피트니스, 야구 분석",
         images=["https://upload.wikimedia.org/wikipedia/commons/6/6f/Park_Byung-ho.jpg"]),
    dict(name="최형우", team="KIA 타이거즈", age=41, position="외야수",
         records="꾸준한 클러치 히터", hobby="골프, 가족",
         images=["https://upload.wikimedia.org/wikipedia/commons/4/4a/Choi_Hyung-woo.jpg"]),
    dict(name="배지환", team="두산 베어스", age=24, position="내야수",
         records="젊은 유망주", hobby="게임, 드라이브",
         images=["https://example.com/bae1.jpg"]),
]

# 상태 보관: 세션 상태에 선수 목록 유지
if "players" not in st.session_state:
    st.session_state.players = initial_players.copy()

# -------------------------
# 사이드바: 추가/업로드/설정
# -------------------------
st.sidebar.title("관리 패널")
with st.sidebar.expander("➕ 선수 추가 / 업로드 (이미지 파일 가능)"):
    add_name = st.text_input("이름", key="add_name")
    add_team = st.text_input("팀", key="add_team")
    add_age = st.number_input("나이", min_value=15, max_value=60, value=25, key="add_age")
    add_position = st.text_input("포지션", key="add_position")
    add_records = st.text_area("업적/설명", key="add_records")
    add_hobby = st.text_input("취미", key="add_hobby")
    add_image_url = st.text_input("대표 이미지 URL (선택)", key="add_img_url")
    uploaded_files = st.file_uploader("이미지 업로드 (선택, 여러개 가능)", accept_multiple_files=True)
    if st.button("선수 추가하기"):
        img_urls = []
        # 우선 업로드된 파일을 세션에 저장하고 이미지 데이터 URI로 사용
        for f in uploaded_files:
            st.session_state.setdefault('uploaded_images', {})
            fid = f.name + str(len(st.session_state.uploaded_images))
            st.session_state.uploaded_images[fid] = f.getvalue()
            # convert to datauri
            img = load_image(f)
            if img:
                img_urls.append(img_to_datauri(img))
        if add_image_url:
            img_urls.append(add_image_url)
        if not img_urls:
            img_urls = [""]
        st.session_state.players.append(dict(name=add_name, team=add_team, age=add_age,
                                             position=add_position, records=add_records,
                                             hobby=add_hobby, images=img_urls))
        st.success(f"선수 '{add_name}' 추가됨")

st.sidebar.markdown("---")
if st.sidebar.button("데이터 CSV로 내보내기"):
    flat = []
    for p in st.session_state.players:
        flat.append({"name": p.get('name',''), "team": p.get('team',''), "age": p.get('age',''),
                     "position": p.get('position',''), "records": p.get('records',''), "hobby": p.get('hobby','')})
    df = pd.DataFrame(flat)
    csv = df.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button("CSV 다운로드", data=csv, file_name="korean_baseball_players.csv", mime="text/csv")

# -------------------------
# 메인: 검색, 비교, 상세 카드
# -------------------------
st.header("한국 야구선수 비교 · 프로필 뷰어")

# 검색/필터
col1, col2, col3 = st.columns([3, 2, 2])
with col1:
    q = st.text_input("선수 검색 / 필터 (이름, 팀, 포지션)")
with col2:
    min_age, max_age = st.slider("나이 범위", 15, 60, (15, 60))
with col3:
    show_images = st.checkbox("이미지 표시", value=True)

# 필터링된 선수 목록
filtered = []
for p in st.session_state.players:
    if q:
        if q.lower() not in p.get('name','').lower() and q.lower() not in p.get('team','').lower() and q.lower() not in p.get('position','').lower():
            continue
    if not (min_age <= int(p.get('age',0)) <= max_age):
        continue
    filtered.append(p)

st.subheader(f"검색 결과: {len(filtered)}명")

# 다중 선택 비교
names = [p['name'] for p in filtered]
selected = st.multiselect("비교할 선수 선택 (2~5명) — 선택하지 않으면 모두 카드로 표시됩니다", options=names)

if selected and len(selected) >= 2:
    comp = [p for p in filtered if p['name'] in selected]
    comp_flat = [{"이름": p['name'], "팀": p.get('team',''), "나이": p.get('age',''), "포지션": p.get('position',''), "업적": p.get('records',''), "취미": p.get('hobby','')} for p in comp]
    st.table(pd.DataFrame(comp_flat))
    st.markdown("---")

# 상세 카드 그리기 (선택된 게 있으면 선택된 것만, 없으면 필터된 전부)
render_list = [p for p in filtered if (not selected) or (p['name'] in selected)]

for p in render_list:
    col_a, col_b = st.columns([1,2])
    with col_a:
        # 배경 이미지 우선 로드 (첫 이미지가 datauri이면 직접 사용)
        bg = p.get('images',[None])[0]
        bg_img = None
        if bg:
            if bg.startswith('data:image'):
                bg_datauri = bg
            else:
                img = load_image(bg)
                if img:
                    bg_datauri = img_to_datauri(ImageOps.fit(img, (800,300)))
                else:
                    bg_datauri = ""
        else:
            bg_datauri = ""

        st.markdown(highlight_card_html(p['name'], f"{p.get('team','')} • {p.get('position','')} • 나이 {p.get('age','')}", bg_datauri), unsafe_allow_html=True)
        # 주요 정보
        st.markdown(f"**업적 / 소개**\n\n{p.get('records','정보 없음')}")
        st.markdown(f"**취미 / 성격**\n\n{p.get('hobby','-')}")

    with col_b:
        if show_images and p.get('images'):
            imgs = p.get('images', [])
            cols = st.columns(3)
            for i, u in enumerate(imgs):
                if not u:
                    continue
                img = None
                if u.startswith('data:image'):
                    # decode
                    header, b64 = u.split(',',1)
                    img = Image.open(BytesIO(base64.b64decode(b64))).convert('RGBA')
                else:
                    img = load_image(u)
                if img:
                    cols[i%3].image(img, use_column_width=True, caption=f"{p['name']} 이미지 {i+1}")
        # 버튼: 상세 프로필 다운로드 (간단 텍스트)
        prof_text = f"이름: {p.get('name','')}\n팀: {p.get('team','')}\n나이: {p.get('age','')}\n포지션: {p.get('position','')}\n업적: {p.get('records','')}\n취미: {p.get('hobby','')}\n"
        b = prof_text.encode('utf-8')
        st.download_button(label="프로필 텍스트 다운로드", data=b, file_name=f"{p['name']}_profile.txt")

    st.markdown("---")

st.caption("원하면 팀별 색상 테마, 시즌 성적 차트, WAR 정렬, 또는 카드 애니메이션을 추가해줄게요 — 어떤 걸 먼저 넣어볼까?")

# -------------------------
# requirements
# -------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("필요 패키지")
st.sidebar.code("""
streamlit
pandas
Pillow
requests
""")
