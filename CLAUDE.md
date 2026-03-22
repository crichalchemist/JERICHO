# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Commands

### JavaScript (Node.js — legacy, Phase 0 transition)
```bash
npm install          # install JS dependencies
npm run dev          # Node API (port 3000) + Vite client (port 5173) concurrently
npm run dev:api      # Node API only — uses STATE_PATH=src/data/state_good.json
npm run dev:client   # Vite client only
npm test             # Jest suite with coverage (src/core only)
npm run lint         # ESLint + Prettier rules
npm run build        # lint + test + vite build
```
Run a single JS test: `NODE_OPTIONS=--experimental-vm-modules jest tests/core/scoring-engine.test.js`

### Python (FastAPI — active backend, port 8000)
```bash
cd backend
uv venv .venv && source .venv/bin/activate   # one-time setup
uv pip install -e ".[test]"                  # install all deps including test extras
uv run uvicorn jericho.main:app --reload     # run FastAPI dev server
uv run pytest                                # full test suite with coverage
uv run pytest tests/domain/ --no-cov -v     # domain-only tests, verbose
uv run pytest tests/domain/test_pipeline.py -v --no-cov   # single file
```

### Cutover (switching frontend from Node to FastAPI)
```bash
VITE_API_BASE_URL=http://localhost:8000 npm run dev:client
python scripts/compare_routes.py            # verify parity before cutover
```

The FastAPI dev server reads state from `STATE_PATH` env var (defaults to `../src/data/state_good.json`).

## Architecture

The system is a **closed-loop behavioral execution engine**. The pipeline is the architectural spine:

```
Goal Input → validateGoal → deriveIdentityRequirements → computeCapabilityGaps
  → generateTasksForCycle → computeIntegrityScore → applyIdentityUpdate
  → (repeat next cycle)
```

`src/core/pipeline.js` is the orchestrator — it imports and sequences every engine module. This is the entry point for understanding the system.

### Layer map

| Layer | Path | Role |
|---|---|---|
| Core engines | `src/core/` | Pure functions, no I/O. All business logic lives here. |
| API | `src/api/server.js` | Single HTTP server (Node `http`, no framework). Routes call core engines. |
| Services | `src/services/` | I/O-bound side effects: reinforcement, integrity writes, calendar sync. |
| LLM | `src/llm/` | Isolated behind `callLLM()`. Stubs when `LLM_API_KEY` is absent. |
| AI | `src/ai/` | LLM contract spec (`llm-contract.js`) and commands schema. |
| Data | `src/data/` | State storage (`storage.js`), schemas, mock data, fixture JSONs. |
| UI | `src/ui/` | React/Vite client. `App.jsx` → view components + `api-client.js`. |

### Key design decisions

- **Pure functions everywhere in `src/core/`** — no hidden state, no I/O. Every engine takes plain data, returns plain data. This is why Jest coverage targets only `src/core`.
- **State persisted as JSON** — `src/data/storage.js` reads/writes via `STATE_PATH` env var. State shape is enforced by `state-validator.js` and `validation/invariants.js`.
- **ESM only** — `"type": "module"` in package.json. All imports use `.js` extensions. No CommonJS.
- **LLM is a stub by default** — `callLLM()` returns a deterministic stub when `LLM_API_KEY` is unset. Tests don't need to mock it.
- **Team layer is optional** — pipeline accepts an optional `team` argument; all team engines (`team-model.js`, `team-identity-engine.js`, `team-governance-engine.js`) gracefully handle `undefined`.

### Behavioral control

`behavioral-control-engine.js` implements pacing mode selection (`stabilize` / `build` / `advance`) based on integrity score, pressure, and completion rate. The `portfolio-optimizer.js` and `cycle-governance.js` modules gate which tasks advance to the next cycle.

### Validation subsystem

`src/core/validation/` contains two modules:
- `invariants.js` — structural constraints that must always hold (checked on every write)
- `health.js` — aggregated advisory health signals surfaced at `/api/health`

### Scoring

`scoring-engine.js` computes an `integrityScore` (0–100) by weighting task outcomes by `estimatedImpact × difficultyWeight × timelinessWeight`. Missed tasks subtract from the raw total; pending tasks are excluded. This score feeds back into pacing mode and identity updates.
