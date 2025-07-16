import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 행정구역 중심좌표 (예시)
region_coords = {
    "경기도  (4100000000)": [37.4138, 127.5183],
    "서울특별시  (1100000000)": [37.5665, 126.9780],
    "부산광역시  (2600000000)": [35.1796, 129.0756],
    "경상남도  (4800000000)": [35.4606, 128.2132],
    "인천광역시  (2800000000)": [37.4563, 126.7052]
}

# CSV 파일 읽기
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')
df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 지도 생성
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 크고 선명한 원 추가
for _, row in top5_df.iterrows():
    region = row['행정구역']
    pop = row['총인구수']
    coords = region_coords.get(region)
    if coords:
        folium.Circle(
            location=coords,
            radius=int(pop) / 200,   # 🔍 원 크기를 키움 (기존 /50 → /20)
            color='darkblue',       # 진한 외곽선 색상
            fill=True,
            fill_color='blue',      # 내부 색상
            fill_opacity=1.0,       # 완전히 불투명
            popup=f"{region} : {pop:,}명",
            tooltip=region
        ).add_to(m)

# Streamlit에 지도 출력
st.title("상위 5개 행정구역 인구수 지도 (크고 선명한 원 마커)")
st_data = st_folium(m, width=700, height=500)
