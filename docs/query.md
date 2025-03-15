# Solana Forum MCP Server Query Examples

This document provides a comprehensive list of example queries you can use with the Solana Forum MCP Server through any of its interfaces (CLI, HTTP API, or Python API).

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

## Natural Language Queries (POST /api/query)

### Latest Posts Queries

```bash
# CLI
python solana_cli.py query "What are the latest posts?"
python solana_cli.py query "Show me recent posts in the Governance category"
python solana_cli.py query "What's new in the sRFC category?"

# HTTP API
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest posts?"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me recent posts in the Governance category"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is new in the sRFC category?"}'

# Python API
server.query("What are the latest posts?")
server.query("Show me recent posts in the Governance category")
server.query("What's new in the sRFC category?")
```

### Most Viewed Posts Queries

```bash
# CLI
python solana_cli.py query "What are the most viewed posts?"
python solana_cli.py query "Show me popular posts in the Research category"
python solana_cli.py query "What are the top posts on Solana?"

# HTTP API
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the most viewed posts?"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me popular posts in the Research category"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the top posts on Solana?"}'

# Python API
server.query("What are the most viewed posts?")
server.query("Show me popular posts in the Research category")
server.query("What are the top posts on Solana?")
```

### Most Commented Posts Queries

```bash
# CLI
python solana_cli.py query "Which posts have the most comments?"
python solana_cli.py query "Show me the most discussed topics"
python solana_cli.py query "What are the most active discussions?"

# HTTP API
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Which posts have the most comments?"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me the most discussed topics"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the most active discussions?"}'

# Python API
server.query("Which posts have the most comments?")
server.query("Show me the most discussed topics")
server.query("What are the most active discussions?")
```

### Statistics Queries

```bash
# CLI
python solana_cli.py query "Show me forum statistics"
python solana_cli.py query "What are the stats for the Solana forum?"
python solana_cli.py query "Give me a summary of the forum data"

# HTTP API
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me forum statistics"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the stats for the Solana forum?"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Give me a summary of the forum data"}'

# Python API
server.query("Show me forum statistics")
server.query("What are the stats for the Solana forum?")
server.query("Give me a summary of the forum data")
```

### Semantic Search Queries

```bash
# CLI
python solana_cli.py query "Tell me about Solana validators"
python solana_cli.py query "What are people saying about staking?"
python solana_cli.py query "Find posts about performance improvements"
python solana_cli.py query "What discussions are there about security?"
python solana_cli.py query "Show me posts related to transaction fees"

# HTTP API
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about Solana validators"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are people saying about staking?"}'

curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Find posts about performance improvements"}'

# Python API
server.query("Tell me about Solana validators")
server.query("What are people saying about staking?")
server.query("Find posts about performance improvements")
```

## Direct API Endpoints

### Latest Posts (GET /api/latest)

```bash
# CLI
python solana_cli.py latest
python solana_cli.py latest --category "Governance" --limit 10

# HTTP API
curl "http://localhost:5000/api/latest"
curl "http://localhost:5000/api/latest?category=Governance&limit=10"

# Python API
server.get_latest_posts()
server.get_latest_posts(category="Governance", limit=10)
```

### Most Viewed Posts (GET /api/most-viewed)

```bash
# CLI
python solana_cli.py most-viewed
python solana_cli.py most-viewed --category "Research" --limit 10

# HTTP API
curl "http://localhost:5000/api/most-viewed"
curl "http://localhost:5000/api/most-viewed?category=Research&limit=10"

# Python API
server.get_most_viewed_posts()
server.get_most_viewed_posts(category="Research", limit=10)
```

### Most Commented Posts (GET /api/most-commented)

```bash
# CLI
python solana_cli.py most-commented
python solana_cli.py most-commented --limit 10

# HTTP API
curl "http://localhost:5000/api/most-commented"
curl "http://localhost:5000/api/most-commented?limit=10"

# Python API
server.get_most_commented_posts()
server.get_most_commented_posts(limit=10)
```

### Forum Statistics (GET /api/statistics)

```bash
# CLI
python solana_cli.py stats

# HTTP API
curl "http://localhost:5000/api/statistics"

# Python API
server.get_forum_statistics()
```

### Semantic Search (GET /api/search)

```bash
# CLI
python solana_cli.py search "Solana validators"
python solana_cli.py search "staking rewards" --limit 10

# HTTP API
curl "http://localhost:5000/api/search?q=Solana%20validators"
curl "http://localhost:5000/api/search?q=staking%20rewards&limit=10"

# Python API
server.semantic_search("Solana validators")
server.semantic_search("staking rewards", limit=10)
```

### List Categories (GET /api/categories)

```bash
# CLI
python solana_cli.py categories

# HTTP API
curl "http://localhost:5000/api/categories"

# Python API
list(server.data.keys())
```

## Topic-Specific Semantic Search Examples

Here are additional semantic search queries focused on specific Solana topics:

```bash
# CLI
python solana_cli.py query "How does Solana achieve high throughput?"
python solana_cli.py query "What are the latest developments in Solana's governance?"
python solana_cli.py query "Tell me about Solana's approach to smart contracts"
python solana_cli.py query "What are the challenges with Solana's consensus mechanism?"
python solana_cli.py query "How does Solana handle network congestion?"
python solana_cli.py query "What are people saying about Solana's developer experience?"
python solana_cli.py query "Find discussions about Solana's token economics"
python solana_cli.py query "What are the recent proposals for Solana improvement?"

# HTTP API
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How does Solana achieve high throughput?"}'

# Python API
server.query("How does Solana achieve high throughput?")
```

## Response Format

The server returns responses in JSON format. Here's an example response for a query about the latest posts:

```json
{
  "query_type": "latest_posts",
  "category": "Governance",
  "count": 5,
  "posts": [
    {
      "id": 12345,
      "title": "Example Post Title",
      "url": "https://forum.solana.com/t/example-post/12345",
      "description": "This is an example post description...",
      "comments": "[username]: Comment text...",
      "original_poster": "username",
      "views": 1000,
      "reply_count": 15,
      "comment_count": 20,
      "posts_count": 21,
      "created_at": "2023-01-01T00:00:00Z",
      "activity": "2023-01-10T00:00:00Z",
      "category_name": "Governance",
      "category_id": 5
    },
    // More posts...
  ]
}
```

For semantic search queries, each post will also include a `similarity_score` field indicating how relevant the post is to the query:

```json
{
  "query_type": "semantic_search",
  "query": "Solana validators",
  "count": 3,
  "posts": [
    {
      "title": "Validator Requirements Update",
      "similarity_score": 0.85,
      // Other post fields...
    },
    // More posts...
  ]
}
```

## Using the Interactive Mode

The interactive mode is the easiest way to explore the data and try different queries:

```bash
python solana_cli.py interactive
```

This will start a prompt where you can type natural language queries and see the results immediately. Type 'exit', 'quit', or 'q' to exit the interactive mode. 