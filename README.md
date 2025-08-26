# Google Places API Scraper

A lightweight Python MVP for scraping business data using the Google Places API. This scraper can fetch detailed information about places (restaurants, stores, hospitals, etc.) in any location and export the results to CSV or JSON format.

## Features

- 🔍 Search for places by type and location
- 📄 Handle API pagination (up to 60 results per search)
- 📊 Extract detailed place information including:
  - Name and address
  - Coordinates (latitude/longitude)
  - Rating and review count
  - Phone number and website
  - Place ID
- 💾 Export results to CSV or JSON
- 🔒 Secure API key management with `.env` file
- ⚠️ Built-in error handling and rate limiting
- 🧹 Clean, modular code structure

## Requirements

- Python 3.7+
- Google Places API key
- Required packages: `requests`, `python-dotenv`

## Setup Instructions

### 1. Get a Google Places API Key

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Places API** for your project
4. Create credentials (API key)
5. (Optional but recommended) Restrict the API key to Places API only

### 2. Install Dependencies

```bash
pip install requests python-dotenv
```

### 3. Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API key:
   ```
   GOOGLE_MAPS_API_KEY=your_actual_api_key_here
   ```

## Usage

### Basic Usage

Run the scraper with default settings:

```bash
python places_scraper.py
```

### Customizing the Search

Edit the configuration in `src/config.py`:

```python
# Default scraping parameters
DEFAULT_PLACE_TYPE = "business"  # Change to: restaurant, hotel, pharmacy, etc.
DEFAULT_LOCATION = "La Défense"  # Change to any city or coordinates
DEFAULT_FETCH_DETAILS = True     # Set False for faster scraping without details
```

### Supported Place Types

Common place types include:
- `restaurant`
- `hotel`
- `gas_station`
- `hospital`
- `pharmacy`
- `bank`
- `store`
- `gym`
- `school`

For a complete list, see the [Google Places API documentation](https://developers.google.com/maps/documentation/places/web-service/supported_types).

### Location Formats

You can specify locations as:
- City names: `"New York, NY"`, `"London, UK"`
- Coordinates: `"40.7128,-74.0060"` (latitude,longitude)
- Addresses: `"Times Square, New York"`

## Output

The scraper generates two files with timestamps:
- `{place_type}_{location}_{timestamp}.json` - JSON format
- `{place_type}_{location}_{timestamp}.csv` - CSV format

### Sample Output Structure

```json
[
  {
    "name": "Joe's Pizza",
    "place_id": "ChIJXxXxXxXxXxXxXxXxXxXxXxX",
    "address": "123 Main St, New York, NY 10001, USA",
    "latitude": 40.7128,
    "longitude": -74.0060,
    "rating": 4.5,
    "user_ratings_total": 1234,
    "phone_number": "+1 212-555-0123",
    "website": "https://www.joespizza.com"
  }
]
```

## Error Handling

The scraper handles common API errors:

- **Invalid API Key**: Validates key before starting
- **Quota Exceeded**: Stops gracefully with error message
- **Network Issues**: Retries and continues with available data
- **No Results**: Reports when no places are found
- **Rate Limiting**: Includes delays between requests

## API Limits

- Google Places API has usage quotas and billing
- Text Search: $32 per 1000 requests
- Place Details: $17 per 1000 requests
- The scraper includes delays to respect rate limits
- Monitor your usage in the Google Cloud Console

## Customization

### Advanced Usage

You can also use the `GooglePlacesScraper` class directly:

```python
from places_scraper import GooglePlacesScraper

# Initialize scraper
scraper = GooglePlacesScraper("your_api_key")

# Search for places
results = scraper.scrape_places("coffee shop", "Seattle, WA")

# Save results
scraper.save_to_csv(results, "coffee_shops.csv")
```

### Configuration Options

- `radius`: Search radius in meters (max 50,000)
- `fetch_details`: Whether to get detailed info for each place
- File naming and output format can be customized

## Troubleshooting

### Common Issues

1. **"API key not found"**
   - Ensure `.env` file exists and contains your API key
   - Check that the key name is exactly `GOOGLE_MAPS_API_KEY`

2. **"REQUEST_DENIED"**
   - API key might be invalid or restricted
   - Ensure Places API is enabled for your project

3. **"OVER_QUERY_LIMIT"**
   - You've exceeded your API quota
   - Check usage in Google Cloud Console

4. **Empty results**
   - Try a different location or place type
   - Check if the location name is recognized by Google

### Debug Mode

Add print statements or modify the logging to see detailed API responses:

```python
print(f"API Response: {data}")  # Add this in the scraper methods
```

## License

This project is provided as-is for educational and development purposes. Please ensure compliance with Google's Terms of Service when using their APIs.

## Contributing

This is an MVP implementation. Potential improvements:
- Add support for more search parameters
- Implement caching to avoid duplicate API calls
- Add data validation and cleaning
- Create a web interface
- Add support for multiple output formats