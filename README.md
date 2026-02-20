# Tech Debt Negotiator

> An AI-powered tool that ends PM–Engineer standoffs with data.
> Point it at your repositories and Jira backlog → get a data-driven **Refactor First vs Build Now** recommendation.

**Live demo:** [GitHub Pages](https://priyanka-patil-tech.github.io/technical-debt-negotiator/)

---

## What Problem It Solves

Engineering teams and product managers frequently disagree on whether to pay down technical debt or ship new features. This argument usually stalls without hard numbers. Tech Debt Negotiator breaks the deadlock by:

1. Scanning your codebase for 18+ debt patterns
2. Translating each issue into an annual dollar cost
3. Cross-referencing debt against your JIRA backlog to see which features are blocked
4. Running a negotiation model that compares both paths (build now vs refactor first) with timelines, success rates, and ROI

The output is a recommendation that both a PM and an engineer can act on.

---

## Repository Structure

```
technical-debt-negotiator/
├── index.html              ← Interactive demo (single-file React app, GitHub Pages)
├── agent/
│   └── agent.py            ← Python backend: 5-agent pipeline using Claude API
├── analyzers/
│   └── code_analyzer.py    ← Standalone static code analyzer (no LLM required)
├── requirements.txt
└── README.md
```

---

## Part 1 — Interactive Demo (`index.html`)

The demo is a single-file React application hosted on GitHub Pages. No server, no build step, no API key needed to view it.

### Supported Products

The demo ships with two pre-loaded products. Use the product selector on step 1 to switch between them — the entire analysis resets and reloads for the selected product.

| Product | Stack | Annual Debt Cost | Debt Items |
|---|---|---|---|
| Fraud Detection ML Platform | Python / FastAPI / Airflow / Spark | ~$2.56M | 10 items across 3 repos |
| Payment Platform | Java / Spring Boot | ~$1.47M | 8 items across 1 repo |

Switching products resets: phase, selected JIRA ticket, repository scan, debt selection, cost model, and negotiation output.

---

### Demo Flow — 6 Steps

The demo walks through the same sequence that the backend agent runs, one step at a time. A stepper at the top of the page shows your position.

```
Step 1        Step 2        Step 3        Step 4        Step 5        Step 6
JIRA Backlog → Repository  → Debt Analysis → Cost Model → Negotiation → Report
```

---

#### Step 1 — JIRA Backlog

**What you see:**
- Product selector (2 cards): choose Fraud Detection ML Platform or Payment Platform
- Phase header with the JIRA project ID and name (e.g. `ML-1401 — Fraud Detection ML Platform`)
- An editable JIRA backlog URL input — paste your own backlog URL or use the pre-loaded one
- An **Open ↗** link that opens the backlog URL in a new tab

**On clicking "Load JIRA Backlog":**
- The agent log simulates connecting to JIRA Cloud, authenticating via OAuth, and querying the backlog with a JQL filter for tech-debt-labelled tickets
- Once loaded, a 2-column card grid shows the backlog tickets

**JIRA ticket cards show:**
- Ticket key (e.g. `ML-1401`)
- Title in plain English (not tech jargon)
- Priority badge: `critical` (red) / `high` (amber) / `medium` (blue)
- Story points
- A deep-link to the actual JIRA issue

**Behaviour:** Click any ticket card to select it. This traces the ticket to its linked repository and advances to Step 2.

---

#### Step 2 — Repository

**What you see:**
- The repository linked to the selected JIRA ticket
- Repository metadata: name, description, language/stack, file count, last commit
- A read-only GitHub URL field

**On clicking "Scan Repositories":**
- The agent log simulates Claude reading all files in the repository
- Pattern detection runs (god classes, batch pipelines, missing registries, etc.)
- Advances automatically to Step 3 once complete

---

#### Step 3 — Debt Analysis

**What you see:**
- All debt items found in the selected repository
- Each item shows:
  - Severity pill: `critical` / `high` / `medium`
  - Debt type label (plain English, e.g. "Batch-Only Pipeline", "God Commons Library")
  - Description in non-technical language — explains *what it means for the business*, not the code
  - Annual cost if left unfixed (e.g. `$520,000/yr`)
  - Estimated weeks to fix

**Behaviour:**
- All debt items are pre-selected by default (checkboxes)
- Uncheck any item to exclude it from the cost calculation
- A running total of selected annual cost is shown in the header
- Click "Calculate Effort & Cost" to advance to Step 4

---

#### Step 4 — Cost Model

**What you see:**
- 6 KPI boxes computed from the selected debt items:

| KPI | What It Means |
|---|---|
| Refactoring Cost | Total engineer cost to fix selected items (weeks × 4 engineers × $8K/week) |
| Annual Savings | Sum of annual costs for all selected debt items — eliminated after fixing |
| Break-Even | The week at which cumulative savings exceed the refactoring investment |
| First-Year ROI | `(annual_savings − refactoring_cost) / refactoring_cost × 100` |
| Critical Issues | Count of critical-severity items in selection |
| Prod Risk (Build Now) | Fixed at 65% — probability of regression if you ship without fixing the debt |

**Behaviour:** Click "Run Negotiations" to advance to Step 5.

---

#### Step 5 — Negotiation

**What you see:**
- Side-by-side comparison of two options:

**Option A — Build Features Now** (shown in red)

| Field | Value |
|---|---|
| Timeline | 16 weeks (promise) |
| Success Rate | 35% |
| Risk | HIGH |
| Regression Risk | 65% |
| Ongoing Cost | $23K/month |
| Break-Even | Never (costs grow) |

Followed by product-specific bullet points showing what happens if you do not fix the debt first (e.g. for Fraud Detection: alerts stay delayed 5+ min, model accuracy stuck at 67%).

**Option B — Refactor First, Then Build** (shown in green)

| Field | Value |
|---|---|
| Refactor | 12 weeks |
| Feature Build | 4 weeks |
| Total | 16 weeks |
| Success Rate | 92% |
| Risk | LOW |
| Break-Even | Computed from cost model |

Followed by product-specific bullet points showing what is unlocked after fixing the debt.

**Agent Recommendation box** includes:
- The recommendation text (generated from the negotiation run)
- A 2×2 tradeoff grid covering: success rate gap, realistic timelines, what happens if Option A fails, and first-year net gain
- A "Why This Is a Clear Call, Not a Close Call" confidence section that explains the 57-point gap between Option A (35%) and Option B (92%) success rates, and why Option A's 8-week estimate becomes 16+ weeks in practice

**Behaviour:** Click "View Final Dashboard" to advance to Step 6.

---

#### Step 6 — Report

**What you see:**
- 5 summary KPIs: Annual Debt Cost, Refactoring Investment, Break-Even week, First-Year ROI, Features Unblocked
- Final recommendation title and narrative (product-specific)
- Full list of selected debt items with severity, type, description, annual cost, and fix duration
- A visual summary of all 5 agent stages completed

---

### Agent Log Panel

A collapsible log panel on the right side of the screen captures every agent action in real time:
- JIRA authentication and query
- Per-ticket tracing to repository
- File scanning progress
- Debt item discovery with cost
- Cost model calculations
- Negotiation engine output

Click the panel to expand/collapse. The badge shows the log line count.

---

## Part 2 — Backend Agent Pipeline (`agent/agent.py`)

The Python backend runs the same analysis non-interactively against real repositories and a live JIRA API. It uses the Anthropic Claude API for the three LLM-powered stages.

### Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-...

# 3. Run against your repos and JIRA backlog
python agent/agent.py \
  --repos payment-platform-tech-debt fraud-detection-model-techdebt \
  --jira  "https://yourco.atlassian.net/rest/api/3/search?jql=project=PLATFORM" \
  --jira-token "Bearer your_token"

# 4. Output is written to output_analysis.json
```

### CLI Arguments

| Argument | Required | Default | Description |
|---|---|---|---|
| `--repos` | Yes | — | One or more local repo directory paths |
| `--jira` | No | `""` | Jira REST API search URL with JQL |
| `--jira-token` | No | `""` | Auth token (`Bearer your_token`) |
| `--team-size` | No | `5` | Number of engineers for cost model |
| `--weekly-rate` | No | `10000` | Engineer cost per week in USD |
| `--api-key` | No | env var | Anthropic API key (or set `ANTHROPIC_API_KEY`) |

---

### Agent Pipeline — 5 Stages

```
Stage 1 (no LLM)          Stage 2 (no LLM)
  Repo Scanner         +    Jira Fetcher
       │                        │
       └──────────┬─────────────┘
                  ▼
          Stage 3 — Debt Analysis Agent (Claude)
                  │
                  ▼
          Stage 4 — Cost Model Agent (Claude)
                  │
                  ▼
          Stage 5 — Negotiation Agent (Claude)
                  │
                  ▼
          output_analysis.json
```

---

#### Stage 1 — RepoScannerAgent (no LLM)

Walks each local repository directory and collects file content for LLM analysis.

**File selection rules:**
- Included extensions: `.py`, `.java`, `.js`, `.ts`, `.yaml`, `.yml`, `.json`, `.xml`, `.txt`, `.md`, `.properties`, `.sh`
- Skipped directories: `node_modules`, `__pycache__`, `.git`, `venv`, `dist`, `build`
- Priority files read first: `pom.xml`, `package.json`, `requirements.txt`, `build.gradle`, `Dockerfile`, `docker-compose.yml`
- Per-file cap: 20 KB
- Total repo cap: 150 KB

**Repository type detection:**

| Type | Detection Signal |
|---|---|
| `ml` | `tensorflow`, `sklearn`, `torch`, `model.pkl`, `feature_engineering` |
| `data_pipeline` | `airflow`, `kafka`, `spark`, `pyspark`, `dag` |
| `swe` | `pom.xml`, `package.json`, `build.gradle` |
| `mixed` | Both ML and pipeline signals present |

**Output:** Structured dict with file contents, language breakdown, and repo type — ready to pass to the LLM.

---

#### Stage 2 — JiraFetcherAgent (no LLM)

Fetches backlog tickets from a Jira REST API endpoint.

**Behaviour:**
- Makes an authenticated HTTP GET to the provided Jira URL
- Extracts: ticket key, summary, story points, priority, description, status
- If Jira is unreachable or the URL is empty, falls back to 5 built-in demo tickets automatically

**Output:** List of feature tickets with story points and priority.

---

#### Stage 3 — DebtAnalysisAgent (Claude API)

Sends the scanned repository files to Claude with a structured system prompt. Claude identifies debt patterns and returns a JSON array of debt items.

**Debt patterns detected:**

*Software Engineering:*
- `dependency_hell` — outdated packages (>2 years old) blocking features
- `god_library` — single module imported by 10+ services
- `god_class` — files over 500 lines that should be split
- `security_vulnerability` — hardcoded credentials, SQL injection risks, known CVEs
- `zombie_feature_flags` — old A/B test flags never removed
- `test_debt` — low test coverage causing manual QA cycles
- `hardcoded_logic` — business rules (pricing, thresholds) in source code
- `code_duplication` — same logic repeated in multiple places

*ML / AI:*
- `model_staleness` — model not retrained in >90 days
- `data_staleness` — training data older than 6 months
- `undocumented_features` — magic feature names like `feature_22`, `feature_v3_final`
- `dead_model_versions` — multiple `.pkl` / `.h5` files when only one is active
- `no_experiment_tracking` — no MLflow or Weights & Biases usage in training scripts
- `inference_bottleneck` — batch-only pipeline where real-time processing is needed
- `framework_lockin` — old TensorFlow/PyTorch versions blocking modern tooling

*Data Pipelines:*
- `version_sprawl` — multiple versions of the same DAG or ETL script
- `storage_hoarding` — old S3 buckets or data folders never cleaned up
- `no_batching` — row-by-row database operations instead of bulk inserts
- `manual_backfills` — comments in code about running scripts manually

**Output per debt item:** `id`, `type`, `severity`, `location`, `description`, `business_impact`, `annual_cost`, `fix_effort_weeks`

---

#### Stage 4 — CostModelAgent (Claude API)

Takes the raw debt analysis and validates / enriches the cost estimates against industry benchmarks (DORA metrics, State of DevOps reports, case studies from Netflix, LinkedIn, Airbnb, Spotify).

**Cost components per debt item:**
- **Direct costs** — infrastructure waste, cloud overspend, security incident risk
- **Productivity costs** — engineer time wasted per week × team size × rate
- **Opportunity costs** — blocked features × estimated feature value
- **Risk costs** — probability of incident × estimated incident cost

**Computed financial metrics:**

| Metric | Formula |
|---|---|
| `refactoring_cost` | total fix weeks × team size × weekly rate |
| `annual_savings` | sum of all debt item annual costs |
| `break_even_weeks` | `ceil(refactoring_cost / (annual_savings / 52))` |
| `roi_year_1` | `(annual_savings − refactoring_cost) / refactoring_cost × 100` |

**Output:** Enriched debt items with validated costs, all financial metrics, and a `cost_narrative` — a 2–3 sentence plain-English summary written for a non-technical PM.

---

#### Stage 5 — NegotiationAgent (Claude API)

Cross-references all debt items from all repositories against the JIRA feature backlog. For each JIRA ticket, Claude assesses which debt items block or slow it, the risk of building now, and the recommended path.

**Per-feature output:**
- `blocked_by` — list of debt type slugs that affect this feature
- `risk_if_built_now` — `high` / `medium` / `low`
- `recommendation` — `refactor_first` or `build_now`
- `reasoning` — plain-English sentence explaining the tradeoff

**Overall recommendation:** `refactor_first` | `build_now` | `partial_refactor`

**Option A vs Option B comparison:**

| | Option A: Build Now | Option B: Refactor First |
|---|---|---|
| Timeline | Feature weeks only (underestimate) | Refactor weeks + feature weeks |
| Success Rate | 35% (debt causes regression) | 92% |
| Risk | High | Low |
| Ongoing Cost | $23K/month compounding | Eliminated post-refactor |
| Break-Even | Never | Week N (computed) |

---

### Output File — `output_analysis.json`

```json
{
  "generated_at": "ISO timestamp",
  "repositories": ["repo-a", "repo-b"],
  "summary": {
    "total_debt_items": 18,
    "critical": 5,
    "high": 8,
    "medium": 5,
    "total_annual_cost": 2560000,
    "refactoring_effort_weeks": 39,
    "break_even_weeks": 19,
    "health_score": 35
  },
  "repositories_analysis": [ ... per-repo debt items and cost model ... ],
  "jira_features": [ ... tickets with blocking analysis ... ],
  "negotiation": {
    "overall_recommendation": "refactor_first",
    "recommendation_reason": "...",
    "option_a": { ... },
    "option_b": { ... },
    "feature_analysis": [ ... per-ticket assessment ... ]
  }
}
```

---

## Pre-loaded Sample Products

### Fraud Detection ML Platform

**Repositories:** `ml-inference-engine`, `training-orchestrator`, `feature-store-service`
**Stack:** Python / FastAPI / Airflow / Redis / Spark

| Debt Item | Severity | Annual Cost |
|---|---|---|
| Batch-Only Pipeline | Critical | $520,000 |
| No Safe Rollback | Critical | $380,000 |
| 15-Month-Old Training Data | Critical | $440,000 |
| Test Results Don't Match Production | High | $290,000 |
| One File Does Everything | High | $210,000 |
| Hardcoded Business Rules | High | $175,000 |
| Experiments Tracked in Spreadsheets | High | $185,000 |
| No Audit Trail for Model Inputs | Medium | $140,000 |
| Training Limited to One Machine | Medium | $120,000 |
| No Performance Monitoring | Medium | $95,000 |

**Total annual cost: ~$2.56M**

---

### Payment Platform

**Repository:** `payment-platform-tech-debt`
**Stack:** Java / Spring Boot

| Debt Item | Severity | Annual Cost |
|---|---|---|
| Hardcoded API Keys & Config Sprawl | Critical | $312,000 |
| God Commons Library | Critical | $268,000 |
| Log4Shell Vulnerability (CVE-2021-44228) | Critical | $240,000 |
| PaymentController Does Everything | High | $200,000 |
| 89 Dead Feature Flags on Every Payment | High | $150,000 |
| Four Payment Providers, Four Different Patterns | Medium | $120,000 |
| 800-Line Deploy Script With No Safety Net | Medium | $100,000 |
| Critical Knowledge Exists Only in Two People's Heads | Medium | $80,000 |

**Total annual cost: ~$1.47M**

---

## Design Decisions

**Why plain English descriptions?**
The tool is built for mixed audiences: PMs, engineers, and non-technical stakeholders. Every debt description is written to explain business impact, not code structure. The phrase "Batch-Only Pipeline" is immediately followed by an explanation that "fraud alerts take 5+ minutes" — something a PM understands without knowing what a batch pipeline is.

**Why a fixed 65% production risk?**
The 65% regression risk shown in Step 4 is a static industry benchmark based on DORA research for codebases with multiple critical-severity debt items. It is intentionally non-dynamic — it represents the risk class of the codebase, not a variable to be negotiated down by selecting fewer debt items.

**Why is Option B's total timeline the same as Option A?**
Option A promises to ship in fewer weeks, but the 65% regression rate means engineers spend the "saved" time on debugging, rollbacks, and rework. Option B takes longer upfront but delivers at 92% confidence with a predictable schedule. The dashboard makes this tradeoff explicit: Option A's 8-week promise becomes 16+ weeks in practice.

**Why a product selector instead of a single product?**
Different teams carry different types of debt. The product selector lets a presenter switch between an ML platform scenario and a payments platform scenario without reloading the page, making the demo reusable across different audiences.

---

## License

MIT
