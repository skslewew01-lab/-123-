# streamlit_korean_baseball_top10.py
# Streamlit app: "한국 야구선수 Top10"
# - Displays Top 10 Korean baseball players with career, team, styled background per player
# - Lots of images (image URLs) shown in galleries
# - Copy this file to Streamlit Cloud (or run `streamlit run streamlit_korean_baseball_top10.py` locally)

import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="한국 야구선수 Top10", layout="wide")

st.title("⚾ 한국 야구선수 Top 10 — 커리어 & 팀 소개")
st.caption("주관적 순위입니다. 선수별 이미지와 배경을 풍성하게 꾸몄어요.")

# Top10 선수 데이터 (간단 소개 + 이미지 URL 리스트)
players = [
    {
        "rank": 1,
        "name": "류현진 (Ryu Hyun-jin)",
        "position": "투수",
        "team": "프리/역대: 토론토, LA다저스 등",
        "career": "KBO와 MLB에서 모두 성공을 거둔 대한민국 대표 좌완 에이스. 2019-2020년대 MLB에서 뛰어난 성적을 기록.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/6/60/Hyun-jin_Ryu_2019.jpg",
            "https://pbs.twimg.com/media/ExampleRyu1.jpg",
            "https://images.espncdn.com/i/headshots/mlb/players/full/32582.png"
        ],
        "bg": "https://images.espncdn.com/i/headshots/mlb/players/full/32582.png"
    },
    {
        "rank": 2,
        "name": "김하성 (Kim Ha-seong)",
        "position": "유격수/내야수",
        "team": "MLB: 최근 소속팀(변동 가능)",
        "career": "수비력과 기동력을 갖춘 대표적인 한국인 내야수. MLB에서 골드글러브와 주목받는 활약을 보여줌.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/5/5d/Ha-seong_Kim_2023.jpg",
            "https://images.espncdn.com/i/headshots/mlb/players/full/4089862.png",
            "https://example.com/kim_gallery1.jpg"
        ],
        "bg": "https://images.espncdn.com/i/headshots/mlb/players/full/4089862.png"
    },
    {
        "rank": 3,
        "name": "추신수 (Choo Shin-soo)",
        "position": "외야수",
        "team": "은퇴/역대: MLB(텍사스, 신시내티 등)",
        "career": "긴 MLB 경력과 꾸준한 출루 능력으로 한국 최초 세대의 글로벌 스타 중 한 명.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/1/12/Choo_Shin-soo_2013.jpg",
            "https://example.com/choo2.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/1/12/Choo_Shin-soo_2013.jpg"
    },
    {
        "rank": 4,
        "name": "이승엽 (Lee Seung-yeop)",
        "position": "지명타자/1루수",
        "team": "은퇴/역대: KBO·NPB 전설",
        "career": "KBO 역사상 최고의 슬러거 중 한 명. 홈런 기록과 장타력으로 전설적 입지 확보.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/8/87/Lee_Seung-yeop.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/8/87/Lee_Seung-yeop.jpg"
    },
    {
        "rank": 5,
        "name": "양의지 (Yang Eui-ji)",
        "position": "포수",
        "team": "두산 베어스(경력 변동 가능)",
        "career": "국내 최고의 포수 중 하나로 안정된 수비와 클러치 능력 보유. 여러 차례 골든글러브 수상.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/2/29/Yang_Eui-ji.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/2/29/Yang_Eui-ji.jpg"
    },
    {
        "rank": 6,
        "name": "안현민 (Ahn Hyun-min)",
        "position": "외야수",
        "team": "KT 위즈",
        "career": "2025 시즌 주목받는 타자 중 한 명으로, 강한 타격과 컨택 능력이 인상적.",
        "images": [
            "https://example.com/ahn1.jpg",
            "https://example.com/ahn2.jpg"
        ],
        "bg": "https://example.com/ahn_bg.jpg"
    },
    {
        "rank": 7,
        "name": "김광현 (Kim Kwang-hyun)",
        "position": "투수",
        "team": "KBO/MLB 경력",
        "career": "KBO와 MLB에서 모두 활약한 베테랑 좌완 투수. 꾸준한 제구와 경험이 강점.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/3/3f/Kim_Kwang-hyun.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/3/3f/Kim_Kwang-hyun.jpg"
    },
    {
        "rank": 8,
        "name": "박병호 (Park Byung-ho)",
        "position": "1루수/지명타자",
        "team": "KBO/MLB 경력",
        "career": "강한 장타력으로 유명한 슬러거. KBO에서 MVP 급 활약을 펼친 바 있음.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/6/6f/Park_Byung-ho.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Park_Byung-ho.jpg"
    },
    {
        "rank": 9,
        "name": "최형우 (Choi Hyung-woo)",
        "position": "외야수",
        "team": "KIA 타이거즈",
        "career": "KBO에서 오랜 시간 꾸준한 성적을 낸 베테랑 타자. 클러치 히터로 유명.",
        "images": [
            "https://upload.wikimedia.org/wikipedia/commons/4/4a/Choi_Hyung-woo.jpg"
        ],
        "bg": "https://upload.wikimedia.org/wikipedia/commons/4/4a/Choi_Hyung-woo.jpg"
    },
    {
        "rank": 10,
        "name": "배지환 (Bae Ji-hwan)",
        "position": "내야수",
        "team": "두산/롯데 등",
        "career": "젊고 잠재력 있는 내야 유망주로 주목받는 선수. 향후 역량 기대.",
        "images": [
            "https://example.com/bae1.jpg",
            "https://example.com/bae2.jpg"
        ],
        "bg": "https://example.com/bae_bg.jpg"
    }
]

