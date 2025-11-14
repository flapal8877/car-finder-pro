# CarFinder Pro - Frontend

A modern, real-time vehicle sourcing tool that searches 35+ marketplaces for private-party deals. Built with React, TypeScript, and Tailwind CSS.

## Features

- 🚗 **Multi-Source Search**: Searches Facebook Marketplace, Craigslist, eBay Motors, and 30+ more platforms
- ⚡ **Real-Time Progress**: Live updates showing which sites are being searched
- 📊 **Smart Results**: Sortable table with filtering capabilities
- 📥 **Export to CSV**: One-click export of all results with timestamp
- 🎨 **Beautiful UI**: Modern gradient design with dark mode support
- 📱 **Responsive**: Works perfectly on mobile, tablet, and desktop

## Setup

### 1. Configure Railway Backend URL

Create a `.env` file in the root directory:

```bash
VITE_RAILWAY_API_URL=https://your-app.railway.app
```

Or use the in-app configuration dialog if you haven't set an environment variable.

### 2. Install Dependencies

```bash
npm install
```

### 3. Run Development Server

```bash
npm run dev
```

## Railway Backend Requirements

Your Railway Python backend should expose the following endpoint:

### `POST /api/search`

**Request Body:**
```json
{
  "keyword": "Honda Civic",
  "location": "Los Angeles, CA",
  "maxPrice": 25000
}
```

**Response:** Server-Sent Events (SSE) stream

**Progress Events:**
```
data: {"type": "progress", "current": 5, "total": 35, "site": "Facebook Marketplace"}
```

**Result Events:**
```
data: {"type": "result", "vehicle": {
  "id": "unique-id",
  "source": "Facebook Marketplace",
  "title": "2020 Honda Civic",
  "price": 18500,
  "location": "Los Angeles, CA",
  "url": "https://...",
  "timestamp": "2025-01-14T12:00:00Z"
}}
```

## Project Structure

```
src/
├── components/
│   ├── SearchForm.tsx          # Search input form
│   ├── ProgressIndicator.tsx   # Real-time progress bar
│   ├── ResultsTable.tsx        # Sortable results table
│   └── ApiConfigBanner.tsx     # API configuration UI
├── services/
│   └── api.ts                  # Railway API client
├── types/
│   └── vehicle.ts              # TypeScript interfaces
└── pages/
    └── Index.tsx               # Main application page
```

## Technologies

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Shadcn/ui** - UI components
- **Lucide React** - Icons
- **Vite** - Build tool

## Deployment

Deploy the frontend on Lovable by clicking Share → Publish. The Railway backend handles all scraping and API calls.

## Project Info

**Lovable Project URL**: https://lovable.dev/projects/b4186dfd-9803-49fc-96aa-666ceca7f0f7
