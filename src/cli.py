#!/usr/bin/env python3
"""
Command-line interface for the Solana Forum MCP Server.

This CLI allows users to interact with the MCP server directly from the command line.
"""

import sys
import json
import argparse
import os
from typing import Dict, Any, List, Optional
import textwrap

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Now import from src
from src.mcp_server import SolanaForumMCPServer

def format_post(post: Dict[str, Any], index: Optional[int] = None) -> str:
    """
    Format a post for display in the terminal.
    
    Args:
        post: The post to format
        index: Optional index to display
        
    Returns:
        Formatted post string
    """
    prefix = f"{index}. " if index is not None else ""
    
    # Format the post
    lines = []
    lines.append(f"{prefix}{post.get('title', 'No Title')}")
    
    if 'similarity_score' in post:
        lines.append(f"   Relevance: {post['similarity_score']:.2f}")
        
    lines.append(f"   Category: {post.get('category_name', 'Unknown')}")
    lines.append(f"   Views: {post.get('views', 0)}, Comments: {post.get('comment_count', 0)}")
    lines.append(f"   Posted by: {post.get('original_poster', 'Unknown')}")
    lines.append(f"   URL: {post.get('url', '')}")
    
    # Add a short description if available
    if 'description' in post and post['description']:
        description = post['description']
        # Truncate and wrap the description
        if len(description) > 200:
            description = description[:197] + "..."
        wrapped_description = textwrap.fill(description, width=80, initial_indent="   ", subsequent_indent="   ")
        lines.append(f"\n{wrapped_description}")
    
    return "\n".join(lines)

def format_evaluation(evaluation: Dict[str, Any]) -> str:
    """
    Format a post evaluation for display in the terminal.
    
    Args:
        evaluation: The evaluation to format
        
    Returns:
        Formatted evaluation string
    """
    lines = []
    lines.append(f"Post: {evaluation.get('post_title', 'Unknown')}")
    lines.append(f"URL: {evaluation.get('post_url', '')}")
    lines.append(f"Category: {evaluation.get('category', 'Unknown')}")
    lines.append(f"Overall Score: {evaluation.get('overall_score', 0):.2f}/1.00\n")
    
    if 'evaluations' in evaluation:
        lines.append("Evaluation by Perspective:")
        for perspective, data in evaluation['evaluations'].items():
            lines.append(f"\n{perspective.title()} - Score: {data.get('score', 0):.2f}/1.00")
            explanation = data.get('explanation', '')
            wrapped_explanation = textwrap.fill(explanation, width=80, initial_indent="  ", subsequent_indent="  ")
            lines.append(wrapped_explanation)
    
    return "\n".join(lines)

