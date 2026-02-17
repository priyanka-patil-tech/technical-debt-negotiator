"""
Technical Debt Negotiator — Main Agent
========================================
Orchestrates 5 sub-agents in sequence:
  1. RepoScannerAgent    → reads repo files
  2. JiraFetcherAgent    → fetches Jira backlog
  3. DebtAnalysisAgent   → Claude API: identifies debt patterns
  4. CostModelAgent      → Claude API: translates to dollars
  5. NegotiationAgent    → Claude API: refactor vs feature decision

Usage:
    python agent/run.py \
        --repos payment-platform-tech-debt fraud-detection-model-techdebt \
        --jira  https://yourcompany.atlassian.net/rest/api/3/search?jql=project=PLATFORM \
        --jira-token "Bearer your_token_here"
"""

import os, json, asyncio, re, argparse
from datetime import datetime
from pathlib import Path
import anthropic

# ─── CONFIG ────────────────────────────────────────────────────────────────
CLAUDE_MODEL   = "claude-sonnet-4-5-20250929"
TEAM_SIZE      = 5
WEEKLY_RATE    = 10_000   # $ per engineer per week

# ─── HELPER ────────────────────────────────────────────────────────────────
def call_claude(client: anthropic.Anthropic, system: str, user: str) -> str:
    """Single Claude API call — returns text content."""
    response = client.messages.create(
        model      = CLAUDE_MODEL,
        max_tokens = 4096,
        system     = system,
        messages   = [{"role": "user", "content": user}],
    )
    return response.content[0].text

def extract_json(text: str) -> dict | list:
    """Pull first JSON block out of Claude response."""
    match = re.search(r"```(?:json)?\s*([\s\S]+?)```", text)
    raw   = match.group(1) if match else text
    return json.loads(raw)

# ═══════════════════════════════════════════════════════════════════════════
# 1. REPO SCANNER AGENT
# ═══════════════════════════════════════════════════════════════════════════
class RepoScannerAgent:
    """
    Walks a local repo directory and collects text content from key files.
    Returns a structured dict with file contents ready for LLM analysis.
    """
    INCLUDE_EXT  = {".py",".java",".js",".ts",".yaml",".yml",
                    ".json",".xml",".txt",".md",".properties",".sh"}
    SKIP_DIRS    = {"node_modules","__pycache__",".git","venv","dist","build"}
    PRIORITY     = {"pom.xml","package.json","requirements.txt",
                    "build.gradle","Dockerfile","docker-compose.yml"}
    MAX_FILE_KB  = 20
    MAX_TOTAL_KB = 150

    def scan(self, repo_path: str) -> dict:
        path = Path(repo_path)
        if not path.exists():
            return {"repository": repo_path, "error": f"Path not found: {repo_path}", "files": []}

        print(f"  📂  Scanning  {path.name} …")
        files, total_kb, langs = [], 0, {}

        # priority files first
        for name in self.PRIORITY:
            fp = path / name
            if fp.exists():
                r = self._read(fp, path)
                if r:
                    files.append(r); total_kb += r["kb"]
                    langs[r["lang"]] = langs.get(r["lang"], 0) + 1

        # rest of repo
        for root, dirs, names in os.walk(path):
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            for n in names:
                if total_kb > self.MAX_TOTAL_KB: break
                fp = Path(root) / n
                if fp.name in self.PRIORITY or fp.suffix.lower() not in self.INCLUDE_EXT:
                    continue
                r = self._read(fp, path)
                if r:
                    files.append(r); total_kb += r["kb"]
                    langs[r["lang"]] = langs.get(r["lang"], 0) + 1

        repo_type = self._detect(path, files)
        print(f"      ✓  {len(files)} files | {sum(f['lines'] for f in files):,} lines | type={repo_type}")
        return {
            "repository": path.name,
            "repo_path":  str(path),
            "repo_type":  repo_type,
            "files":      files,
            "metadata":   {"file_count": len(files), "languages": langs,
                           "total_kb": round(total_kb, 1)},
        }

    def _read(self, fp: Path, base: Path) -> dict | None:
        try:
            raw     = fp.read_bytes()[: self.MAX_FILE_KB * 1024]
            content = raw.decode("utf-8", errors="replace")
            return {"path": str(fp.relative_to(base)), "content": content,
                    "lines": content.count("\n"), "kb": len(raw)/1024,
                    "lang": fp.suffix.lstrip(".")}
        except Exception:
            return None

    def _detect(self, path: Path, files: list) -> str:
        names   = {f["path"].lower() for f in files}
        content = " ".join(f["content"][:500] for f in files)
        is_ml   = any(x in content for x in ["tensorflow","sklearn","torch","model.pkl","feature_engineering"])
        is_pipe = any(x in content for x in ["airflow","kafka","spark","pyspark","dag"])
        is_swe  = any(x in names for x in {"pom.xml","package.json","build.gradle"})
        if is_ml and is_pipe: return "mixed"
        if is_ml:   return "ml"
        if is_pipe: return "data_pipeline"
        return "swe"


