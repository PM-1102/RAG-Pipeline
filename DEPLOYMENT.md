# Deployment Checklist

Follow this checklist before pushing to GitHub and deploying to Streamlit Cloud.

## Pre-GitHub Cleanup

### 1. Remove Development Files
```bash
# Delete Jupyter notebooks (development only)
rm -r notebook/

# Delete data directory (users upload PDFs)
rm -r data/
```

### 2. Remove Python Artifacts
```bash
# Clear Python cache (should already be in .gitignore)
rm -rf pipeline/__pycache__
rm -rf app/__pycache__
rm -f pipeline/*.pyc

# Delete notebook conversion artifact
rm -f pipeline/"# %% [markdown].py"
```

### 3. Create .env File (LOCAL ONLY)
```bash
# Do NOT commit this file!
echo 'GROQ_API_KEY=your_api_key_here' > .env
```

### 4. Verify .gitignore
Check that these are excluded:
- ✅ .env (API keys)
- ✅ __pycache__/
- ✅ data/
- ✅ .venv/
- ✅ *.pyc
- ✅ .streamlit/secrets.toml

## Files to Keep in GitHub

### Production Code
- ✅ `app/streamlit_app.py` - Main Streamlit UI
- ✅ `pipeline/*.py` - All 7 pipeline modules
- ✅ `main.py` - CLI entry point (optional)

### Configuration
- ✅ `requirements.txt` - CLEANED dependencies
- ✅ `pyproject.toml` - Project metadata (UPDATED)
- ✅ `.streamlit/config.toml` - Streamlit config (NEW)
- ✅ `README.md` - Documentation (UPDATED)
- ✅ `.gitignore` - File exclusions (UPDATED)
- ✅ `.env.example` - Template for API keys

### Version Control
- ✅ `.git/` - Git history
- ✅ `.gitignore` - File exclusions

## Streamlit Cloud Deployment

### Step 1: Push to GitHub
```bash
git add -A
git commit -m "Initial RAG chatbot release"
git push origin main
```

### Step 2: Connect to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your GitHub repository
4. Select branch: `main`
5. Set main file path: `app/streamlit_app.py`

### Step 3: Add Secrets
1. In Streamlit Cloud dashboard, go to App settings
2. Click "Secrets" 
3. Add:
```
GROQ_API_KEY = "your_groq_api_key_here"
```

### Step 4: Deploy
- Click "Deploy"
- Wait for build to complete
- Your app is live!

## After Deployment

### Test the App
1. Upload a sample PDF
2. Click "⚙️ Process File"
3. Ask a question
4. Verify sources show with scores

### Monitor
- Check logs for errors
- Monitor quota usage: https://console.groq.com

### Update Code
```bash
# Make changes locally
git add .
git commit -m "Description of changes"
git push origin main

# Streamlit Cloud auto-updates within 2 minutes
```

## Troubleshooting

### "ModuleNotFoundError"
- Verify all files are committed
- Check requirements.txt is in root directory
- Ensure pipeline/__init__.py exists

### "GROQ_API_KEY not found"
- Add secret to Streamlit Cloud dashboard Secrets tab
- Use exact name: `GROQ_API_KEY`

### App times out
- PDF too large (>100 pages)
- Groq quota exceeded
- Check limits at console.groq.com

### Slow startup
- First run builds Streamlit cache (~2 min)
- Embedding model downloads (~400MB)
- Subsequent runs are fast (cached)

## Performance Optimization

### For Large PDFs (Streamlit only)
Increase chunk_size in `pipeline/chunker.py`:
```python
split_documents(docs, chunk_size=2000, chunk_overlap=300)
```

### For Faster Responses
Use smaller embedding model in `pipeline/embedder.py`:
```python
model_name="all-MiniLM-L6-v2"  # Smallest, fastest
```

## Security Notes

- ⚠️ NEVER commit `.env` file
- ✅ Use `.env.example` for template
- ✅ Use Streamlit Secrets for production
- ✅ API rate limits: Check Groq console
- ✅ Vector store is ephemeral (rebuilds on restart)

## Scaling Considerations

- Current setup: Single user, in-memory vector store
- For multiple users: Add persistent database (PostgreSQL + pgvector)
- For high traffic: Add caching layer (Redis)
- For large PDFs: Implement streaming responses

---

**Ready to deploy?** Follow the steps above and your RAG chatbot will be live in ~5 minutes!
