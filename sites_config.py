"""
Configuration for 35+ vehicle listing sites.
Each site config includes scraping method, selectors, and parameters.
"""

FAST_SITES = [
    {
        'name': 'Facebook Marketplace',
        'base_url': 'https://www.facebook.com',
        'search_path': '/marketplace/search',
        'params': {'query': '{keyword}', 'radius': '{radius}', 'latitude': '{lat}', 'longitude': '{lon}'},
        'method': 'playwright',
        'selectors': {
            'container': 'div[data-testid="marketplace-search-result"]',
            'title': 'span',
            'price': 'span',
            'location': 'span',
            'url': 'a[href]'
        },
        'delay': 3,
        'max_pages': 2,
        'private_filter': True
    },
    {
        'name': 'Craigslist',
        'base_url': 'https://losangeles.craigslist.org',
        'search_path': '/search/cta',
        'params': {'query': '{keyword}', 'max_price': '{maxPrice}', 'search_distance': '{radius}'},
        'method': 'requests',
        'selectors': {
            'container': 'li.result-row',
            'title': 'a.result-title',
            'price': 'span.result-price',
            'location': 'span.result-hood',
            'url': 'a.result-title'
        },
        'delay': 2,
        'max_pages': 3,
        'private_filter': True
    },
    {
        'name': 'eBay Motors',
        'base_url': 'https://www.ebay.com',
        'search_path': '/sch/Cars-Trucks/6001',
        'params': {'_nkw': '{keyword}', '_udhi': '{maxPrice}'},
        'method': 'api',  # Will try API first, fallback to requests
        'selectors': {
            'container': 'li.s-item',
            'title': 'div.s-item__title',
            'price': 'span.s-item__price',
            'location': 'span.s-item__location',
            'url': 'a.s-item__link'
        },
        'delay': 2,
        'max_pages': 3,
        'private_filter': False
    },
    {
        'name': 'OfferUp',
        'base_url': 'https://offerup.com',
        'search_path': '/search',
        'params': {'q': '{keyword}', 'max_price': '{maxPrice}'},
        'method': 'playwright',
        'selectors': {
            'container': 'div[data-testid="listing-card"]',
            'title': 'h2',
            'price': 'span',
            'location': 'span',
            'url': 'a'
        },
        'delay': 3,
        'max_pages': 2,
        'private_filter': True
    },
    {
        'name': 'Autotrader',
        'base_url': 'https://www.autotrader.com',
        'search_path': '/cars-for-sale',
        'params': {'searchRadius': '{radius}', 'zip': '{zipCode}', 'listingTypes': 'USED', 'makeCodeList': '{make}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.inventory-listing',
            'title': 'h2.text-bold',
            'price': 'span.first-price',
            'location': 'div.dealer-location',
            'url': 'a.item-card'
        },
        'delay': 2,
        'max_pages': 3,
        'private_filter': True
    },
    {
        'name': 'Cars.com',
        'base_url': 'https://www.cars.com',
        'search_path': '/shopping/results',
        'params': {'stock_type': 'used', 'makes[]': '{make}', 'maximum_distance': '{radius}', 'zip': '{zipCode}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.vehicle-card',
            'title': 'h2.title',
            'price': 'span.primary-price',
            'location': 'div.miles-from',
            'url': 'a.vehicle-card-link'
        },
        'delay': 2,
        'max_pages': 3,
        'private_filter': False
    },
    {
        'name': 'CarGurus',
        'base_url': 'https://www.cargurus.com',
        'search_path': '/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action',
        'params': {'zip': '{zipCode}', 'distance': '{radius}', 'maxPrice': '{maxPrice}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.car-blade',
            'title': 'h4.car-title',
            'price': 'span.price-badge',
            'location': 'span.dealer-distance',
            'url': 'a.car-blade-link'
        },
        'delay': 2,
        'max_pages': 3,
        'private_filter': False
    },
    {
        'name': 'TrueCar',
        'base_url': 'https://www.truecar.com',
        'search_path': '/used-cars-for-sale/listings',
        'params': {'zip': '{zipCode}', 'searchRadius': '{radius}'},
        'method': 'requests',
        'selectors': {
            'container': 'div[data-test="usedListing"]',
            'title': 'span[data-test="vehicleCardHeader"]',
            'price': 'div[data-test="vehicleCardPricingBlockPrice"]',
            'location': 'div[data-test="vehicleCardLocation"]',
            'url': 'a[data-test="usedListing"]'
        },
        'delay': 2,
        'max_pages': 2,
        'private_filter': False
    },
    {
        'name': 'Carsforsale.com',
        'base_url': 'https://www.carsforsale.com',
        'search_path': '/search',
        'params': {'q': '{keyword}', 'zip': '{zipCode}', 'radius': '{radius}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.listing-item',
            'title': 'h4.listing-title',
            'price': 'span.listing-price',
            'location': 'span.listing-location',
            'url': 'a.listing-link'
        },
        'delay': 2,
        'max_pages': 3,
        'private_filter': False
    },
    {
        'name': 'Autolist',
        'base_url': 'https://www.autolist.com',
        'search_path': '/search',
        'params': {'zip': '{zipCode}', 'radius': '{radius}', 'maxPrice': '{maxPrice}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.car-listing',
            'title': 'h3.title',
            'price': 'span.price',
            'location': 'span.location',
            'url': 'a.listing-link'
        },
        'delay': 2,
        'max_pages': 2,
        'private_filter': False
    }
]

