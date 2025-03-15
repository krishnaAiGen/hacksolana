"""
Multiple Context Protocol (MCP) server for Solana Forum Data.

This server provides an interface to query the Solana forum data
using different approaches based on the query type.
"""

import json
import re
import os
import sys
import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import Counter
import pandas as pd
import requests

# Import MCP modules
import httpx
from mcp.server.fastmcp import FastMCP
# Import utility functions
from src.utils import load_json, get_data_directory
from src.mcp_server import SolanaForumMCPServer

# Initialize the MCP server
mcp = FastMCP("solana")

# Initialize the Solana Forum MCP server
# Get OpenAI API key from environment variable if available
openai_api_key = os.environ.get("OPENAI_API_KEY")
solana_server = SolanaForumMCPServer(openai_api_key=openai_api_key)

@mcp.tool()
async def get_latest_posts(category: Optional[str] = None, limit: int = 5) -> str:
    """Get the latest posts from the Solana forum.
    
    Args:
        category: Optional category to filter posts by
        limit: Maximum number of posts to return (default: 5)
    """
    result = solana_server.get_latest_posts(category=category, limit=limit)
    
    if not result or "posts" not in result or not result["posts"]:
        return "No posts found."
    
    posts = result["posts"]
    formatted_posts = []
    
    for post in posts:
        formatted_post = f"""
Title: {post.get('title', 'Unknown')}
Category: {post.get('category', 'Unknown')}
Author: {post.get('author', 'Unknown')}
Date: {post.get('date', 'Unknown')}
Views: {post.get('views', 0)}
Comments: {post.get('comments', 0)}
URL: {post.get('url', 'Unknown')}
"""
        formatted_posts.append(formatted_post)
    
    return "\n---\n".join(formatted_posts)

@mcp.tool()
async def get_most_viewed_posts(category: Optional[str] = None, limit: int = 5) -> str:
    """Get the most viewed posts from the Solana forum.
    
    Args:
        category: Optional category to filter posts by
        limit: Maximum number of posts to return (default: 5)
    """
    result = solana_server.get_most_viewed_posts(category=category, limit=limit)
    
    if not result or "posts" not in result or not result["posts"]:
        return "No posts found."
    
    posts = result["posts"]
    formatted_posts = []
    
    for post in posts:
        formatted_post = f"""
Title: {post.get('title', 'Unknown')}
Category: {post.get('category', 'Unknown')}
Author: {post.get('author', 'Unknown')}
Date: {post.get('date', 'Unknown')}
Views: {post.get('views', 0)}
Comments: {post.get('comments', 0)}
URL: {post.get('url', 'Unknown')}
"""
        formatted_posts.append(formatted_post)
    
    return "\n---\n".join(formatted_posts)

@mcp.tool()
async def get_most_commented_posts(limit: int = 5) -> str:
    """Get the most commented posts from the Solana forum.
    
    Args:
        limit: Maximum number of posts to return (default: 5)
    """
    result = solana_server.get_most_commented_posts(limit=limit)
    
    if not result or "posts" not in result or not result["posts"]:
        return "No posts found."
    
    posts = result["posts"]
    formatted_posts = []
    
    for post in posts:
        formatted_post = f"""
Title: {post.get('title', 'Unknown')}
Category: {post.get('category', 'Unknown')}
Author: {post.get('author', 'Unknown')}
Date: {post.get('date', 'Unknown')}
Views: {post.get('views', 0)}
Comments: {post.get('comments', 0)}
URL: {post.get('url', 'Unknown')}
"""
        formatted_posts.append(formatted_post)
    
    return "\n---\n".join(formatted_posts)

