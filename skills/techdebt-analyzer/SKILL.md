# Technical Debt Analyzer Skill

## Purpose
Analyze codebases to identify technical debt patterns and quantify their business impact using AI-powered pattern recognition.

---

## Overview

This skill helps Claude identify and quantify technical debt across three domains:
1. **Traditional Software** - Code quality, dependencies, architecture
2. **ML/AI Systems** - Model staleness, feature engineering, pipelines
3. **Data Pipelines** - Storage, processing, orchestration

---

## Usage

When analyzing a repository:

1. **Scan Files** - Use `view` tool to read key files
2. **Identify Patterns** - Match against debt patterns below
3. **Calculate Costs** - Use cost models to quantify impact
4. **Generate Report** - Output structured analysis

---

## Debt Patterns to Detect

### Traditional Software Debt (10 patterns)

#### 1. Outdated Dependencies
**Files to check:** `requirements.txt`, `package.json`, `pom.xml`, `Gemfile`

**Detection rules:**
```python
# Flag if package is >2 years old
if package_age_years > 2:
    severity = "high" if has_security_cve else "medium"
```

**Cost calculation:**
```python
# Estimate blocked features
blocked_features = count_incompatible_features()
annual_cost = blocked_features * 50000  # $50K per blocked feature

# Security risk
if has_critical_cve:
    annual_cost += 100000  # Mandatory security sprint
```

**Examples to flag:**
- TensorFlow 1.15 (from 2019, blocks modern ML tools)
- Log4j 1.2.17 (CVE-2021-44228, critical vulnerability)
- React 16 (current is 19, blocks features)

---

#### 2. God Libraries/Classes
**Files to check:** All source files

**Detection rules:**
```python
# God Library: Imported by many files
import_count = count_files_importing(library)
if import_count > 20:
    flag_as_god_library()

# God Class: File with >500 lines
if line_count > 500:
    flag_as_god_class()
```

**Cost calculation:**
```python
affected_services = import_count
deploy_delay_weeks = 3 if affected_services > 20 else 1
annual_cost = deploy_delay_weeks * 52 * 5 * 1000  # Team size * weeks * rate
```

**Examples to flag:**
- `shared-commons/` imported by 23 services
- `PaymentController.java` with 4,500 lines
- Any file with >100 functions

---

#### 3. Security Vulnerabilities
**Files to check:** All files, especially configs

**Detection rules:**
```python
# Hardcoded credentials
patterns = [
    r'password\s*=\s*["\'][\w!@#$%^&*]+["\']',
    r'api_key\s*=\s*["\'][A-Za-z0-9]+["\']',
    r'secret\s*=\s*["\'][A-Za-z0-9]+["\']',
]

# SQL injection
if 'f"SELECT' in code or 'f"INSERT' in code:
    flag_sql_injection_risk()
```

**Cost calculation:**
```python
if hardcoded_credentials:
    annual_cost = 100000  # Security breach risk

if sql_injection:
    annual_cost = 200000  # Data breach risk
```

---

#### 4. Zombie Feature Flags
**Files to check:** Config files, feature flag services

**Detection rules:**
```python
# Look for dated flag names
if re.search(r'(2019|2020|2021|2022).*test|experiment', flag_name):
    flag_as_zombie()

# Check flag file comments
if 'ended' in comment or 'concluded' in comment:
    flag_as_zombie()
```

**Cost calculation:**
```python
zombie_count = len(zombie_flags)
performance_impact_percent = min(0.15, zombie_count / 100)
monthly_compute_cost = 100000  # Typical compute budget
annual_cost = monthly_compute_cost * performance_impact_percent * 12
```

---

#### 5. Code Duplication
**Files to check:** All source files

**Detection rules:**
```python
# Look for similar function names
if function_name.endswith('_v1') and function_name + '_v2' exists:
    flag_duplication()

# Look for copy-paste comments
if 'same as' in comment or 'duplicate of' in comment:
    flag_duplication()
```

**Cost calculation:**
```python
# Bug fix requires updating multiple places
duplicate_locations = count_duplicates()
annual_cost = duplicate_locations * 20000  # Bugs from inconsistency
```

---

### ML/AI Debt (9 patterns)

#### 6. Model Staleness
**Files to check:** `train.py`, `*.ipynb`, training scripts

**Detection rules:**
```python
# Check for last training date in comments
match = re.search(r'Last (?:run|trained?):\s*(\d{4}-\d{2}-\d{2})', content)
if match:
    days_since = (today - last_training_date).days
    if days_since > 90:
        flag_model_staleness()
```

**Cost calculation:**
```python
# Accuracy degrades over time
days_since_training = (today - last_training_date).days
accuracy_degradation = min(0.18, days_since_training / 1000)

# Fraud detection example
monthly_transactions = 1000000
fraud_rate = 0.01
avg_fraud_amount = 500
monthly_missed_fraud = (
    monthly_transactions * fraud_rate * avg_fraud_amount * accuracy_degradation
)
annual_cost = monthly_missed_fraud * 12
```