# ═══════════════════════════════════════════════════════════════════════════
# 2. JIRA FETCHER AGENT
# ═══════════════════════════════════════════════════════════════════════════
class JiraFetcherAgent:
    """
    Fetches feature tickets from a Jira REST API URL.
    Falls back to mock data if URL is unreachable or empty.
    """
    def fetch(self, jira_url: str, token: str = "") -> dict:
        print(f"  🎫  Fetching Jira backlog …")
        try:
            import urllib.request
            req = urllib.request.Request(jira_url)
            if token:
                req.add_header("Authorization", token)
            req.add_header("Accept", "application/json")
            with urllib.request.urlopen(req, timeout=8) as resp:
                data     = json.loads(resp.read())
                features = self._parse(data)
                print(f"      ✓  {len(features)} tickets fetched from Jira")
                return {"source": "jira_live", "features": features}
        except Exception as e:
            print(f"      ⚠  Jira unreachable ({e}), using demo data")
            return {"source": "demo", "features": self._mock()}

    def _parse(self, data: dict) -> list:
        issues = data.get("issues", [])
        out = []
        for i in issues:
            f = i.get("fields", {})
            out.append({
                "key":          i.get("key",""),
                "summary":      f.get("summary",""),
                "story_points": f.get("customfield_10000") or f.get("story_points", 3),
                "priority":     f.get("priority",{}).get("name","Medium"),
                "description":  (f.get("description") or "")[:400],
                "status":       f.get("status",{}).get("name","Backlog"),
            })
        return out

    def _mock(self) -> list:
        return [
            {"key":"PLAT-101","summary":"Add real-time fraud alerts",
             "story_points":8,"priority":"High","status":"Backlog",
             "description":"Product wants real-time fraud detection instead of nightly batch."},
            {"key":"PLAT-102","summary":"Dynamic pricing engine",
             "story_points":13,"priority":"Critical","status":"Backlog",
             "description":"Flash sales require pricing changes without code deploy."},
            {"key":"PLAT-103","summary":"Personalized recommendations",
             "story_points":8,"priority":"High","status":"Backlog",
             "description":"Requires refactoring ML pipeline and upgrading TensorFlow."},
            {"key":"PLAT-104","summary":"Upgrade payment gateway to Stripe v3",
             "story_points":5,"priority":"Medium","status":"Backlog",
             "description":"Blocked by outdated dependencies in shared-commons library."},
            {"key":"PLAT-105","summary":"Customer churn predictor",
             "story_points":13,"priority":"High","status":"Backlog",
             "description":"New ML feature. Blocked by fragile existing ML pipeline."},
        ]