def display_results(result: Dict[str, Any]):
    """
    Display query results in a formatted way.
    
    Args:
        result: The query result to display
    """
    query_type = result.get('query_type', 'unknown')
    
    print(f"\nQuery Type: {query_type}")
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        if 'available_categories' in result:
            print("\nAvailable categories:")
            for i, category in enumerate(result['available_categories']):
                print(f"{i+1}. {category}")
        return
    
    if query_type == 'post_evaluation':
        print(format_evaluation(result))
        return
    
    if 'category' in result and result['category']:
        print(f"Category: {result['category']}")
        
    if 'query' in result:
        print(f"Query: {result['query']}")
        
    if 'count' in result:
        print(f"Found {result['count']} results")
    
    if 'posts' in result and result['posts']:
        print("\nResults:")
        for i, post in enumerate(result['posts']):
            print(f"\n{format_post(post, i+1)}")
            
    elif 'posts_per_category' in result:
        print("\nPosts per category:")
        for category, count in result['posts_per_category'].items():
            print(f"- {category}: {count} posts")
            
        if 'most_active_users' in result:
            print("\nMost active users:")
            for user, count in result['most_active_users']:
                print(f"- {user}: {count} posts")
                
        if 'total_posts' in result:
            print(f"\nTotal posts: {result['total_posts']}")
            print(f"Total views: {result['total_views']}")
            print(f"Total comments: {result['total_comments']}")
    
    else:
        print(json.dumps(result, indent=2))

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Solana Forum MCP CLI")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Query parser
    query_parser = subparsers.add_parser("query", help="Process a natural language query")
    query_parser.add_argument("text", help="The query text")
    
    # Latest posts parser
    latest_parser = subparsers.add_parser("latest", help="Get the latest posts")
    latest_parser.add_argument("--category", "-c", help="Category to filter by")
    latest_parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum number of posts to return")
    
    # Most viewed posts parser
    viewed_parser = subparsers.add_parser("most-viewed", help="Get the most viewed posts")
    viewed_parser.add_argument("--category", "-c", help="Category to filter by")
    viewed_parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum number of posts to return")
    
    # Most commented posts parser
    commented_parser = subparsers.add_parser("most-commented", help="Get posts with the most comments")
    commented_parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum number of posts to return")
    
    # Statistics parser
    subparsers.add_parser("stats", help="Get forum statistics")
    
    # Search parser
    search_parser = subparsers.add_parser("search", help="Perform semantic search")
    search_parser.add_argument("text", help="The search query")
    search_parser.add_argument("--limit", "-l", type=int, default=5, help="Maximum number of posts to return")
    
    # Categories parser
    subparsers.add_parser("categories", help="List all categories")
    
    # Category posts parser (NEW)
    category_parser = subparsers.add_parser("category", help="Get all posts from a specific category")
    category_parser.add_argument("name", help="The category name")
    category_parser.add_argument("--limit", "-l", type=int, default=20, help="Maximum number of posts to return")
    
    # Post evaluation parser (NEW)
    evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate a post from different perspectives")
    evaluate_parser.add_argument("post_id", type=int, help="The ID of the post to evaluate")
    
    # Interactive mode
    subparsers.add_parser("interactive", help="Start interactive mode")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the MCP server
    print("Initializing MCP server...")
    # Get OpenAI API key from environment variable
    openai_api_key = os.environ.get("OPENAI_API_KEY")
    server = SolanaForumMCPServer(openai_api_key=openai_api_key)
    
    # Process the command
    if args.command == "query":
        result = server.query(args.text)
        display_results(result)
        
    elif args.command == "latest":
        result = server.get_latest_posts(args.category, args.limit)
        display_results(result)
        
    elif args.command == "most-viewed":
        result = server.get_most_viewed_posts(args.category, args.limit)
        display_results(result)
        
    elif args.command == "most-commented":
        result = server.get_most_commented_posts(args.limit)
        display_results(result)
        
    elif args.command == "stats":
        result = server.get_forum_statistics()
        display_results(result)
        
    elif args.command == "search":
        result = server.semantic_search(args.text, args.limit)
        display_results(result)
        
    elif args.command == "categories":
        categories = list(server.data.keys())
        print("\nAvailable categories:")
        for i, category in enumerate(categories):
            print(f"{i+1}. {category}")
    
    elif args.command == "category":
        result = server.get_posts_by_category(args.name, args.limit)
        display_results(result)
        
    elif args.command == "evaluate":
        result = server.evaluate_post(args.post_id)
        display_results(result)
            
    elif args.command == "interactive":
        print("\nEntering interactive mode. Type 'exit' to quit.")
        print("Example queries:")
        print("- What are the latest posts in the Governance category?")
        print("- What is the most viewed post on Solana?")
        print("- Which posts have the most comments?")
        print("- Show me forum statistics")
        print("- Tell me about Solana validators")
        print("- Give me all posts on Governance")
        print("- For this post id 123, give me its evaluation")
        
        while True:
            try:
                query_text = input("\nEnter your query: ")
                if query_text.lower() in ['exit', 'quit', 'q']:
                    break
                    
                result = server.query(query_text)
                display_results(result)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 