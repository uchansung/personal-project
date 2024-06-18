import streamlit as st
import pandas as pd
import pydeck as pdk                # pydeck 라이브러리를 pdk로 import
from urllib.error import URLError   # URL 에러를 위한 라이브러리

st.set_page_config(
    page_title="Mapping Demo", 
    page_icon="🌍"
    )

st.markdown("# Mapping Demo")
st.sidebar.header("Mapping Demo")
st.write(
    """This demo shows how to use
[`st.pydeck_chart`](https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart)
to display geospatial data."""
)

@st.cache_data   # 캐싱을 위한 데코레이터
def from_data_file(filename):   # url로 부터 데이터 파일을 JSON으로 읽어오는 함수
    url = (
        "http://raw.githubusercontent.com/streamlit/"
        "example-data/master/hello/v1/%s" % filename
    )
    return pd.read_json(url)


try:   # 예외처리를 위한 try-except문
    ALL_LAYERS = {  # 지도 레이어 딕셔너리 생성
        "Bike Rentals": pdk.Layer(
            "HexagonLayer",
            data=from_data_file("bike_rental_stats.json"),
            get_position=["lon", "lat"],
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            extruded=True,
        ),
        "Bart Stop Exits": pdk.Layer(
            "ScatterplotLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_color=[200, 30, 0, 160],
            get_radius="[exits]",
            radius_scale=0.05,
        ),
        "Bart Stop Names": pdk.Layer(
            "TextLayer",
            data=from_data_file("bart_stop_stats.json"),
            get_position=["lon", "lat"],
            get_text="name",
            get_color=[0, 0, 0, 200],
            get_size=15,
            get_alignment_baseline="'bottom'",
        ),
        "Outbound Flow": pdk.Layer(
            "ArcLayer",
            data=from_data_file("bart_path_stats.json"),
            get_source_position=["lon", "lat"],
            get_target_position=["lon2", "lat2"],
            get_source_color=[200, 30, 0, 160],
            get_target_color=[200, 30, 0, 160],
            auto_highlight=True,
            width_scale=0.0001,
            get_width="outbound",
            width_min_pixels=3,
            width_max_pixels=30,
        ),
    }
    st.sidebar.markdown("### Map Layers")   # 사이드바에 헤더 작성
    selected_layers = [   # 선택된 레이어 리스트 생성
        layer
        for layer_name, layer in ALL_LAYERS.items()  # 레이어 이름과 레이어를 순회
        if st.sidebar.checkbox(layer_name, True)  # 체크박스 생성
    ]
    if selected_layers:  # 선택된 레이어가 있으면
        st.pydeck_chart(   # pydeck 차트 생성
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v9",
                initial_view_state={
                    "latitude": 37.76,
                    "longitude": -122.4,
                    "zoom": 11,
                    "pitch": 50,
                },
                layers=selected_layers,
            )
        )
    else:
        st.error("Please choose at least one layer above.")  # 선택된 레이어가 없으면 에러 메시지 출력
except URLError as e:  # URL 에러가 발생하면 에러 메시지 출력
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )