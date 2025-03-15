"""
API Server for Solana Forum MCP.

This server exposes the MCP functionality via HTTP endpoints.
"""

import json
import sys
import os
import re
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Now import from src
from src.mcp_server import SolanaForumMCPServer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the MCP server
# Get OpenAI API key from environment variable
openai_api_key = os.environ.get("OPENAI_API_KEY")
mcp_server = SolanaForumMCPServer(openai_api_key=openai_api_key)

@app.route('/query', methods=['GET', 'POST'])
def query():
    """
    Universal endpoint that processes all types of queries.
    
    This endpoint analyzes the query content and invokes the appropriate function.
    
    For POST requests:
    {
        "query": "What is the most viewed post on Solana?"
    }
    
    For GET requests, use query parameters:
    - q: The query text
    - type: Optional query type (latest, most-viewed, most-commented, stats, search, category, evaluate)
    - category: Optional category name
    - post_id: Optional post ID for evaluation
    - limit: Maximum number of posts to return (default varies by query type)
    """
    result = {}
    
    # Handle POST requests with JSON body
    if request.method == 'POST' and request.is_json:
        data = request.json
        
        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing query parameter'
            }), 400
        
        query_text = data['query']
        result = mcp_server.query(query_text)
    
    # Handle GET requests with query parameters
    elif request.method == 'GET':
        query_type = request.args.get('type', '').lower()
        query_text = request.args.get('q', '')
        category = request.args.get('category')
        limit = int(request.args.get('limit', 5))
        post_id = request.args.get('post_id')
        
        # If query text is provided but no type, use natural language processing
        if query_text and not query_type:
            result = mcp_server.query(query_text)
        
        # Otherwise, use the specified query type
        elif query_type == 'latest':
            result = mcp_server.get_latest_posts(category, limit)
        
        elif query_type == 'most-viewed':
            result = mcp_server.get_most_viewed_posts(category, limit)
        
        elif query_type == 'most-commented':
            result = mcp_server.get_most_commented_posts(limit)
        
        elif query_type == 'stats':
            result = mcp_server.get_forum_statistics()
        
        elif query_type == 'search' and query_text:
            result = mcp_server.semantic_search(query_text, limit)
        
        elif query_type == 'categories':
            categories = list(mcp_server.data.keys())
            result = {
                'categories': categories,
                'count': len(categories)
            }
        
        elif query_type == 'category' and category:
            result = mcp_server.get_posts_by_category(category, limit)
        
        elif query_type == 'evaluate' and post_id:
            try:
                post_id_int = int(post_id)
                result = mcp_server.evaluate_post(post_id_int)
            except ValueError:
                result = {
                    'error': f"Invalid post ID: {post_id}. Must be an integer."
                }
        
        else:
            return jsonify({
                'error': 'Invalid or incomplete query parameters',
                'help': 'Use either "q" parameter for natural language queries or "type" parameter with appropriate additional parameters'
            }), 400
    
    else:
        return jsonify({
            'error': 'Invalid request method or content type',
            'help': 'Send a POST request with JSON body containing "query" parameter or a GET request with appropriate query parameters'
        }), 400
    
    return jsonify(result)

@app.route('/', methods=['GET'])
def index():
    """
    Root endpoint that provides API documentation.
    """
    docs = {
        'name': 'Solana Forum MCP API',
        'description': 'API for querying Solana forum data using the Multiple Context Protocol',
        'endpoints': {
            '/query': {
                'methods': ['GET', 'POST'],
                'description': 'Universal endpoint for all types of queries',
                'examples': {
                    'POST': {
                        'body': {'query': 'What is the most viewed post on Solana?'}
                    },
                    'GET': {
                        'natural_language': '/query?q=What is the most viewed post on Solana?',
                        'latest_posts': '/query?type=latest&limit=10',
                        'category_posts': '/query?type=category&category=Governance&limit=20',
                        'post_evaluation': '/query?type=evaluate&post_id=123'
                    }
                }
            }
        },
        'documentation': 'See /docs/query.md for more examples and details'
    }
    
    return jsonify(docs)

def run_app():
    """Run the Flask application."""
    app.run(debug=True, host='0.0.0.0', port=5001)

if __name__ == '__main__':
    run_app() 