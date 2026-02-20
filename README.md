# Technical Debt Negotiator 🔍💰

> An AI agent that ends PM-Engineer standoffs with data.
> Point it at your repos + Jira backlog → get a data-driven refactor-vs-feature recommendation.

---

## Quick Start

```bash
# 1. Install
pip install -r requirements.txt

# 2. Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Run the agent
python agent/agent.py \
  --repos payment-platform-tech-debt fraud-detection-model-techdebt \
  --jira  "https://yourco.atlassian.net/rest/api/3/search?jql=project=PLATFORM" \
  --jira-token "Bearer your_token"

# 4. Open the dashboard
open dashboard/index.html
```

---

## What It Does

The agent runs 5 sub-agents in sequence:

```
Jira Fetcher  →  Repo Scanner  →  Debt Analyzer (LLM)  →  Cost Model (LLM)  →  Negotiator (LLM)
     │                │                    │                       │                     │
  Fetches Jira     Reads all           Identifies 18+         Translates to         Recommends:
   backlog         repo files          debt patterns           dollar costs        Refactor or Build?
```

**Inputs:**
- `payment-platform-tech-debt/` — local repo directory
- `fraud-detection-model-techdebt/` — local repo directory
- Jira REST API URL — your feature backlog

**Output:**
- `output_analysis.json` — full structured analysis
- Interactive dashboard at `dashboard/index.html`

---

## Agent Architecture

### 1. RepoScannerAgent (no LLM)
- Walks repo directory, reads all code + config files
- Detects repo type: `swe`, `ml`, `data_pipeline`, `mixed`
- Returns structured file content for LLM analysis

### 2. JiraFetcherAgent (no LLM)
- Calls Jira REST API to fetch backlog tickets
- Falls back to demo data if Jira is unreachable
- Returns list of features with story points and priority

### 3. DebtAnalysisAgent (Claude API)
- Reads all repo files
- Identifies 18+ debt patterns across SWE, ML, data pipelines
- Returns JSON: debt items with location, description, severity

### 4. CostModelAgent (Claude API)
- Validates cost estimates using industry benchmarks
- Computes: `refactoring_cost`, `break_even_weeks`, `roi_year_1`
- Writes plain-English `cost_narrative` for PM audiences

### 5. NegotiationAgent (Claude API)
- Cross-references debt items against Jira features
- For each feature: which debt blocks it? What's the risk?
- Produces overall recommendation: `refactor_first` | `build_now`

---

## Dashboard

Open `dashboard/index.html` in any browser — no server needed.

**5 tabs:**
1. **Overview** — All debt items, costs by repo and severity
2. **By Repository** — Drill into each repo's specific debt
3. **Refactor vs Build** — The negotiation view with timeline chart
4. **Jira Features** — Each ticket assessed against existing debt
5. **How It Works** — Visual explainer of the agent architecture

The dashboard works with demo data out of the box (no API key needed to view).

---

## Sample Repositories

The agent is pre-configured for:
- `payment-platform-tech-debt` → SWE debt ($708K/year)
- `fraud-detection-model-techdebt` → ML debt ($1.4M/year)

Put these directories alongside this project folder, then run the agent.

---

## Debt Patterns Detected (18+)

**Software:** dependency_hell, god_library, god_class, security_vulnerability,
zombie_feature_flags, test_debt, hardcoded_logic, code_duplication

**ML/AI:** model_staleness, data_staleness, undocumented_features,
dead_model_versions, no_experiment_tracking, inference_bottleneck, framework_lockin

**Data Pipelines:** version_sprawl, storage_hoarding, no_batching, manual_backfills

---

## License
MIT
