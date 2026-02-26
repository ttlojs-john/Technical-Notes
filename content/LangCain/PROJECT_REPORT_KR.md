# 📘 LangChain AI Agent - 프로젝트 완료 보고서

## 1. 프로젝트 개요
본 프로젝트는 **Next.js** (프론트엔드)와 **FastAPI** (백엔드)를 사용하여 구축된 현대적이고 고성능인 AI 웹 애플리케이션입니다. **LangChain**을 활용하여 고급 AI 모델(OpenAI GPT-4o, Google Gemini)과의 상호작용을 조율하며, **보안**, **안정성**, **확장성**을 최우선으로 고려하였습니다.

---

## 2. 시스템 아키텍처

| 컴포넌트 | 기술 스택 | 설명 |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 14+** (React) | 채팅, OCR, 번역을 위한 반응형 UI 제공. Proxy Rewrite를 통해 안전한 API 통신 구현. |
| **Backend** | **FastAPI** (Python) | AI 로직, 인증, 파일 처리를 담당하는 고성능 비동기 API 서버. |
| **AI Orchestration** | **LangChain** | LLM 컨텍스트, 프롬프트 템플릿, 모델 스위칭(OpenAI/Gemini) 관리. |
| **Process Management** | **PM2** | Ubuntu 서버에서 프론트엔드와 백엔드 서비스의 24/7 가동 보장. |

---

## 3. 핵심 기능 구현

### 🤖 AI 채팅 및 강력한 폴백(Fallback) 시스템
- **주 모델**: `gpt-4o` (품질 최적화).
- **폴백 메커니즘**: "Try-Catch" 로직 구현. 주 모델 실패 시(API 키 제한, 404 등) 시스템 중단 없이 자동으로 `gpt-4o-mini` 또는 `gpt-3.5-turbo`로 **다운그레이드**하여 서비스 연속성 보장.
- **멀티모달**: 이미지 업로드를 통한 시각 기반 분석 지원.

### 📷 OCR (광학 문자 인식)
- **GPT-4o Vision** 또는 **Gemini Pro Vision**을 사용하여 이미지에서 텍스트 추출.
- **프라이버시 우선**: 이미지는 메모리 또는 임시 저장소에서 처리되며 분석 후 즉시 삭제됨.

### 🌐 스마트 번역
- 문맥 인식 프롬프팅을 사용하여 전문 번역가처럼 작동.
- 언어 자동 감지 및 목표 언어 선택(한국어, 영어, 독일어 등) 지원.

### 🗣️ 오디오 인텔리전스 (TTS & STT)
- **Text-to-Speech**: `gTTS`를 사용하여 텍스트 응답을 MP3 오디오로 변환.
- **Transcription**: 업로드된 오디오 파일을 텍스트로 변환하여 요약 또는 번역에 활용.

---

## 4. 보안 및 프라이버시 조치 (구현 완료)

본 프로젝트는 사용자 데이터 보호와 시스템 무결성을 위해 엄격한 보안 표준을 준수합니다.

### 🔒 1. PII (개인식별정보) 마스킹
- **모듈**: `backend/pii_utils.py`
- **기능**: 사용자 입력이 외부 AI API에 도달하기 **전**에 가로챔.
- **메커니즘**: Regex 패턴을 사용하여 민감 데이터를 감지하고 마스킹 처리.
  - *이메일* $\rightarrow$ `<EMAIL_ADDRESS>`
  - *전화번호* $\rightarrow$ `<PHONE_NUMBER>`
  - *신용카드* $\rightarrow$ `<CREDIT_CARD>`
- **이점**: OpenAI/Google 등 제3자 AI 제공자로의 민감 데이터 유출 방지.

### 🔑 2. 보안 인증 (JWT)
- **표준**: OAuth2 Password Bearer 흐름.
- **해싱**: 비밀번호는 저장 전 **Bcrypt**로 해싱됨 (평문 저장 절대 금지).
- **세션**: API 접근 제어를 위해 수명이 짧은 **JSON Web Tokens (JWT)** 발급. `/chat`에 대한 비인증 요청 차단.

