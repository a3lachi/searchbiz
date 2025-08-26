"""
Utility functions for the Google Places API scraper.
"""

import requests
from typing import Optional


def validate_api_key(api_key: str) -> bool:
    """
    Validate the API key by making a test request.
    
    Args:
        api_key: Google Places API key to validate
        
    Returns:
        True if the API key is valid, False otherwise
    """
    if not api_key:
        print("Error: No API key provided")
        return False
        
    test_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        'key': api_key,
        'query': 'restaurant in New York',
        'radius': 1000
    }
    
    try:
        response = requests.get(test_url, params=params)
        data = response.json()
        
        if data['status'] == 'REQUEST_DENIED':
            print("API key validation failed: Invalid or restricted key")
            return False
        elif data['status'] == 'OVER_QUERY_LIMIT':
            print("API key validation failed: Quota exceeded")
            return False
        elif data['status'] in ['OK', 'ZERO_RESULTS']:
            return True
        else:
            print(f"API key validation uncertain: {data['status']}")
            return True  # Allow to proceed as it might work
            
    except Exception as e:
        print(f"Error validating API key: {e}")
        return False


def sanitize_filename(text: str) -> str:
    """
    Sanitize a string to be safe for use as a filename.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized string safe for filenames
    """
    # Replace problematic characters with underscores
    sanitized = text.replace(' ', '_').replace(',', '_').replace('/', '_')
    # Remove any remaining problematic characters
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c in ('_', '-'))
    return sanitized.lower()


def get_coordinates_from_string(location_str: str) -> Optional[tuple]:
    """
    Extract latitude and longitude from a location string if it contains coordinates.
    
    Args:
        location_str: Location string that might contain coordinates
        
    Returns:
        Tuple of (lat, lng) if coordinates found, None otherwise
    """
    try:
        # Check if the string looks like coordinates (lat,lng)
        if ',' in location_str:
            parts = location_str.split(',')
            if len(parts) == 2:
                lat = float(parts[0].strip())
                lng = float(parts[1].strip())
                # Basic validation for coordinate ranges
                if -90 <= lat <= 90 and -180 <= lng <= 180:
                    return (lat, lng)
    except (ValueError, AttributeError):
        pass
    
    return None


def format_phone_number(phone: str) -> str:
    """
    Format phone number for consistent display.
    
    Args:
        phone: Raw phone number string
        
    Returns:
        Formatted phone number
    """
    if not phone:
        return ""
    
    # Remove common separators and spaces
    cleaned = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # If it starts with +, keep the + format
    if phone.startswith('+'):
        return phone
    
    return cleaned