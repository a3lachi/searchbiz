"""
Data processing and export functionality for the Google Places API scraper.
"""

import json
import csv
import time
from typing import List, Dict, Optional

from .utils import sanitize_filename, format_phone_number


def extract_place_data(place_basic: Dict, place_details: Optional[Dict] = None) -> Dict:
    """
    Extract and format place data from API responses.
    
    Args:
        place_basic: Basic place data from search
        place_details: Detailed place data from details API
        
    Returns:
        Formatted dictionary with extracted data
    """
    # Start with basic data
    extracted = {
        'name': place_basic.get('name', ''),
        'place_id': place_basic.get('place_id', ''),
        'address': place_basic.get('formatted_address', ''),
        'latitude': '',
        'longitude': '',
        'rating': place_basic.get('rating', ''),
        'user_ratings_total': place_basic.get('user_ratings_total', ''),
        'phone_number': '',
        'website': ''
    }
    
    # Extract coordinates
    geometry = place_basic.get('geometry', {})
    location = geometry.get('location', {})
    extracted['latitude'] = location.get('lat', '')
    extracted['longitude'] = location.get('lng', '')
    
    # Override with detailed data if available
    if place_details:
        extracted.update({
            'name': place_details.get('name', extracted['name']),
            'address': place_details.get('formatted_address', extracted['address']),
            'rating': place_details.get('rating', extracted['rating']),
            'user_ratings_total': place_details.get('user_ratings_total', extracted['user_ratings_total']),
            'phone_number': format_phone_number(place_details.get('formatted_phone_number', '')),
            'website': place_details.get('website', '')
        })
        
        # Update coordinates from details if available
        details_geometry = place_details.get('geometry', {})
        details_location = details_geometry.get('location', {})
        if details_location:
            extracted['latitude'] = details_location.get('lat', extracted['latitude'])
            extracted['longitude'] = details_location.get('lng', extracted['longitude'])
    
    return extracted


def generate_filename(place_type: str, location: str, file_extension: str) -> str:
    """
    Generate a timestamped filename for output files.
    
    Args:
        place_type: Type of place being scraped
        location: Location being scraped
        file_extension: File extension (json, csv)
        
    Returns:
        Generated filename with timestamp
    """
    timestamp = int(time.time())
    safe_place_type = sanitize_filename(place_type)
    safe_location = sanitize_filename(location)
    
    return f"{safe_place_type}_{safe_location}_{timestamp}.{file_extension}"


def save_to_json(data: List[Dict], filename: str) -> bool:
    """
    Save data to JSON file.
    
    Args:
        data: List of dictionaries to save
        filename: Output filename
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to JSON: {e}")
        return False


def save_to_csv(data: List[Dict], filename: str) -> bool:
    """
    Save data to CSV file.
    
    Args:
        data: List of dictionaries to save
        filename: Output filename
        
    Returns:
        True if successful, False otherwise
    """
    if not data:
        print("No data to save")
        return False
        
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False


def export_data(data: List[Dict], place_type: str, location: str, formats: List[str] = None) -> Dict[str, bool]:
    """
    Export data to multiple formats.
    
    Args:
        data: Data to export
        place_type: Type of places
        location: Location searched
        formats: List of formats to export ('json', 'csv')
        
    Returns:
        Dictionary mapping format to success status
    """
    if formats is None:
        formats = ['json', 'csv']
    
    results = {}
    
    for fmt in formats:
        if fmt == 'json':
            filename = generate_filename(place_type, location, 'json')
            results['json'] = save_to_json(data, filename)
        elif fmt == 'csv':
            filename = generate_filename(place_type, location, 'csv')
            results['csv'] = save_to_csv(data, filename)
        else:
            print(f"Unsupported format: {fmt}")
            results[fmt] = False
    
    return results