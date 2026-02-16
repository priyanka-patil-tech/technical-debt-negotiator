# Technical Debt Negotiator 🔍💰

> An AI-powered tool that quantifies technical debt and helps teams make data-driven refactoring decisions.

[![Demo](https://img.shields.io/badge/demo-live-brightgreen)](https://your-demo-url.com)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue)](https://python.org)

---

## The Problem

Every engineering team faces this standoff:
- **PMs say:** "We need to ship features"
- **Engineers say:** "We need to refactor first"
- **Result:** Endless debates with no data

## The Solution

Technical Debt Negotiator uses AI to:
1. 📊 **Quantify technical debt** in dollars and time
2. 🎯 **Calculate ROI** of refactoring vs. building features
3. 📈 **Show break-even timelines** for informed decisions
4. 🤝 **End PM-Engineer standoffs** with data

---

## ✨ Features

- 🔍 **Scans GitHub repositories** for 18+ debt patterns
- 💰 **Calculates annual costs** ($708K/year for our sample repo!)
- ⚖️ **Compares scenarios:** Refactor first vs. Build now
- 📊 **Interactive dashboard** showing tradeoffs
- 🤖 **AI-powered analysis** using Claude + custom skills
- 📦 **Sample repositories** with realistic technical debt

---

## 🚀 Quick Start

### Option 1: Try with Sample Repositories

```bash
# Clone the repository
git clone https://github.com/yourusername/technical-debt-negotiator.git
cd technical-debt-negotiator

# Install dependencies
pip install -r requirements.txt

# Analyze a sample repository (you need to download these separately)
python scripts/run_analysis.py ../demo-repositories/payment-platform

# View results
python scripts/generate_report.py output/payment-platform-analysis.json
```

### Option 2: Use with Claude.ai

1. Upload your repository to Claude.ai
2. Upload the skill from `skills/techdebt-analyzer/SKILL.md`
3. Ask Claude: "Analyze this repository for technical debt using the skill"
4. Claude will generate an interactive dashboard

### Option 3: Analyze Your Own Repository

```python
from analyzers.code_analyzer import CodeAnalyzer

analyzer = CodeAnalyzer()
results = analyzer.analyze_repository('/path/to/your/repo')

print(f"Total annual cost: ${results.total_cost:,}")
print(f"Refactoring effort: {results.effort_weeks} weeks")
print(f"Break even: Week {results.break_even_weeks}")
```

---

## 💡 Example Output

### Payment Platform Analysis

**Technical Debt Found:**
- 🔴 God Library affecting 23 services → **$268K/year**
- 🔴 Log4Shell vulnerability (CVE-2021-44228) → **3-week security sprint**
- 🟡 89 zombie feature flags → **15% performance hit**
- 🟡 4,500-line God class → **3x slower development**

**Total Annual Cost:** **$708,000**

**Refactoring Plan:**
- **Effort:** 7 weeks
- **Break Even:** Week 19
- **Annual Savings:** $268,000

**Recommendation:** Refactor first, then build features
- Success rate: 92% vs 35%
- Enables daily deploys (vs 3-week cycles)
- Unlocks 3 blocked features

[See full report →](examples/payment-platform-analysis.json)

---

## 🎯 Use Cases

### For Product Managers
- Understand engineering requests in business terms
- Make data-driven roadmap decisions
- Justify refactoring to leadership

### For Engineers
- Quantify technical debt impact
- Build business case for refactoring
- Prioritize debt by ROI

### For Engineering Managers
- Communicate debt to non-technical stakeholders
- Balance feature delivery and debt reduction
- Track debt reduction over time

### For CTOs
- Portfolio-wide debt visibility
- Resource allocation decisions
- Risk assessment

---

## 📊 Supported Debt Patterns

### Traditional Software (10 patterns)
- ✅ Outdated dependencies (blocking features)
- ✅ God classes/libraries (deployment delays)
- ✅ Security vulnerabilities (CVEs)
- ✅ Zombie feature flags (performance degradation)
- ✅ Hardcoded credentials (security risk)
- ✅ Code duplication (maintenance burden)
- ✅ Missing tests (manual QA cycles)
- ✅ Poor documentation (onboarding time)
- ✅ Fragile architecture (regression risk)
- ✅ Deployment scripts (deployment time)

### ML/AI Systems (9 patterns)
- ✅ Model staleness (accuracy degradation)
- ✅ Data staleness (prediction quality)
- ✅ Undocumented features (compliance risk)
- ✅ Preprocessing duplication (bug rate)
- ✅ No experiment tracking (reproducibility)
- ✅ Framework lock-in (blocked features)
- ✅ No monitoring (silent failures)
- ✅ Dead model versions (infrastructure waste)
- ✅ Inference bottlenecks (latency)

### Data Pipelines (8 patterns)
- ✅ Version sprawl (debugging time)
- ✅ Storage hoarding (S3 costs)
- ✅ Slow Spark jobs (compute waste)
- ✅ Manual backfills (on-call burden)
- ✅ No batching (database load)
- ✅ Triple consumers (3x infrastructure)
- ✅ No data quality checks (incidents)
- ✅ Outdated orchestration (blocked features)

[See detailed pattern descriptions →](docs/DEBT_PATTERNS.md)

---

## 🏗️ Architecture

```
┌─────────────┐
│   GitHub    │
│ Repository  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   File Scanner  │  ← Read files, detect patterns
│   (view tool)   │     
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Claude API +   │  ← AI-powered analysis
│  Custom Skills  │     Debt classification
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Cost Calculator │  ← ROI modeling
│   (Python)      │     Break-even analysis
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Dashboard     │  ← Interactive UI
│   (React)       │     Visualization
└─────────────────┘
```

### How It Works:

1. **Upload Repository** - Upload your repo to Claude or point script at local path
2. **Pattern Detection** - Claude skill identifies 27+ debt patterns
3. **Cost Calculation** - Python analyzers quantify impact in dollars and time
4. **ROI Modeling** - Calculate break-even for refactoring scenarios
5. **Visualization** - Generate interactive dashboard showing tradeoffs

[See detailed architecture →](docs/ARCHITECTURE.md)

---

## 📦 Sample Repositories

Three realistic repositories with intentional technical debt:

### 1. payment-platform (Traditional SWE Debt)
- **Cost:** $708K/year
- **Issues:** God Library, Log4Shell, zombie flags
- **Fix:** 7 weeks, break-even Week 19

### 2. fraud-detection-model (ML Debt)
- **Cost:** $1.4M/year
- **Issues:** Model staleness, 47 magic features, 14-hour batch
- **Fix:** 12 weeks, break-even Week 6

### 3. analytics-pipeline (Data Pipeline Debt)
- **Cost:** $1.0M/year
- **Issues:** Triple Kafka consumers, 14-hour Spark, 12 TB mystery data
- **Fix:** 12 weeks, break-even Week 2

**Download these separately from the demo-repositories bundle.**

---

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Claude API key (optional, for automated analysis)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/technical-debt-negotiator.git
cd technical-debt-negotiator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up Claude API key (optional)
export ANTHROPIC_API_KEY=your-key-here

# Run tests
pytest tests/
```

---

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Cost Calculation Models](docs/COST_MODELS.md)
- [Debt Pattern Catalog](docs/DEBT_PATTERNS.md)
- [Adding New Patterns](docs/CONTRIBUTING.md)
- [Demo Guide for Presentations](docs/DEMO_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)

---

## 🎓 Background & Research

This tool is based on:
- Real technical debt patterns from FAANG companies
- Academic research on software maintenance costs
- Industry reports (DORA, State of DevOps)
- Personal experience leading microservices migration at Dell

### Real-World Parallels:
- **Netflix:** Storage optimization saved $1M/year
- **LinkedIn:** Kafka consumer consolidation (65% cost reduction)
- **Airbnb:** Spark optimization (14h → 2h)
- **Spotify:** DAG consolidation (70% fewer failures)

**Sample repositories** contain intentional debt based on these case studies.

---

## 🤝 Contributing

Contributions welcome! We're especially interested in:

- 🆕 New debt pattern detectors
- 💰 Improved cost models (industry-specific)
- 🌍 Benchmarks from different companies
- 📊 Better visualizations
- 🧪 More test coverage
- 📝 Documentation improvements

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

---

## 🎤 Presentations & Talks

This tool was presented at:
- GenAI and Agentic Fair 2026 (your university)

Want to present this at your company/conference? Contact us!

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 👨‍💻 Author

**[Your Name]**
- Former Dell Engineering (led microservices migration, 60% performance boost)
- Built this after seeing PM-Engineer debates waste months
- [LinkedIn](your-linkedin) | [Twitter](your-twitter) | [Blog](your-blog)

---

## 🙏 Acknowledgments

- Claude AI for analysis capabilities
- Sample repos inspired by real-world patterns at Netflix, LinkedIn, Airbnb, Spotify
- Beta testers from [your program]
- Open source community

---

## 📬 Contact

Questions? Suggestions? Want to use this at your company?

- Open an [issue](https://github.com/yourusername/technical-debt-negotiator/issues)
- Email: your.email@example.com
- LinkedIn: [your-linkedin]

---

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- ✅ Basic debt pattern detection
- ✅ Cost calculation models
- ✅ Sample repositories
- ✅ Interactive dashboard

### Phase 2: Automation (Q2 2026)
- ⏳ GitHub Actions integration
- ⏳ Continuous scanning
- ⏳ Jira backlog analysis
- ⏳ Automated PR comments

### Phase 3: Advanced (Q3 2026)
- ⏳ Multi-repo portfolio view
- ⏳ Historical trend tracking
- ⏳ Team benchmarking
- ⏳ Custom debt patterns

### Phase 4: Enterprise (Q4 2026)
- ⏳ SaaS offering
- ⏳ Enterprise features
- ⏳ API/SDK
- ⏳ Integrations (Slack, PagerDuty)

---

## ⭐ Star History

If this tool helps you, please star the repo! It helps others discover the project and motivates continued development.

[![Stargazers over time](https://starchart.cc/yourusername/technical-debt-negotiator.svg)](https://starchart.cc/yourusername/technical-debt-negotiator)

---

**Made with ❤️ to end PM-Engineer standoffs everywhere**
