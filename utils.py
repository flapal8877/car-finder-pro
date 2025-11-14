"""
Utility functions for vehicle search and deduplication.
"""

import re
from fuzzywuzzy import fuzz
from typing import List, Dict

def extract_number(text: str) -> int:
    """Extract numeric value from price/mileage strings"""
    if not text:
        return 0
    
    # Remove common currency symbols and text
    clean = text.replace('$', '').replace(',', '').replace('K', '000')
    
    # Find all numbers
    numbers = re.findall(r'\d+', clean)
    if numbers:
        return int(numbers[0])
    
    return 0

def normalize_location(location: str) -> str:
    """Standardize location strings"""
    if not location:
        return 'Unknown'
    
    # Remove extra whitespace and parentheses
    location = re.sub(r'\s+', ' ', location.strip())
    location = location.replace('(', '').replace(')', '')
    
    return location

def validate_zip(zip_code: str) -> bool:
    """Validate ZIP code format"""
    if not zip_code:
        return False
    
    # US ZIP code: 5 digits or 5+4 format
    pattern = r'^\d{5}(-\d{4})?$'
    return bool(re.match(pattern, zip_code))

def passes_filters(vehicle: Dict, params) -> bool:
    """Apply search filters to vehicle listing"""
    
    # Price filter
    if vehicle['price'] > params.maxPrice:
        return False
    
    if vehicle['price'] < 100:  # Skip obviously wrong prices
        return False
    
    # Private seller filter
    if params.privateOnly:
        dealer_keywords = ['dealer', 'dealership', 'auto sales', 'motors inc']
        title_lower = vehicle.get('title', '').lower()
        location_lower = vehicle.get('location', '').lower()
        
        for keyword in dealer_keywords:
            if keyword in title_lower or keyword in location_lower:
                return False
    
    # Make filter
    if params.make:
        if params.make.lower() not in vehicle.get('title', '').lower():
            return False
    
    # Model filter
    if params.model:
        if params.model.lower() not in vehicle.get('title', '').lower():
            return False
    
    # Year filters (if year is in title)
    if params.minYear or params.maxYear:
        years = re.findall(r'\b(19\d{2}|20\d{2})\b', vehicle.get('title', ''))
        if years:
            year = int(years[0])
            if params.minYear and year < params.minYear:
                return False
            if params.maxYear and year > params.maxYear:
                return False
    
    # Body style filter
    if params.bodyStyles:
        title_lower = vehicle.get('title', '').lower()
        has_match = any(style.lower() in title_lower for style in params.bodyStyles)
        if not has_match:
            return False
    
    # Fuel type filter
    if params.fuelTypes:
        title_lower = vehicle.get('title', '').lower()
        fuel_keywords = {
            'Electric': ['electric', 'ev', 'tesla'],
            'Hybrid': ['hybrid', 'plug-in'],
            'Diesel': ['diesel', 'tdi'],
        }
        
        has_match = False
        for fuel_type in params.fuelTypes:
            keywords = fuel_keywords.get(fuel_type, [fuel_type.lower()])
            if any(kw in title_lower for kw in keywords):
                has_match = True
                break
        
        if not has_match and params.fuelTypes != ['Gas']:
            return False
    
    return True

def deduplicate_vehicles(vehicles: List[Dict]) -> List[Dict]:
    """
    Remove duplicate listings using fuzzy string matching.
    Compares title + price + location with 85% similarity threshold.
    """
    unique = []
    
    for vehicle in vehicles:
        signature = f"{vehicle['title']}|{vehicle['price']}|{vehicle['location']}"
        
        is_duplicate = False
        for existing in unique:
            existing_sig = f"{existing['title']}|{existing['price']}|{existing['location']}"
            
            # Fuzzy match with 85% threshold
            similarity = fuzz.ratio(signature, existing_sig)
            if similarity > 85:
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique.append(vehicle)
    
    return unique

def format_price(price: int) -> str:
    """Format price as currency string"""
    return f"${price:,}"

def calculate_distance(zip1: str, zip2: str) -> float:
    """
    Calculate distance between ZIP codes (placeholder).
    In production, use a geocoding API like Google Maps or Mapbox.
    """
    # TODO: Implement actual distance calculation
    return 0.0
