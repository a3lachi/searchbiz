#!/usr/bin/env python3
"""
Google Places API Scraper
A lightweight MVP for scraping business data using Google Places API.

Main entry point that coordinates the scraping workflow.
"""

from src.config import (
    GOOGLE_MAPS_API_KEY, DEFAULT_PLACE_TYPE, DEFAULT_LOCATION, 
    DEFAULT_FETCH_DETAILS, DEFAULT_RADIUS
)
from src.scraper import GooglePlacesScraper
from src.data_processor import export_data
from src.utils import validate_api_key


def main():
    """Main function to run the scraper."""
    # Get API key from config
    api_key = GOOGLE_MAPS_API_KEY
    if not api_key:
        print("Error: GOOGLE_MAPS_API_KEY not found in environment variables.")
        print("Please create a .env file with your API key.")
        return
    
    # Validate API key
    print("Validating API key...")
    if not validate_api_key(api_key):
        return
    print("API key validated successfully!")
    
    # Initialize scraper
    scraper = GooglePlacesScraper(api_key)
    
    # Configuration (modify these as needed)
    place_type = DEFAULT_PLACE_TYPE
    location = DEFAULT_LOCATION
    fetch_details = DEFAULT_FETCH_DETAILS
    radius = DEFAULT_RADIUS
    
    # Run scraping
    try:
        results = scraper.scrape_places(place_type, location, fetch_details, radius)
        
        if results:
            # Export results using the data processor
            export_results = export_data(results, place_type, location)
            
            print(f"\nScraping completed successfully!")
            print(f"Found {len(results)} {place_type}s in {location}")
            
            # Report export status
            for format_type, success in export_results.items():
                status = "✓" if success else "✗"
                print(f"{status} {format_type.upper()} export {'successful' if success else 'failed'}")
        else:
            print("No results found.")
            
    except KeyboardInterrupt:
        print("\nScraping interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()