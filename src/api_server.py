"""
API Server for Solana Forum MCP.

This server exposes the MCP functionality via HTTP endpoints.
"""

import json
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.mcp_server import SolanaForumMCPServer

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the MCP server
mcp_server = SolanaForumMCPServer()

@app.route('/api/query', methods=['POST'])
def query():
    """
    Process a natural language query.
    
    Request body:
    {
        "query": "What is the most viewed post on Solana?"
    }
    """
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({
            'error': 'Missing query parameter'
        }), 400
    
    query_text = data['query']
    result = mcp_server.query(query_text)
    
    return jsonify(result)

@app.route('/api/latest', methods=['GET'])
def latest_posts():
    """
    Get the latest posts, optionally filtered by category.
    
    Query parameters:
    - category: Optional category to filter by
    - limit: Maximum number of posts to return (default: 5)
    """
    category = request.args.get('category')
    limit = int(request.args.get('limit', 5))
    
    result = mcp_server.get_latest_posts(category, limit)
    return jsonify(result)

@app.route('/api/most-viewed', methods=['GET'])
def most_viewed_posts():
    """
    Get the most viewed posts, optionally filtered by category.
    
    Query parameters:
    - category: Optional category to filter by
    - limit: Maximum number of posts to return (default: 5)
    """
    category = request.args.get('category')
    limit = int(request.args.get('limit', 5))
    
    result = mcp_server.get_most_viewed_posts(category, limit)
    return jsonify(result)

@app.route('/api/most-commented', methods=['GET'])
def most_commented_posts():
    """
    Get posts with the most comments.
    
    Query parameters:
    - limit: Maximum number of posts to return (default: 5)
    """
    limit = int(request.args.get('limit', 5))
    
    result = mcp_server.get_most_commented_posts(limit)
    return jsonify(result)

@app.route('/api/statistics', methods=['GET'])
def forum_statistics():
    """
    Get overall statistics about the forum data.
    """
    result = mcp_server.get_forum_statistics()
    return jsonify(result)

@app.route('/api/search', methods=['GET'])
def semantic_search():
    """
    Perform semantic search on the forum data.
    
    Query parameters:
    - q: The query text to search for
    - limit: Maximum number of posts to return (default: 5)
    """
    query_text = request.args.get('q')
    limit = int(request.args.get('limit', 5))
    
    if not query_text:
        return jsonify({
            'error': 'Missing query parameter'
        }), 400
    
    result = mcp_server.semantic_search(query_text, limit)
    return jsonify(result)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
    Get a list of all categories.
    """
    categories = list(mcp_server.data.keys())
    
    return jsonify({
        'categories': categories,
        'count': len(categories)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 