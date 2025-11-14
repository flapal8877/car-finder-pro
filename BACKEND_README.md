# CarFinder Pro Backend

Python FastAPI backend for CarFinder Pro - searches 35+ vehicle marketplaces and returns real-time results via streaming API.

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Railway account (for deployment)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/flapal8877/Car-finder-backend.git
cd Car-finder-backend
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

3. **Create environment file** (optional)
```bash
cp .env.example .env
# Add your API keys if you have them
```

4. **Run the server**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

5. **Test the API**
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

## 📦 Project Structure

```
Car-finder-backend/
├── main.py              # FastAPI application & endpoints
├── scrapers.py          # Web scraping orchestration
├── sites_config.py      # Configuration for 35+ sites
├── api_clients.py       # API integrations (eBay, Nextdoor, Edmunds)
├── utils.py             # Helper functions
├── requirements.txt     # Python dependencies
├── Procfile            # Railway deployment config
├── railway.json        # Railway build configuration
└── .env.example        # Environment variable template
```

## 🌐 API Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{"status": "healthy"}
```

### Search Vehicles
```http
POST /api/search
Content-Type: application/json
```

**Request Body:**
```json
{
  "keyword": "Honda Civic",
  "location": "Los Angeles, CA",
  "maxPrice": 25000,
  "searchMode": "fast",
  "make": "Honda",
  "model": "Civic",
  "minYear": 2018,
  "maxYear": 2024,
  "maxMileage": 50000,
  "zipCode": "90210",
  "radius": 50,
  "bodyStyles": ["sedan"],
  "condition": "used",
  "fuelTypes": ["gasoline"],
  "privateOnly": false
}
```

**Response:** Server-Sent Events (SSE) stream

**Event Types:**
- `progress`: `{"type": "progress", "current": 1, "total": 10, "site": "Craigslist"}`
- `result`: `{"type": "result", "vehicle": {...}}`
- `complete`: `{"type": "complete"}`
- `error`: `{"type": "error", "message": "..."}`

## 🔧 Configuration

### Environment Variables (Optional)

API keys are optional but improve speed and results:

```bash
# eBay Motors API (Free - 5,000 calls/day)
EBAY_APP_ID=your_ebay_app_id
EBAY_CERT_ID=your_ebay_cert_id

# Nextdoor API (Free - 100 calls/day)
NEXTDOOR_API_KEY=your_nextdoor_api_key

# Edmunds API (Partner/Paid)
EDMUNDS_API_KEY=your_edmunds_api_key

# KBB API (Partner/Paid)
KBB_API_KEY=your_kbb_api_key

# Carfax API (Partner/Paid)
CARFAX_API_KEY=your_carfax_api_key
```

### Search Modes

- **Fast Mode** (`searchMode: "fast"`): Searches 10 major sites (~15-30 seconds)
- **Full Mode** (`searchMode: "full"`): Searches all 35+ sites (~30-60 seconds)

## 🚂 Railway Deployment

### Quick Deploy

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login to Railway**
```bash
railway login
```

3. **Initialize project**
```bash
railway init
```

4. **Deploy**
```bash
railway up
```

5. **Generate public URL**
```bash
railway domain
```

6. **Copy your URL** (e.g., `https://car-finder-backend-production.up.railway.app`)

### Important: Fix Procfile

**Your Procfile is named `Procfile.txt` - this is WRONG!**

Railway requires the file to be named exactly `Procfile` (no extension).

**To fix:**
1. Rename `Procfile.txt` to `Procfile`
2. Commit and push:
```bash
git mv Procfile.txt Procfile
git commit -m "Fix Procfile name"
git push
```

### Adding Environment Variables to Railway

1. Go to Railway Dashboard → Your Project
2. Click "Variables" tab
3. Add your API keys (optional)
4. Railway will auto-redeploy

### Troubleshooting Railway Builds

**Build fails with Python version error:**
- Solution: Railway auto-detects Python 3.13 from requirements.txt versions
- If issues persist, add `runtime.txt` with content: `python-3.13`

**Playwright installation timeout:**
- Normal behavior - Railway may take 3-5 minutes to install Chromium
- The build will retry automatically

**Port binding error:**
- Make sure `Procfile` uses: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Railway automatically provides the `$PORT` variable

## 🔍 Supported Sites