# ═══════════════════════════════════════════════════════════════════════════
# 3. DEBT ANALYSIS AGENT  (LLM-powered)
# ═══════════════════════════════════════════════════════════════════════════
DEBT_ANALYSIS_SYSTEM = """
You are an expert software engineering consultant specializing in technical debt analysis.
Analyze repository files and identify technical debt patterns.

DEBT PATTERNS TO DETECT:

SOFTWARE DEBT:
- dependency_hell: outdated packages blocking features (flag >2yr old)
- god_library: single module imported by many services (>10 files)
- god_class: files >500 lines that should be split
- security_vulnerability: hardcoded credentials, SQL injection, known CVEs
- zombie_feature_flags: old A/B test flags never cleaned up
- test_debt: low test coverage causing manual QA cycles
- hardcoded_logic: business rules in source code (pricing, thresholds)
- code_duplication: same logic in multiple places

ML DEBT:
- model_staleness: model not retrained in >90 days (accuracy degrading)
- data_staleness: training data >6 months old
- undocumented_features: magic feature names like feature_22, feature_v3_final
- dead_model_versions: multiple .pkl/.h5 files when only one needed
- no_experiment_tracking: no MLflow/W&B imports in training scripts
- inference_bottleneck: batch-only pipeline where real-time needed
- framework_lockin: old TF/torch versions blocking modern tools

DATA PIPELINE DEBT:
- version_sprawl: multiple versions of same DAG/script
- storage_hoarding: old S3/data buckets never cleaned
- no_batching: row-by-row DB operations
- manual_backfills: comments about running scripts manually

OUTPUT RULES:
- Return ONLY valid JSON, no markdown prose around it
- Be specific: reference actual file names and line content
- Severity: "critical" (immediate business impact), "high" (significant), "medium" (notable)
- Cost estimates should be annual in USD

Return this exact JSON structure:
{
  "repository": "repo-name",
  "repo_type": "swe|ml|data_pipeline|mixed",
  "debt_items": [
    {
      "id": 1,
      "type": "debt_type_slug",
      "severity": "critical|high|medium",
      "location": "filename:line or folder/",
      "description": "Clear 1-sentence description of the problem",
      "business_impact": "Plain English: what this costs the business",
      "annual_cost": 150000,
      "fix_effort_weeks": 2
    }
  ],
  "total_annual_cost": 708000,
  "refactoring_effort_weeks": 7,
  "health_score": 35
}
"""

class DebtAnalysisAgent:
    """Uses Claude API to identify technical debt patterns from scanned files."""

    def __init__(self, client: anthropic.Anthropic):
        self.client = client

    def analyze(self, scan_data: dict) -> dict:
        if scan_data.get("error"):
            return {"repository": scan_data["repository"], "debt_items": [],
                    "total_annual_cost": 0, "refactoring_effort_weeks": 0, "health_score": 100}

        repo  = scan_data["repository"]
        rtype = scan_data.get("repo_type", "swe")
        print(f"  🔍  Analyzing debt in {repo} ({rtype}) via Claude …")

        # Build file digest
        digest_parts = []
        for f in scan_data["files"][:30]:   # cap at 30 files
            digest_parts.append(f"=== {f['path']} ===\n{f['content'][:3000]}")
        digest = "\n\n".join(digest_parts)

        prompt = f"""
Repository: {repo}  (type: {rtype})

FILES:
{digest}

Analyze ALL files above for technical debt. Be thorough — check every file.
Return the JSON analysis as specified.
"""
        raw    = call_claude(self.client, DEBT_ANALYSIS_SYSTEM, prompt)
        result = extract_json(raw)

        if isinstance(result, dict):
            result.setdefault("repository", repo)
            result.setdefault("repo_type", rtype)
            n = len(result.get("debt_items", []))
            print(f"      ✓  {n} debt items found, annual cost ${result.get('total_annual_cost',0):,}")
            return result

        return {"repository": repo, "repo_type": rtype, "debt_items": [],
                "total_annual_cost": 0, "refactoring_effort_weeks": 0, "health_score": 80}


# ═══════════════════════════════════════════════════════════════════════════
# 4. COST MODEL AGENT  (LLM-powered)
# ═══════════════════════════════════════════════════════════════════════════
COST_MODEL_SYSTEM = """
You are a financial analyst specializing in software engineering ROI.
Given technical debt items, validate and enrich their cost estimates using
industry benchmarks (DORA metrics, State of DevOps reports, case studies from
Netflix, LinkedIn, Airbnb, Spotify).

For each debt item, ensure the annual_cost reflects:
- Direct costs: infrastructure waste, cloud over-spend, security incident risk
- Productivity costs: engineer time wasted per week × team size × rate
- Opportunity costs: blocked features × estimated feature value
- Risk costs: probability of incident × estimated incident cost

Also compute:
- refactoring_cost = total fix weeks × team_size × weekly_rate
- annual_savings   = total_annual_cost (what is saved post-fix)
- break_even_weeks = ceil(refactoring_cost / (annual_savings / 52))
- roi_year_1       = (annual_savings - refactoring_cost) / refactoring_cost * 100

Return ONLY valid JSON:
{
  "repository": "...",
  "debt_items": [ ...same items with validated costs... ],
  "total_annual_cost": 0,
  "refactoring_effort_weeks": 0,
  "refactoring_cost": 0,
  "annual_savings": 0,
  "break_even_weeks": 0,
  "roi_year_1": 0,
  "health_score": 0,
  "cost_narrative": "2-3 sentence plain English summary for a PM"
}
"""

