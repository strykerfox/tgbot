#!/bin/bash

# Telegram Bot Deployment Helper

echo "🚀 Telegram Bot Deployment Setup"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    echo "   Visit: https://git-scm.com/download/mac"
    exit 1
fi

# Check if in correct directory
if [ ! -f "bot.py" ]; then
    echo "❌ Error: Please run this script from the Tgbot directory"
    echo "   Run: cd /Users/sagar/Tgbot && bash deploy.sh"
    exit 1
fi

echo "✅ Checking requirements..."

# Initialize git if not already
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - Telegram bot ready for deployment"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "📋 Files ready for deployment:"
ls -la | grep -E "(bot.py|config.py|requirements.txt|Procfile|.env.example|.gitignore|README.md)"

echo ""
echo "✅ Deployment Setup Complete!"
echo ""
echo "📝 Next Steps:"
echo "1. Create a GitHub account (if you don't have one): https://github.com"
echo "2. Create a new repository on GitHub"
echo "3. Push your code:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/Tgbot.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "4. Then deploy on Railway.app:"
echo "   - Go to https://railway.app"
echo "   - Click 'New Project' → 'Deploy from GitHub'"
echo "   - Select your Tgbot repository"
echo "   - Add environment variables from .env"
echo "   - Done! Your bot will run 24/7"
echo ""
echo "Need help? Check HOSTING_GUIDE.md"
