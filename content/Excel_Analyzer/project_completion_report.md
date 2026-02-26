# 📄 프로젝트 완료 보고서 (Project Completion Report)

## 🇰🇷 한국어 버전 (Korean Version)

### 1. 프로젝트 개요 (Project Overview)
**프로젝트명:** Excel Task Analyzer (엑셀 데이터 분석 자동화 툴)
**목표:** IT 지원 및 티켓 시스템 등에서 추출한 대량의 엑셀 데이터를 자동으로 분석, 가공, 요약하여 실무자의 수작업 시간을 단축하는 데스크톱 애플리케이션 개발.
**주요 기능:**
- **Task 1 (작업자별 실적 요약):** 특정 작업자(`Closed by`) 기준으로 데이터를 필터링하고 누적 작업 시간(`Man minute`), 실제 시작부터 종료 시점까지의 처리 시간(`Time Diff`)을 계산한 후 자동으로 합계 행을 추가하여 리포트 생성.
- **Task 2 (키워드 검색 및 추출):** 티켓 설명(`Short description`) 내 특정 키워드가 포함된 항목만 빠르고 정확하게 추출 및 엑셀 저장.
- **Task 3 (문제가 가장 많이 발생하는 유형 분석):** 주요 이슈(`Short description`)의 발생 빈도를 계산하고, 내림차순(빈도수 기준) 정렬하여 리포트 생성.

### 2. 아키텍처 (Architecture)
- **언어:** Python 3.x
- **UI 프레임워크:** Tkinter (기본 내장 라이브러리로써 가벼운 데스크톱 환경 제공)
- **데이터 처리:** Pandas (대용량 엑셀 데이터 필터링, 컬럼 생성, 수학/통계 연산 최적화)
- **파일 I/O:** Openpyxl 엔진을 활용하여 `.xlsx` 파일의 안정적인 읽기/쓰기 구현
- **테스트 환경:** `unittest` 모듈을 이용한 주요 로직 모의 검증 (`test_logic.py`)

### 3. AI 활용 전략 (AI Utilization Strategy)
개발 생산성 극대화와 안정성 확보를 위해 여러 단계에서 AI를 적극 활용했습니다.
- **초기 GUI 스캐폴딩:** Tkinter 기반의 레이아웃(프레임, 버튼, 상태표시줄 등)을 AI를 통해 빠르게 초안 및 구조화.
- **Pandas 데이터 조작 최적화:** 엑셀의 복잡한 날짜 서식 및 포맷팅 결함을 안전하게 처리하는 로직(예: `errors='coerce'`)을 AI를 통해 도출 및 구현.
- **테스트 코드 자동 생성:** `test_logic.py` 작성 시 AI를 활용하여 엣지 케이스(대소문자 무시 검색, 누락된 데이터 처리) 등에 대한 단위 테스트를 설계.

### 4. 트러블슈팅 및 기술적 의사 결정 (Troubleshooting & Technical Decisions)
- **이슈:** 엑셀의 `Man minute`, `Actual start`, `Closed` 컬럼에 빈 칸 시(NaN) 연산 에러가 발생.
  - **해결 방안:** `pd.to_numeric(errors='coerce').fillna(0)` 및 `pd.to_datetime(errors='coerce')`를 적용하여 결측치나 문자열 에러를 강제 변환/처리하여 프로그램 다운 현상을 방지.
- **이슈:** 하단에 합계(Total) 행을 추가할 때 기존 코드에서 지원 중단 예정인 `append()` 메서드를 사용할 경우 경고 발생 및 속도 저하 문제.
  - **결정 (Decision):** 단일 열짜리 요약 딕셔너리를 임시 Series/DataFrame으로 구축시킨 후 `pd.concat([Filtered_df, Sum_df], ignore_index=True)` 방식을 채택하여 최신 Pandas 사양에 맞추고 성능을 안정시킴.
- **이슈:** UI 스레드가 데이터 로드나 저장 시 잠시 멈추는(프리징) 문제.
  - **해결 방안:** `self.root.update_idletasks()`를 로그 출력에 결합해 사용자에게 진행 상황 메시지(Status Bar)가 즉각적으로 반영되도록 개선.

