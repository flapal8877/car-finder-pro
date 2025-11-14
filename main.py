from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import json
from scrapers import search_all_sites

app = FastAPI(title="CarFinder Pro API", version="2.0")

# CORS - Allow your Lovable frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to specific domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchParams(BaseModel):
    keyword: str
    location: str
    maxPrice: int
    make: Optional[str] = None
    model: Optional[str] = None
    minYear: Optional[int] = None
    maxYear: Optional[int] = None
    maxMileage: Optional[int] = None
    zipCode: Optional[str] = None
    radius: Optional[int] = 50
    bodyStyles: Optional[List[str]] = None
    condition: Optional[str] = None
    fuelTypes: Optional[List[str]] = None
    privateOnly: Optional[bool] = False
    searchMode: Optional[str] = 'fast'

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "CarFinder Pro API",
        "version": "2.0",
        "endpoints": ["/api/search"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/search")
async def search_vehicles(params: SearchParams):
    """
    Stream vehicle search results using Server-Sent Events (SSE).
    
    Event types:
    - progress: {type: 'progress', current: int, total: int, site: str}
    - result: {type: 'result', vehicle: {...}}
    - complete: {type: 'complete'}
    - error: {type: 'error', message: str}
    """
    async def event_generator():
        try:
            total_sites = 35 if params.searchMode == 'full' else 10
            
            async for event in search_all_sites(params, total_sites):
                if event['type'] in ['progress', 'result']:
                    yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0.05)  # Small delay for smooth streaming
            
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"
            
        except Exception as e:
            print(f"Search error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
