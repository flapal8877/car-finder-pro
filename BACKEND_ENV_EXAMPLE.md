# Environment Variables for Backend

Copy this to `.env` file in your backend repository:

```env
# ===========================================
# CarFinder Pro Backend - Environment Variables
# ===========================================

# ---------------------------------------------
# API Keys (All Optional - Improves Performance)
# ---------------------------------------------

# eBay Motors API (Free Tier Available)
# Sign up: https://developer.ebay.com
# Get App ID and Cert ID from your developer account
EBAY_APP_ID=
EBAY_CERT_ID=

# Nextdoor Marketplace API (Free Tier Available)
# Sign up: https://nextdoor.com/developers
# Get API key from developer portal
NEXTDOOR_API_KEY=

# Edmunds Dealer API (Partner/Paid - Requires Dealer Partnership)
# Contact: https://developer.edmunds.com
EDMUNDS_API_KEY=

# KBB API (Partner/Paid - Requires Partnership)
# Contact Kelley Blue Book for API access
KBB_API_KEY=

# Carfax API (Partner/Paid - Requires Partnership)
# Contact Carfax for API access
CARFAX_API_KEY=

# ---------------------------------------------
# Application Settings (Optional)
# ---------------------------------------------

# Server port (Railway provides this automatically)
# PORT=8000

# Log level (debug, info, warning, error)
# LOG_LEVEL=info

# Enable/disable specific scrapers (true/false)
# ENABLE_PLAYWRIGHT=true
# ENABLE_REQUESTS=true
# ENABLE_API_CLIENTS=true

# Timeout settings (in seconds)
# SCRAPE_TIMEOUT=30
# API_TIMEOUT=10

# ---------------------------------------------
# CORS Settings (Update for Production)
# ---------------------------------------------

# Comma-separated list of allowed origins
# ALLOWED_ORIGINS=https://your-app.lovable.app,http://localhost:5173

# ---------------------------------------------
# Notes
# ---------------------------------------------

# 1. NO API KEYS REQUIRED FOR BASIC FUNCTIONALITY
#    - Backend works with web scraping alone
#    - API keys just make searches faster and more reliable

# 2. FREE API TIERS AVAILABLE
#    - eBay: 5,000 calls/day FREE
#    - Nextdoor: 100 calls/day FREE

# 3. NEVER COMMIT THIS FILE WITH REAL API KEYS
#    - Add .env to your .gitignore
#    - Use Railway's environment variables for production

# 4. TO ADD VARIABLES TO RAILWAY:
#    - Go to Railway Dashboard → Your Project
#    - Click "Variables" tab
#    - Add each variable individually
#    - Railway will auto-redeploy with new variables
```

## How to Use This File

### For Local Development:

1. **Create .env file:**
```bash
cp .env.example .env
```

2. **Add your API keys** (optional)

3. **Make sure .env is in .gitignore:**
```bash
echo ".env" >> .gitignore
```

### For Railway Deployment:

**Don't create a .env file!** Instead:

1. Go to Railway Dashboard
2. Select your project
3. Click "Variables" tab
4. Click "Add Variable"
5. Add each API key individually
6. Railway will auto-redeploy

## API Key Setup Guides

### eBay Motors (FREE)

1. Go to https://developer.ebay.com
2. Create a developer account
3. Create a new application
4. Get your App ID and Cert ID
5. Add to Railway:
   - `EBAY_APP_ID=your_app_id`
   - `EBAY_CERT_ID=your_cert_id`

### Nextdoor (FREE)

1. Go to https://nextdoor.com/developers
2. Sign up for API access
3. Create an application
4. Get your API key
5. Add to Railway:
   - `NEXTDOOR_API_KEY=your_api_key`

### Edmunds (PARTNER/PAID)

1. Contact Edmunds at https://developer.edmunds.com
2. Requires dealer partnership
3. Pricing varies by volume
4. Add to Railway:
   - `EDMUNDS_API_KEY=your_api_key`

## Testing Environment Variables

**Test if variables are loaded:**

```python
# Add to main.py temporarily
import os
print("eBay App ID:", os.getenv("EBAY_APP_ID", "Not set"))
print("Nextdoor Key:", os.getenv("NEXTDOOR_API_KEY", "Not set"))
```

**Check Railway variables:**
```bash
railway variables
```

## Security Best Practices

✅ **DO:**
- Use Railway variables for production
- Keep API keys secret
- Add .env to .gitignore
- Rotate keys periodically

❌ **DON'T:**
- Commit .env files to GitHub
- Share API keys in public channels
- Use production keys in development
- Hardcode keys in source code
