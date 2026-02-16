# Technical Debt Negotiator - Demo Guide

## For GenAI & Agentic Fair Presentation

---

## 🎯 Demo Objectives

By the end of your 3-minute demo, judges should understand:
1. The problem (PM-Engineer standoffs)
2. Your solution (AI-powered debt analysis)
3. The value (data-driven decisions, clear ROI)
4. How it works (live demonstration)

---

## 📋 Pre-Demo Checklist

### Hardware/Setup:
- [ ] Laptop fully charged + charger
- [ ] Claude.ai account logged in
- [ ] Sample repositories ready to upload
- [ ] Backup: Screenshots if API fails
- [ ] Internet connection tested

### Materials:
- [ ] QR code to GitHub repo on poster
- [ ] Business cards with project link
- [ ] One-pager handouts (optional)
- [ ] Backup: Video recording of demo

### Practice:
- [ ] Run through demo 5 times
- [ ] Time yourself (should be 2-3 minutes)
- [ ] Practice without looking at notes
- [ ] Prepare answers to likely questions

---

## 🎤 Demo Script (3 Minutes)

### Opening Hook (15 seconds)

**Stand up, make eye contact, smile**

*"Hi! I'm [Your Name]. Have you ever been in a meeting where engineers say 'we need to refactor' and product managers say 'we need features,' and you argue for 2 hours with zero data?"*

*"I built an AI tool that ends that conversation in 2 minutes."*

---

### Problem Setup (20 seconds)

*"Here's the situation: This is a real payment platform from a mid-sized tech company."*

[Upload payment-platform folder to Claude.ai]

*"The engineers say the code is messy and needs refactoring. The PM says we need to ship a new shopping cart feature. Who's right?"*

*"Traditional approach: Endless debate. My tool: Let's ask the data."*

---

### Live Demo Part 1: Analysis (60 seconds)

*"I'm going to ask Claude to analyze this repository using my custom skill."*

[Type in Claude.ai:]
```
Analyze this repository for technical debt using the techdebt-analyzer skill.
```

[While Claude analyzes, narrate:]

*"The tool is scanning the codebase right now, looking for 27 different patterns of technical debt across software, ML, and data systems."*

[Claude returns analysis, point to screen:]

*"And here's what it found:"*
- *"$708,000 per year in technical debt"*
- *"A God Library that forces 23 services to redeploy together"*
- *"Log4Shell security vulnerability"*
- *"89 zombie feature flags from old A/B tests"*

---

### Live Demo Part 2: The Negotiation (60 seconds)

*"Now here's where it gets interesting. The PM wants to build that shopping cart feature."*

[Continue with Claude:]
```
Now show me: should we build the feature first, or refactor and then build?
Create an interactive dashboard comparing both options.
```

[Claude generates dashboard, point to screen:]

*"Look at this comparison:"*

**Option A: Just Build the Feature**
- *"3 weeks development"*
- *"But 65% risk of breaking things because the code is fragile"*
- *"Success rate: 35%"*

**Option B: Refactor First, Then Build**
- *"7 weeks refactoring + 2 weeks feature = 9 weeks total"*
- *"Success rate: 92%"*
- *"And here's the key: Break-even at Week 19"*

[Point to break-even chart:]

*"After Week 19, you're saving $268,000 per year, forever. The data makes the case."*

---

### The Differentiator (20 seconds)

*"What makes this different:"*
- *"Not just finding bugs—quantifying business impact"*
- *"Not just code analysis—showing when refactoring pays off"*
- *"Not just for engineers—PMs can finally see the ROI"*

---

### Call to Action (15 seconds)

*"You can try it yourself."*

[Point to QR code on poster:]

*"Scan this QR code for the GitHub repo. All the sample repositories are there, the skills are open source, and you can run it on your own code."*

*"Questions?"*

---

## 🎨 Booth Setup

### Layout:
```
┌─────────────────────────────────────┐
│                                     │
│         POSTER (on wall)            │
│  Title: Technical Debt Negotiator  │
│  Subtitle: AI-Powered Refactoring  │
│           ROI Analysis              │
│                                     │
│  [Problem] [Solution] [Results]    │
│                                     │
│      [Large QR Code]                │
│   "Try it yourself →"               │
│                                     │
└─────────────────────────────────────┘

        [Table with laptop]
         ┌─────────┐
         │ LAPTOP  │ ← Claude.ai open
         │  OPEN   │    Ready to demo
         └─────────┘
      
     [You standing here]
        Ready to engage!
```

### On Table:
- Laptop (Claude.ai open to new conversation)
- Business cards in holder
- One-page handouts (optional)
- Water bottle for you

### On Poster:
- Project title + tagline
- 3-panel layout: Problem | Solution | Results
- Large QR code
- Key statistics ($708K, 92% success rate, Week 19 break-even)
- Screenshots of dashboard

---

## 💬 Handling Questions

### "How does the AI know what's technical debt?"

*"Great question! I created a custom Claude skill with 27 detection patterns based on real tech debt at companies like Netflix, LinkedIn, and Airbnb. The AI scans for things like outdated dependencies, God classes, hardcoded credentials, and calculates their business impact using industry benchmarks."*

---

### "What if the cost calculations are wrong?"

*"The costs are estimates based on industry research and case studies. The tool errs on the conservative side—better to over-estimate than under. But the real value isn't the exact number, it's having *any* number to base the conversation on instead of just opinions."*

