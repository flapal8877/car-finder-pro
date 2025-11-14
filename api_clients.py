"""
API client integrations for vehicle listing platforms.
Handles OAuth authentication and API calls for eBay, Nextdoor, Edmunds, etc.
"""

import os
import requests
from requests_oauthlib import OAuth2Session
from typing import List, Dict, Optional
import asyncio
import httpx

class EbayAPIClient:
    """eBay Motors Finding API with OAuth 2.0 client credentials flow"""
    
    def __init__(self):
        self.client_id = os.getenv('EBAY_APP_ID')
        self.client_secret = os.getenv('EBAY_CERT_ID')
        self.base_url = 'https://svcs.ebay.com/services/search/FindingService/v1'
        self.access_token = None
    
    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret)
    
    async def get_access_token(self) -> Optional[str]:
        """Get OAuth 2.0 access token"""
        if not self.is_configured():
            return None
        
        try:
            auth_url = 'https://api.ebay.com/identity/v1/oauth2/token'
            data = {
                'grant_type': 'client_credentials',
                'scope': 'https://api.ebay.com/oauth/api_scope'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    auth_url,
                    data=data,
                    auth=(self.client_id, self.client_secret)
                )
                
                if response.status_code == 200:
                    self.access_token = response.json()['access_token']
                    return self.access_token
        except Exception as e:
            print(f"eBay OAuth error: {e}")
        
        return None
    
    async def search_vehicles(self, params) -> List[Dict]:
        """
        Search eBay Motors for vehicles matching criteria.
        Returns list of vehicle dicts.
        """
        if not await self.get_access_token():
            return []
        
        try:
            search_params = {
                'OPERATION-NAME': 'findItemsAdvanced',
                'SERVICE-VERSION': '1.0.0',
                'SECURITY-APPNAME': self.client_id,
                'RESPONSE-DATA-FORMAT': 'JSON',
                'REST-PAYLOAD': '',
                'keywords': params.keyword,
                'categoryId': '6001',  # Cars & Trucks
                'itemFilter(0).name': 'MaxPrice',
                'itemFilter(0).value': str(params.maxPrice),
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(self.base_url, params=search_params)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('findItemsAdvancedResponse', [{}])[0].get('searchResult', [{}])[0].get('item', [])
                    
                    vehicles = []
                    for item in items[:20]:
                        vehicle = {
                            'id': item.get('itemId', [''])[0],
                            'source': 'eBay Motors',
                            'title': item.get('title', [''])[0],
                            'price': int(float(item.get('sellingStatus', [{}])[0].get('currentPrice', [{}])[0].get('__value__', 0))),
                            'location': item.get('location', [''])[0],
                            'url': item.get('viewItemURL', [''])[0],
                            'imageUrl': item.get('galleryURL', [''])[0],
                            'timestamp': item.get('listingInfo', [{}])[0].get('startTime', [''])[0]
                        }
                        vehicles.append(vehicle)
                    
                    return vehicles
        except Exception as e:
            print(f"eBay API search error: {e}")
        
        return []


class NextdoorAPIClient:
    """Nextdoor Search API with Bearer token authentication"""
    
    def __init__(self):
        self.api_key = os.getenv('NEXTDOOR_API_KEY')
        self.base_url = 'https://api.nextdoor.com/v1'
    
    def is_configured(self) -> bool:
        return bool(self.api_key)
    
    async def search_marketplace(self, params) -> List[Dict]:
        """
        Search Nextdoor marketplace for local vehicle listings.
        """
        if not self.is_configured():
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Nextdoor requires geolocation
            search_params = {
                'query': params.keyword,
                'category': 'FOR_SALE',
                'max_price': params.maxPrice,
                'limit': 20
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'{self.base_url}/marketplace/search',
                    headers=headers,
                    params=search_params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('results', [])
                    
                    vehicles = []
                    for item in items:
                        vehicle = {
                            'id': item.get('id'),
                            'source': 'Nextdoor',
                            'title': item.get('title'),
                            'price': int(item.get('price', 0)),
                            'location': item.get('neighborhood'),
                            'url': item.get('url'),
                            'imageUrl': item.get('photos', [{}])[0].get('url'),
                            'description': item.get('description'),
                            'timestamp': item.get('created_at')
                        }
                        vehicles.append(vehicle)
                    
                    return vehicles
        except Exception as e:
            print(f"Nextdoor API error: {e}")
        
        return []


class EdmundsAPIClient:
    """Edmunds Inventory API (OAuth 2.0) - Dealer partnership required"""
    
    def __init__(self):
        self.client_id = os.getenv('EDMUNDS_CLIENT_ID')
        self.client_secret = os.getenv('EDMUNDS_CLIENT_SECRET')
        self.base_url = 'https://api.edmunds.com/api/inventory/v2'
        self.access_token = None
    
    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret)
    
    async def get_access_token(self) -> Optional[str]:
        """Get OAuth 2.0 access token"""
        if not self.is_configured():
            return None
        
        try:
            auth_url = 'https://api.edmunds.com/oauth/token'
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'client_credentials'
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(auth_url, data=data)
                
                if response.status_code == 200:
                    self.access_token = response.json()['access_token']
                    return self.access_token
        except Exception as e:
            print(f"Edmunds OAuth error: {e}")
        
        return None
    
    async def search_inventory(self, params) -> List[Dict]:
        """
        Search Edmunds dealer inventory.
        Note: Requires dealer partnership account.
        """
        if not await self.get_access_token():
            return []
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}'
            }
            
            search_params = {
                'zip': params.zipCode or params.location,
                'radius': params.radius,
                'pagesize': 20
            }
            
            if params.make:
                search_params['make'] = params.make
            if params.model:
                search_params['model'] = params.model
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'{self.base_url}/inventories',
                    headers=headers,
                    params=search_params
                )
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('results', [])
                    
                    vehicles = []
                    for item in items:
                        vehicle = {
                            'id': item.get('vin'),
                            'source': 'Edmunds',
                            'title': f"{item.get('year')} {item.get('make')} {item.get('model')}",
                            'price': int(item.get('price', {}).get('total', 0)),
                            'location': item.get('dealer', {}).get('city'),
                            'url': item.get('link'),
                            'imageUrl': item.get('photos', [{}])[0].get('url'),
                            'timestamp': item.get('inventoryDate')
                        }
                        vehicles.append(vehicle)
                    
                    return vehicles
        except Exception as e:
            print(f"Edmunds API error: {e}")
        
        return []
