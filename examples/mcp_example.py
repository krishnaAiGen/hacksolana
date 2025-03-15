#!/usr/bin/env python3
"""
Example script demonstrating how to use the Solana Forum MCP Server.
"""

import os
import sys
import json
from typing import Dict, Any

# Add the parent directory to the Python path to allow importing the src package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the MCP server
from src.mcp_server import SolanaForumMCPServer

def print_result(result: Dict[str, Any], title: str):
    """
    Print a query result with a title.
    
    Args:
        result: The query result to print
        title: The title to display
    """
    print(f"\n{'-' * 80}")
    print(f"{title}")
    print(f"{'-' * 80}")
    
    if 'posts' in result:
        print(f"Found {result['count']} posts")
        for i, post in enumerate(result['posts']):
            print(f"\n{i+1}. {post.get('title', 'No Title')}")
            print(f"   Category: {post.get('category_name', 'Unknown')}")
            print(f"   Views: {post.get('views', 0)}, Comments: {post.get('comment_count', 0)}")
            print(f"   URL: {post.get('url', '')}")
    else:
        print(json.dumps(result, indent=2))

def main():
    """Main function demonstrating MCP server usage."""
    print("Initializing MCP server...")
    server = SolanaForumMCPServer()
    
    # Example 1: Natural language query
    query = "What are the latest posts in the Governance category?"
    result = server.query(query)
    print_result(result, f"Example 1: Natural Language Query - '{query}'")
    
    # Example 2: Get most viewed posts
    result = server.get_most_viewed_posts(limit=3)
    print_result(result, "Example 2: Most Viewed Posts")
    
    # Example 3: Get most commented posts
    result = server.get_most_commented_posts(limit=3)
    print_result(result, "Example 3: Most Commented Posts")
    
    # Example 4: Get forum statistics
    result = server.get_forum_statistics()
    print_result(result, "Example 4: Forum Statistics")
    
    # Example 5: Semantic search
    query = "Solana validators and staking"
    result = server.semantic_search(query, limit=3)
    print_result(result, f"Example 5: Semantic Search - '{query}'")
    
    print("\nDone!")

if __name__ == "__main__":
    main() 