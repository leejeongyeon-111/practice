
# 신세계 프리미엄 아울렛 데모 v2 (Streamlit)

실제 통합 페이지 구성을 참고해 5개 지점(여주/파주/부산/시흥/제주) 선택과
지점 내부 탭(점포안내/이벤트/서비스/고객센터)을 구현했습니다.
서비스 탭에는 **주차 현황**과 **예약(데모)** UI가 포함됩니다.
상단에는 실제 페이지의 **지점 선택/통합검색/전점센터맵** 느낌을 반영했습니다.

## 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 데이터 교체
- data/<key>_stores.csv : 지점별 매장
- data/events.csv : 지점별 이벤트
- data/<key>_parking.csv : 주차 구역별 수용/사용
- 실서비스에서는 게이트/IoT API로 대체하세요.