# Additional 25+ sites for FULL mode
FULL_SITES = FAST_SITES + [
    {
        'name': 'Edmunds',
        'base_url': 'https://www.edmunds.com',
        'search_path': '/inventory/srp.html',
        'params': {'zip': '{zipCode}', 'radius': '{radius}'},
        'method': 'api',  # Try API, fallback to requests
        'selectors': {
            'container': 'div.inventory-listing',
            'title': 'h3.heading-3',
            'price': 'span.heading-4',
            'location': 'span.size-14',
            'url': 'a'
        },
        'delay': 2,
        'max_pages': 2,
        'private_filter': False
    },
    {
        'name': 'Hemmings',
        'base_url': 'https://www.hemmings.com',
        'search_path': '/classifieds',
        'params': {'q': '{keyword}', 'max_price': '{maxPrice}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.listing',
            'title': 'h3.title',
            'price': 'span.price',
            'location': 'span.location',
            'url': 'a'
        },
        'delay': 2,
        'max_pages': 2,
        'private_filter': True
    },
    {
        'name': 'Bring a Trailer',
        'base_url': 'https://bringatrailer.com',
        'search_path': '/search',
        'params': {'q': '{keyword}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.listing-item',
            'title': 'h3.listing-title',
            'price': 'span.current-bid',
            'location': 'span.item-location',
            'url': 'a'
        },
        'delay': 3,
        'max_pages': 2,
        'private_filter': True
    },
    {
        'name': 'Nextdoor',
        'base_url': 'https://nextdoor.com',
        'search_path': '/for_sale_and_free',
        'params': {'query': '{keyword}'},
        'method': 'api',  # Requires API key
        'selectors': {
            'container': 'div.post-card',
            'title': 'h3',
            'price': 'span.price',
            'location': 'span.neighborhood',
            'url': 'a'
        },
        'delay': 3,
        'max_pages': 2,
        'private_filter': True
    },
    {
        'name': 'Carvana',
        'base_url': 'https://www.carvana.com',
        'search_path': '/cars',
        'params': {'zip': '{zipCode}', 'maxPrice': '{maxPrice}'},
        'method': 'requests',
        'selectors': {
            'container': 'div[data-testid="result-tile"]',
            'title': 'div.tk-heading',
            'price': 'div.price',
            'location': 'div.delivery-chip',
            'url': 'a'
        },
        'delay': 2,
        'max_pages': 2,
        'private_filter': False
    },
    {
        'name': 'CarMax',
        'base_url': 'https://www.carmax.com',
        'search_path': '/cars',
        'params': {'zip': '{zipCode}', 'distance': '{radius}'},
        'method': 'requests',
        'selectors': {
            'container': 'div.car-tile',
            'title': 'h2',
            'price': 'span.price',
            'location': 'span.store-name',
            'url': 'a'
        },
        'delay': 2,
        'max_pages': 2,
        'private_filter': False
    },
    # Add 20+ more sites (Vroom, AutoNation, CarsDirect, UsedCars, Kijiji, etc.)
    # Each following the same structure
]
