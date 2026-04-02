# [Phase 6] 모니터링 시스템 실전 가이드 (Monitoring Guide)

**목적**: 본 문서는 `chaeyul.uk` 인프라를 관제하기 위해 구축된 중앙 모니터링 스택 (Grafana, Prometheus, Loki)의 실무 활용법을 안내합니다.

## 📌 1. 도구별 역할 개요

- **Grafana (그라파나)**: 복잡한 시계열 수치(메모리, CPU)와 로그를 예쁜 차트와 대시보드로 시각화해 주는 메인 관제 센터입니다.
- **Prometheus (프로메테우스)**: 서버(Node)와 개별 도커(Docker) 컨테이너에서 숫자로 된 성능 지표(Metrics)를 긁어와 저장하는 핵심 데이터베이스입니다.
- **Loki & Promtail (로키)**: 시스템 로그 및 보안 인증 로그(auth.log)를 중앙 집중식으로 수집하고 검색할 수 있게 해주는 엔진입니다.

---

## 📊 2. Grafana (그라파나) 핵심 사용법

![cAdvisor Container Monitoring Dashboard](./cadvisor_monitoring_dashboard_20260308.png)
*<그림: 도커 컨테이너들의 리소스 사용량을 실시간으로 보여주는 cAdvisor 대시보드 예시>*

### 1) 접속 경로 및 초기 설정
* **접속**: `https://[도메인]/grafana/` (또는 관리자 대시보드의 'Grafana ↗' 버튼 클릭)
* 초기 계정 정보: `admin` / `admin` (최초 접속 시 즉시 강력한 비밀번호로 변경 권장)

### 2) 데이터 소스(Data Source) 연결하기
Grafana에서 화면을 그리기 위해 데이터 공급처를 연결하는 과정입니다.
1. 왼쪽 메뉴 막대(☰) -> **Connections** -> **Data sources** 로 이동.
2. **Prometheus 연결**: URL에 `http://prometheus:9090` 입력 후 맨 아래 파란색 **[Save & test]** 클릭 (도커 내부망 통신).
3. **Loki 연결**: URL에 `http://loki:3100` 입력 후 **[Save & test]** 클릭.

### 3) 템플릿 대시보드 불러오기 (Import)
전문가들이 미리 만들어 둔 템플릿 번호를 입력하여 10초 만에 완벽한 대시보드를 생성합니다.
1. 왼쪽 메뉴 막대(☰) -> **Dashboards** 클릭 -> 우측 상단 **[New]** -> **[Import]**.
2. ID 입력창에 **`1860`** (Node Exporter용) 또는 **`14282`** (cAdvisor, 도커 컨테이너용)를 입력 후 **[Load]** 클릭.
3. 가장 하단 데이터 소스 선택란에서 방금 연결한 **Prometheus**를 선택하고 **[Import]** 수행.

![Grafana Real-time Monitoring Dashboard](./grafana_success.png)
*<그림: 템플릿 Import가 완료되어 서버 상태가 실시간으로 표출되는 Grafana 모니터링 화면>*

---

## 🔍 3. Prometheus (프로메테우스) 직접 쿼리

* **접속**: `https://[도메인]/prometheus/`
* Prometheus 자체 UI는 복잡한 그라파나 대시보드에 없는 날 것의 데이터를 직접 쿼리해볼 때 사용합니다.
* 예: 검색창에 `node_cpu_seconds_total` 입력 후 [Execute] 버튼을 누르면 서버 전체 프로세서의 누적 가동 시간을 원시 데이터 형태로 볼 수 있습니다. (Grafana 데이터 소스 점검 목적에 활용)

---

## 🚨 4. Loki를 활용한 보안 및 로그 점검

누군가 서버에 무단 접속을 시도하는지 등 텍스트형 기록(Log)을 검색하는 방법입니다.

### 로그 탐색 (Explore)
1. Grafana 왼쪽 메뉴 막대(☰) -> **Explore** 메뉴 클릭.
2. 상단 데이터 소스를 **Loki**로 변경.
3. **보안 로그(불법 로그인 시도) 필터링**:
   - `Label browser` 대신 직접 쿼리 창에 입력합니다:
   - `{job="varlogs", filename="/var/log/auth.log"} |= "Failed password"`
   - 이 쿼리를 실행(`Run query`)하면 서버 접속 실패 로그(Brute-force 스캔 등)만 색출할 수 있습니다. 

### 대시보드에 로그 창 추가하기
이미 만들어둔 `1860` 인프라 대시보드 모서리에 로그 터미널 창을 추가할 수 있습니다.
1. 대시보드 우측 상단 **[Add panel]** -> **[Add new panel]** 클릭.
2. 데이터 소스를 **Loki** 설정 후 쿼리에 `{job="varlogs"}` 명시.
3. 시각화 방식(Visualizations)에서 **Logs**를 선택하고 저장하면 CPU 그래프와 텍스트 로그를 한눈에 볼 수 있습니다.