class CostModelAgent:
    """Validates and enriches cost estimates using Claude."""

    def __init__(self, client: anthropic.Anthropic):
        self.client = client

    def compute(self, analysis: dict, team_size: int = 5, weekly_rate: int = 10_000) -> dict:
        repo = analysis.get("repository", "unknown")
        print(f"  💰  Computing cost model for {repo} …")

        prompt = f"""
Team size: {team_size} engineers
Weekly rate per engineer: ${weekly_rate:,}

Debt analysis to validate:
{json.dumps(analysis, indent=2)}

Validate each debt item's annual_cost using industry benchmarks.
Compute refactoring_cost, break_even_weeks, and roi_year_1.
Write a cost_narrative that a non-technical PM can understand.
Return enriched JSON.
"""
        raw    = call_claude(self.client, COST_MODEL_SYSTEM, prompt)
        result = extract_json(raw)
        if isinstance(result, dict):
            print(f"      ✓  Break-even week {result.get('break_even_weeks','?')}, ROI {result.get('roi_year_1','?')}%")
            return result
        return analysis


# ═══════════════════════════════════════════════════════════════════════════
# 5. NEGOTIATION AGENT  (LLM-powered)
# ═══════════════════════════════════════════════════════════════════════════
NEGOTIATION_SYSTEM = """
You are a technical advisor helping engineering and product teams make
data-driven decisions about whether to refactor technical debt first or
build new features immediately.

Given:
- Technical debt analyses from one or more repositories
- A Jira backlog of planned features

For EACH Jira feature, assess:
1. Is it BLOCKED or SLOWED by existing debt? Which items?
2. What is the risk of building it NOW on the current codebase?
3. What is the recommended path?

Then produce an overall recommendation.

Return ONLY valid JSON:
{
  "overall_recommendation": "refactor_first|build_now|partial_refactor",
  "recommendation_reason": "2-3 plain-English sentences",
  "health_score": 42,
  "break_even_weeks": 19,
  "option_a": {
    "label": "Build Features Now",
    "total_weeks": 8,
    "success_rate": 35,
    "risk_level": "high",
    "risks": ["65% regression risk", "ML pipeline blocks real-time features"],
    "ongoing_monthly_cost": 23000
  },
  "option_b": {
    "label": "Refactor First, Then Build",
    "refactor_weeks": 7,
    "feature_weeks": 4,
    "total_weeks": 11,
    "success_rate": 92,
    "risk_level": "low",
    "benefits": ["Daily deploys enabled", "ML pipeline supports real-time"],
    "annual_savings": 268000
  },
  "feature_analysis": [
    {
      "key": "PLAT-101",
      "summary": "Add real-time fraud alerts",
      "blocked_by": ["inference_bottleneck", "model_staleness"],
      "risk_if_built_now": "high",
      "recommendation": "refactor_first",
      "reasoning": "Real-time alerts require ML pipeline upgrade. Building now = 3x longer dev."
    }
  ]
}
"""

class NegotiationAgent:
    """Produces the refactor-vs-feature recommendation using Claude."""

    def __init__(self, client: anthropic.Anthropic):
        self.client = client

    def decide(self, analyses: list[dict], jira_data: dict,
                team_size: int = 5, weekly_rate: int = 10_000) -> dict:
        print(f"  ⚖️   Running negotiation engine …")

        prompt = f"""
Team: {team_size} engineers at ${weekly_rate:,}/week each

DEBT ANALYSES (all repos combined):
{json.dumps(analyses, indent=2)[:6000]}

JIRA BACKLOG:
{json.dumps(jira_data.get('features', []), indent=2)}

Produce the negotiation recommendation JSON.
"""
        raw    = call_claude(self.client, NEGOTIATION_SYSTEM, prompt)
        result = extract_json(raw)
        if isinstance(result, dict):
            rec = result.get("overall_recommendation","?")
            print(f"      ✓  Recommendation: {rec}")
            return result
        return {"overall_recommendation": "refactor_first",
                "recommendation_reason": "Could not determine recommendation.",
                "option_a": {}, "option_b": {}, "feature_analysis": []}


