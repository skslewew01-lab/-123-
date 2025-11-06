# app.py
import streamlit as st

st.set_page_config(page_title="MBTI 진로 추천 🌿", layout="centered")

MBTI_DATA = {
    "ISTJ": [
        {
            "career": "회계사 / 재무담당자",
            "majors": ["경영학(회계)", "세무학", "재무금융"],
            "personality": "섬세하고 책임감 강함. 규칙·절차 지키는 걸 좋아함. 숫자에 강한 타입."
        },
        {
            "career": "공무원 / 행정직",
            "majors": ["행정학", "법학", "공기업/행정관련 학과"],
            "personality": "안정 지향, 계획 수립 잘함. 책임감 있는 조직인."
        }
    ],
    "ISFJ": [
        {
            "career": "간호사 / 임상보건",
            "majors": ["간호학", "보건학", "의료행정"],
            "personality": "배려심 많고 섬세함. 사람들 돌보는 일에 에너지 충만."
        },
        {
            "career": "사회복지사 / 상담지원",
            "majors": ["사회복지학", "상담심리학"],
            "personality": "헌신적이고 신뢰감 줌. 안정적으로 돕는 걸 좋아함."
        }
    ],
    "INFJ": [
        {
            "career": "상담가 / 임상심리사",
            "majors": ["심리학", "상담학"],
            "personality": "통찰력 있고 공감 능력 높음. 깊은 의미 추구."
        },
        {
            "career": "작가 / 콘텐츠 크리에이터",
            "majors": ["문예창작", "국어국문", "미디어학"],
            "personality": "내면 표현 좋아하고 스토리텔링 능력 탁월."
        }
    ],
    "INTJ": [
        {
            "career": "연구원 / 데이터 사이언티스트",
            "majors": ["수학", "통계학", "컴퓨터공학"],
            "personality": "전략적이고 분석적. 복잡한 시스템 좋아함."
        },
        {
            "career": "전략기획 / 컨설턴트",
            "majors": ["경영학", "경제학", "산업공학"],
            "personality": "장기 플랜 잘 세우고 논리적으로 설계함."
        }
    ],
    "ISTP": [
        {
            "career": "기계·설비 엔지니어 / 테크니션",
            "majors": ["기계공학", "전기공학", "산업설비"],
            "personality": "문제 해결 즉흥적·실용적. 손으로 만지는 일 잘함."
        },
        {
            "career": "파일럿 / 드론 조종사",
            "majors": ["항공운항학", "전자공학(제어)"],
            "personality": "냉정하고 침착. 순간 판단력 좋음."
        }
    ],
    "ISFP": [
        {
            "career": "디자이너 (패션/그래픽)",
            "majors": ["디자인학(패션/그래픽)", "시각디자인"],
            "personality": "감각적이고 표현력 풍부. 실물·시각적 결과물 선호."
        },
        {
            "career": "사진작가 / 영상제작",
            "majors": ["미디어학", "사진/영상 학과"],
            "personality": "감성적이고 순간 포착 능력 우수. 자유로운 분위기 선호."
        }
    ],
    "INFP": [
        {
            "career": "작가 / 에디터",
            "majors": ["국문학", "문예창작", "미디어문예"],
            "personality": "이상주의자, 상상력 풍부. 자기표현 좋아함."
        },
        {
            "career": "심리상담 / 예술치료",
            "majors": ["심리학", "예술치료학"],
            "personality": "공감능력 높고 사람의 깊은 면에 관심 많음."
        }
    ],
    "INTP": [
        {
            "career": "시스템 설계자 / 소프트웨어 아키텍트",
            "majors": ["컴퓨터공학", "전자공학", "정보통신"],
            "personality": "논리적이고 이론적 탐구심 강함. 구조 만들기 좋아함."
        },
        {
            "career": "연구개발(R&D) / 학문 연구",
            "majors": ["물리학", "수학", "컴퓨터과학"],
            "personality": "호기심 많고 독립적. 깊이 파고드는 스타일."
        }
    ],
    "ESTP": [
        {
            "career": "영업 / 세일즈",
            "majors": ["경영학", "마케팅", "커뮤니케이션"],
            "personality": "활발하고 설득력 있음. 즉흥적 상황에 강함."
        },
        {
            "career": "응급구조 / 소방관",
            "majors": ["응급구조학", "소방안전학"],
            "personality": "실전형, 빠른 판단과 체력 필요."
        }
    ],
    "ESFP": [
        {
            "career": "연예·공연예술 / 이벤트 기획",
            "majors": ["연극영화학", "문화예술경영", "이벤트학"],
            "personality": "에너지 넘치고 사람 앞에서 빛남. 분위기 메이커."
        },
        {
            "career": "리테일 매니저 / 패션 판매",
            "majors": ["패션디자인", "유통물류", "비즈니스"],
            "personality": "사람과 교류하는 걸 즐김. 실무 중심적."
        }
    ],
    "ENFP": [
        {
            "career": "마케팅·브랜딩 / 콘텐츠 기획",
            "majors": ["광고홍보학", "미디어커뮤니케이션"],
            "personality": "아이디어 뿜뿜, 창의력 대박. 사람 연결 잘함."
        },
        {
            "career": "HR·리크루터 / 커뮤니티 매니저",
            "majors": ["심리학", "경영학", "인적자원관리"],
            "personality": "사람의 가능성 보는 걸 좋아함. 따뜻하고 에너지 많음."
        }
    ],
    "ENTP": [
        {
            "career": "스타트업 창업가 / 제품 개발",
            "majors": ["경영학", "컴퓨터공학", "디자인"],
            "personality": "아이디어 실험 좋아하고 톡톡 튀는 발상력 소유."
        },
        {
            "career": "변호사(소송/IT분야) / 논쟁 전문직",
            "majors": ["법학", "지적재산권 관련 학과"],
            "personality": "언변 좋고 논리로 이끄는 타입. 토론 즐김."
        }
    ],
    "ESTJ": [
        {
            "career": "프로젝트 매니저 / 운영 관리자",
            "majors": ["경영학", "산업공학", "공학관리"],
            "personality": "조직 운영·관리 탁월. 현실적이고 결단력 있음."
        },
        {
            "career": "군·경찰·행정관리",
            "majors": ["경찰학", "행정학", "국방 관련 학과"],
            "personality": "규율과 책임을 잘 지키는 리더형."
        }
    ],
    "ESFJ": [
        {
            "career": "교사 / 교육행정",
            "majors": ["교육학", "아동학", "특수교육"],
            "personality": "사람 돕는 것에 성취감. 조직 내 조화 추구."
        },
        {
            "career": "헬스케어 매니저 / 병원 행정",
            "majors": ["보건행정학", "경영학"],
            "personality": "친절하고 체계적. 사람 중심 업무에 강함."
        }
    ],
    "ENFJ": [
        {
            "career": "PR·홍보 매니저 / 커뮤니케이션",
            "majors": ["커뮤니케이션학", "광고홍보학"],
            "personality": "사람을 이끄는 카리스마. 공감 능력과 조직력 좋음."
        },
        {
            "career": "조직 개발 / 코칭·컨설팅",
            "majors": ["경영학", "심리학", "리더십 관련 전공"],
            "personality": "영향력 있고 동기부여 잘함. 타인 성장에 집중."
        }
    ],
    "ENTJ": [
        {
            "career": "CEO·임원 / 경영컨설턴트",
            "majors": ["경영학", "경제학", "공학(관리)"],
            "personality": "결단력 있고 목표지향적. 큰 그림 그리기 좋아함."
        },
        {
            "career": "프로젝트 리더 / 전략기획",
            "majors": ["경영정보학", "산업공학", "전략경영"],
            "personality": "리더십 강하고 효율성 최우선. 성과 중심."
        }
    ]
}

