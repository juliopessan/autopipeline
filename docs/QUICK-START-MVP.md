# 🚀 Quick Start: Run the MVP in 5 Minutes

## What You'll Do

1. Install dependencies
2. Set Claude API key
3. Run the MVP prototype
4. Watch agent autonomously optimize

**Total time:** ~5 minutes

---

## Step 1: Install Dependencies

```bash
# Clone or download the files
cd /path/to/azure-autonomous-data-platform

# Install Python packages
pip install anthropic pandas pydantic python-dotenv

# Verify Python version (3.10+)
python --version
```

---

## Step 2: Set API Key

```bash
# macOS / Linux
export ANTHROPIC_API_KEY=sk-your-actual-key-here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-your-actual-key-here"

# Verify it's set
echo $ANTHROPIC_API_KEY  # Should print your key
```

If you don't have an API key:
1. Go to https://console.anthropic.com/account/keys
2. Create new key
3. Copy it
4. Paste into command above

---

## Step 3: Run the MVP

```bash
# From the directory with MVP-PROTOTYPE.py
python MVP-PROTOTYPE.py
```

**You should see:**

```
════════════════════════════════════════════════════════════
  Azure Autonomous Data Platform — MVP Prototype
  
  This demo shows:
  • Claude agent proposing improvements
  • Experiment execution with budget enforcement
  • Results tracking (TSV)
  • Autonomous loop (never asks for approval)
  
  Results saved to: results.tsv
════════════════════════════════════════════════════════════

🚀 AUTONOMOUS AGENT LOOP STARTING
══════════════════════════════════════════════════════════════

[Iteration 1] 14:32:15
──────────────────────────────────────────────────────────────
Current best metric: inf
Experiments completed: 0
Success rate: 0/0

💡 Proposal: Add caching to reduce redundant calculations
▶️  Running experiment...
   Metric: 118.8000 📉
   Cost: $2.10
   Time: 0.52s
   Status: success
   ✅ KEEP (improved!)

📊 Progress: +1.0% improvement

[Iteration 2] 14:32:16
...
```

---

## Step 4: Monitor Results

While running, the agent will:
- Propose ideas (Claude)
- Run experiments (executor)
- Keep good ideas, discard bad ones
- Log everything to `results.tsv`

After 10 iterations (< 1 minute), you'll see:

```
══════════════════════════════════════════════════════════════
📊 FINAL SUMMARY
══════════════════════════════════════════════════════════════
Total experiments: 10
Successful: 9
Crashes: 0
Success rate: 90.0%
Baseline metric: 120.0000
Best metric: 111.0000
Improvement: +7.5%

Results saved to: results.tsv
══════════════════════════════════════════════════════════════
```

---

## Step 5: View Results

```bash
# View results.tsv (tab-separated values)
cat results.tsv

# Output:
# commit  metric      cost_usd    status  description
# a1b2c3d 118.8000   2.10        keep    Add caching to reduce...
# b2c3d4e 117.5000   2.15        keep    Optimize loop unrolling...
# c3d4e5f 118.2000   2.12        discard Tried parallelization (worse)
# d4e5f6g 116.8000   2.18        keep    Filter data earlier...
# ...
```

---

## What Happened?

1. **You ran an autonomous data optimization loop**
   - Claude agent proposed improvements
   - Each proposal was executed
   - Results were tracked

2. **Agent learned over iterations**
   - Iteration 1-2: Small improvements
   - Iteration 3-5: Larger gains
   - Iteration 6+: Diminishing returns or plateau

3. **Every decision is auditable**
   - Every commit hash in results.tsv
   - Every experiment logged
   - Rationale documented

---

## Next Steps

### Option 1: Understand the Code (20 min)

1. Open `MVP-PROTOTYPE.py`
2. Read through the 4 main classes:
   - `ExperimentEngine` — Runs experiments
   - `ResultsTracker` — Logs results
   - `AutonomousAgent` — Claude loop
   - `program.md` — Agent boundaries

### Option 2: Customize for Your Pipeline (1 hour)

Edit these sections in MVP-PROTOTYPE.py:

