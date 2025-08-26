"""
Configuration settings and constants for the Google Places API scraper.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
GOOGLE_PLACES_BASE_URL = "https://maps.googleapis.com/maps/api/place"

# Default scraping parameters
DEFAULT_RADIUS = 50000  # meters
DEFAULT_PLACE_TYPE = "business"
DEFAULT_LOCATION = "La Défense"
DEFAULT_FETCH_DETAILS = True

# API Rate limiting
REQUEST_DELAY = 0.1  # seconds between detail requests
PAGINATION_DELAY = 2  # seconds between paginated requests

# Place details fields to fetch
PLACE_DETAIL_FIELDS = (
    "name,formatted_address,geometry,rating,user_ratings_total,"
    "formatted_phone_number,website,place_id"
)

# Output configuration
OUTPUT_FORMATS = ['json', 'csv']
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"

# Supported place types (common ones)
COMMON_PLACE_TYPES = [
    'restaurant', 'hotel', 'gas_station', 'hospital', 'pharmacy',
    'bank', 'store', 'gym', 'school', 'business', 'cafe', 'bar',
    'shopping_mall', 'supermarket', 'tourist_attraction'
]