# Helper: safely load image from URL (returns PIL Image or None)
def load_image(url):
    try:
        resp = requests.get(url, timeout=5)
        img = Image.open(BytesIO(resp.content)).convert("RGBA")
        return img
    except Exception:
        return None

# Layout: display top title + a gallery of player cards
for p in players:
    # Each player: wide expander with styled header
    with st.container():
        cols = st.columns([1, 2])
        left, right = cols
        # Left column: big rank + main image
        with left:
            st.markdown(f"<div style='text-align:center;padding:8px;border-radius:12px;background:#111; color:white;'>"
                        f"<h2 style='margin:6px'>#{p['rank']} {p['name']}</h2>"
                        f"<p style='margin:0;font-size:14px'>{p['position']} • {p['team']}</p>"
                        f"</div>", unsafe_allow_html=True)
            # show first available image
            shown = False
            for img_url in p['images']:
                img = load_image(img_url)
                if img is not None:
                    st.image(img, use_column_width=True, output_format='PNG')
                    shown = True
                    break
            if not shown:
                st.write("(이미지 없음)")

        # Right column: career + image gallery + styled background sample
        with right:
            st.markdown(f"**커리어 하이라이트**\n\n{p['career']}")
            st.markdown("---")
            # Small gallery of images (2 across)
            gallery_cols = st.columns(3)
            i = 0
            for img_url in p['images']:
                col = gallery_cols[i % 3]
                img = load_image(img_url)
                with col:
                    if img is not None:
                        st.image(img, width=140)
                    else:
                        st.write("")
                i += 1

            # Player-themed background sample block (using bg image if available)
            bg_img = p.get('bg')
            if bg_img:
                st.markdown(
                    f"<div style='margin-top:8px;padding:14px;border-radius:12px;background-image:url({bg_img});background-size:cover;color:white;'>"
                    f"<h4 style='margin:2px;padding:2px;background:rgba(0,0,0,0.5);display:inline-block;border-radius:6px;'>"
                    f"{p['name']} — 스타일 샘플</h4>"
                    f"<p style='margin-top:6px;background:rgba(0,0,0,0.35);padding:8px;border-radius:6px;'>팀: {p['team']} • 포지션: {p['position']}</p>"
                    f"</div>", unsafe_allow_html=True)

    st.write("\n")

st.sidebar.title("설정")
st.sidebar.write("이미지 로딩에 실패할 경우 로컬 파일 또는 안정적인 URL로 교체하세요.")

st.sidebar.markdown("---")
st.sidebar.markdown("**앱 사용 팁**\n- 이미지는 외부 URL에 의존합니다.\n- 배포 전 이미지 라이선스를 확인하세요.")

# Footer: requirements.txt content (displayed so user can copy)
st.markdown("---")
st.subheader("requirements.txt (복사해서 프로젝트 루트에 저장)")
requirements_text = '''
streamlit
Pillow
requests
'''
st.code(requirements_text)

st.caption("앱을 더 꾸미고 싶으면 말해줘요 — 색상, 레이아웃, 또는 특정 선수에 대한 더 상세한 데이터(연도별 성적 등)도 추가해줄게요!")