@mcp.tool()
async def get_forum_statistics() -> str:
    """Get general statistics about the Solana forum."""
    result = solana_server.get_forum_statistics()
    
    if not result:
        return "Unable to fetch forum statistics."
    
    stats = f"""
Total Posts: {result.get('total_posts', 'Unknown')}
Total Categories: {result.get('total_categories', 'Unknown')}
Most Active Category: {result.get('most_active_category', 'Unknown')}
Most Viewed Category: {result.get('most_viewed_category', 'Unknown')}
Average Views per Post: {result.get('avg_views_per_post', 'Unknown')}
Average Comments per Post: {result.get('avg_comments_per_post', 'Unknown')}
"""
    
    # Add top categories if available
    if "top_categories" in result and result["top_categories"]:
        stats += "\nTop Categories by Post Count:\n"
        for category, count in result["top_categories"].items():
            stats += f"- {category}: {count} posts\n"
    
    return stats

@mcp.tool()
async def semantic_search(query_text: str, limit: int = 5) -> str:
    """Search for posts semantically related to the query.
    
    Args:
        query_text: The search query text
        limit: Maximum number of posts to return (default: 5)
    """
    result = solana_server.semantic_search(query_text=query_text, limit=limit)
    
    if not result or "posts" not in result or not result["posts"]:
        return "No matching posts found."
    
    posts = result["posts"]
    formatted_posts = []
    
    for post in posts:
        formatted_post = f"""
Title: {post.get('title', 'Unknown')}
Category: {post.get('category', 'Unknown')}
Author: {post.get('author', 'Unknown')}
Date: {post.get('date', 'Unknown')}
Relevance Score: {post.get('score', 0):.2f}
Snippet: {post.get('snippet', 'No snippet available')}
URL: {post.get('url', 'Unknown')}
"""
        formatted_posts.append(formatted_post)
    
    return "\n---\n".join(formatted_posts)

@mcp.tool()
async def get_posts_by_category(category: str, limit: int = 20) -> str:
    """Get posts from a specific category.
    
    Args:
        category: The category name to filter by
        limit: Maximum number of posts to return (default: 20)
    """
    result = solana_server.get_posts_by_category(category=category, limit=limit)
    
    if not result or "posts" not in result or not result["posts"]:
        return f"No posts found in category '{category}'."
    
    posts = result["posts"]
    formatted_posts = []
    
    for post in posts:
        formatted_post = f"""
Title: {post.get('title', 'Unknown')}
Author: {post.get('author', 'Unknown')}
Date: {post.get('date', 'Unknown')}
Views: {post.get('views', 0)}
Comments: {post.get('comments', 0)}
URL: {post.get('url', 'Unknown')}
"""
        formatted_posts.append(formatted_post)
    
    return f"Posts in category '{category}':\n\n" + "\n---\n".join(formatted_posts)

@mcp.tool()
async def evaluate_post(post_id: int) -> str:
    """Evaluate a specific post for sentiment, quality, and relevance.
    
    Args:
        post_id: The ID of the post to evaluate
    """
    result = solana_server.evaluate_post(post_id=post_id)
    
    if not result or "post" not in result:
        return f"Unable to evaluate post with ID {post_id}."
    
    post = result["post"]
    evaluation = result.get("evaluation", {})
    
    formatted_result = f"""
Post Title: {post.get('title', 'Unknown')}
Author: {post.get('author', 'Unknown')}
Category: {post.get('category', 'Unknown')}
Date: {post.get('date', 'Unknown')}

Evaluation:
- Overall Quality: {evaluation.get('quality_score', 'N/A')}/10
- Sentiment: {evaluation.get('sentiment', 'N/A')}
- Technical Depth: {evaluation.get('technical_depth', 'N/A')}/10
- Community Value: {evaluation.get('community_value', 'N/A')}/10

Analysis:
{evaluation.get('analysis', 'No analysis available')}

Recommendations:
{evaluation.get('recommendations', 'No recommendations available')}
"""
    
    return formatted_result

@mcp.tool()
async def universal_query(query_text: str) -> str:
    """Process any type of query about Solana forum data.
    
    This tool analyzes the query and routes it to the appropriate specialized function.
    
    Args:
        query_text: The query text to process
    """
    result = solana_server.query(query_text=query_text)
    
    if not result or "response" not in result:
        return "Unable to process your query."
    
    return result["response"]

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')