import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="외국인이 좋아하는 서울 관광지 TOP10", layout="wide")

st.title("🌏 외국인이 좋아하는 서울 관광지 TOP10 (Folium 지도)")

# 관광지 데이터
data = {
    "관광지": [
        "경복궁", "명동", "남산타워(N서울타워)", "홍대", "북촌한옥마을",
        "동대문디자인플라자(DDP)", "롯데월드", "청계천", "광장시장", "이태원"
    ],
    "위도": [
        37.579617, 37.563756, 37.551169, 37.556332, 37.582604,
        37.566295, 37.511000, 37.569091, 37.570221, 37.534937
    ],
    "경도": [
        126.977041, 126.982708, 126.988227, 126.922874, 126.983018,
        127.009200, 127.098100, 126.978550, 126.999859, 126.994690
    ],
    "설명": [
        "조선의 대표 궁궐, 아름다운 전통 건축물과 근정전으로 유명",
        "쇼핑과 음식의 천국, 외국인 관광객 필수 코스",
        "서울 전경을 한눈에 볼 수 있는 랜드마크 전망대",
        "젊음과 예술의 거리, 클럽과 카페가 가득",
        "한옥이 모여있는 전통 마을, 포토 명소로 인기",
        "현대적 건축물과 전시공간이 있는 복합문화공간",
        "테마파크와 쇼핑몰이 함께 있는 서울의 대표 놀이공원",
        "도심 속 하천 산책로, 야경이 아름다움",
        "전통시장 음식천국, 빈대떡과 마약김밥이 유명",
        "다양한 문화가 공존하는 글로벌 거리"
    ]
}

df = pd.DataFrame(data)

# 서울 중심 좌표 기준 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)

# 마커 추가
for i, row in df.iterrows():
    folium.Marker(
        location=[row["위도"], row["경도"]],
        popup=f"<b>{row['관광지']}</b><br>{row['설명']}",
        tooltip=row["관광지"],
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m)

# 지도 표시
st_data = st_folium(m, width=900, height=600)

# 하단 설명
st.markdown("---")
st.subheader("💡 참고")
st.write("데이터는 외국인 관광객 선호도, SNS 언급량, 서울시 관광자료를 기반으로 작성된 예시입니다.")



