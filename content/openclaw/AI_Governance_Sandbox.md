# AI Governance & Sandbox Field Notes

> **Purpose**: Document how an infrastructure-focused engineer can transition into AI-era DevOps by building repeatable guidelines, safe sandboxes, and concrete evaluation logs.

## 1. Why This Track Exists
- Traditional infra roles are shrinking, but the need for **trustworthy AI operations** is exploding.
- Goal: reuse 17+ years of DC/Infra expertise to become the person who **designs, hardens, and operates AI systems**.
- This note captures:
  - What was tested (guidelines, sandboxes, cost controls)
  - How the experiments were run in OpenClaw
  - Action items for the next iteration of the portfolio site (doc.chaeyul.uk)

## 2. AI Guidelines — Experiments & Lessons
| 날짜 | 프레임워크/도구 | 목적 | 결과/메모 |
| --- | --- | --- | --- |
| 2026-03-18 | NIST AI RMF quick audit | 이해당사자/리스크 체크리스트 만들기 | 기존 인프라 Change Management 양식을 재활용 가능. Needs mapping sheet. |
| 2026-03-19 | Credo AI demo 계정 | 모델 거버넌스 SaaS 검증 | 규제 산업용 기능 많음. API 로그 연동 테스트 예정. |
| 2026-03-21 | 자체 가이드라인 v0.1 | doc.chaeyul.uk에 게시할 기준 초안 | Input/Output 검증, HIL, 로그 보존 항목 초안 완성. |

**적용 포인트**
- OpenClaw `guardrails-proxy` 정책을 NIST RMF 흐름에 맞춰 문서화 → PDF/MD 업로드 예정
- doc.chaeyul.uk에 "AI Governance" 섹션 신설 + 체크리스트 템플릿 공개

## 3. AI Sandbox — Experiments & Lessons
| 날짜 | 샌드박스 | 사용 모델 | 관찰 포인트 |
| --- | --- | --- | --- |
| 2026-03-17 | OpenAI Playground | GPT-4o | 프롬프트 코스트/토큰 추적 수동. 클라우드 비용 감시 연동 필요. |
| 2026-03-18 | Azure AI Studio | gpt-4o, dall-e | VNet 통합으로 보안 좋음. 초기 설정 복잡. |
| 2026-03-20 | Hugging Face Spaces | Mixtral | 커스터마이징 빠름, 비용 투명. 자체 모니터링 없음. |
| 2026-03-21 | OpenClaw Local Sandbox | Gemini 2.5 Flash, GPT-4o | 로컬 워크로드+Langfuse 연동 테스트. Cron 뉴스 봇 개선 대상으로 선정. |

**적용 포인트**
- 매일 아침 뉴스 스크립터를 ClawaTeams와 연동해, 샌드박스 실험 노트를 팀 채널로 브로드캐스트
- 샌드박스별 비용/성능 비교표를 추후 Grafana 대시보드로 시각화 (토큰/시간/실패율)

## 4. 작업 항목 (Working Tasks)
- [ ] `AI_Governance_Checklist.md` 작성 → doc.chaeyul.uk 에 게시
- [ ] 샌드박스 비용 수집 스크립트: OpenAI + Vertex AI Usage API → Google Sheet
- [ ] OpenClaw Agents 4명 간 로그 공유용 `tasks.yaml` 제작 (뉴스/가이드라인/테스트 구분)
- [ ] ClawaTeams 접근 권한 확보 후 뉴스 브리핑 작업 이관 PoC

## 5. 다음 단계
1. **콘텐츠**: AI 가이드라인, 샌드박스 노트를 정리해 Personal Website 섹션에 반영
2. **자동화**: OpenClaw → ClawaTeams 연동 실험으로 협업 스토리 강화
3. **DevOps화**: GitHub Actions + Netlify 로 Quartz 사이트 자동 배포, 변경 히스토리 공개
4. **포트폴리오 메시지**: "Infra Veteran ➔ AI DevOps Lead"를 모든 문서에서 일관되게 강조

---
**Log**
- 2026-03-23: 초기 정리 (자비스) — GitHub SSH 세팅 후 Technical-Notes 동기화 완료. AI 가이드라인/샌드박스 섹션 초안 작성.