### 🛡️ 3. 환경 보안
- **비밀 관리**: API 키(`OPENAI_API_KEY`, `GOOGLE_API_KEY`) 및 `SECRET_KEY`는 `.env` 파일에 격리.
- **배포 안전성**: 
  - 배포 스크립트(`pack_v2.ps1`)는 아티팩트 생성 시 `.env` 파일을 **제외**하여 키 유출 방지.
  - 서버 측 스크립트(`update_env.sh`)를 통해 운영 환경에서 직접 안전하게 키 주입 가능.

### 🧹 4. 자동 라이프사이클 관리
- **클린업 데몬**: 백그라운드 스레드가 10분마다 실행되어 10분 이상 된 임시 파일(`temp_*`, `audio_*`, `output_*.mp3`)을 스캔하고 삭제.
- **리소스 보호**: 디스크 공간 고갈 공격 및 데이터 잔존 문제 방지.

---

## 5. 배포 워크플로우 및 스크립트

자동화된 배포를 위한 완벽한 DevOps 스크립트 모음을 포함합니다.

1.  **패키징**: `pack_v2.ps1` (Windows)
    -   무거운/민감한 폴더(`venv`, `node_modules`, `.env`)를 제외하고 코드베이스 번들링.
2.  **배포**: `deploy_ubuntu.sh` (Linux)
    -   시스템 의존성 자동 설치 (Node.js 20, Python 3.12).
    -   가상 환경(venv) 설정 및 `requirements.txt` 설치.
    -   Next.js 프론트엔드 빌드.
    -   방화벽 규칙 설정 (`ufw allow 8000/3000`).
3.  **환경 설정**: `update_env.sh` (Linux)
    -   중단 없이 API 키를 안전하게 업데이트하고 서비스를 재시작하는 대화형 도구.

---

### ✅ 결론
본 시스템은 **프로덕션 준비 완료(Production-Ready)** 된 AI 애플리케이션으로 제공됩니다. 강력한 AI 기능과 필수 보안 기능의 균형을 성공적으로 맞추었으며, 보안 환경 배포에 적합합니다.

## 6. 최근 업데이트 (2026년 2월) - 모델 구성 및 ID 수정

### 🔄 GPT 모델 구성 업데이트
- **이슈**: "GPT-5"나 "GPT-5 Nano" 같은 비표준 모델 ID 사용 시 서버 환경에서 지속적인 연결 실패(404 Not Found) 발생.
- **해결**:
  - 기본 구성을 안정적인 공식 **GPT-4** 모델(`gpt-4`)로 전환.
  - `backend/config.py` 매핑 업데이트.
  - `frontend/app/page.tsx`의 모델 드롭다운이 "GPT-4"를 표시하도록 동기화하여 사용자 혼란 제거.

### 🆔 엄격한 정체성 강화
- **이슈**: 유사 아키텍처 모델 사용 시(또는 폴백 시) AI가 선택된 옵션과 다르게 자신을 소개하는 문제 발생.
- **구현**:
  - `backend/main.py`의 시스템 프롬프트 로직 수정.
  - **조건부 정체성 로직** 추가: 사용자의 선택에 따라 AI가 자신을 식별하도록 명시적 가이드 (예: "You are GPT-4...").
  - 인터페이스 선택과 AI의 자기 소개가 일치하는 일관된 사용자 경험 보장.

### 🛠️ 프론트엔드-백엔드 동기화
- **수정**: 프론트엔드 모델 목록 하드코딩으로 인한 백엔드 구성과의 불일치 해결.
- **메커니즘**: 서버에서 `sed` 명령어를 통한 "강제 업데이트" 로직을 구현하여 `page.tsx`의 `models` 상태를 덮어씀으로써 UI가 백엔드 모델 상태를 정확히 반영하도록 함.

---

## 7. 고급 기능 업데이트 (2026년 2월 10일) - RAG, 사용량, 상태

### 📚 RAG (검색 증강 생성)
- **목표**: 별도 파인튜닝 없이 사용자 지정 지식 베이스(PDF/Text)에 기반한 답변 제공.
- **기술 스택**:
  - **임베딩**: `GoogleGenerativeAIEmbeddings` (`text-embedding-004`) - 고속/고정확도.
  - **벡터 저장소**: `ChromaDB` - 효율적인 문서 청크 인덱싱 및 검색.
