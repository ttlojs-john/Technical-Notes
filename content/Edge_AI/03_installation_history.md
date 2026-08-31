# 🛠️ 03. 단계별 초기 구축 및 설치 내역 (Step-by-Step Installation History)
> **Edge AI 텔레그램 멀티모달 번역 및 웹 통합 관리 시스템 가이드**

---

## 🔗 문서 이동 (Navigation)
- [01. 시스템 개요](file:///home/aiadmin01/edge_ai_guide/01_system_overview.md)
- [02. 전체 시스템 구성도 및 아키텍처](file:///home/aiadmin01/edge_ai_guide/02_system_architecture.md)
- **[03. 단계별 초기 구축 및 설치 내역](file:///home/aiadmin01/edge_ai_guide/03_installation_history.md)**
- [04. 설치 이후 추가 기능 및 업그레이드](file:///home/aiadmin01/edge_ai_guide/04_upgrades_and_evolution.md)
- [05. 상세 컴포넌트 동작 및 데이터 흐름](file:///home/aiadmin01/edge_ai_guide/05_detailed_workflows.md)
- [06. 보안 및 인프라 성능 최적화](file:///home/aiadmin01/edge_ai_guide/06_security_and_tuning.md)
- [07. 운영 관리, 검증 테스트 및 배포 가이드](file:///home/aiadmin01/edge_ai_guide/07_operations_and_deployment.md)

---

## 1. 개요 (Overview)

본 시스템은 설계 수립 단계에서 정의된 5단계의 인프라 및 핵심 애플리케이션 구축 절차를 거쳐 완벽하게 동작하는 마이크로서비스로 배포되었습니다. 이하 단계별 상세 설치 내역을 설명합니다.

---

## 2. 단계별 설치 내역 (Phase-by-Phase Installation)

### 📌 Step 1: 쿠버네티스(K3s) 엣지 인프라 환경 구축
1. **Ubuntu 26 LTS 환경 준비 및 K3s 설치**:
   - 시스템 가용 리소스를 파악한 뒤 경량 쿠버네티스인 K3s를 기본 컨테이너 런타임인 containerd와 함께 단일 노드(Single-Node) 클러스터로 설치하였습니다.
   ```bash
   curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644
   export KUBECONFIG=/home/aiadmin01/.kube/config
   ```
2. **K3s 상태 확인 및 네임스페이스 준비**:
   - 노드 및 기본 시스템 포드가 정상 기동(Running) 중인지 확인하였습니다.
   ```bash
   kubectl get nodes
   ```

---

### 📌 Step 2: Edge AI Engine 백엔드 구축 및 배포
1. **FastAPI 기반 인공지능 처리 서버 구축**:
   - 이미지 OCR: Tesseract v5 엔진 및 파이썬 Wrapper인 `pytesseract` 라이브러리를 연동하였습니다.
   - 번역: 기계 번역 엔진 통합 라이브러리 탑재.
   - 음성 인식(STT): 음성 데이터 청크 디코딩 및 텍스트 변환 파이프라인 설계.
2. **도커 컨테이너화 및 배포 구성**:
   - 로컬 컴파일을 거친 Docker 이미지를 빌드하고, 외부 도커 허브를 거치지 않고 K3s 내부 containerd 이미지 레지스트리에 직접 수입(Import)하여 프라이빗 배포를 진행했습니다.
   ```bash
   cd /home/aiadmin01/edge-ai-engine
   docker build -t edge-ai-engine:latest .
   docker save edge-ai-engine:latest | sudo k3s ctr images import -
   ```
3. **K8s Deployment 및 Service 매니페스트 적용**:
   - `edge-ai-engine-service`를 ClusterIP(포트 80 ➡️ 컨테이너 8000)로 정의하여 내부 도메인으로 통신할 수 있게 하였습니다.
   ```bash
   kubectl apply -f deployment.yaml
   ```

---

### 📌 Step 3: 텔레그램 봇(Telegram Bot) 서비스 구축
1. **비동기 텔레그램 클라이언트 작성**:
   - `aiogram` 기반 텔레그램 봇 파이썬 코드를 작성하고 사용자의 텍스트, 이미지, 음성 메시지를 비동기로 가로채는 핸들러를 구현했습니다.
2. **봇 토큰 비밀 보관 (K8s Secret)**:
   - 봇의 API 토큰 노출 방지를 위해 Kubernetes Secret을 먼저 생성하였습니다.
   ```bash
   kubectl create secret generic telegram-bot-secret --from-literal=token="<YOUR_TELEGRAM_BOT_TOKEN>"
   ```
3. **Telegram Bot 배포**:
   - `telegram-bot` Deployment를 배포하고 내부에서 `edge-ai-engine-service` 도메인 주소(`http://edge-ai-engine-service:80/api/v1/process`)로 REST API 요청을 보내도록 설정했습니다.
   ```bash
   cd /home/aiadmin01/telegram-bot
   kubectl apply -f deployment.yaml
   ```

---

### 📌 Step 4: 웹 관리자 대시보드(Web Dashboard) 구축
1. **실시간 관제 대시보드 제작**:
   - FastAPI 기반 웹 애플리케이션에 관리자 계정 로그인을 처리하는 인증/인가 로직(JWT)을 구성하였습니다.
   - 실시간 메트릭 모니터링을 위해 `/api/v1/telemetry`를 만들고, 웹 브라우저에서 폴링할 수 있도록 HTML/CSS/JS 프론트엔드를 패키징했습니다.
2. **K8s Ingress 노출**:
   - 포트 80으로 외부에서 직접 웹 대시보드 화면에 접속할 수 있도록 `web-dashboard-ingress` 리소스를 정의하였습니다.
   ```bash
   cd /home/aiadmin01/web-dashboard
   kubectl apply -f deployment.yaml
   ```

---

### 📌 Step 5: End-to-End 기초 검증
- 텔레그램 채널에서 지정된 봇에게 메시지를 전송하고 정상적으로 한국어로 번역 및 회신이 처리되는지 수동 검증을 진행했습니다.
- 웹 브라우저로 `http://<EDGE_NODE_IP>` 에 접속해 대시보드 로그인 및 텔레메트리 연동이 정상임을 검증하며 초기 설치 단계를 마무리했습니다.
