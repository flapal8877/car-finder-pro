# Railway Backend Setup - Step by Step

## Prerequisites
- Railway account (sign up at https://railway.app)
- Git installed on your computer

## Step 1: Prepare Backend Files (5 minutes)

Create a new folder on your computer called `carfinder-backend` and copy these files into it:

**Required Files:**
- `main.py`
- `sites_config.py`
- `api_clients.py`
- `scrapers.py`
- `utils.py`
- `requirements.txt`
- `Procfile`
- `railway.json`

All files are ready in your Lovable project - download or copy them to your local folder.

## Step 2: Deploy to Railway (10 minutes)

### Option A: Deploy via Railway Dashboard (Recommended - No CLI needed)

1. **Go to Railway Dashboard**
   - Visit https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo" or "Empty Project"

2. **Upload Your Code**
   - If using GitHub:
     - Create a new GitHub repo
     - Push your `carfinder-backend` folder
     - Connect Railway to that repo
   
   - If using Empty Project:
     - Click "Deploy from local"
     - Select your `carfinder-backend` folder
     - Railway will auto-detect Python and start building

3. **Wait for Build**
   - Railway will automatically:
     - Install Python dependencies
     - Install Playwright + Chromium
     - Start the server
   - Watch the build logs (takes 3-5 minutes)

4. **Generate Domain**
   - Go to Settings → Networking
   - Click "Generate Domain"
   - Copy your URL (e.g., `carfinder-backend-production.up.railway.app`)

### Option B: Deploy via Railway CLI

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Navigate to your backend folder
cd carfinder-backend

# 4. Initialize git (if not already)
git init
git add .
git commit -m "Initial backend"

# 5. Create Railway project
railway init

# 6. Deploy
railway up

# 7. Generate domain
railway domain

# 8. Copy the URL shown
```

## Step 3: Connect to Lovable Frontend (2 minutes)

### Option A: Via Environment Variable (Recommended)

1. In Lovable, click your project name → Settings
2. Go to "Environment Variables"
3. Click "Add Variable"
4. Enter:
   - Key: `VITE_RAILWAY_API_URL`
   - Value: `https://your-railway-url.railway.app` (paste your Railway URL)
5. Click "Save"
6. Click "Update" in the publish dialog to deploy changes

### Option B: Via UI Configuration Banner

1. Your app already has an API Config Banner
2. Open your deployed app
3. Paste your Railway URL in the configuration banner
4. Click "Save Configuration"

## Step 4: Test the Connection (3 minutes)

1. **Test Backend Health**
   ```bash
   curl https://your-railway-url.railway.app/health
   ```
   Should return: `{"status":"healthy"}`

2. **Test Search in Frontend**
   - Open your Lovable app
   - Enter search: "Honda Civic", "Los Angeles", "$25000"
   - Click "Search Vehicles"
   - You should see progress updates and results streaming in

## Step 5: Optional - Add API Keys (10 minutes)

To make searches faster using APIs instead of scraping:

1. **In Railway Dashboard:**
   - Go to your project → Variables tab
   - Click "Add Variable"

2. **Add eBay API Keys (Free):**
   - Sign up at https://developer.ebay.com
   - Create an app → Get App ID and Cert ID
   - Add to Railway:
     - `EBAY_APP_ID` = your_app_id
     - `EBAY_CERT_ID` = your_cert_id

3. **Add Nextdoor API Key (Free):**
   - Sign up at https://nextdoor.com/developers
   - Get API key
   - Add to Railway:
     - `NEXTDOOR_API_KEY` = your_api_key

4. **Redeploy** (Railway will auto-redeploy after adding variables)

## Troubleshooting

### Build Fails
- Check Railway logs: Dashboard → Deployments → Click failed build
- Common issue: Playwright installation timeout
  - Solution: Railway will retry automatically
  - Or: Increase timeout in `railway.json`

### CORS Errors in Frontend
- Update `main.py` line 13:
  ```python
  allow_origins=["https://your-lovable-domain.lovable.app"]
  ```
- Redeploy to Railway

### Slow Searches
- Without API keys: 30-60 seconds (normal - scraping 10-35 sites)
- With API keys: 15-30 seconds (faster)
- Solution: Add API keys (Step 5)

### No Results Found
- Check Railway logs for errors
- Verify sites are accessible
- Some sites may block scrapers (expected behavior)
- Try different search terms

## Cost Estimate

**Railway Pricing:**
- Hobby Plan: $5/month (included free credits)
- Covers typical usage (100-500 searches/day)
- No credit card needed for trial

**API Costs (Optional):**
- eBay: FREE (5,000 calls/day)
- Nextdoor: FREE (100 calls/day)
- Total: $0/month if using free APIs

## Next Steps After Deployment

✅ Backend deployed and connected
✅ Frontend searching across 10-35 sites
✅ Real-time progress and results

**Enhancements to Consider:**
1. Add user authentication (save searches, favorites)
2. Email alerts for new listings
3. Price history tracking
4. VIN lookup integration
5. Map view of results

## Support

**Railway Issues:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway

**CarFinder Pro Questions:**
- Check RAILWAY_BACKEND.md for architecture details
- Review deployment logs in Railway dashboard

---

## Quick Reference

**Your URLs:**
- Railway Backend: `https://________.railway.app` (fill in after deployment)
- Lovable Frontend: `https://carfinder-pro-live.lovable.app`

**Environment Variable:**
```
VITE_RAILWAY_API_URL=https://________.railway.app
```

**Test Command:**
```bash
curl https://________.railway.app/health
```

Should return: `{"status":"healthy"}`
