---
title: "Hostinger VPS Hermes 멀티플렉스 게이트웨이와 Slack 3봇·Quartz 배포 테스트"
date: 2026-11-24
draft: true
tags:
  - Hermes
  - Slack
  - Hostinger
  - Quartz
  - GitHub-Pages
description: "Hostinger VPS에서 확인한 Hermes 3프로필 멀티플렉스 게이트웨이, Slack 봇 연계, Deploy Key와 Quartz 배포 경로의 검증 기록."
---

# Hostinger VPS의 Hermes 멀티플렉스 게이트웨이 테스트

> **상태: 비공개 초안.** 이 글은 확인된 구성과 아직 검증하지 못한 단계를 구분한다. `draft: true`인 동안 Quartz의 `RemoveDrafts` 필터가 공개 페이지에서 제외한다. GitHub 저장소에 푸시할 경우 **저장소 접근 권한은 별개**이므로, 비공개 자료는 저장소의 공개 여부도 확인해야 한다.

![Hostinger VPS의 단일 Hermes 게이트웨이에서 세 봇과 Quartz 배포 경로가 연결되는 개념도](./hermes-multiplex-quartz-hero.png)

## 1. 목표와 범위

2026년 11월 24일, Hostinger 관리 Docker 환경의 Hermes 게이트웨이 한 프로세스가 `default`, `plan`, `research` 프로필을 함께 서빙하는 구성을 점검했다. 사용자 의도는 Slack의 `@research`, `@Plan`, `@chaeyulai` 세 봇을 계획·조사·검토의 순서로 연계하고, 산출물을 SSH Deploy Key로 GitHub에 전달해 Quartz 사이트에 배포하는 것이다. **프로필 3개가 동시에 연결되는 것과 실제 자동 핸드오프가 끝까지 성공하는 것은 다른 검증 항목**이다.

```mermaid
flowchart LR
  U["사용자 / Slack"] --> G["Hermes gateway · 단일 프로세스"]
  G --> R["research 프로필"]
  G --> P["plan 프로필"]
  G --> D["default 프로필"]
  R -. "산출물 전달: 별도 검증 필요" .-> P
  P -. "검토 요청: 별도 검증 필요" .-> D
  D --> K["SSH Deploy Key"]
  K --> GH["GitHub Technical-Notes / main"]
  GH --> A["Actions: Quartz build"]
  A --> S["GitHub Pages · doc.chaeyul.uk"]
```

## 2. 게이트웨이 구성 확인

- `hermes profile list`에서 `default`, `plan`, `research` 세 프로필의 게이트웨이가 실행 중으로 표시됐다.
- `hermes gateway status`는 **PID 1881**, 기본 프로필에서 구동되는 게이트웨이를 보고했다. `gateway_state.json`의 `served_profiles`는 `default`, `plan`, `research`였다.
- `hermes -p research gateway status`와 `hermes -p plan gateway status`는 각각 **default-profile multiplexer를 통해 실행 중**이라고 보고했다. 별도의 세 게이트웨이가 필요하지 않다.
- 상태 파일에서 기본 프로필의 `slack`, `telegram`, `api_server` 연결 상태는 `connected`였다. 이것만으로 각 Slack 봇의 종단 간 메시지 응답 또는 봇 간 연쇄 완료를 입증하지는 못한다.
- 이 설치는 Hostinger 관리 환경이다. 게이트웨이 상태에 설치 산출물 동기화 경고가 출력됐으므로 별도 운영 점검 항목으로 남겨 둔다. 관리형 Hermes 자체를 수동 업데이트하는 절차는 여기서 다루지 않는다.

공식 문서에 따르면 멀티플렉스는 한 프로세스가 프로필별 어댑터·자격증명·세션을 분리해 서비스한다. **프로필 간 모델·토큰의 공유를 전제로 하지 않는다.** [Hermes 다중 프로필 게이트웨이 문서](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways).

## 3. 세 봇 연쇄 실행: 구성과 미검증 부분

