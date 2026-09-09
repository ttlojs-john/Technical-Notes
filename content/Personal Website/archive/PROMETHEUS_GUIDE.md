# Prometheus(프로메테우스) 핵심 사용 가이드

Prometheus는 시스템과 컨테이너의 상태 수치(Metric)를 시계열로 저장하고 검색할 수 있게 해주는 핵심 모니터링 엔진입니다.
보통은 바로 옆에 있는 Grafana가 데이터를 대신 꺼내 예쁘게 그려주지만, Prometheus 자체 UI를 통해서도 아주 상세한 데이터 검색과 진단을 할 수 있습니다.

## 1. Prometheus UI 접속하기
- `admin.html`에 있는 **[Prometheus ↗]** 버튼을 통해 접속하거나, 웹 주소창에 `https://chaeyul.uk/prometheus/` (또는 로컬 `/prometheus/`)로 접속합니다.
- 상단 메뉴 중 **"Graph"** 나 **"Table"** 탭이 가장 자주 쓰이는 부분입니다.

## 2. PromQL (Prometheus Query Language) 쿼리 기본
검색창(Expression)에 PromQL이라는 전용 명령어를 입력하여 데이터를 조회합니다.

### 📌 자주 쓰이는 필수 쿼리 모음
Prometheus 페이지 검색창에 아래 명렁어들을 복사해서 넣고 `Execute` 버튼을 눌러보세요.

* **컨테이너별 CPU 사용량 확인:**
  도커 컨테이너들이 1초에 CPU를 얼마나 사용하고 있는지 보여줍니다.
  ```promql
  rate(container_cpu_usage_seconds_total{image!=""}[1m])
  ```
* **컨테이너별 메모리 사용량 확인:**
  각 도커 컨테이너가 점유하고 있는 실제 메모리 용량(Byte)을 알려줍니다. (Table 탭에서 보기 좋습니다)
  ```promql
  container_memory_usage_bytes{name=~".+"}
  ```
* **물리 서버의 남은 디스크 용량 (Node Exporter 필요):**
  서버 물리 디스크(`/`)의 남아있는 여유 공간(Byte)을 보여줍니다.
  ```promql
  node_filesystem_free_bytes{mountpoint="/"}
  ```
* **특정 컨테이너(예: DB)의 네트워크 트래픽 확인:**
  `db` 컨테이너가 외부로 보내는 네트워크 송신량 추이를 살펴봅니다.
  ```promql
  rate(container_network_transmit_bytes_total{name="web_db"}[1m])
  ```

## 3. 타겟(Target) 상태 확인하기
Prometheus가 데이터를 잘 수집하고 있는지 확인하고 싶을 때는 상단 메뉴의 **"Status" -> "Targets"** 로 이동합니다.
- State 열에 **`UP`** 이라고 표시된 녹색 뱃지가 나타나면 데이터가 정상 수집 중이라는 의미입니다.

## 4. 실전 활용 팁
- 프로메테우스의 데이터는 1초/5초/15초 단위로 수시로 변하는 데이터를 모은 것이므로, 주로 `rate()` 함수나 `irate()` 함수와 함께 써서 **"1분 동안 변화의 평균값"**을 확인하는 방식으로 자주 씁니다.
- 굳이 복잡한 쿼리를 외우실 필요는 없습니다! 현업에서도 아주 깊게 분석해야 할 때만 Prometheus에서 쿼리를 직접 작성하고, 평소에는 **Grafana의 예쁜 대시보드**를 시각적으로 감상하는 용도로 활용합니다.
