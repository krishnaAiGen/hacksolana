# Solana Forum MCP Server

This document explains how to use the Multiple Context Protocol (MCP) server for querying Solana forum data.

## Overview

The MCP server provides a flexible interface for querying Solana forum data using different approaches:

1. **Function-based Processing**: For simple queries like getting the latest posts
2. **SQL-like Queries**: Using Pandas DataFrames for structured queries like finding the most viewed posts
3. **Vector Search**: For semantic queries and natural language understanding

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the MCP Server

There are three ways to run the MCP server:

### Method 1: Using the wrapper scripts (recommended)

```bash
# Run the CLI
python solana_cli.py interactive

# Run the API server
python solana_api.py
```

### Method 2: Install as a package

```bash
# Install the package in development mode
pip install -e .

# Run the CLI
solana-cli interactive

# Run the API server
solana-api
```

### Method 3: Run the scripts directly

```bash
# Run the CLI
python -m src.cli interactive

# Run the API server
python -m src.api_server
```

## Usage

### Command-Line Interface

The MCP server can be used via a command-line interface:

```bash
# Start interactive mode
python solana_cli.py interactive

# Process a natural language query
python solana_cli.py query "What are the latest posts in the Governance category?"

# Get the latest posts
python solana_cli.py latest --category Governance --limit 10

# Get the most viewed posts
python solana_cli.py most-viewed

# Get posts with the most comments
python solana_cli.py most-commented

# Get forum statistics
python solana_cli.py stats

# Perform semantic search
python solana_cli.py search "Solana validators" --limit 10

# List all categories
python solana_cli.py categories

# Get all posts from a specific category
python solana_cli.py category "Governance" --limit 20

# Evaluate a post from different perspectives
python solana_cli.py evaluate 123
```

### API Server

The MCP server can also be used via an HTTP API:

```bash
# Start the API server
python solana_api.py
```

#### API Endpoint

The API server now uses a single `/query` endpoint for all types of queries. It analyzes the query content and invokes the appropriate function based on the query type.

- `POST /query`: Process a natural language query
  ```json
  {
    "query": "What is the most viewed post on Solana?"
  }
  ```

- `GET /query`: Process a query with parameters
  - Query parameters:
    - `q`: The query text for natural language processing
    - `type`: Optional query type (latest, most-viewed, most-commented, stats, search, category, evaluate)
    - `category`: Optional category name
    - `post_id`: Optional post ID for evaluation
    - `limit`: Maximum number of posts to return (default varies by query type)

#### Examples

```bash
# Natural language query (POST method)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the most viewed post on Solana?"}'

# Natural language query (GET method)
curl "http://localhost:5001/query?q=What%20is%20the%20most%20viewed%20post%20on%20Solana?"

# Get the latest posts
curl "http://localhost:5001/query?type=latest"
curl "http://localhost:5001/query?type=latest&category=Governance&limit=10"

# Get the most viewed posts
curl "http://localhost:5001/query?type=most-viewed"
curl "http://localhost:5001/query?type=most-viewed&category=Research&limit=10"

# Get posts with the most comments
curl "http://localhost:5001/query?type=most-commented&limit=10"

# Get forum statistics
curl "http://localhost:5001/query?type=stats"

# Perform semantic search
curl "http://localhost:5001/query?type=search&q=Solana%20validators&limit=10"

# List all categories
curl "http://localhost:5001/query?type=categories"

# Get all posts from a specific category
curl "http://localhost:5001/query?type=category&category=Governance&limit=20"

# Evaluate a post from different perspectives
curl "http://localhost:5001/query?type=evaluate&post_id=123"
```

## Example Queries

The MCP server can handle a variety of natural language queries:

- "What are the latest posts in the Governance category?"
- "What is the most viewed post on Solana?"
- "Which posts have the most comments?"
- "Show me forum statistics"
- "Tell me about Solana validators"
- "Give me all posts on Governance"
- "For this post id 123, give me its evaluation"

## Implementation Details

### Query Processing

The MCP server uses a combination of regular expressions and semantic understanding to process queries:

1. **Pattern Matching**: For structured queries like "latest posts" or "most viewed"
2. **Category Extraction**: To identify specific categories mentioned in the query
3. **Semantic Search**: For general queries that don't match specific patterns

### Data Storage

The server uses three different data representations:

1. **Original JSON**: Preserves the original nested structure by category
2. **Flattened List**: For function-based processing
3. **Pandas DataFrame**: For SQL-like queries
4. **TF-IDF Vectors**: For semantic search

### Vector Search

The semantic search functionality uses:

1. **TF-IDF Vectorization**: To convert text to numerical vectors
2. **Cosine Similarity**: To find the most relevant posts
3. **NLTK**: For text preprocessing

### Post Evaluation

The post evaluation functionality uses OpenAI's API to evaluate posts from five different perspectives:

1. **Technical Innovation**: How innovative the post is from a technical perspective
2. **Ecosystem Growth**: How the post contributes to the growth of the Solana ecosystem
3. **Community Benefit**: How the post benefits the Solana community
4. **Economic Sustainability**: How the post contributes to economic sustainability
5. **Decentralization**: How the post impacts decentralization

Each perspective receives a score between 0.0 and 1.0, with an explanation for the score. The overall score is the average of all perspective scores.

## Extending the MCP Server

To add new query types:

1. Add a new method to the `SolanaForumMCPServer` class
2. Update the `query` method to route to your new method
3. Update the API server's `/query` endpoint to handle the new query type

## Troubleshooting

### Import Errors

If you encounter an error like `ModuleNotFoundError: No module named 'src'`, it means Python can't find the `src` module. There are three solutions:

1. **Use the wrapper scripts**: Use `solana_cli.py` and `solana_api.py` in the project root
2. **Install the package**: Run `pip install -e .` to install the package in development mode
3. **Use the Python module syntax**: Run `python -m src.cli` instead of `python src/cli.py`

### OpenAI API Key

For the post evaluation functionality, you need to set the OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Or you can pass it directly to the MCP server constructor:

```python
from src.mcp_server import SolanaForumMCPServer

server = SolanaForumMCPServer(openai_api_key="your_api_key_here")
``` 