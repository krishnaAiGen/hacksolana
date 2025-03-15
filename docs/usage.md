# Solana Forum Data Scraper Usage Guide

This document explains how to use the Solana Forum Data Scraper to collect data from the Solana forum.

## Prerequisites

- Python 3.6 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - requests
  - json
  - csv
  - datetime
  - re

## Running the Scraper

There are three ways to run the scraper:

### Method 1: Using the wrapper script (recommended)

```bash
python solana_download.py
```

### Method 2: Install as a package

```bash
# Install the package in development mode
pip install -e .

# Run the scraper
solana-download
```

### Method 3: Run the script directly

```bash
python -m src.scripts.download_data
```

This will:
1. Fetch categories from the Solana forum
2. Scrape posts from each category (up to 5 pages per category by default)
3. Save the data in both JSON and CSV formats

## Configuration

You can modify the following parameters in the script:

- `max_pages_per_category`: The maximum number of pages to scrape per category (default: 5)
- `target_categories`: The list of categories to scrape (default: "Governance", "sRFC", "RFP", "SIMD", "Releases", "Research", "Announcements")

## Output

The scraper generates two types of output:

1. **JSON file**: A single JSON file containing all scraped data, saved to `data/processed/solana_forum_posts.json`
2. **CSV files**: One CSV file per category, saved to the `data/raw/` directory

## CSV File Structure

Each CSV file contains the following columns:

- `id`: Post ID
- `title`: Post title
- `url`: URL to the post
- `description`: Post content
- `comments`: Comments on the post
- `original_poster`: Username of the original poster
- `views`: Number of views
- `reply_count`: Number of replies
- `comment_count`: Number of comments
- `posts_count`: Total number of posts (including the original post)
- `created_at`: Creation date
- `activity`: Last activity date
- `category_name`: Category name
- `category_id`: Category ID
- `last_posted_at`: Date of the last post

## Example Usage in Python

```python
# Add the parent directory to the Python path to allow importing the src package
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scripts.download_data import SolanaForumAPIClient

# Create a client
client = SolanaForumAPIClient()

# Fetch only 2 pages from each category
success = client.scrape_all_categories(max_pages_per_category=2)

if success:
    # Save data
    client.save_to_json()
    client.save_to_csv()
```

## Running the Example Scripts

The package includes example scripts in the `examples` directory:

```bash
# Run the data processing example
python examples/process_data.py

# Run the MCP server example
python examples/mcp_example.py
``` 