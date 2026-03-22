# ⚡ Quick GitHub Setup (5 Minutes)

Fast track to push your code to GitHub.

## Prerequisites

- Git installed: `git --version`
- GitHub account: https://github.com/join
- SSH key configured OR HTTPS enabled

## Option A: HTTPS (Easiest)

```bash
# 1. Create repo on GitHub
#    https://github.com/new
#    Repository name: autopipeline
#    DO NOT initialize with README or .gitignore

# 2. In your local directory
cd /path/to/autopipeline

# 3. Initialize git (if not already)
git init
git config user.name "Your Name"
git config user.email "your@email.com"

# 4. Add all files
git add .

# 5. First commit
git commit -m "feat: Initial commit - Azure Autonomous Data Platform v1.0"

# 6. Add remote
git remote add origin https://github.com/YOUR_USERNAME/autopipeline.git

# 7. Push to GitHub
git branch -M main
git push -u origin main

# ✅ Done! Your code is now on GitHub
```

Visit: https://github.com/YOUR_USERNAME/autopipeline

## Option B: SSH (Recommended for Developers)

```bash
# 1-5. Same as above (1-5)

# 6. Add remote using SSH
git remote add origin git@github.com:YOUR_USERNAME/autopipeline.git

# 7. Push
git branch -M main
git push -u origin main
```

## Verify

```bash
# Should show GitHub URL
git remote -v

# Should show commits
git log --oneline -3

# Should show all files
git ls-tree -r main --name-only | wc -l
```

## Repository is Live! 🎉

- **Repository:** https://github.com/YOUR_USERNAME/autopipeline
- **Code:** All your files pushed
- **Documentation:** README.md visible
- **History:** All commits visible

## Configure Repository (Optional)

### Add Topics (for discoverability)

Go to: https://github.com/YOUR_USERNAME/autopipeline/settings/general

Add topics: `ai`, `automation`, `azure`, `claude`, `fastapi`, `react`

### Add Secrets (for CI/CD)

Go to: Settings → Secrets and variables → Actions

Add:
- `ANTHROPIC_API_KEY=sk-...`
- `AZURE_SUBSCRIPTION_ID=...`

### Protect Main Branch

Go to: Settings → Branches

Add protection for `main`:
- ✅ Require pull request reviews
- ✅ Require status checks to pass

## Common Commands

```bash
# Check status
git status

# See recent commits
git log --oneline -5

# Push changes
git add .
git commit -m "your message"
git push

# Create feature branch
git checkout -b feature/my-feature
git push -u origin feature/my-feature

# Pull latest
git pull origin main
```

---

**Repository setup complete!** 🚀

Next: Read README.md to get started!
