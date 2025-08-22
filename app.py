import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
import random
import time

# 페이지 설정
st.set_page_config(
    page_title="신세계사이먼 프리미엄 아울렛",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        background: #222222;
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .outlet-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-left: 4px solid #c41e3a;
        margin-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .available-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .occupied-card {
        background: linear-gradient(135deg, #ff9a56 0%, #ff6b35 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
    }
    
    .status-high {
        background-color: #d4edda;
        color: #155724;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .status-medium {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .status-low {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    
    .update-time {
        text-align: center;
        color: #666;
        font-size: 0.9rem;
        margin-top: 2rem;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# 매장 데이터
@st.cache_data
# 매장 데이터
@st.cache_data
def load_outlet_data():
    return {
        "시흥 프리미엄 아울렛": {
            "address": "경기도 시흥시 서해안로 699",
            "phone": "1644-4001",
            "fee": "무료", 
            "total": 2700,
            "areas": [
                {"name": "주차타워 1층", "total": 225, "type": "indoor"},
                {"name": "주차타워 2층", "total": 225, "type": "indoor"},
                {"name": "주차타워 3층", "total": 225, "type": "indoor"},
                {"name": "야외 A구역", "total": 675, "type": "outdoor"},
                {"name": "야외 B구역", "total": 675, "type": "outdoor"},
                {"name": "야외 C구역", "total": 675, "type": "outdoor"}
            ],
           "hours": "AM 10:30 - PM 21:00"
        },
        "여주 프리미엄 아울렛": {
            "address": "경기도 여주시 명품로 360",
            "phone": "1644-4001",
            "fee": "무료",
            "total": 1000, # 총면수는 기존과 동일, 세부 구역만 변경
            "areas": [
                {"name": "주차타워 B2F", "total": 200, "type": "indoor"},
                {"name": "주차타워 B1F", "total": 200, "type": "indoor"},
                {"name": "주차타워 1F", "total": 200, "type": "indoor"},
                {"name": "주차타워 2F", "total": 200, "type": "indoor"},
                {"name": "야외 A구역", "total": 50, "type": "outdoor"},
                {"name": "야외 B구역", "total": 50, "type": "outdoor"},
                {"name": "야외 D구역", "total": 25, "type": "outdoor"},
                {"name": "야외 E구역", "total": 25, "type": "outdoor"},
                {"name": "야외 F구역", "total": 25, "type": "outdoor"},
                {"name": "야외 H구역", "total": 25, "type": "outdoor"}
            ],
            "hours": "AM 10:30 - PM 21:00"
        },
        "파주 프리미엄 아울렛": {
            "address": "경기도 파주시 탄현면 필승로 200",
            "phone": "1644-4001",
            "fee": "무료",
            "total": 1300, 
            "areas": [
                {"name": "주차타워 A동", "total": 250, "type": "indoor"},
                {"name": "주차타워 B동", "total": 250, "type": "indoor"},
                {"name": "주차타워 E동", "total": 200, "type": "indoor"},
                {"name": "야외 C구역", "total": 300, "type": "outdoor"}, 
                {"name": "야외 D구역", "total": 300, "type": "outdoor"}  
            ],
            "hours": "AM 10:30 - PM 21:00"
        },
        "부산 프리미엄 아울렛": {
            "address": "부산광역시 기장군 장안읍 정관로 1133",
            "phone": "1644-4001",
            "fee": "무료",
            "total": 862, 
            "areas": [
                {"name": "주차타워", "total": 500, "type": "indoor"},
                {"name": "주차장 C구역", "total": 20, "type": "indoor"},
                {"name": "주차장 G구역", "total": 12, "type": "indoor"},
                {"name": "주차장 H구역", "total": 10, "type": "indoor"},
                {"name": "야외 B구역", "total": 120, "type": "outdoor"},
                {"name": "야외 E구역", "total": 120, "type": "outdoor"},
                {"name": "야외 F구역", "total": 80, "type": "outdoor"}
            ],
            "hours": "AM 10:30 - PM 21:00"
        },
        "제주 프리미엄 아울렛": {
            "address": "제주특별자치도 서귀포시 안덕면 신화역사로 304번길 38",
            "phone": "1644-4001",
            "fee": "무료",
            "total": 2500,
            "areas": [
                {"name": "신화월드 랜딩관 지상주차장", "total": 2500, "type": "outdoor"}
            ],
            "hours": "AM 10:30 - PM 21:00"
        }
    }

# 실시간 주차 현황 시뮬레이션
@st.cache_data(ttl=60)  
def generate_parking_status(outlet_data):
    """실시간 주차 현황을 시뮬레이션합니다."""
    status = {}
    
    for outlet_name, data in outlet_data.items():
        outlet_status = {"areas": []}
        total_occupied = 0
        
        for area in data["areas"]:
            # 시뮬레이션을 위해 랜덤 값 생성
            base_rate = 0.6 if area["type"] == "indoor" else 0.5
            variation = random.uniform(-0.2, 0.3)
            occupancy_rate = max(0.1, min(0.95, base_rate + variation))
            
            occupied = int(area["total"] * occupancy_rate)
            available = area["total"] - occupied
            
            area_status = {
                "name": area["name"],
                "total": area["total"],
                "occupied": occupied,
                "available": available,
                "occupancy_rate": occupancy_rate,
                "type": area["type"]
            }
            
            outlet_status["areas"].append(area_status)
            total_occupied += occupied
        
        outlet_status["total"] = data["total"]
        outlet_status["total_occupied"] = total_occupied
        outlet_status["total_available"] = data["total"] - total_occupied
        outlet_status["overall_occupancy"] = total_occupied / data["total"]
        
        status[outlet_name] = outlet_status
    
    return status

def get_status_indicator(occupancy_rate):
    """주차 가능률에 따른 상태 표시기 반환"""
    available_rate = 1 - occupancy_rate
    if available_rate >= 0.4:
        return "여유", "status-high"    #40% 이상 남아 있는 경우
    elif available_rate >= 0.2:
        return "보통", "status-medium"  #20% 이상 40% 미만 남아 있는 경우
    else:
        return "혼잡", "status-low"     #20% 미만 남아 있는 경우

def main():
    # 헤더
    st.markdown("""
    <div class="main-header">
        <h1>PREMIUM OUTLETS</h1>
        <h1>SHINSEGAE SIMON</h1>
        <h3>실시간 주차 현황 서비스</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # 데이터 로드
    outlet_data = load_outlet_data()
    parking_status = generate_parking_status(outlet_data)
    
    # 사이드바
    with st.sidebar:
        st.header("매장 선택")
        selected_outlet = st.selectbox(
            "매장을 선택하세요:",
            list(outlet_data.keys()),
            index=0
        )
        
        st.markdown("---")
        st.header("서비스")
        service_menu = st.radio(
            "더 자세히 알아보기:",
            ["매장 정보", "주차 현황", "매장별 전체 주차 현황"]
        )
        
        st.markdown("---")
        st.info("💡 데이터는 1분마다 자동 갱신됩니다.")
        
        # 새로고침 버튼
        if st.button("🔄 새로고침"):
            st.cache_data.clear()
            st.rerun()
    
    # 메인 컨텐츠
    if service_menu == "주차 현황":
        show_parking_status(selected_outlet, outlet_data, parking_status)
    elif service_menu == "매장 정보":
        show_store_info(selected_outlet, outlet_data)
    else:
        show_overall_status(outlet_data, parking_status)

def show_parking_status(selected_outlet, outlet_data, parking_status):
    """선택된 매장의 주차 현황 표시"""
    st.header(f"🅿️ {selected_outlet} 주차 현황")
    
    outlet_info = outlet_data[selected_outlet]
    status = parking_status[selected_outlet]
    
    # 전체 현황 요약
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2>{status['total']:,}</h2>
            <p>총 주차면</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="available-card">
            <h2>{status['total_available']:,}</h2>
            <p>이용 가능</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="occupied-card">
            <h2>{status['total_occupied']:,}</h2>
            <p>주차 중</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 주차구역별 상세 현황
    st.subheader("📍 주차구역별 현황")
    
    cols = st.columns(2)
    
    for i, area in enumerate(status['areas']):
        col_idx = i % 2
        
        with cols[col_idx]:
            status_text, status_class = get_status_indicator(area['occupancy_rate'])
            
            st.markdown(f"""
            <div class="outlet-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4>{area['name']}</h4>
                    <span class="{status_class}">{status_text}</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 1rem;">
                    <div style="text-align: center;">
                        <h3 style="color: #c41e3a; margin: 0;">{area['available']}</h3>
                        <small>이용가능</small>
                    </div>
                    <div style="text-align: center;">
                        <h3 style="color: #666; margin: 0;">{area['occupied']}</h3>
                        <small>주차중</small>
                    </div>
                    <div style="text-align: center;">
                        <h3 style="color: #333; margin: 0;">{area['total']}</h3>
                        <small>총 면수</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # 진행률 바
            st.progress(1 - area['occupancy_rate'])
            st.caption(f"이용 가능률: {(1-area['occupancy_rate'])*100:.1f}%")
    
    # 시각화
    st.markdown("---")
    st.subheader("📊 주차 현황 차트")
    
    # 도넛 차트
    fig = go.Figure(data=[go.Pie(
        labels=['이용 가능', '주차 중'],
        values=[status['total_available'], status['total_occupied']],
        hole=0.5,
        marker_colors=['#38ef7d', '#ff6b35']
    )])
    
    fig.update_layout(
        title=f"{selected_outlet} 전체 주차 현황",
        annotations=[dict(text=f"{status['total']:,}<br>총 주차면", x=0.5, y=0.5, 
                         font_size=16, showarrow=False)]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 구역별 상세 차트
    area_names = [area['name'] for area in status['areas']]
    available = [area['available'] for area in status['areas']]
    occupied = [area['occupied'] for area in status['areas']]
    
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(name='이용 가능', x=area_names, y=available, marker_color='#38ef7d'))
    fig2.add_trace(go.Bar(name='주차 중', x=area_names, y=occupied, marker_color='#ff6b35'))
    
    fig2.update_layout(
        title='구역별 주차 현황',
        barmode='stack',
        xaxis_title='주차구역',
        yaxis_title='주차면 수'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # 업데이트 시간
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div class="update-time">
        📅 마지막 업데이트: {current_time}
    </div>
    """, unsafe_allow_html=True)

def show_store_info(selected_outlet, outlet_data):
    """매장 정보 표시"""
    st.header(f"🏪 {selected_outlet} 매장 정보")
    
    info = outlet_data[selected_outlet]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 기본 정보")
        st.write(f"**주소:** {info['address']}")
        st.write(f"**전화번호:** {info['phone']}")
        st.write(f"**주차요금:** {info['fee']}")
        st.write(f"**총 주차면:** {info['total']:,}대")
        
        st.subheader("🕒 운영시간")
        st.write("f"**일반 매장:** {info['hours']})
        st.write("**주차장:** 10:30 - 21:00") 
        
    with col2:
        st.subheader("🅿️ 주차장 구성")
        for area in info['areas']:
            type_icon = {
                'indoor': '🏢',
                'outdoor': '🌳',
                'special': '♿'
            }
            st.write(f"{type_icon.get(area['type'], '🚗')} **{area['name']}**: {area['total']}대")
        

def show_overall_status(outlet_data, parking_status):
    """전체 매장 현황 표시"""
    st.header("전체 매장 주차 현황")
    
    # 전체 통계
    total_spaces = sum(data['total'] for data in outlet_data.values())
    total_occupied = sum(status['total_occupied'] for status in parking_status.values())
    total_available = total_spaces - total_occupied
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("전체 매장", "5개소")
    with col2:
        st.metric("총 주차면", f"{total_spaces:,}대")
    with col3:
        st.metric("이용 가능", f"{total_available:,}대")
    with col4:
        st.metric("전체 이용률", f"{(total_occupied/total_spaces)*100:.1f}%")
    
    st.markdown("---")
    
    # 매장별 현황 카드
    cols = st.columns(2)
    
    for i, (outlet_name, status) in enumerate(parking_status.items()):
        col_idx = i % 2
        
        with cols[col_idx]:
            overall_status, status_class = get_status_indicator(status['overall_occupancy'])
            
            st.markdown(f"""
            <div class="outlet-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h4>{outlet_name}</h4>
                    <span class="{status_class}">{overall_status}</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <div style="text-align: center;">
                        <h3 style="color: #c41e3a; margin: 0;">{status['total_available']}</h3>
                        <small>이용가능</small>
                    </div>
                    <div style="text-align: center;">
                        <h3 style="color: #333; margin: 0;">{status['total']}</h3>
                        <small>총 면수</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(1 - status['overall_occupancy'])
    
    # 전체 현황 차트
    st.markdown("---")
    st.subheader("📊 매장별 주차 현황 비교")
    
    outlet_names = list(parking_status.keys())
    outlet_available = [status['total_available'] for status in parking_status.values()]
    outlet_occupied = [status['total_occupied'] for status in parking_status.values()]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='이용 가능', x=outlet_names, y=outlet_available, marker_color='#38ef7d'))
    fig.add_trace(go.Bar(name='주차 중', x=outlet_names, y=outlet_occupied, marker_color='#ff6b35'))
    
    fig.update_layout(
        title='매장별 주차 현황 비교',
        barmode='stack',
        xaxis_title='매장',
        yaxis_title='주차면 수',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 실시간 업데이트 표시
    st.markdown("---")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.markdown(f"""
    <div class="update-time">
        🔄 실시간 업데이트 중 | 마지막 갱신: {current_time}
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
