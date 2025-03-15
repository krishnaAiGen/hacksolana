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
```

### API Server

The MCP server can also be used via an HTTP API:

```bash
# Start the API server
python solana_api.py
```

#### API Endpoints

- `POST /api/query`: Process a natural language query
  ```json
  {
    "query": "What is the most viewed post on Solana?"
  }
  ```

- `GET /api/latest`: Get the latest posts
  - Query parameters: `category` (optional), `limit` (default: 5)

- `GET /api/most-viewed`: Get the most viewed posts
  - Query parameters: `category` (optional), `limit` (default: 5)

- `GET /api/most-commented`: Get posts with the most comments
  - Query parameters: `limit` (default: 5)

- `GET /api/statistics`: Get forum statistics

- `GET /api/search`: Perform semantic search
  - Query parameters: `q` (required), `limit` (default: 5)

- `GET /api/categories`: Get a list of all categories

## Example Queries

The MCP server can handle a variety of natural language queries:

- "What are the latest posts in the Governance category?"
- "What is the most viewed post on Solana?"
- "Which posts have the most comments?"
- "Show me forum statistics"
- "Tell me about Solana validators"

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

## Extending the MCP Server

To add new query types:

1. Add a new method to the `SolanaForumMCPServer` class
2. Update the `query` method to route to your new method
3. Add a new endpoint to the API server if needed
4. Add a new command to the CLI if needed

## Troubleshooting

### Import Errors

If you encounter an error like `ModuleNotFoundError: No module named 'src'`, it means Python can't find the `src` module. There are three solutions:

1. **Use the wrapper scripts**: Use `solana_cli.py` and `solana_api.py` in the project root
2. **Install the package**: Run `pip install -e .` to install the package in development mode
3. **Use the Python module syntax**: Run `python -m src.cli` instead of `python src/cli.py` 