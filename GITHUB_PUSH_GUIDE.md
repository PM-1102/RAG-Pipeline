# 🚀 GitHub Push Guide

Follow these steps in order to push your RAG chatbot to GitHub.

## Prerequisites

1. **GitHub Account** - Create one at [github.com](https://github.com)
2. **Git Installed** - Check: `git --version`
3. **GitHub CLI** (Optional) - Or use HTTPS with token

---

## Step 1: Create GitHub Repository

### Option A: Using GitHub Web
1. Go to [github.com/new](https://github.com/new)
2. Repository name: `RAG` or `rag-chatbot`
3. Description: "Retrieval-Augmented Generation chatbot for PDF Q&A"
4. Public (if you want to share) or Private
5. **Do NOT initialize with README** (we already have one)
6. Click "Create repository"
7. Copy the repository URL from the page (looks like `https://github.com/yourname/RAG.git`)

### Option B: Using GitHub CLI
```powershell
gh repo create RAG --public --source=. --remote=origin --push
```

---

## Step 2: Open PowerShell in RAG Directory

```powershell
cd h:\RAG
```

---

## Step 3: Initialize Git (if not already done)

```powershell
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## Step 4: Delete Non-Essential Files

```powershell
# Delete development notebooks
rm -r notebook

# Delete data directory (users upload their own PDFs)
rm -r data

# Delete Jupyter artifact
rm "pipeline/# %% [markdown].py" -Force

# Clear pycache
rm -r -Force pipeline/__pycache__
rm -r -Force app/__pycache__

# Check for .env file and ensure it's NOT committed
if (Test-Path .env) { 
    Write-Host "✅ .env exists (good - won't be committed due to .gitignore)"
} else {
    Write-Host "ℹ️ No .env file yet - create one with your API key"
}
```

---

## Step 5: Add Remote Repository

Replace `YOUR_GITHUB_USERNAME` and `REPO_NAME` with your actual values:

```powershell
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/REPO_NAME.git
```

Example:
```powershell
git remote add origin https://github.com/johndoe/RAG.git
```

---

## Step 6: Verify Files to Be Committed

```powershell
git status
```

You should see these files (and NOT see `.env`):
```
✅ app/
✅ pipeline/
✅ .git/
✅ .gitignore
✅ .python-version
✅ .streamlit/
✅ main.py
✅ requirements.txt
✅ pyproject.toml
✅ README.md
✅ DEPLOYMENT.md
✅ .env.example

❌ .env (should NOT appear)
❌ data/
❌ notebook/
```

---

## Step 7: Add All Files to Git

```powershell
git add -A
```

---

## Step 8: Create Initial Commit

```powershell
git commit -m "Initial commit: Production-ready RAG chatbot

- Complete RAG pipeline with semantic search
- Streamlit web interface
- ChromaDB vector storage
- Groq LLM integration
- Full documentation and deployment guide"
```

---

## Step 9: Push to GitHub

```powershell
git branch -M main
git push -u origin main
```

**First time?** You may be prompted for authentication:
- **HTTPS**: Enter your GitHub username + personal access token (not password)
  - Create token: [github.com/settings/tokens](https://github.com/settings/tokens)
- **SSH**: Use SSH key if configured

---

## Step 10: Verify on GitHub

1. Go to your repository: `https://github.com/YOUR_USERNAME/RAG`
2. Verify all files are there
3. Check that `.env` is NOT visible (should be in .gitignore)
4. README.md should display nicely

---

## Troubleshooting

### "fatal: Not a git repository"
```powershell
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

### "failed to push some refs to 'origin'"
```powershell
# Force push if needed (careful!)
git push -u origin main --force
```

### "warning: LF will be converted to CRLF"
Just a Windows warning - it's fine, press enter

### ".env appearing in git"
```powershell
# Remove it from git tracking
git rm --cached .env
git commit -m "Remove .env file"
```

### Authentication issues with HTTPS
1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Create new token with `repo` scope
3. Use token as password when prompted
4. Or store it: `git credential fill`

---

## Complete Command Sequence (Copy & Paste)

If you just want to run all commands at once:

```powershell
# Navigate to project
cd h:\RAG

# Initialize git (if needed)
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/RAG.git

# Stage all files
git add -A

# Commit
git commit -m "Initial commit: Production-ready RAG chatbot"

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## After Pushing: Update Code

For future updates:
```powershell
git add .
git commit -m "Description of changes"
git push origin main
```

---

## Next: Deploy to Streamlit Cloud

Once your code is on GitHub:

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repo
4. Set main file: `app/streamlit_app.py`
5. Click "Deploy"
6. In Streamlit dashboard, add secret: `GROQ_API_KEY=your_key`

See `DEPLOYMENT.md` for detailed instructions.

---

**✅ Ready to push?** Run the commands above and your project will be on GitHub! 🚀