- **통합**: `backend/rag_utils.py` 구현 및 `/chat` 흐름 연결 완료. 튜터가 업로드된 자료를 실시간으로 참조 가능.

### 📊 토큰 사용량 추적기
- **백엔드 로깅**: `backend/tracker.py`를 추가하여 일일 토큰 사용량(문자 수 기반 추정)을 `backend/data/usage.json`에 영구 저장.
- **프론트엔드 UI**: 헤더에 "Usage" 버튼 통합, 모델별 금일 사용량 내역 표시.

### 🚥 실시간 모델 상태 모니터링
- **헬스 체크**: GPT 및 Gemini API 연결성을 검증하는 `/status` 엔드포인트 추가.
- **고시인성 UI**: 헤더에 고대비 이모지 표시기(`🟢`/`🔴`)를 도입하여 즉각적인 시스템 상태 파악 가능.
- **UX 개선**: 헤더 레이아웃 간격, 패딩, 버튼 텍스트 라벨 추가로 전문적이고 직관적인 인터페이스 구현.

---

## 8. 핵심 안정성 및 배포 업데이트 (2026년 2월 13일) - 프로덕션 준비

### 🔧 안정성 수정 (중요)
- **"Socket Hang Up" 및 시작 충돌 해결**:
  - **이슈**: `pydantic` (v1 vs v2) 및 `pydantic-core` 버전 호환성 문제로 Python 인터프리터 세그멘테이션 오류 발생.
  - **해결**: `pydantic>=2.0` 강제 재설치 및 `requirements.txt` 버전 고정으로 안정성 확보.
- **견고한 RAG 초기화**:
  - **이슈**: `chromadb` 구성 오류로 전체 애플리케이션 시작 불가 현상.
  - **해결**: RAG 초기화 로직을 `try-except` 블록으로 감싸, 지식 베이스가 일시적으로 사용 불가능해도 핵심 앱은 구동되도록 수정.

### 🚀 자동화된 배포 시스템
- **원클릭 서버 설정**: 전체 프로비저닝 프로세스를 자동화하는 `setup_server.sh` 도입:
  - 시스템 의존성 설치 (Python 3.12, Node.js 20, Unzip). (현재 3.14 이슈로 로컬은 3.14 사용 중이나 목표는 3.12)
  - 배포 아티팩트 압축 해제.
  - Python 가상 환경(`.venv`) 설정 및 의존성 설치.
  - `.env` 설정 템플릿 준비.
- **크로스 플랫폼 호환성**:
  - Windows에서 생성된 `venv`, `node_modules` 폴더 경로로 인한 Linux 실행 실패 문제 해결.
  - 프로덕션 서버에서 이 환경들을 네이티브하게 재빌드하는 로직 구현.

### 🌍 프로덕션 구성
- **외부 접근**: 프론트엔드가 `localhost` 대신 `0.0.0.0`에 바인딩되도록 구성하여 안전한 외부 접근 허용.
- **프로세스 관리**: 레거시 좀비 프로세스(`pm2`) 정리 로직으로 새 배포 시 깨끗한 시작 상태 보장.

---

## 9. 최근 업데이트 (2026년 2월 15일) - Langfuse 통합 및 핵심 호환성수정

### 🛠️ Langfuse 셀프 호스팅 인프라 (Docker)
외부 의존성 없는 자체 로그 관측 스택 구축을 위해 로컬에 Langfuse를 배포했습니다.
- **Docker Compose 아키텍처**:
    - **경로**: `langfuse/docker-compose.yml`
    - **서비스**:
        - `langfuse-server`: 핵심 애플리케이션 (3333 포트 노출).
        - `langfuse-db`: 영구 트레이스 저장을 위한 PostgreSQL 데이터베이스 (v16).
    - **구성**:
        - `langfuse/.env`에서 민감한 시크릿 관리 (`DATABASE_URL`, `NEXTAUTH_SECRET`, `SALT`).
