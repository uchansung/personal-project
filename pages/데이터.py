import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError

st.set_page_config(  # 페이지 설정
    page_title="DataFrame Demo", 
    page_icon="📊"
    )

st.markdown("# DataFrame Demo")  # st.markdown()을 이용한 헤더 작성
st.sidebar.header("DataFrame Demo")  # 사이드바에 헤더 작성
st.write(
    """This demo shows how to use `st.write` to visualize Pandas DataFrames.
(Data courtesy of the [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)


@st.cache_data  # 캐싱을 위한 데코레이터
def get_UN_data():  # url로 부터 데이터 파일을 읽어오는 함수
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")


try:  # 예외처리를 위한 try-except문
    df = get_UN_data()   # 데이터 파일을 데이터프레임 df로 읽어옴
    countries = st.multiselect(   # 멀티셀렉트 위젯 생성
        # 선택할 수 있는 국가 리스트, 중국과 미국을 기본값으로 설정
        "Choose countries", list(df.index), ["China", "United States of America"]  
    )
    if not countries:  # 선택된 국가가 없을 경우
        st.error("Please select at least one country.")  # 에러메시지 출력
    else:  # 선택된 국가가 있을 경우
        data = df.loc[countries]  # 선택된 국가의 데이터만 추출
        data /= 1000000.0         # 데이터를 백만 단위로 나눔
        st.write("### Gross Agricultural Production ($B)", data.sort_index())  # 데이터프레임을 인덱스 순으로 출력

        data = data.T.reset_index() # 데이터프레임을 전치하고 인덱스를 재설정
        data = pd.melt(data, id_vars=["index"]).rename(   # 데이터프레임을 melting(연도와 GAP로 변환)하여 재설정
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)  # 데이터프레임을 차트로 변환
            .mark_area(opacity=0.3)  # area chart를 그리고 차트의 투명도 설정
            .encode(     # 차트의 옵션 설정
                x="year:T",    # x축은 연도
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),  # y축은 GAP, stack은 없음
                color="Region:N",   # 색상은 지역별로 구분
            )
        )
        st.altair_chart(chart, use_container_width=True)  # 차트를 출력
except URLError as e:  # URL 에러가 발생할 경우
    st.error(  # 에러메시지 출력
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )