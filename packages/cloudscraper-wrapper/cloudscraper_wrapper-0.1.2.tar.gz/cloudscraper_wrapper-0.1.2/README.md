# CloudScraper Wrapper

A Python wrapper for CloudScraper that adds proxy support, rate limiting, and caching capabilities.

## Installation

```bash
pip install cloudscraper-wrapper
```

## Basic Usage

```python
from cloudscraper_wrapper import CloudScraperWrapper

# Basic initialization
scraper = CloudScraperWrapper(delay_range=(2, 5))

# Simple GET request
response = scraper.get('https://example.com')
if response:
    print("Successfully retrieved page")

# POST request
response = scraper.post(
    'https://example.com/api',
    json_data={'key': 'value'}
)
```

## Proxy Support

```python
# Using a single proxy
scraper = CloudScraperWrapper(
    proxy='http://user:pass@host:port'
)

# Using proxy rotation
proxies = [
    'http://user1:pass1@host1:port1',
    'http://user2:pass2@host2:port2',
    'http://user3:pass3@host3:port3'
]

scraper = CloudScraperWrapper(
    proxy_rotation=True,
    proxy_list=proxies
)

# Managing proxies
scraper.add_proxy_to_rotation('http://user4:pass4@host4:port4')
scraper.remove_proxy_from_rotation('http://user1:pass1@host1:port1')
scraper.set_proxy('http://newuser:newpass@newhost:port')
```

## Cache Management

```python
# Using cache with custom expiration
response = scraper.get(
    'https://example.com',
    use_cache=True,
    max_cache_age=7200  # Cache for 2 hours
)

# Clear cache
scraper.clear_cache()  # Clear all cache
scraper.clear_cache(max_age=86400)  # Clear cache older than 24 hours
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| delay_range | tuple | (2, 5) | Delay between requests in seconds |
| proxy | str/dict | None | Single proxy configuration |
| proxy_rotation | bool | False | Enable proxy rotation |
| proxy_list | list | None | List of proxies for rotation |

## Error Handling

```python
try:
    response = scraper.get('https://example.com')
    if response is None:
        print("Request failed, check logs for details")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

## License

MIT License

## Disclaimer

This tool is for educational purposes. Follow websites' terms of service when scraping.