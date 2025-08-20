
import streamlit as st
import pandas as pd
import json, os
from datetime import datetime
import matplotlib.pyplot as plt
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="신세계 프리미엄 아울렛 (Demo)", page_icon="🛍️", layout="wide")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

@st.cache_data
def load_outlets():
    with open(os.path.join(DATA_DIR,"outlets.json"), encoding="utf-8") as f:
        return json.load(f)

def load_stores(key): return pd.read_csv(os.path.join(DATA_DIR, f"{key}_stores.csv"))
def load_events(): return pd.read_csv(os.path.join(DATA_DIR, "events.csv"))
@st.cache_data
def load_services():
    with open(os.path.join(DATA_DIR,"services.json"), encoding="utf-8") as f:
        return json.load(f)
def load_parking(key): return pd.read_csv(os.path.join(DATA_DIR, f"{key}_parking.csv"))
@st.cache_data
def load_faqs():
    with open(os.path.join(DATA_DIR,"faqs.json"), encoding="utf-8") as f:
        return json.load(f)

# Top bar like integration page: locations + global search + links
outlets = load_outlets()
loc_map = {o["key"]:o["name"] for o in outlets}
keys = list(loc_map.keys())

st.markdown("""
<style>
.topbar { position:sticky; top:0; z-index:100; padding:10px 0; background:rgba(255,255,255,0.85); backdrop-filter:saturate(180%) blur(8px); border-bottom:1px solid #eee; }
.topnav { display:flex; gap:16px; align-items:center; }
.topnav a { text-decoration:none; font-weight:600; color:#111; }
.brand-strip { font-size:12px; color:#666; white-space:nowrap; overflow:auto; }
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("<div class='topbar'>", unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns([1.4,3,3,2])
    with c1:
        st.markdown("**PREMIUM OUTLETS**  \n신세계사이먼", unsafe_allow_html=True)
    with c2:
        sel_key = st.segmented_control("지점", options=keys, format_func=lambda k: loc_map[k], default=keys[0])
    with c3:
        gq = st.text_input("통합검색 (브랜드/매장)", "", placeholder="예: NIKE, COS, STARBUCKS")
    with c4:
        st.markdown("[전점센터맵](#)  \n[WORLDWIDE](#)")
    st.markdown("</div>", unsafe_allow_html=True)

# Global brand search results
if gq.strip():
    st.subheader("통합검색 결과")
    all_rows = []
    for k in keys:
        df = load_stores(k)
        m = df["브랜드"].str.contains(gq, case=False) | df["태그"].str.contains(gq, case=False)
        hit = df[m].copy()
        if len(hit):
            hit.insert(0,"지점", loc_map[k])
            all_rows.append(hit)
    if all_rows:
        st.dataframe(pd.concat(all_rows, ignore_index=True), use_container_width=True, hide_index=True)
    else:
        st.info("검색 결과가 없습니다.")

# Outlet header
target = next(o for o in outlets if o["key"] == sel_key)
st.title(target["name"])
st.caption(f"주소: {target['address']} · 대표번호: {target['phone']} (데모)")

tabs = st.tabs(["점포안내", "이벤트", "서비스", "고객센터"])

# 점포안내
with tabs[0]:
    df = load_stores(sel_key)
    c1,c2 = st.columns([2,1])
    with c1:
        st.subheader("브랜드 목록")
        q = st.text_input("매장 검색", "", placeholder="브랜드명/태그 입력")
        show = df
        if q.strip():
            show = df[df["브랜드"].str.contains(q, case=False) | df["태그"].str.contains(q, case=False)]
        st.dataframe(show, use_container_width=True, hide_index=True)
    with c2:
        st.subheader("카테고리 분포")
        fig = plt.figure()
        df["카테고리"].value_counts().plot(kind="bar")
        plt.xlabel("카테고리"); plt.ylabel("브랜드 수")
        st.pyplot(fig)

# 이벤트
with tabs[1]:
    ev = load_events()
    ev = ev[ev["아울렛"] == sel_key].copy()
    st.subheader("진행/예정 이벤트")
    if len(ev)==0:
        st.info("현재 표시할 이벤트가 없습니다.")
    else:
        today = pd.Timestamp.today().normalize()
        def status(row):
            s = pd.to_datetime(row["시작일"]); e = pd.to_datetime(row["종료일"])
            if s <= today <= e: return "진행중"
            elif today < s: return "예정"
            return "종료"
        ev["상태"] = ev.apply(status, axis=1)
        st.dataframe(ev[["이벤트명","시작일","종료일","상태","설명"]], use_container_width=True, hide_index=True)

# 서비스 (주차 현황 포함)
with tabs[2]:
    st.subheader("편의시설 안내")
    svc = load_services().get(sel_key, {})
    cols = st.columns(3)
    items = list(svc.items())
    for i,(k,v) in enumerate(items):
        with cols[i%3]:
            st.metric(k, "가능" if v else "제공 안함")
    st.markdown("---")
    st.subheader("주차 현황")
    # auto refresh
    count = st_autorefresh(interval=10_000, key="auto_refresh_key")
    pk = load_parking(sel_key).copy()
    total_cap = int(pk["capacity"].sum())
    total_used = int(pk["used"].sum())
    rate = int(round(total_used/total_cap*100))
    c1,c2 = st.columns([2,1])
    with c1:
        st.write(f"**전체 혼잡도: {rate}%**  · 사용 {total_used} / 수용 {total_cap} 대")
        fig2 = plt.figure()
        (pk["used"]/pk["capacity"]*100).round(1).plot(kind="bar")
        plt.xticks(range(len(pk)), pk["zone"])
        plt.ylim(0,100); plt.ylabel("점유율(%)"); plt.xlabel("구역")
        st.pyplot(fig2)
        st.dataframe(pk, use_container_width=True, hide_index=True)
    with c2:
        st.write("""**주차 예약**""")
- 멤버십 등급별 예약 우선권 제공  
- 예약 시간대: 2시간 단위  
- QR/번호판 인식으로 비대면 입차\"\"\")
        st.text_input("차량 번호", placeholder="12가 3456")
        st.selectbox("예약 구역", options=list(pk["zone"]))
        st.selectbox("시간대", options=["09:00-11:00","11:00-13:00","13:00-15:00","15:00-17:00","17:00-19:00"])
        st.button("예약 요청 (데모)")
    st.caption("※ 실제 서비스에서는 주차 IoT/게이트 API 연동으로 실시간 점유율·예약 가능 수량을 반영합니다.")

# 고객센터
with tabs[3]:
    st.subheader("자주 묻는 질문(FAQ)")
    for item in load_faqs():
        with st.expander(item["질문"]):
            st.write(item["답변"])
    st.markdown("---")
    st.subheader("문의하기")
    st.text_input("이름")
    st.text_input("연락처")
    st.text_area("문의 내용")
    st.button("문의 접수 (데모)")

st.markdown(\"\"\"\n<div style='margin-top:2rem; color:#7a7a7a; font-size:12px'>\n© Demo — 본 프로젝트는 학습/포트폴리오 목적의 데모입니다. 실제 상표/브랜드는 각 사의 자산입니다.\n</div>\n\"\"\", unsafe_allow_html=True)