---

#### 7. Data Staleness
**Files to check:** Data loading scripts, config files

**Detection rules:**
```python
# Check training data file dates
if re.search(r'training.*data.*(2019|2020|2021|2022|2023)', filename):
    flag_data_staleness()

# Check comments about data age
if re.search(r'data (?:from|since) (Q\d \d{4})', content):
    flag_data_staleness()
```

**Cost calculation:**
```python
# Similar to model staleness
data_age_months = (today - data_date).months
quality_degradation = min(0.25, data_age_months / 12)
annual_cost = base_ml_value * quality_degradation
```

---

#### 8. Undocumented Features
**Files to check:** `feature_engineering.py`, feature scripts

**Detection rules:**
```python
# Count generic feature names
magic_features = re.findall(r'feature_\d+', content)

# Check for mysterious calculations
if re.search(r'\* 2\.7183|\* 1\.618|/ 42', content):
    flag_magic_numbers()

# Check for "Sarah's feature" or "John's calculation"
if re.search(r"(Sarah|John|[A-Z][a-z]+)'s (feature|calculation)", content):
    flag_tribal_knowledge()
```

**Cost calculation:**
```python
undocumented_count = len(magic_features)
onboarding_delay_weeks = 6 if undocumented_count > 20 else 2
annual_cost = onboarding_delay_weeks * 4 * 10000  # New hires * cost
```

---

#### 9. No Experiment Tracking
**Files to check:** Training scripts, notebooks

**Detection rules:**
```python
# Check for MLflow, W&B imports
has_tracking = (
    'import mlflow' in content or
    'import wandb' in content or
    'from mlflow' in content
)

if not has_tracking and 'train' in filename:
    flag_no_experiment_tracking()
```

**Cost calculation:**
```python
# Time wasted on reproducibility
experiments_per_month = 10
time_per_reproduction_hours = 20
hourly_rate = 100
annual_cost = experiments_per_month * time_per_reproduction_hours * hourly_rate * 12
```

---

### Data Pipeline Debt (8 patterns)

#### 10. Version Sprawl
**Files to check:** `airflow-dags/`, pipeline scripts

**Detection rules:**
```python
# Count versions of same pipeline
versions = []
for file in dag_files:
    if file.startswith('etl_pipeline'):
        versions.append(file)

if len(versions) > 2:
    flag_version_sprawl()
```

**Cost calculation:**
```python
# Debugging time
version_count = len(versions)
hours_per_week_debugging = version_count * 2
annual_cost = hours_per_week_debugging * 52 * 100  # Hourly rate
```

---

#### 11. Storage Hoarding
**Files to check:** S3 paths, storage config, scripts

**Detection rules:**
```python
# Look for year-based bucket names
if re.search(r'(2019|2020|2021|2022)-', bucket_name):
    flag_old_storage()

# Look for "archive" folders
if 'archive' in path and 'no one knows' in comment:
    flag_mystery_storage()
```

**Cost calculation:**
```python
# S3 storage costs
old_buckets = count_buckets_with_year()
avg_bucket_size_tb = 4.7
monthly_cost_per_tb = 23
annual_cost = old_buckets * avg_bucket_size_tb * monthly_cost_per_tb * 12
```

---

#### 12. Slow Spark Jobs
**Files to check:** PySpark scripts, processing jobs

**Detection rules:**
```python
# Check for performance antipatterns
if 'df.count()' in content:  # Expensive operation
    flag_unnecessary_count()

if 'for' in content and 'iterrows' in content:
    flag_row_by_row_processing()

if not re.search(r'spark\.sql\.shuffle\.partitions', content):
    flag_no_spark_tuning()
```

**Cost calculation:**
```python
# If job takes 14 hours instead of 2
current_runtime_hours = 14
optimal_runtime_hours = 2
wasted_hours = current_runtime_hours - optimal_runtime_hours
cluster_cost_per_hour = 50
daily_runs = 1
annual_cost = wasted_hours * cluster_cost_per_hour * 365 * daily_runs
```

---

#### 13. Triple/Multiple Consumers
**Files to check:** Kafka consumers, message queue scripts

**Detection rules:**
```python
# Count consumer versions
consumer_versions = []
for file in files:
    if re.match(r'kafka-consumer-v\d+\.py', file):
        consumer_versions.append(file)

if len(consumer_versions) > 1:
    flag_multiple_consumers()
```

**Cost calculation:**
```python
consumer_count = len(consumer_versions)
single_consumer_cost = 15000  # Monthly infrastructure
annual_cost = single_consumer_cost * (consumer_count - 1) * 12
```

---

## Cost Calculation Models

### General Formula
```python
annual_cost = (
    direct_cost +           # Infrastructure, licenses, cloud
    opportunity_cost +      # Blocked features, lost revenue
    productivity_cost +     # Engineer time wasted
    risk_cost              # Security, compliance, incidents
)
```

