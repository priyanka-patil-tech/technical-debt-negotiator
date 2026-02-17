---
name: techdebt-analyzer
description: Analyze codebases to identify technical debt patterns and quantify their business impact. Use when scanning repositories for SWE, ML, or data pipeline debt.
---

# Technical Debt Analyzer Skill

## Purpose
Scan repository files and return a structured JSON analysis of all technical debt found, with annual cost estimates and fix effort for each item.

## Debt Patterns to Detect

### Traditional Software (SWE) Debt
1. **dependency_hell** — Check package.json, pom.xml, requirements.txt for packages >2 years old
2. **god_library** — Module imported by >10 other files; blocks independent deployment
3. **god_class** — File >500 lines that handles too many responsibilities
4. **security_vulnerability** — Hardcoded credentials, SQL injection via f-strings, known CVEs (Log4j, etc.)
5. **zombie_feature_flags** — Feature flags from A/B tests that concluded >3 months ago
6. **test_debt** — Low or zero test coverage; manual QA required per release
7. **hardcoded_logic** — Business rules (pricing, thresholds) burned into source code
8. **code_duplication** — Same logic in multiple files; fixes must be applied N times

### ML/AI Debt
1. **model_staleness** — Training script last run >90 days ago (look for "Last run:" comments)
2. **data_staleness** — Training data files with dates >6 months old
3. **undocumented_features** — Feature names like feature_1, feature_22_v2, "Sarah's feature"
4. **dead_model_versions** — Multiple .pkl / .h5 / .pt files when only one is active
5. **no_experiment_tracking** — No MLflow, W&B, or similar import in training code
6. **inference_bottleneck** — Batch-only pipeline where real-time is needed; row-by-row DB writes
7. **framework_lockin** — TensorFlow 1.x, old PyTorch, scikit-learn <0.24 blocking modern tools

### Data Pipeline Debt
1. **version_sprawl** — Multiple versions of same script (v1, v2, final, final_v2, actually_final)
2. **storage_hoarding** — Buckets/folders named with years >2 years ago; no retention policy
3. **no_batching** — Kafka consumer commits per-message; Spark job loads entire history daily
4. **manual_backfills** — Comments about running scripts manually; hardcoded date ranges

## Cost Calculation Rules

```python
# dependency_hell
annual_cost = blocked_feature_count * 50000  # $50K per blocked feature

# god_library
affected_services = import_count
annual_cost = affected_services * 3 * 52 * 1000  # 3 extra days/deploy * 52 deploys * $1K/day

# model_staleness
days_stale = (today - last_training_date).days
accuracy_drop = min(0.18, days_stale / 1000)
annual_cost = monthly_transactions * fraud_rate * avg_amount * accuracy_drop * 12

# dead_model_versions
extra_models = count - 1
annual_cost = extra_models * 800 * 12  # $800/month each

# no_batching
wasted_hours = actual_runtime - optimal_runtime  # e.g. 14h - 2h = 12h
annual_cost = wasted_hours * cluster_hourly_rate * 365
```

## Output Format

Return ONLY valid JSON (no prose before or after):

```json
{
  "repository": "payment-platform",
  "repo_type": "swe",
  "debt_items": [
    {
      "id": 1,
      "type": "god_library",
      "severity": "critical",
      "location": "services/shared-commons/",
      "description": "Imported by 23 services — any change forces full system redeploy",
      "business_impact": "3-week deploy cycles instead of daily; blocks all 23 teams",
      "annual_cost": 268000,
      "fix_effort_weeks": 3
    }
  ],
  "total_annual_cost": 708000,
  "refactoring_effort_weeks": 7,
  "health_score": 38,
  "cost_narrative": "2-3 sentences in plain English for a PM"
}
```

## Severity Rules
- **critical**: Immediate, ongoing business impact ($100K+/yr or security/compliance risk)
- **high**: Significant impact ($30K–$99K/yr or blocks multiple features)
- **medium**: Notable but manageable ($5K–$29K/yr)

## Instructions for Claude
1. Read every file in the repository
2. Check PRIORITY_FILES first (pom.xml, requirements.txt, package.json)
3. Look for ALL patterns above — don't stop after finding one
4. Reference specific file names and line numbers in `location`
5. Write `business_impact` in language a PM understands (no jargon)
6. Be specific with costs — use the formulas above
7. Return ONLY the JSON block, nothing else