def render_career_card(item):
    st.markdown(f"### 🔥 {item['career']}")
    st.markdown(f"- **추천 학과**: {', '.join(item['majors'])}")
    st.markdown(f"- **어울리는 성격**: {item['personality']}")

st.title("MBTI로 딱! 맞는 진로 골라줄게 ✨")
st.caption("성수동 vibe로 알려주는 현실적인 추천 — 가볍게 보고 골라봐요 😏")

with st.sidebar:
    st.header("사용법")
    st.write("1) MBTI 고르고 2) 진로 2개 중 관심 있는 걸 눌러봐 — 자세한 설명 뜸.\n")
    st.write("※ 외부 라이브러리 불필요, Streamlit만 사용함.")

mbti_choice = st.selectbox("너 MBTI 뭐야? (골라봐)", ["선택하세요"] + list(MBTI_DATA.keys()))

if mbti_choice == "선택하세요":
    st.info("MBTI를 선택하면 진로 추천 두 개가 바로 뜰걸? 🤙")
else:
    st.markdown(f"## `{mbti_choice}`님을 위한 추천 라인업 🎯")
    careers = MBTI_DATA.get(mbti_choice, [])
    # 두 개를 카드 스타일로 나열
    cols = st.columns(2)
    for i, item in enumerate(careers):
        with cols[i]:
            render_career_card(item)
            # 센스 있는 한 줄 코멘트 (성수동 알바생 말투)
            if i == 0:
                st.markdown("> 오우 첫번째는 실전형 추천! 바로 현장 뛰어들기 좋은 코스 🎒")
            else:
                st.markdown("> 두번째는 좀 더 느긋히, 근데 오래갬. 안정적으로 루트 굳히기 좋아. ☕️")

    st.markdown("---")
    st.markdown("### 팁 from 성수동 알바 🧢")
    st.markdown("- 인생 진로는 한 번에 확정 안 돼. 사이드로 경험해보고 골라. ✌️")
    st.markdown("- 전공은 기본 가이드. 인턴·아르바이트로 실전 감각 채우자. 💼")
    st.markdown("### 더 원해?")
    if st.button("다른 유형도 보여줘"):
        st.experimental_rerun()
