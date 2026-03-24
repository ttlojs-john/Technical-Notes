# AI Governance & Sandbox Lab Log

> _Living notes on how I am translating 17 years of infra/operations experience into practical AI guardrails and safe experimentation workflows._

## 🎯 Objectives
- Establish working **AI usage guidelines** that reflect real infra/DevOps constraints (security, audit, reliability).
- Build a repeatable **sandbox workflow** for evaluating LLM prompts, tools, and agents before they touch production systems.
- Document every experiment so that future me (or a future team) can reuse the pattern without guessing.

## 🧱 Governance Building Blocks
| Area | Current Practice | Next Iteration |
| --- | --- | --- |
| Data Handling | Classify datasets (Public/Internal/Restricted) before letting agents ingest them. | Automate tagging via metadata and block Restricted data at gateway level. |
| Tool Approval | High-risk tools (email, deletion, finance APIs) always require Human-in-the-Loop approval. | Add per-tool checklists + Slack/Telegram approval logs for audits. |
| Logging & Audit | Langfuse traces for every LLM call, tagged when guardrails trigger. | Export weekly summaries to GitHub repo for long-term storage. |

## 🧪 Sandbox Strategy
1. **Prompt/Tool smoke test** → OpenAI / Gemini playgrounds or local notebooks.
2. **Guardrail rehearsal** → run through `guardrails-proxy` to confirm filters & tagging.
3. **Full agent rehearsal** → Launch disposable browser + code sandbox, record Langfuse traces.
4. **Publish findings** → push Markdown note + screenshots into this repo.

### Recent Experiments
- ✅ **OpenClaw security filters** against prompt-injection scripts from OWASP LLM Top 10.
- ✅ **Disposable browser sandbox** measuring crawl latency & isolation.
- 🔄 **ClawaTeams vs OpenClaw** division of labor tests (news briefings, cron tasks).
- 🔜 **Budget tracker** for OpenAI + Vertex AI usage (Apps Script prototype).

## 📋 Checklists
**AI Guideline Draft v0.2**
- [x] Define approval matrix per tool (READ/WRITE/EMAIL/DELETE).
- [x] Sanitise all external HTML via readability + html2text.
- [ ] Run monthly review of Langfuse traces for `security_threat` tags.
- [ ] Publish user-facing policy page (in progress).

**Sandbox Smoke Test**
1. Prompt quality OK? (No hallucinated commands)
2. Guardrails triggered? (If yes, expectation vs reality)
3. Latency acceptable? (< 8s total)
4. Logs stored? (Langfuse + repo note)

## 🗂️ How to Use This Folder
- `AI_Governance_Sandbox_Log.md` (this file): running summary.
- Future additions:
  - `guideline_template.md` – formal checklist for new projects.
  - `sandbox_runbooks/` – step-by-step guides per LLM/tool chain.

Feel free to create new notes under this directory for each experiment. Use timestamps in filenames so the Quartz graph stays tidy. 