### Break-Even Calculation
```python
refactoring_cost = effort_weeks * team_size * weekly_rate
annual_savings = current_annual_cost - post_refactoring_annual_cost
break_even_weeks = refactoring_cost / (annual_savings / 52)
```

### ROI Calculation
```python
first_year_roi = (
    (annual_savings - refactoring_cost) / refactoring_cost
) * 100
```

---

## Output Format

Return analysis as JSON:

```json
{
  "repository": "payment-platform",
  "scan_date": "2026-02-16",
  "summary": {
    "total_debt_items": 15,
    "critical": 5,
    "high": 6,
    "medium": 4,
    "total_annual_cost": 708000,
    "refactoring_effort_weeks": 7,
    "break_even_weeks": 19
  },
  "debt_items": [
    {
      "id": 1,
      "type": "god_library",
      "severity": "critical",
      "category": "architecture",
      "location": "services/shared-commons/",
      "description": "God Library imported by 23 services",
      "details": {
        "affected_services": 23,
        "deploy_delay_days": 21,
        "current_deploy_cycle": "3 weeks",
        "target_deploy_cycle": "3 days"
      },
      "impact": {
        "annual_cost": 268000,
        "blocked_features": 0,
        "engineering_velocity": "-70%"
      },
      "fix": {
        "effort_weeks": 3,
        "description": "Break into focused libraries",
        "roi": "Enables daily deploys, saves $268K/year"
      }
    },
    {
      "id": 2,
      "type": "security_vulnerability",
      "severity": "critical",
      "category": "security",
      "location": "shared-commons/LoggingUtils.java:10",
      "description": "Log4Shell vulnerability (CVE-2021-44228)",
      "details": {
        "cve": "CVE-2021-44228",
        "cvss": 10.0,
        "package": "log4j",
        "current_version": "1.2.17",
        "fixed_version": "2.17.0+"
      },
      "impact": {
        "annual_cost": 100000,
        "risk": "Remote code execution",
        "compliance": "Mandatory security sprint"
      },
      "fix": {
        "effort_weeks": 1,
        "description": "Upgrade to Log4j 2.17+",
        "roi": "Eliminates critical security risk"
      }
    }
  ],
  "recommendations": [
    {
      "priority": 1,
      "title": "Fix Critical Security Issues",
      "effort_weeks": 2,
      "annual_savings": 100000,
      "items": [2, 5]
    },
    {
      "priority": 2,
      "title": "Refactor God Library",
      "effort_weeks": 3,
      "annual_savings": 268000,
      "items": [1]
    }
  ],
  "comparison": {
    "option_a_build_feature": {
      "effort_weeks": 3,
      "success_rate": 0.35,
      "ongoing_cost_monthly": 23000,
      "risk": "high"
    },
    "option_b_refactor_first": {
      "effort_weeks": 9,
      "success_rate": 0.92,
      "annual_savings": 268000,
      "break_even_weeks": 19,
      "risk": "low"
    },
    "recommendation": "option_b"
  }
}
```

---

## Dashboard Generation

After analysis, generate an interactive React dashboard:

```jsx
<TechDebtDashboard 
  data={analysis_results}
  showNegotiation={true}
  enableInteractive={true}
/>
```

The dashboard should show:
1. **Summary Card** - Total cost, effort, break-even
2. **Debt Inventory** - List of issues by severity
3. **Cost Breakdown** - Chart showing cost by category
4. **Negotiation View** - Refactor vs. Build comparison
5. **Timeline** - Break-even point visualization
6. **Recommendations** - Prioritized action items

---

## Best Practices

1. **Be Conservative** - Err on side of higher costs (better to over-estimate than under)
2. **Use Real Examples** - Reference actual company case studies when possible
3. **Show Break-Even** - Always calculate when refactoring pays off
4. **Prioritize by ROI** - Sort recommendations by payback period
5. **Include Context** - Explain WHY each debt item matters

---

## Example Analysis Session

**User:** "Analyze the payment-platform repository for technical debt"

**Claude (using this skill):**

1. Scans key files (pom.xml, source code, configs)
2. Identifies patterns:
   - God Library (shared-commons)
   - Log4Shell (pom.xml)
   - Zombie flags (feature-flags.json)
   - God Class (PaymentController.java)
3. Calculates costs for each
4. Generates JSON analysis
5. Creates interactive dashboard
6. Shows refactor vs. build comparison

**Output:** "Found $708K/year in technical debt. Refactoring takes 7 weeks but pays off in Week 19. Here's the breakdown..."

---

## Updating This Skill

To add new debt patterns:

1. Add pattern detection rules above
2. Add cost calculation model
3. Update output format if needed
4. Test on sample repositories
5. Update documentation

---

**Remember:** The goal is to translate technical debt into business language that PMs and executives understand: dollars, timelines, and risk.
