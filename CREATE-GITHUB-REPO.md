# 📝 How to Create GitHub Repository

Step-by-step guide to create and push the repository to GitHub.

## Option 1: Using GitHub Web UI (Easiest)

### Step 1: Create Empty Repository

1. Go to https://github.com/new
2. Fill in details:
   - **Owner:** fcamara (or your account)
   - **Repository name:** `autopipeline`
   - **Description:** "Azure Autonomous Data Platform - AI-powered pipeline optimization"
   - **Visibility:** `Public`
   - **DO NOT** initialize with README, .gitignore, or license
3. Click "Create repository"

### Step 2: Push Local Code

```bash
# In the autopipeline directory:
cd /path/to/autopipeline

# Add remote
git remote add origin https://github.com/fcamara/autopipeline.git

# Verify
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Verify on GitHub

Visit: https://github.com/fcamara/autopipeline
- ✅ Should see all your files
- ✅ Should see commit history
- ✅ Should show "main" branch

---

## Option 2: Using GitHub CLI (Automated)

### Prerequisites

Install GitHub CLI: https://cli.github.com

### Create and Push

```bash
# Login to GitHub
gh auth login

# Create repository
gh repo create autopipeline \
  --public \
  --source=. \
  --remote=origin \
  --push \
  --description "Azure Autonomous Data Platform - AI-powered pipeline optimization"

# Verify
gh repo view
```

---

## Option 3: Complete Script

```bash
#!/bin/bash

# Configuration
GITHUB_USERNAME="fcamara"
REPO_NAME="autopipeline"
REPO_URL="https://github.com/$GITHUB_USERNAME/$REPO_NAME.git"

# Initialize git (if needed)
if [ ! -d ".git" ]; then
    git init
fi

# Configure git
git config user.name "Your Name"
git config user.email "your.email@fcamara.com.br"

# Add remote
git remote rm origin 2>/dev/null || true
git remote add origin "$REPO_URL"

# Add files
git add .
git commit -m "feat: Initial commit - Azure Autonomous Data Platform v1.0"

# Push
git branch -M main
git push -u origin main

echo "✅ Repository created and pushed to $REPO_URL"
```

---

## Verify Repository Was Created

```bash
# Check remote
git remote -v
# Should show: origin https://github.com/fcamara/autopipeline.git

# Check branch
git branch
# Should show: * main

# Check log
git log --oneline -3
# Should show your commits

# Check status
git status
# Should show: "Your branch is up to date with 'origin/main'"
```

---

## Configure Repository Settings

After creating the repository, configure:

### 1. Add Topics

https://github.com/fcamara/autopipeline/settings/general

Add topics (for discoverability):
- `ai`
- `automation`
- `azure`
- `claude`
- `data-pipeline`
- `fastapi`
- `react`

### 2. Enable Discussions

https://github.com/fcamara/autopipeline/settings/general

✅ Enable discussions for community engagement

### 3. Protect Main Branch

https://github.com/fcamara/autopipeline/settings/branches

Add protection rule for `main`:
- ✅ Require pull request reviews
- ✅ Require status checks to pass

### 4. Add Secrets

https://github.com/fcamara/autopipeline/settings/secrets/actions

For CI/CD pipeline:
- `ANTHROPIC_API_KEY` = sk-...
- `AZURE_SUBSCRIPTION_ID` = ...
- `AZURE_CLIENT_ID` = ...
- `AZURE_CLIENT_SECRET` = ...

### 5. Enable Pages

https://github.com/fcamara/autopipeline/settings/pages

- ✅ Enable GitHub Pages
- Source: Deploy from a branch
- Branch: main
- Folder: /docs

---

## Next Steps

1. **Invite collaborators:**
   ```
   Settings → Collaborators and teams → Invite
   ```

2. **Create issue templates:**
   ```
   .github/ISSUE_TEMPLATE/bug_report.md
   .github/ISSUE_TEMPLATE/feature_request.md
   ```

3. **Create pull request template:**
   ```
   .github/pull_request_template.md
   ```

4. **Enable Actions:**
   ```
   Actions → Enable GitHub Actions
   ```

5. **Create releases:**
   ```
   Releases → Create a new release
   ```

---

## Troubleshooting

### Error: "Repository already exists"

```bash
# If remote already exists
git remote rm origin
git remote add origin https://github.com/fcamara/autopipeline.git
```

### Error: "Permission denied (publickey)"

SSH key not configured. Use HTTPS instead:
```bash
git remote set-url origin https://github.com/fcamara/autopipeline.git
```

### Error: "fatal: Not a git repository"

Initialize git first:
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@fcamara.com.br"
git add .
git commit -m "Initial commit"
```

### Error: "branch 'main' does not exist"

Rename branch:
```bash
git branch -M main
git push -u origin main
```

---

## Verify Everything Works

```bash
# 1. Check origin
git remote -v
# origin https://github.com/fcamara/autopipeline.git (fetch)
# origin https://github.com/fcamara/autopipeline.git (push)

# 2. Check branch
git branch -a
# * main
#   remotes/origin/main

# 3. Check commits
git log --oneline -5

# 4. Check files pushed
git ls-tree -r main --name-only | head -10

# 5. Visit GitHub
# https://github.com/fcamara/autopipeline
```

---

## Repository Ready! 🎉

Your GitHub repository is now set up and ready for:
- ✅ Collaboration
- ✅ CI/CD (GitHub Actions)
- ✅ Issue tracking
- ✅ Pull requests
- ✅ Community contributions
- ✅ Documentation

**Next:** Read GITHUB-SETUP.md for complete configuration!

---

**Questions?** Check GitHub Docs: https://docs.github.com