# ═══════════════════════════════════════════════════════════════════════════
# ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════
class TechDebtNegotiatorAgent:
    """Runs all 5 sub-agents in order and returns final payload."""

    def __init__(self, api_key: str = ""):
        key = api_key or os.environ.get("ANTHROPIC_API_KEY", "")
        self.client       = anthropic.Anthropic(api_key=key)
        self.scanner      = RepoScannerAgent()
        self.jira_fetcher = JiraFetcherAgent()
        self.analyzer     = DebtAnalysisAgent(self.client)
        self.cost_model   = CostModelAgent(self.client)
        self.negotiator   = NegotiationAgent(self.client)

    def run(self, repos: list[str], jira_url: str,
            jira_token: str = "", team_size: int = TEAM_SIZE,
            weekly_rate: int = WEEKLY_RATE) -> dict:

        print("\n╔══════════════════════════════════════════╗")
        print("║  TECHNICAL DEBT NEGOTIATOR  v1.0         ║")
        print("╚══════════════════════════════════════════╝")
        print(f"  Repos : {repos}")
        print(f"  Jira  : {jira_url}\n")

        # Stage 1 — Scan repos + fetch Jira (fast, no LLM)
        print("▶ Stage 1 — Input Gathering")
        scan_results = [self.scanner.scan(r) for r in repos]
        jira_data    = self.jira_fetcher.fetch(jira_url, jira_token)

        # Stage 2 — LLM debt analysis per repo
        print("\n▶ Stage 2 — LLM Debt Analysis")
        analyses = [self.analyzer.analyze(s) for s in scan_results]

        # Stage 3 — Cost modelling
        print("\n▶ Stage 3 — Cost Modelling")
        costed = [self.cost_model.compute(a, team_size, weekly_rate) for a in analyses]

        # Stage 4 — Negotiation decision
        print("\n▶ Stage 4 — Negotiation Engine")
        negotiation = self.negotiator.decide(costed, jira_data, team_size, weekly_rate)

        # Assemble final payload
        all_items = [item for a in costed for item in a.get("debt_items", [])]
        total_cost = sum(a.get("total_annual_cost", 0) for a in costed)
        payload = {
            "generated_at": datetime.now().isoformat(),
            "repositories": [a["repository"] for a in costed],
            "summary": {
                "total_debt_items":         len(all_items),
                "critical":                 sum(1 for i in all_items if i.get("severity") == "critical"),
                "high":                     sum(1 for i in all_items if i.get("severity") == "high"),
                "medium":                   sum(1 for i in all_items if i.get("severity") == "medium"),
                "total_annual_cost":        total_cost,
                "refactoring_effort_weeks": sum(a.get("refactoring_effort_weeks", 0) for a in costed),
                "break_even_weeks":         negotiation.get("break_even_weeks", 0),
                "health_score":             negotiation.get("health_score", 50),
            },
            "repositories_analysis": costed,
            "jira_features":         jira_data.get("features", []),
            "negotiation":           negotiation,
        }

        print(f"\n╔══════════════════════════════════════════╗")
        print(f"║  COMPLETE  —  ${total_cost:,} annual debt found")
        print(f"╚══════════════════════════════════════════╝\n")

        out_path = Path("output_analysis.json")
        out_path.write_text(json.dumps(payload, indent=2))
        print(f"  Results saved → {out_path}\n")
        return payload


# ─── CLI ENTRY POINT ────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Technical Debt Negotiator Agent")
    parser.add_argument("--repos",       nargs="+", required=True,
                        help="Paths to repo directories")
    parser.add_argument("--jira",        default="",
                        help="Jira REST API URL")
    parser.add_argument("--jira-token",  default="",
                        help="Jira auth token (Bearer ...)")
    parser.add_argument("--team-size",   type=int, default=TEAM_SIZE)
    parser.add_argument("--weekly-rate", type=int, default=WEEKLY_RATE)
    parser.add_argument("--api-key",     default="",
                        help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
    args = parser.parse_args()

    agent  = TechDebtNegotiatorAgent(api_key=args.api_key)
    result = agent.run(
        repos       = args.repos,
        jira_url    = args.jira,
        jira_token  = getattr(args, "jira_token", ""),
        team_size   = args.team_size,
        weekly_rate = args.weekly_rate,
    )
    print(json.dumps(result["summary"], indent=2))