```python
# 1. Change the metric
def get_metric():
    # Replace: return 120.0
    # With: real pipeline code that returns metric
    
# 2. Update program.md
PROGRAM_MD = """
# Your Pipeline Optimization

## What you CAN do:
- Your constraints here

## Optimization Goal:
Your metric here
"""

# 3. Update config
CONFIG = {
    "time_budget_seconds": 600,  # Real: 10 minutes
    "max_iterations": 100,  # Real: overnight
}
```

### Option 3: Deploy to Azure (2-4 hours)

Follow the implementation roadmap:
1. Set up Azure resources (Terraform from quick-start-guide.md)
2. Deploy agent to Container Instance
3. Monitor with Application Insights
4. Set up Slack alerts

---

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# If empty, set it again
export ANTHROPIC_API_KEY=sk-your-key

# Verify
echo $ANTHROPIC_API_KEY  # Should show key
```

### "ModuleNotFoundError: No module named 'anthropic'"

```bash
pip install anthropic --upgrade
```

### "Rate limit exceeded"

Wait a few minutes, then run again. The MVP makes ~1-2 API calls per iteration.

### Agent producing "crash" status

This is by design — the MVP simulates realistic failures. The agent learns to avoid them.

---

## What's Different from Production?

| Aspect | MVP | Production |
|---|---|---|
| Time budget | 30 sec | 600 sec (10 min) |
| Experiments | 10 max | 100+ (overnight) |
| Metric | Simulated | Real pipeline |
| Storage | Local TSV | Git + Cloud |
| Monitoring | Console | Application Insights |
| Alerts | None | Slack/Email |
| Infra | Local | Azure services |

The MVP proves the **concept**; production provides the **scale**.

---

## Next: Full Platform

After running the MVP successfully:

1. **Read the full documentation** (2-3 hours)
   - 00-EXECUTIVE-SUMMARY.md
   - quick-start-guide.md
   - azure_platform_architecture.md

2. **Plan your first real pipeline** (1-2 weeks)
   - Define metric
   - Set constraints (program.md)
   - Provision Azure resources

3. **Deploy to production** (4-6 weeks)
   - Follow implementation-roadmap.md
   - Gate reviews every 2 weeks
   - Scale to 5+ pipelines by week 8

---

## Success Indicators

✅ **MVP runs without errors**
✅ **Agent proposes real ideas** (not gibberish)
✅ **Metric improves over 10 iterations** (even slightly)
✅ **results.tsv shows clear progression**
✅ **You understand the loop** (read code, not just output)

If all ✅ → You're ready for production 🚀

---

## Getting Help

### Read the Docs
- **Stuck on concept?** → 00-EXECUTIVE-SUMMARY.md
- **Want to customize?** → quick-start-guide.md
- **Need architecture details?** → azure_platform_architecture.md
- **Unsure about operations?** → autonomous-data-research-SKILL.md

### Debug the MVP
1. Add print statements to see what Claude proposes
2. Check results.tsv for patterns
3. Run multiple times (randomness in Claude's responses)

### Scale to Production
- Follow IMPLEMENTATION-ROADMAP.md week by week
- Use the code templates from quick-start-guide.md
- Join weekly syncs with your team

---

## The Big Picture

```
You are here (MVP):
  Agent proposes → Execute → Track → Iterate (10x)

Next: Full platform:
  Agent proposes → Execute → Track → Iterate (100x/night)
  → Azure infrastructure
  → Multi-pipeline orchestration
  → Advanced analytics
  → Customer deployment
```

**Time to first value:** 5 minutes (MVP)  
**Time to production:** 4-6 weeks  
**Time to ROI:** Month 2-3  

---

## 🎉 Let's Go!

```bash
export ANTHROPIC_API_KEY=sk-your-key
python MVP-PROTOTYPE.py
```

Watch your agent optimize. 🤖✨

---

**Questions?** Check the README.md or ARCHITECTURE-DIAGRAMS.md for visual reference.

**Ready to scale?** Read IMPLEMENTATION-ROADMAP.md and start Week 1 planning.

**Let's automate the boring stuff.** 🚀
