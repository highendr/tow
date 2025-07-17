import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 - 지도 시각화")

# CSV 파일 로드
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 데이터 전처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수', '위도', '경도'] + age_columns].copy()  # 위도, 경도 열이 있어야 합니다.
df_age.columns = ['행정구역', '총인구수', '위도', '경도'] + new_columns

# 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 지도 생성 (대한민국 중심)
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 지도에 원형 마커 추가
for _, row in top5_df.iterrows():
    folium.CircleMarker(
        location=[row['위도'], row['경도']],
        radius=row['총인구수'] / 20000,  # 인구수 비례 원 크기 조정
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.4,  # 반투명
        popup=folium.Popup(f"{row['행정구역']}<br>총인구수: {row['총인구수']:,}", max_width=200)
    ).add_to(m)

# Streamlit에 지도 표시
st.subheader("📍 상위 5개 행정구역 - 인구수 원형 마커 지도")
st_folium(m, width=700, height=500)
