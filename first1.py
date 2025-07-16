import streamlit as st



# 페이지 제목
st.title("📚 프로젝트 메인 페이지")

# 제목과 링크 리스트
projects = [
    {"제목": "2025년 5월 인구 통계 분석"},
    {"제목": "행정구역별 지도 시각화" },
    {"제목": "데이터 기반 직업 추천 앱"},
    {"제목": "AI 학습 성과 대시보드"},
    {"제목": "Streamlit 튜토리얼 페이지"}
]

st.subheader("📌 프로젝트 목록")

# 프로젝트 목록 출력
for project in projects:
    st.markdown(f"### [{project['제목']}]")

# 하단 안내
st.info("상단 제목과 링크는 소스 코드에서 직접 수정하여 사용할 수 있습니다.")
