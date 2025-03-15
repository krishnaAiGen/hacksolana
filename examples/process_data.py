#!/usr/bin/env python3
"""
Example script demonstrating how to use the Solana Forum Data Scraper package.
"""

import os
import sys

# Add the parent directory to the Python path to allow importing the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from the package
from src.utils import load_json, save_json, get_data_directory
from src.scripts import SolanaForumAPIClient

def main():
    """Main function to demonstrate package usage."""
    print("Solana Forum Data Processing Example")
    print("===================================")
    
    # Example 1: Load JSON data
    try:
        data = load_json('solana_forum_posts')
        print(f"\nSuccessfully loaded data with {sum(len(posts) for posts in data.values())} total posts")
        
        # Print some statistics
        print("\nCategory statistics:")
        for category, posts in data.items():
            print(f"- {category}: {len(posts)} posts")
    except FileNotFoundError:
        print("\nNo data found. You need to run the scraper first.")
        print("Run: python src/scripts/download_data.py")
        return
    
    # Example 2: Process and save filtered data
    print("\nFiltering posts with more than 10 comments...")
    filtered_data = {}
    
    for category, posts in data.items():
        filtered_posts = [post for post in posts if post.get('comment_count', 0) > 10]
        if filtered_posts:
            filtered_data[category] = filtered_posts
    
    # Save the filtered data
    if filtered_data:
        total_filtered = sum(len(posts) for posts in filtered_data.values())
        print(f"Found {total_filtered} posts with more than 10 comments")
        
        save_json(filtered_data, 'popular_posts')
        print(f"Saved filtered data to {get_data_directory('processed')}/popular_posts.json")
    else:
        print("No posts found with more than 10 comments")

if __name__ == "__main__":
    main() 