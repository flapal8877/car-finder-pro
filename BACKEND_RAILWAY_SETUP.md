# Railway Deployment Guide - CarFinder Pro Backend

Complete step-by-step guide to deploy your CarFinder Pro backend to Railway.

## 📋 Prerequisites

- GitHub account
- Railway account (sign up at https://railway.app)
- Your backend code in a GitHub repository

## 🚨 CRITICAL: Fix Procfile First!

**Your `Procfile.txt` file has the WRONG name!**

Railway requires a file named exactly `Procfile` (no extension).

### Fix This Now:

```bash
# Navigate to your repository
cd Car-finder-backend

# Rename the file
git mv Procfile.txt Procfile

# Commit the change
git commit -m "Fix Procfile name for Railway deployment"

# Push to GitHub
git push origin main
```

**Why this matters:** Railway looks for a file named exactly `Procfile`. If it's named `Procfile.txt`, Railway won't find it and will fail to start your app.

## 🚀 Deployment Methods

### Method A: Railway Dashboard (Easiest - No CLI)

#### Step 1: Connect to GitHub

1. Go to https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Click **"Login with GitHub"**
5. Authorize Railway to access your repositories

#### Step 2: Select Repository

1. Find and select **"Car-finder-backend"**
2. Click **"Deploy Now"**
3. Railway will automatically:
   - Detect it's a Python project
   - Read `requirements.txt`
   - Read `railway.json` for build config
   - Read `Procfile` for start command
   - Install dependencies
   - Install Playwright + Chromium

#### Step 3: Wait for Build (3-5 minutes)

Watch the build logs:
- **Green checkmarks** = success
- **Red X** = failed (see troubleshooting below)

**Expected build steps:**
```
✓ Installing Python 3.13
✓ Installing pip packages
✓ Installing Playwright
✓ Installing Chromium (this takes longest)
✓ Building application
✓ Starting server
```

#### Step 4: Generate Public URL

1. Click **"Settings"** in your Railway project
2. Go to **"Networking"** section
3. Click **"Generate Domain"**
4. Copy your URL: `https://car-finder-backend-production-xxxx.up.railway.app`

### Method B: Railway CLI (For Developers)

#### Step 1: Install Railway CLI

```bash
npm install -g @railway/cli
```

#### Step 2: Login

```bash
railway login
```

This opens your browser to authenticate.

#### Step 3: Link Repository

```bash
# Navigate to your backend folder
cd Car-finder-backend

# Initialize Railway project
railway init

# Select "Create new project"
# Name it: carfinder-backend
```

#### Step 4: Deploy

```bash
# Deploy to Railway
railway up

# This will:
# - Upload your code
# - Trigger build process
# - Start your server
```

#### Step 5: Generate Domain

```bash
railway domain
```

Copy the generated URL.

## 🧪 Testing Your Deployment

### Test 1: Health Check

```bash
curl https://your-railway-url.railway.app/health
```

**Expected response:**
```json
{"status":"healthy"}
```

### Test 2: Search Endpoint

```bash
curl -X POST https://your-railway-url.railway.app/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "Honda Civic",
    "location": "Los Angeles",
    "maxPrice": 25000,
    "searchMode": "fast"
  }'
```

**Expected:** Stream of SSE events with vehicle results.

### Test 3: Check Logs

**Via Dashboard:**
- Go to your project → Deployments
- Click latest deployment
- View logs in real-time

**Via CLI:**
```bash
railway logs
```

## 🔧 Adding Environment Variables

Environment variables are **optional** but improve performance.

### Via Railway Dashboard:

1. Go to your project
2. Click **"Variables"** tab
3. Click **"Add Variable"**
4. Add each variable:

```
EBAY_APP_ID=your_app_id_here
EBAY_CERT_ID=your_cert_id_here
NEXTDOOR_API_KEY=your_api_key_here
```

5. Railway auto-redeploys when you add variables

### Via Railway CLI:

```bash
# Set a single variable
railway variables set EBAY_APP_ID=your_app_id

# Set multiple variables
railway variables set EBAY_APP_ID=your_app_id EBAY_CERT_ID=your_cert_id
```

## 🔗 Connect to Frontend

### Option 1: Environment Variable in Lovable

1. Open your Lovable project
2. Go to **Settings** → **Environment Variables**
3. Add new variable:
   - **Key:** `VITE_RAILWAY_API_URL`
   - **Value:** `https://your-railway-url.railway.app`
4. Click **"Save"**
5. Redeploy your Lovable app

### Option 2: API Config Banner

Your frontend already has an API configuration banner:

1. Open your deployed Lovable app
2. See the banner at the top
3. Paste your Railway URL
4. Click **"Save Configuration"**

The URL is saved in browser localStorage.

## 🐛 Troubleshooting

### Build Fails: Python Version Error

**Error:**
```
ERROR: Could not find a version that satisfies the requirement pydantic==2.9.2
```

**Solution:**
Your `requirements.txt` has Python 3.13 compatible versions. Make sure you:
1. Pushed the updated `requirements.txt` to GitHub
2. Railway pulled the latest code

**Force rebuild:**
```bash
# Via CLI
railway up --force

# Via Dashboard
Settings → Redeploy
```

### Build Fails: Playwright Installation Timeout

**Error:**
```
Playwright installation timed out
```

**Solution:**
This is normal for the first build. Railway will retry automatically.

**If it keeps failing:**
1. Check `railway.json` has:
```json
{
  "build": {
    "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt && playwright install --with-deps chromium"
  }
}
```

2. Increase timeout in `railway.json`:
```json
{
  "deploy": {
    "healthcheckTimeout": 300
  }
}
```

### Build Succeeds But App Won't Start

**Error:**
```
Error: Address already in use
```

**Solution:**
Check your `Procfile` (not `Procfile.txt`!):
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Important:** Use `$PORT` (Railway provides this), not a hardcoded port.

### CORS Errors in Frontend

**Error in browser console:**
```
Access to fetch at 'https://...' from origin 'https://...' has been blocked by CORS
```

**Solution:**
Update `main.py` line 13:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-lovable-app.lovable.app"],  # Update this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Then redeploy:
```bash
git commit -am "Fix CORS for production"
git push
```

Railway will auto-redeploy.

### App Deployed But Returns 503

**Error:**
```
503 Service Unavailable
```

**Possible causes:**

1. **Health check failing**
   - Check logs for startup errors
   - Verify `/health` endpoint works locally

2. **App crashed on startup**
   - Check logs: `railway logs`
   - Common issue: Missing dependencies

3. **Port not bound correctly**
   - Verify `Procfile` uses `$PORT`

**Solution:**
```bash
# Check what went wrong
railway logs

# Force restart
railway restart
```

### Searches Are Slow

**Without API keys:**
- Fast mode: 20-30 seconds (normal)
- Full mode: 45-60 seconds (normal)

**Solution: Add API keys**
- eBay: FREE (5,000 calls/day)
- Nextdoor: FREE (100 calls/day)

With API keys:
- Fast mode: 10-20 seconds
- Full mode: 30-45 seconds

### No Results Returned

**Possible causes:**

1. **Sites blocking scrapers**
   - Some sites detect and block automated scraping
   - This is expected behavior
   - Try different search terms

2. **Network timeout**
   - Check Railway logs for timeout errors
   - Increase timeout in `railway.json`

3. **Search parameters too restrictive**
   - Try broader search (higher price, larger radius)

## 📊 Monitoring & Logs

### View Real-Time Logs

**Via Dashboard:**
- Project → Deployments → Latest → Logs

**Via CLI:**
```bash
# Stream logs
railway logs

# Follow logs (like tail -f)
railway logs --follow
```

### Common Log Messages

**Normal:**
```
INFO: Started server process
INFO: Waiting for application startup
INFO: Application startup complete
INFO: Uvicorn running on http://0.0.0.0:$PORT
```

**Errors to watch for:**
```
ERROR: Could not connect to browser
ERROR: Timeout waiting for page load
WARNING: Site returned no results
```

## 💰 Cost & Usage

### Railway Pricing

**Hobby Plan: $5/month**
- 500 hours runtime (enough for 24/7)
- $5 usage credit
- Suitable for: 100-500 searches/day

**Pro Plan: $20/month**
- Unlimited hours
- $20 usage credit
- Priority support
- Suitable for: 1000+ searches/day

### Estimating Your Costs

**Typical usage:**
- 100 searches/day = ~$5/month
- 500 searches/day = ~$7/month
- 1000 searches/day = ~$15/month

**Why costs vary:**
- Playwright browser instances use more resources
- Longer searches (full mode) cost more than fast mode
- API usage (with keys) is cheaper than scraping

## 🔒 Security Best Practices

### 1. Update CORS

In `main.py`, change:
```python
allow_origins=["*"]  # ❌ Too permissive!
```

To:
```python
allow_origins=["https://your-app.lovable.app"]  # ✅ Specific domain
```

### 2. Add Rate Limiting

Consider adding rate limiting for production:

```bash
pip install slowapi
```

```python
# In main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.post("/api/search")
@limiter.limit("10/minute")  # 10 searches per minute per IP
async def search_vehicles(params: SearchParams):
    # ... existing code
```

### 3. Secure API Keys

- **Never** commit API keys to GitHub
- Use Railway variables for all secrets
- Rotate keys periodically
- Monitor API usage

### 4. Enable HTTPS Only

Railway provides HTTPS by default. In `main.py`:

```python
# Redirect HTTP to HTTPS (optional)
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
app.add_middleware(HTTPSRedirectMiddleware)
```

## 🚀 Performance Optimization

### 1. Use API Keys

Add these to Railway variables for 2-3x faster searches:
- `EBAY_APP_ID` (FREE)
- `EBAY_CERT_ID` (FREE)
- `NEXTDOOR_API_KEY` (FREE)

### 2. Enable Caching

Add Redis for caching search results:

```bash
# In Railway dashboard, add Redis service
# Then add to requirements.txt:
redis==5.0.1
```

### 3. Adjust Concurrency

In `scrapers.py`, increase parallel scraping:

```python
# Scrape more sites concurrently (uses more resources)
results = await asyncio.gather(*[scrape_site(site) for site in sites])
```

## 📝 Deployment Checklist

Before going live:

- [ ] Renamed `Procfile.txt` to `Procfile`
- [ ] Pushed latest code to GitHub
- [ ] Deployed to Railway successfully
- [ ] Generated public domain
- [ ] Tested `/health` endpoint
- [ ] Tested `/api/search` endpoint
- [ ] Added API keys (optional)
- [ ] Updated CORS in `main.py`
- [ ] Updated frontend with backend URL
- [ ] Tested search from frontend
- [ ] Monitored logs for errors
- [ ] Verified SSL certificate (HTTPS)

## 🆘 Getting Help

### Railway Support

- **Docs:** https://docs.railway.app
- **Discord:** https://discord.gg/railway
- **Status:** https://status.railway.app

### Common Commands

```bash
# Check service status
railway status

# View environment variables
railway variables

# Restart service
railway restart

# Open logs
railway logs

# Open Railway dashboard
railway open
```

## 🎯 Next Steps

After successful deployment:

1. **Monitor Performance**
   - Check Railway metrics
   - Monitor API usage
   - Track search success rates

2. **Optimize Costs**
   - Add API keys to reduce scraping
   - Implement caching
   - Consider upgrading plan if needed

3. **Enhance Features**
   - Add more vehicle sites
   - Implement search result caching
   - Add email notifications
   - Create admin dashboard

4. **Scale Up**
   - Upgrade Railway plan
   - Add Redis caching
   - Implement load balancing
   - Consider serverless functions for specific tasks

---

## Quick Reference Card

```
┌─────────────────────────────────────────┐
│  RAILWAY DEPLOYMENT QUICK REFERENCE     │
├─────────────────────────────────────────┤
│  Fix Procfile:                          │
│  $ git mv Procfile.txt Procfile         │
│                                         │
│  Deploy:                                │
│  $ railway up                           │
│                                         │
│  Get URL:                               │
│  $ railway domain                       │
│                                         │
│  View Logs:                             │
│  $ railway logs                         │
│                                         │
│  Add Variable:                          │
│  $ railway variables set KEY=value      │
│                                         │
│  Restart:                               │
│  $ railway restart                      │
└─────────────────────────────────────────┘
```

**Your Backend URL:** `_______________________`

**Status:** [ ] Deployed [ ] Tested [ ] Connected to Frontend
