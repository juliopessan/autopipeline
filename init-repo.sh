#!/bin/bash
set -e

echo "🚀 Azure Autonomous Data Platform - Repository Initialization"
echo "=============================================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📝 Initializing new Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Check if origin remote exists
if git remote | grep -q origin; then
    echo "✅ Remote 'origin' already configured"
else
    echo ""
    echo "🔗 GitHub Repository Configuration"
    echo "-----------------------------------"
    read -p "Enter GitHub repository URL (e.g., https://github.com/fcamara/autopipeline.git): " repo_url
    
    if [ -z "$repo_url" ]; then
        echo "❌ Repository URL is required"
        exit 1
    fi
    
    git remote add origin "$repo_url"
    echo "✅ Remote 'origin' configured"
fi

# Configure git user (optional)
if [ -z "$(git config user.name)" ]; then
    echo ""
    echo "👤 Git Configuration"
    echo "-------------------"
    read -p "Enter your name: " git_name
    read -p "Enter your email: " git_email
    
    if [ ! -z "$git_name" ] && [ ! -z "$git_email" ]; then
        git config user.name "$git_name"
        git config user.email "$git_email"
        echo "✅ Git user configured"
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created (update it with your credentials)"
fi

# Add files to git
echo ""
echo "📦 Staging files..."
git add .
echo "✅ Files staged"

# Check if there are files to commit
if [ -z "$(git status --short)" ]; then
    echo "ℹ️  No changes to commit"
else
    echo ""
    echo "📝 Creating initial commit..."
    git commit -m "feat: Initial commit - Azure Autonomous Data Platform v1.0"
    echo "✅ Initial commit created"
fi

# Show status
echo ""
echo "📊 Repository Status"
echo "-------------------"
git log --oneline -3
git remote -v

echo ""
echo "✨ Repository initialized successfully!"
echo ""
echo "Next steps:"
echo "1. Update .env with your credentials:"
echo "   nano .env"
echo ""
echo "2. Push to GitHub:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Start developing:"
echo "   python backend_main.py  # Terminal 1"
echo "   npm start              # Terminal 2 (in frontend/)"
echo ""
echo "4. Read documentation:"
echo "   cat RUN-NOW.md"
echo ""