설계된 작업 순서는 `@Plan`의 작업 분해 → `@research`의 근거 수집·초안 → `@chaeyulai`의 검토 및 승인 요청이다. 실제 작업에서는 요청자가 `@research`부터 시작하는 경우도 있으므로 단계의 시작점은 호출 메시지에 따라 달라진다. **현재 확인한 것은 세 프로필이 같은 게이트웨이에서 서비스된다는 사실과 각각의 Slack 대화가 생성됐다는 점까지다.** 동일 스레드에서 앞 봇의 출력이 다음 봇에게 자동 전달되고 세 번째 봇의 응답까지 돌아왔다는 메시지 ID·트레이스는 확보하지 못했다. 따라서 이 기록에서 ‘자동 연쇄 실행 성공’이라고 표기하지 않는다.

재검증 시에는 테스트 스레드 하나를 정해 다음 증거를 보존한다.

1. 첫 봇의 요청·응답 메시지 시각과 스레드 ID.
2. 다음 봇의 입력에 이전 단계 산출물이 포함됐는지, 각 프로필의 세션/로그로 확인.
3. 마지막 봇의 결과 및 승인 게이트가 실제 푸시 전에 멈췄는지 확인.

## 4. GitHub Deploy Key → Quartz 배포 경로

저장소 원격은 `git@github.com:ttlojs-john/Technical-Notes.git`이다. VPS의 SSH 설정에서 GitHub 접속용 키 경로는 `/opt/data/.ssh/id_ed25519_quartz`로 해석됐다. `ssh -T -o BatchMode=yes -o StrictHostKeyChecking=yes git@github.com` 호출은 `Hi ttlojs-john/Technical-Notes! You've successfully authenticated`를 반환했다. 이는 **저장소 연결용 키 인증 성공**의 증거이며, 쓰기 권한이나 이번 초안의 푸시·실제 배포 성공 증거는 아니다.

저장소의 `.github/workflows/deploy.yml`은 `main` 푸시 때 Node 22에서 `npm ci`, `npx quartz build`를 실행한 다음 `actions/upload-pages-artifact@v3` 및 `actions/deploy-pages@v4`로 **GitHub Pages**를 배포하도록 구성되어 있다. Netlify/Vercel 경로가 아니다. Quartz의 `baseUrl`은 `doc.chaeyul.uk`이다. 배포 성공 여부는 승인 후 푸시된 커밋의 Actions 실행 결과와 사이트에서 별도로 확인해야 한다.

## 5. 비공개 초안과 승인 경계

현재 저장소의 `quartz.config.ts`에는 `Plugin.RemoveDrafts()`가 활성화돼 있고, 필터는 frontmatter의 `draft: true`를 공개 빌드 대상에서 제외한다. 따라서 **이 포스트의 페이지 공개 여부**와 **초안 파일을 GitHub 저장소에 올리는 행위**를 구분해야 한다. `content/update_index.py`는 카테고리의 Markdown을 스캔할 때 `draft` 여부를 검사하지 않는다. 초안 상태에서 이를 그대로 실행해 인덱스를 배포하면 제목 또는 링크가 공개 카탈로그에 나타날 수 있어, 이 글은 인덱스 갱신 대상으로 넣지 않는다.

- 확인됨: 게이트웨이 1개/PID 1881/3개 프로필, SSH 키 인증, Quartz 배포 워크플로의 구성, draft 필터.
- 미확인: 자동 3봇 연쇄의 종단 간 완료, Deploy Key 쓰기 권한, 이 글에 대한 GitHub Actions 실행·공개 URL.
- 승인 전: 커밋·푸시 및 공개 전환 없음. 승인 후에도 `draft: true` 유지 여부, 저장소 공개 범위, 인덱스 노출 방지를 먼저 결정한다.

## 참고

- [Hermes: Running Many Gateways at Once](https://hermes-agent.nousresearch.com/docs/user-guide/multi-profile-gateways)
- [Hermes: Multiplexing Gateway Internals](https://hermes-agent.nousresearch.com/docs/developer-guide/multiplexing-gateway)
- 로컬 검증 자료: `/opt/data/gateway_state.json`, 저장소의 `quartz.config.ts`, `quartz/plugins/filters/draft.ts`, `.github/workflows/deploy.yml`.