### Fast Mode (10 sites)
- Craigslist
- Facebook Marketplace
- eBay Motors (API)
- Cars.com
- Autotrader
- CarGurus
- OfferUp
- TrueCar
- Carsforsale.com
- Autolist

### Full Mode (35+ sites)
All Fast Mode sites plus:
- Nextdoor (API)
- Edmunds (API)
- Carvana
- CarMax
- Vroom
- Shift
- Hemmings
- Bring a Trailer
- And 17 more specialized marketplaces

## 📊 Performance

**Without API Keys:**
- Fast Mode: ~20-30 seconds
- Full Mode: ~45-60 seconds

**With API Keys:**
- Fast Mode: ~10-20 seconds  
- Full Mode: ~30-45 seconds

## 🧪 Testing

**Test Health Endpoint:**
```bash
curl https://your-railway-url.railway.app/health
```

**Test Search (with curl):**
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

**Test Search (with Python):**
```python
import requests
import json

url = "https://your-railway-url.railway.app/api/search"
data = {
    "keyword": "Honda Civic",
    "location": "Los Angeles",
    "maxPrice": 25000,
    "searchMode": "fast"
}

response = requests.post(url, json=data, stream=True)
for line in response.iter_lines():
    if line:
        event = json.loads(line.decode('utf-8').replace('data: ', ''))
        print(event)
```

## 💰 Cost Estimate

**Railway Hosting:**
- Hobby Plan: $5/month
- Includes 500 hours runtime + $5 usage credit
- Covers ~100-500 searches per day

**API Costs:**
- eBay Motors: FREE (5,000 calls/day)
- Nextdoor: FREE (100 calls/day)
- Edmunds: Partner pricing (contact Edmunds)
- KBB: Partner pricing (contact KBB)
- Carfax: Partner pricing (contact Carfax)

**Total Cost:** $5-10/month for typical usage

## 🔒 Security

**CORS Configuration:**
Update `main.py` line 13 for production:
```python
allow_origins=["https://your-lovable-domain.lovable.app"]
```

**Rate Limiting:**
Consider adding rate limiting for production:
```bash
pip install slowapi
```

## 🤝 Frontend Integration

This backend is designed to work with the CarFinder Pro Lovable frontend.

**Frontend Setup:**
1. Add environment variable in Lovable: `VITE_RAILWAY_API_URL`
2. Set value to your Railway URL: `https://your-app.railway.app`
3. Redeploy frontend

**Or use the API config banner in the UI.**

## 📝 Dependencies

All dependencies are Python 3.13 compatible:

- `fastapi==0.115.0` - Modern web framework
- `uvicorn[standard]==0.32.0` - ASGI server
- `playwright==1.48.0` - Browser automation
- `beautifulsoup4==4.12.3` - HTML parsing
- `lxml==5.3.0` - XML/HTML processing
- `requests==2.32.3` - HTTP library
- `python-dotenv==1.0.1` - Environment variables
- `fuzzywuzzy==0.18.0` - Fuzzy string matching
- `python-Levenshtein==0.25.1` - String similarity
- `requests-oauthlib==2.0.0` - OAuth support
- `httpx==0.27.2` - Async HTTP client
- `pydantic==2.9.2` - Data validation

## 📚 Additional Documentation

- [RAILWAY_SETUP.md](./RAILWAY_SETUP.md) - Detailed Railway deployment guide
- [Frontend Repository](https://github.com/yourusername/carfinder-pro) - Lovable frontend

## 🐛 Issues & Support

**Common Issues:**

1. **No results found** - Some sites may block scrapers intermittently
2. **Slow searches** - Add API keys to improve speed
3. **CORS errors** - Update `allow_origins` in main.py

**Getting Help:**
- Check Railway logs: Dashboard → Deployments → Logs
- Review [RAILWAY_SETUP.md](./RAILWAY_SETUP.md) troubleshooting section

## 📄 License

MIT License - feel free to use for personal or commercial projects.

---

## 🎯 Quick Deploy Checklist

- [ ] Rename `Procfile.txt` to `Procfile`
- [ ] Push to GitHub
- [ ] Deploy to Railway (`railway up`)
- [ ] Generate domain (`railway domain`)
- [ ] Test health endpoint
- [ ] Add environment variables (optional)
- [ ] Update frontend with backend URL
- [ ] Test search functionality

**Your Backend URL:** `_______________________` (fill in after deployment)
