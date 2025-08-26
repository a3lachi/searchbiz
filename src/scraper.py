"""
Google Places API scraper module.
Contains the main scraping logic and API interaction.
"""

import time
import requests
from typing import List, Dict, Optional

from .config import (
    GOOGLE_PLACES_BASE_URL, PLACE_DETAIL_FIELDS,
    REQUEST_DELAY, PAGINATION_DELAY
)


class GooglePlacesScraper:
    """A scraper for Google Places API that handles pagination and data extraction."""
    
    def __init__(self, api_key: str):
        """Initialize the scraper with Google Places API key."""
        self.api_key = api_key
        self.base_url = GOOGLE_PLACES_BASE_URL
        self.session = requests.Session()
        
    def search_places(self, place_type: str, location: str, radius: int = 50000) -> List[Dict]:
        """
        Search for places of a given type in a location.
        
        Args:
            place_type: Type of place (e.g., 'restaurant', 'hospital', 'store')
            location: City name or coordinates (lat,lng)
            radius: Search radius in meters (max 50000)
        
        Returns:
            List of place dictionaries with basic info
        """
        places = []
        next_page_token = None
        
        while True:
            url = f"{self.base_url}/textsearch/json"
            params = {
                'key': self.api_key,
                'query': f"{place_type} in {location}",
                'radius': radius
            }
            
            if next_page_token:
                params['pagetoken'] = next_page_token
                # Google requires a delay between paginated requests
                time.sleep(PAGINATION_DELAY)
            
            try:
                response = self.session.get(url, params=params)
                response.raise_for_status()
                data = response.json()
                
                if data['status'] != 'OK':
                    if data['status'] == 'ZERO_RESULTS':
                        print(f"No results found for {place_type} in {location}")
                        break
                    else:
                        raise Exception(f"API error: {data['status']} - {data.get('error_message', '')}")
                
                places.extend(data.get('results', []))
                print(f"Retrieved {len(data.get('results', []))} places (total: {len(places)})")
                
                # Check for next page
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
                    
            except requests.RequestException as e:
                print(f"Network error: {e}")
                break
            except Exception as e:
                print(f"Error searching places: {e}")
                break
        
        return places
    
    def get_place_details(self, place_id: str) -> Optional[Dict]:
        """
        Get detailed information for a specific place.
        
        Args:
            place_id: Google Places ID
            
        Returns:
            Dictionary with detailed place information
        """
        url = f"{self.base_url}/details/json"
        params = {
            'key': self.api_key,
            'place_id': place_id,
            'fields': PLACE_DETAIL_FIELDS
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] != 'OK':
                print(f"Details API error for {place_id}: {data['status']}")
                return None
                
            return data.get('result')
            
        except requests.RequestException as e:
            print(f"Network error getting details for {place_id}: {e}")
            return None
        except Exception as e:
            print(f"Error getting place details for {place_id}: {e}")
            return None
    
    def scrape_places(self, place_type: str, location: str, fetch_details: bool = True, radius: int = 50000) -> List[Dict]:
        """
        Complete scraping workflow: search places and optionally fetch detailed info.
        
        Args:
            place_type: Type of place to search for
            location: City name or coordinates
            fetch_details: Whether to fetch detailed info for each place
            radius: Search radius in meters
            
        Returns:
            List of dictionaries with place data
        """
        print(f"Searching for {place_type} in {location}...")
        places_basic = self.search_places(place_type, location, radius)
        
        if not places_basic:
            return []
        
        results = []
        
        for i, place in enumerate(places_basic, 1):
            print(f"Processing place {i}/{len(places_basic)}: {place.get('name', 'Unknown')}")
            
            place_details = None
            if fetch_details:
                place_details = self.get_place_details(place['place_id'])
                # Small delay to respect API limits
                time.sleep(REQUEST_DELAY)
            
            from .data_processor import extract_place_data
            extracted_data = extract_place_data(place, place_details)
            results.append(extracted_data)
        
        return results