### 5. 배포 및 향후 과제 (Deployment & Future Tasks)
- **현재 배포 방식:** 파이썬 스크립트 기반 실행. 
- **향후 배포 목표:** 사용자들이 Python 환경 없이도 바로 실행할 수 있도록 `PyInstaller`를 활용해 독립적인 `.exe` 실행 파일로 패키징하여 사내 배포 예정.
- **향후 과제 (Future Features):**
  1. **Matplotlib/Seaborn 연동:** 데이터 시각화(차트, 그래프) 기능을 프로그램 내에 추가하여 요약본 시각화 제공.
  2. **동적 컬럼 매핑:** 현재는 특정 컬럼명(`Closed by` 등)을 하드코딩 중이지만, 추후 사용자가 UI에서 매핑할 컬럼을 직접 선택할 수 있는 유연한 기능 제공.
  3. **대시보드화:** 여러 엑셀 파일을 일괄 등록해 동시에 분석해주는 통합 대시보드 구조 개발.

---

## 🇺🇸 English Version

### 1. Project Overview
**Project Name:** Excel Task Analyzer
**Objective:** To develop a lightweight desktop application that automatically analyzes, processes, and summarizes large volumes of Excel data extracted from IT support/ticket systems, significantly reducing manual effort for users.
**Key Features:**
- **Task 1 (Performance Summary by Assignee):** Filters tickets based on a specific user (`Closed by`), calculates total accumulated workload (`Man minute`) and real processing time (`Time Diff` from start to close), and generates a summarized report with an appended totals row.
- **Task 2 (Keyword Search & Extraction):** Quickly searches and extracts tickets that contain a specific keyword within the `Short description`, saving the result to a new file.
- **Task 3 (Frequency Analysis):** Calculates the occurrence frequency of issues within the `Short description` and generates a report sorted in descending order to identify the most critical or repetitive problems.

### 2. Architecture
- **Language:** Python 3.x
- **UI Framework:** Tkinter (Native library providing a lightweight setup)
- **Data Processing:** Pandas (Optimized for filtering, calculation, grouping, and handling large data scopes natively)
- **File I/O:** Openpyxl engine via Pandas for reliable parsing and formatting of `.xlsx` files.
- **Testing:** Unit test environment established via `unittest` module covering core logic functions (`test_logic.py`).

### 3. AI Utilization Strategy
Artificial Intelligence was utilized across various stages to maximize development productivity and application stability:
- **Rapid GUI Scaffolding:** Drafted the entire structural layout of Tkinter (frames, buttons, internal combo lists, status bars) quickly using AI prompt guidance.
- **Pandas Logic Optimization:** Received and implemented smart refactoring advice for data type handling (such as date formatting logic and concatenations) ensuring error-free data restructuring.
- **Automated Test Generation:** Leveraged AI capabilities to map out edge cases in `test_logic.py`, ensuring core functions behave predictably during case-insensitive keyword searches and NaN data scenarios.

### 4. Troubleshooting & Technical Decisions
- **Issue:** The application crashed when encountering blank cells (`NaN`) or unparseable text in critical columns like `Man minute`, `Actual start`, or `Closed`.
  - **Resolution:** Decided to robustly clean data streams using `pd.to_numeric(errors='coerce').fillna(0)` and `pd.to_datetime(errors='coerce')`, ensuring mathematical functions default to 0 natively rather than raising exceptions.
- **Issue:** Warning messages regarding the deprecation of DataFrame `append()` while inserting the final 'Total' row at the bottom of Task 1 reports.
  - **Decision:** Shifted to a modern, scalable approach. Built a temporary dictionary referencing core calculations then constructed a new DataFrame via `pd.concat([filtered_df, sum_df])`, abiding by the best current Pandas practices and future-proofing the script.
- **Issue:** The GUI froze momentarily when interacting with relatively large files during read/write cycles.
  - **Resolution:** Introduced `self.root.update_idletasks()` explicitly inside the logging function to guarantee that the bottom Status Bar refetches events and informs users synchronously. 

### 5. Deployment & Future Tasks
- **Current Deployment:** Deployed primarily as an executable Python script logic model.
- **Immediate Deployment Goal:** Package the codebase into a portable Standalone Executable (`.exe`) via `PyInstaller`, allowing non-developer colleagues without Python environments to confidently use the tool out-of-the-box.
- **Future Enhancements:**
  1. **Data Visualization:** Integration of `Matplotlib/Seaborn` to present interactive graphical charts rendering performance trends visually.
  2. **Dynamic Column Mapping:** Evolve past hardcoded column variables (e.g. 'Closed by') by letting users selectively choose and map target columns from dropdown interfaces.
  3. **Batch Processing:** Enable the dashboard to ingest, merge, and evaluate multiple chronological target `.xlsx` lists in an aggregated sequence simultaneously.