---

### "Can this integrate with GitHub/Jira?"

*"Not yet! Right now it's MVP—you upload your repo manually. But that's on the roadmap. GitHub Actions integration, Jira backlog analysis, continuous scanning—all planned for Phase 2. Would you use that?"*

---

### "How is this different from SonarQube?"

*"SonarQube finds code quality issues. My tool goes a step further: it quantifies the business impact and shows you when refactoring pays off. SonarQube tells you 'this is messy.' My tool tells you 'this costs $67K per quarter and pays back in 19 weeks if you fix it.' That's the difference—ROI focus."*

---

### "Did you really find $708K in one repo?"

*"These are realistic sample repositories I created based on real patterns from FAANG companies. I built three: payment platform (traditional software), fraud detection (ML), and analytics pipeline (data). Each has intentional technical debt based on actual case studies. The costs are based on real numbers from those companies' post-mortems."*

---

### "What's your background?"

*"I worked at Dell where I led a microservices migration that boosted performance 60%. But we struggled to justify the 6 months of refactoring to leadership because we couldn't quantify the benefit. I built this tool to solve that exact problem—giving engineers the data to make the business case for technical work."*

---

### "Can I use this at my company?"

*"Absolutely! It's MIT licensed, completely open source. The GitHub repo has everything: the analysis code, the Claude skills, the sample repositories. You can run it on your own code right now. If you end up using it, I'd love to hear how it goes!"*

---

### "Are you planning to commercialize this?"

*"Maybe! Right now it's open source because I want to help as many teams as possible. But if there's enterprise demand—continuous scanning, team dashboards, historical tracking—I might build a SaaS version. Would your company pay for that?"*

---

## 🎭 Handling Different Audiences

### For Technical Judges (Engineers/Researchers):
- Emphasize the AI skill architecture
- Show code quality of analyzers
- Discuss future: ML model for predictions
- Mention test coverage, extensibility

### For Product Judges (PMs/Designers):
- Focus on user experience of dashboard
- Emphasize business value translation
- Show how it helps roadmap decisions
- Discuss PM pain points

### For Business Judges (MBAs/Executives):
- Lead with ROI numbers
- Show break-even analysis
- Discuss market opportunity
- Mention enterprise sales potential

### For Alumni:
- Ask about their experience with tech debt
- Get validation of the problem
- Ask if they'd use it
- Networking opportunity!

---

## 🚨 Backup Plans

### If Claude API is slow/down:
- Have screenshots ready
- Show pre-generated analysis
- Walk through the JSON results
- Emphasize it's about the insight, not the speed

### If laptop dies:
- Have phone backup with GitHub open
- Show README and sample outputs
- Talk through the process
- Emphasize the methodology

### If upload fails:
- Use pre-analyzed results
- Show example output files
- Focus on the cost modeling
- Demo the insight value

### If you forget your script:
- Core message: "Ends PM-Engineer debates with data"
- Show: Problem → Analysis → ROI comparison
- Numbers: $708K cost, Week 19 break-even
- Close: "Try it yourself" (QR code)

---

## 📊 Key Statistics to Memorize

- **$708K** - annual cost (payment platform)
- **$1.4M** - annual cost (ML model)
- **$1.0M** - annual cost (data pipeline)
- **92% vs 35%** - success rate comparison
- **Week 19** - break-even point (payment platform)
- **27 patterns** - detected debt types
- **3 domains** - SWE, ML, Data

---

## ⏱️ Time Management

- **0:00-0:15** - Hook (PM-Engineer debate)
- **0:15-0:35** - Problem setup (upload repo)
- **0:35-1:35** - Live analysis (Claude scans)
- **1:35-2:35** - Dashboard + negotiation view
- **2:35-2:55** - Differentiator + value prop
- **2:55-3:00** - Call to action (QR code)

**Total: 3 minutes**

Practice until you can do this in your sleep!

---

## 🏆 What Judges Are Looking For

### Innovation (25 points):
- ✅ Novel approach to old problem
- ✅ AI-powered analysis (timely)
- ✅ Quantifies intangible debt

### Technical Execution (30 points):
- ✅ Works live in demo
- ✅ Clean code architecture
- ✅ Extensible design

### Communication (25 points):
- ✅ Clear problem statement
- ✅ Compelling demonstration
- ✅ Business value articulation

### Impact (20 points):
- ✅ Solves real pain point
- ✅ Clear monetization path
- ✅ Measurable ROI

---

## 🎬 Final Reminders

1. **Smile and make eye contact** - You're excited about this!
2. **Speak slowly and clearly** - Judges are hearing many presentations
3. **Let the tool speak** - Don't over-explain, show the output
4. **Be confident** - You built something genuinely useful
5. **Have fun!** - This is your moment to shine

---

## 📞 Post-Demo Follow-Up

After judges leave:
- [ ] Thank them for their time
- [ ] Offer business card
- [ ] Mention GitHub repo again
- [ ] Ask if they have feedback

After the fair:
- [ ] Email judges who showed interest
- [ ] Post demo video to LinkedIn
- [ ] Share GitHub link on Twitter
- [ ] Write blog post about experience

---

**You've got this! This is a genuinely valuable tool that solves a real problem. Be proud of what you built and show it with confidence.** 🚀

Good luck at the fair!
