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

To run the scraper, execute the following command from the project root directory:

```bash
python src/scripts/download_data.py
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