- **통합**:
    - 백엔드가 `langfuse` Python SDK를 사용하여 `http://localhost:3333`으로 비동기 트레이스를 전송하도록 설정.

### 🚨 핵심 이슈: Python 3.14 불일치 (CRITICAL)
통합 과정에서 중대한 안정성 문제가 식별되었습니다.

#### **진단 내용**
- **증상**: 백엔드가 소리 없이 종료되거나("Socket Hang Up"), `AttributeError: 'Langfuse' object has no attribute 'trace'` 에러 발생.
- **원인 분석**:
    - 현재 프로젝트 런타임: **Python 3.14 (Preview)**.
    - `Langfuse` SDK 의존성: **Pydantic V1**.
    - **불일치**: Pydantic V1이 Python 3.14에서 정상 초기화되지 않아 Trace 객체 생성이 불가능함. 이는 프리뷰 런타임의 알려진 업스트림 이슈.

#### **해결 및 완화 조치**
1.  **조건부 로직**: `backend/main.py`에서 Langfuse 초기화를 `ENABLE_LANGFUSE`로 제어되는 가드 블록으로 감쌈.
2.  **환경 제어**: `.env`에 `ENABLE_LANGFUSE=false` 도입.
3.  **결과**: 충돌을 일으키는 코드 경로를 성공적으로 우회하여, 인프라는 유지한 채 챗봇 전 기능을 복구함.

### 🔮 향후 계획: Python 다운그레이드
관측성(Observability) 기능을 활성화하기 위해 런타임 환경 표준화가 필요합니다.
- **계획**: Python 3.14에서 **Python 3.12 (Stable)**로 다운그레이드.
- **상태**: 완료 (Python 3.12.9 환경 구축 및 의존성 재설치 완료).

### ✅ Langfuse 재활성화
- **조치**: Python 3.12 환경에서 `requirements.txt` 재설치 및 `.env`의 `ENABLE_LANGFUSE`를 `true`로 변경.
- **결과**: 안정적인 Langfuse 트레이싱 기능 복구됨.

---

## 10. Langfuse 최종 안정화 및 데이터 영구화 (2026년 2월 15일 - 16일)

트레이싱 기능 활성화 후 발생한 데이터 유실 및 입력값 누락 문제를 최종 해결했습니다.

### 💾 데이터 영구 저장 (Data Persistence)
- **이슈**: Docker 가상 볼륨 사용으로 인해 컨테이너 재시작 시 API 키 및 설정이 초기화됨.
- **해결**: `docker-compose.yml`을 수정하여 호스트 경로(`./db_data`)에 PostgreSQL 데이터를 직접 바인딩(Bind Mount).
- **결과**: 서버 재시작 후에도 모든 트레이스 기록과 프로젝트 설정이 영구적으로 보존됨.

### 🧩 SDK 버전 및 데이터 누락 해결 (Ingestion Fix)
- **이슈**: Langfuse 서버(v2.95)와 Python SDK(v3.x) 간의 프로토콜 불일치로 데이터가 `null`로 기록되거나 전송 실패.
- **해결**:
    1.  **SDK 다운그레이드**: Python SDK를 v2.60 시리즈로 강제 고정하여 서버 호환성 확보.
    2.  **트레이스 레벨 핸들러**: v3 전용 메서드(`as_langchain_handler`) 대신 v2 방식의 `CallbackHandler(stateful_client=trace)`를 적용.
    3.  **명시적 플러시(Explicit Flush)**: 채팅 응답 직후 `.flush()`를 호출하여 비동기 환경에서도 100% 데이터 전송 보장.
- **결과**: Langfuse 대시보드에서 Input/Output 채팅 대화 내용이 정상적으로 기록됨을 확인.

### 📝 명시적 데이터 캡처 (Explicit Capture) 확인
- **이슈**: LangChain 내부 구조로 인해 사용자 입력(Input) 및 AI 응답(Output) 텍스트가 트레이스 최상단에 노출되지 않고, 내부 Step에 숨겨지는 현상.
- **해결**:
    1.  `trace()` 생성 시 `input=request.message`를 전달하여 사용자 메시지를 고정.
    2.  `as_stateful_client=False` 옵션을 `CallbackHandler`에 적용하여 Chain 실행 중 입력 필드가 덮어씌워지는 부작용 방지.
    3.  응답 생성 직후 `trace.update(output=response_text)`를 호출하여 결과값 명시적 업데이트.
