"""
Hybrid scraping engine for vehicle listings.
Supports Playwright (JS-heavy sites), Requests (static HTML), and API integrations.
"""

import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import random
from datetime import datetime
from sites_config import FAST_SITES, FULL_SITES
from api_clients import EbayAPIClient, NextdoorAPIClient, EdmundsAPIClient
from utils import extract_number, deduplicate_vehicles, passes_filters, normalize_location

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

def build_search_url(site: dict, params) -> str:
    """Build search URL with parameters"""
    url = site['base_url'] + site['search_path']
    
    # Replace placeholders in params
    query_params = []
    for key, value in site['params'].items():
        param_value = value
        if '{keyword}' in value:
            param_value = param_value.replace('{keyword}', params.keyword)
        if '{location}' in value:
            param_value = param_value.replace('{location}', params.location)
        if '{maxPrice}' in value:
            param_value = param_value.replace('{maxPrice}', str(params.maxPrice))
        if '{radius}' in value:
            param_value = param_value.replace('{radius}', str(params.radius or 50))
        if '{zipCode}' in value and params.zipCode:
            param_value = param_value.replace('{zipCode}', params.zipCode)
        if '{make}' in value and params.make:
            param_value = param_value.replace('{make}', params.make)
        
        query_params.append(f"{key}={param_value}")
    
    if query_params:
        url += '?' + '&'.join(query_params)
    
    return url

def extract_vehicle_data(container, selectors: dict, source: str) -> dict:
    """Extract vehicle data from HTML container"""
    try:
        title_elem = container.select_one(selectors['title'])
        price_elem = container.select_one(selectors['price'])
        location_elem = container.select_one(selectors['location'])
        url_elem = container.select_one(selectors['url'])
        
        if not title_elem or not price_elem:
            return None
        
        title = title_elem.get_text(strip=True)
        price_text = price_elem.get_text(strip=True)
        price = extract_number(price_text)
        location = location_elem.get_text(strip=True) if location_elem else 'Unknown'
        url = url_elem.get('href', '') if url_elem else ''
        
        # Make URL absolute
        if url and not url.startswith('http'):
            url = 'https://' + url.lstrip('/')
        
        vehicle = {
            'id': f"{source}_{hash(url)}",
            'source': source,
            'title': title,
            'price': price,
            'location': normalize_location(location),
            'url': url,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        return vehicle
    except Exception as e:
        print(f"Error extracting vehicle data: {e}")
        return None

async def scrape_playwright(site: dict, params) -> list:
    """Scrape JavaScript-heavy sites using Playwright"""
    vehicles = []
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=random.choice(USER_AGENTS),
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            
            url = build_search_url(site, params)
            print(f"Scraping {site['name']}: {url}")
            
            await page.goto(url, wait_until='networkidle', timeout=15000)
            await asyncio.sleep(site['delay'])
            
            content = await page.content()
            soup = BeautifulSoup(content, 'lxml')
            
            containers = soup.select(site['selectors']['container'])
            print(f"Found {len(containers)} containers on {site['name']}")
            
            for container in containers[:20]:  # Limit to 20 results per site
                vehicle = extract_vehicle_data(container, site['selectors'], site['name'])
                if vehicle and passes_filters(vehicle, params):
                    vehicles.append(vehicle)
            
            await browser.close()
    
    except Exception as e:
        print(f"Error scraping {site['name']} with Playwright: {e}")
    
    return vehicles

def scrape_requests(site: dict, params) -> list:
    """Scrape static HTML sites using requests"""
    vehicles = []
    
    try:
        url = build_search_url(site, params)
        print(f"Scraping {site['name']}: {url}")
        
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'lxml')
        containers = soup.select(site['selectors']['container'])
        print(f"Found {len(containers)} containers on {site['name']}")
        
        for container in containers[:20]:  # Limit to 20 results per site
            vehicle = extract_vehicle_data(container, site['selectors'], site['name'])
            if vehicle and passes_filters(vehicle, params):
                vehicles.append(vehicle)
    
    except Exception as e:
        print(f"Error scraping {site['name']} with requests: {e}")
    
    return vehicles

async def search_all_sites(params, total_sites: int = 10):
    """
    Main orchestrator - search all configured sites and stream results.
    Yields progress and result events.
    """
    sites = FAST_SITES[:total_sites] if total_sites <= 10 else FULL_SITES[:total_sites]
    all_vehicles = []
    
    # Initialize API clients
    ebay_client = EbayAPIClient()
    nextdoor_client = NextdoorAPIClient()
    edmunds_client = EdmundsAPIClient()
    
    for idx, site in enumerate(sites, 1):
        # Send progress event
        yield {
            'type': 'progress',
            'current': idx,
            'total': len(sites),
            'site': site['name']
        }
        
        vehicles = []
        
        try:
            # Try API first if configured
            if site['name'] == 'eBay Motors' and ebay_client.is_configured():
                print(f"Using eBay API for {site['name']}")
                vehicles = await ebay_client.search_vehicles(params)
            elif site['name'] == 'Nextdoor' and nextdoor_client.is_configured():
                print(f"Using Nextdoor API for {site['name']}")
                vehicles = await nextdoor_client.search_marketplace(params)
            elif site['name'] == 'Edmunds' and edmunds_client.is_configured():
                print(f"Using Edmunds API for {site['name']}")
                vehicles = await edmunds_client.search_inventory(params)
            # Fallback to scraping
            elif site['method'] == 'playwright':
                vehicles = await scrape_playwright(site, params)
            else:
                vehicles = scrape_requests(site, params)
            
            # Stream each vehicle as found
            for vehicle in vehicles:
                all_vehicles.append(vehicle)
                yield {
                    'type': 'result',
                    'vehicle': vehicle
                }
        
        except Exception as e:
            print(f"Site {site['name']} failed: {e}")
        
        # Random delay between sites to be polite
        await asyncio.sleep(random.uniform(1.0, 2.5))
    
    # Final deduplication
    unique_vehicles = deduplicate_vehicles(all_vehicles)
    print(f"Total found: {len(all_vehicles)}, Unique: {len(unique_vehicles)}")
