"""
Test script to check if the post evaluation functions work with various post IDs.
"""

import asyncio
from solana_mcp import evaluate_post, query_post_evaluation

async def main():
    """Run the test."""
    # Test direct evaluate_post function
    print("\n=== Testing evaluate_post with post ID 3294 ===")
    result1 = await evaluate_post(3294)
    print(result1)
    
    # Test natural language query function
    print("\n=== Testing query_post_evaluation with natural language ===")
    queries = [
        "For this post id 3294, give me its evaluation",
        "Evaluate post #1456",
        "Can you analyze post 5678?",
        "What's your assessment of post ID 9012?",
        "Give me details about post 3456"
    ]
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        result = await query_post_evaluation(query)
        print(result)

if __name__ == "__main__":
    asyncio.run(main()) 