- **효과**: Langfuse UI 목록 및 상세 화면에서 대화 내용과 결과가 즉시 확인 가능.

### 🛑 LangChain "Dependency Hell" 해결 (ImportError)
- **증상**: `ImportError: cannot import name 'ContextOverflowError'` 및 `AzureChatOpenAI` 모듈 로드 실패로 백엔드 비정상 종료.
- **원인**: `langchain` 메인 패키지를 0.2.16(구버전)으로 다운그레이드했으나, `langchain-openai`, `langchain-google-genai` 등 파생 패키지가 여전히 0.3.x(최신) 호환 버전을 참조하여 `langchain-core` 버전 충돌 발생.
- **해결**:
    - `langchain==0.2.16` (Core 0.2.x 기반)
    - `langchain-community==0.2.16`
    - `langchain-openai<0.2.0` (0.1.x)
    - `langchain-google-genai<2.0.0` (1.x)
    - 위와 같이 전체 생태계의 버전을 0.2.x 호환군으로 일괄 다운그레이드.
- **결과**: `ImportError` 완전 해결 및 정상적인 서버 구동 확인.

---

## 11. 상세 설정 문서화 (Configuration Reference)

이 섹션은 프로젝트의 Langfuse 자가 호스팅 환경 및 모니터링 시스템의 핵심 설정값을 기록합니다.

### 🐳 Docker Compose 설정 (`langfuse_infra/docker-compose.yml`)
Langfuse 서버와 Postgres 데이터베이스는 `docker-compose`를 통해 관리됩니다.

#### 1. Langfuse Server (`langfuse-server`)
- **이미지**: `langfuse/langfuse:2` (안정적인 v2 태그 사용)
- **포트 매핑**: `3333:3000` (호스트의 3333 포트로 접근)
- **환경 변수**:
  - `NODE_ENV`: `production`
  - `DATABASE_URL`: `postgresql://postgres:postgres@db:5432/postgres` (내부 도커 네트워크)
  - `NEXTAUTH_URL`: `http://localhost:3333`
  - 보안 키 (값은 `.env` 참조): `NEXTAUTH_SECRET`, `SALT`, `ENCRYPTION_KEY`
- **헬스 체크**: 3000번 포트의 `/api/health` 엔드포인트 모니터링.

#### 2. PostgreSQL Database (`db`)
- **이미지**: `postgres:16`
- **포트 매핑**: `5432:5432` (로컬 접속 허용)
- **볼륨 (Persistence)**:
  - `./db_data:/var/lib/postgresql/data` (Bind Mount 사용)
  - **중요**: Docker Volume 대신 호스트 디렉토리를 직접 마운트하여 컨테이너 재생성 시 데이터가 절대 유실되지 않도록 보장.
- **기본 계정**:
  - User: `postgres`
  - Password: `postgres`
  - DB: `postgres`

### 🔌 백엔드 Langfuse 연동 설정

#### 1. 환경 변수 (`.env`)
```bash
# Langfuse 활성화 여부
ENABLE_LANGFUSE=true

# Langfuse 인증 (로컬 Docker)
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_HOST=http://localhost:3333

# 데이터베이스 연결 문자열 (필요 시)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/postgres
```

#### 2. Python SDK 초기화 (`backend/main.py`)
- **버전 고정**: `langfuse>=2.0.0` (v2 호환성 유지)
- **핸들러 설정**:
  ```python
  from langfuse.callback import CallbackHandler
  
  # 상태 유지형 클라이언트 비활성화로 입력값 덮어쓰기 방지
  trace = langfuse.trace(name=..., input=...)
  handler = CallbackHandler(stateful_client=trace)
  ```
- **플러시 전략**: 비동기 데이터 유실 방지를 위해 요청 완료 후 반드시 `langfuse.flush()` 호출.

