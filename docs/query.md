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

## Natural Language Queries

The MCP server now uses a single `/query` endpoint for all types of queries. You can use natural language to query the server, and it will automatically analyze the query and invoke the appropriate function.

### Latest Posts Queries

```bash
# CLI
python solana_cli.py query "What are the latest posts?"
python solana_cli.py query "Show me recent posts in the Governance category"
python solana_cli.py query "What's new in the sRFC category?"

# HTTP API (POST)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the latest posts?"}'

curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me recent posts in the Governance category"}'

# HTTP API (GET)
curl "http://localhost:5001/query?q=What%20are%20the%20latest%20posts?"
curl "http://localhost:5001/query?q=Show%20me%20recent%20posts%20in%20the%20Governance%20category"

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

# HTTP API (POST)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the most viewed posts?"}'

# HTTP API (GET)
curl "http://localhost:5001/query?q=What%20are%20the%20most%20viewed%20posts?"
curl "http://localhost:5001/query?q=Show%20me%20popular%20posts%20in%20the%20Research%20category"

# Python API
server.query("What are the most viewed posts?")
server.query("Show me popular posts in the Research category")
server.query("What are the top posts on Solana?")
```

### Category Posts Queries

```bash
# CLI
python solana_cli.py query "Give me all posts on Governance"
python solana_cli.py query "All posts in Research"
python solana_cli.py query "Posts from Announcements"

# HTTP API (POST)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Give me all posts on Governance"}'

# HTTP API (GET)
curl "http://localhost:5001/query?q=Give%20me%20all%20posts%20on%20Governance"
curl "http://localhost:5001/query?type=category&category=Governance&limit=20"

# Python API
server.query("Give me all posts on Governance")
server.get_posts_by_category("Governance")
server.get_posts_by_category("Research", limit=10)
```

### Post Evaluation Queries

```bash
# CLI
python solana_cli.py query "For this post id 123, give me its evaluation"
python solana_cli.py query "Evaluate post 456"
python solana_cli.py query "Post id 789 evaluation"

# HTTP API (POST)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "For this post id 123, give me its evaluation"}'

# HTTP API (GET)
curl "http://localhost:5001/query?q=For%20this%20post%20id%20123,%20give%20me%20its%20evaluation"
curl "http://localhost:5001/query?type=evaluate&post_id=123"

# Python API
server.query("For this post id 123, give me its evaluation")
server.evaluate_post(123)
```

### Most Commented Posts Queries

```bash
# CLI
python solana_cli.py query "Which posts have the most comments?"
python solana_cli.py query "Show me the most discussed topics"
python solana_cli.py query "What are the most active discussions?"

# HTTP API (POST)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Which posts have the most comments?"}'

# HTTP API (GET)
curl "http://localhost:5001/query?q=Which%20posts%20have%20the%20most%20comments?"
curl "http://localhost:5001/query?type=most-commented&limit=10"

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

# HTTP API (POST)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show me forum statistics"}'

# HTTP API (GET)
curl "http://localhost:5001/query?q=Show%20me%20forum%20statistics"
curl "http://localhost:5001/query?type=stats"

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

# HTTP API (POST)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about Solana validators"}'

# HTTP API (GET)
curl "http://localhost:5001/query?q=Tell%20me%20about%20Solana%20validators"
curl "http://localhost:5001/query?type=search&q=staking%20rewards&limit=10"

# Python API
server.query("Tell me about Solana validators")
server.query("What are people saying about staking?")
server.query("Find posts about performance improvements")
```

## Direct API Queries

You can also use the `/query` endpoint with specific query parameters to directly access the different functionalities:

### Latest Posts

```bash
# CLI
python solana_cli.py latest
python solana_cli.py latest --category "Governance" --limit 10

# HTTP API
curl "http://localhost:5001/query?type=latest"
curl "http://localhost:5001/query?type=latest&category=Governance&limit=10"

# Python API
server.get_latest_posts()
server.get_latest_posts(category="Governance", limit=10)
```

### Most Viewed Posts

```bash
# CLI
python solana_cli.py most-viewed
python solana_cli.py most-viewed --category "Research" --limit 10

# HTTP API
curl "http://localhost:5001/query?type=most-viewed"
curl "http://localhost:5001/query?type=most-viewed&category=Research&limit=10"

# Python API
server.get_most_viewed_posts()
server.get_most_viewed_posts(category="Research", limit=10)
```

### Most Commented Posts

```bash
# CLI
python solana_cli.py most-commented
python solana_cli.py most-commented --limit 10

# HTTP API
curl "http://localhost:5001/query?type=most-commented"
curl "http://localhost:5001/query?type=most-commented&limit=10"

# Python API
server.get_most_commented_posts()
server.get_most_commented_posts(limit=10)
```

### Forum Statistics

```bash
# CLI
python solana_cli.py stats

# HTTP API
curl "http://localhost:5001/query?type=stats"

# Python API
server.get_forum_statistics()
```

### Semantic Search

```bash
# CLI
python solana_cli.py search "Solana validators"
python solana_cli.py search "staking rewards" --limit 10

# HTTP API
curl "http://localhost:5001/query?type=search&q=Solana%20validators"
curl "http://localhost:5001/query?type=search&q=staking%20rewards&limit=10"

# Python API
server.semantic_search("Solana validators")
server.semantic_search("staking rewards", limit=10)
```

### List Categories

```bash
# CLI
python solana_cli.py categories

# HTTP API
curl "http://localhost:5001/query?type=categories"

# Python API
list(server.data.keys())
```

### Category Posts

```bash
# CLI
python solana_cli.py category "Governance"
python solana_cli.py category "Research" --limit 10

# HTTP API
curl "http://localhost:5001/query?type=category&category=Governance"
curl "http://localhost:5001/query?type=category&category=Research&limit=10"

# Python API
server.get_posts_by_category("Governance")
server.get_posts_by_category("Research", limit=10)
```

### Post Evaluation

```bash
# CLI
python solana_cli.py evaluate 123

# HTTP API
curl "http://localhost:5001/query?type=evaluate&post_id=123"

# Python API
server.evaluate_post(123)
```

## Topic-Specific Semantic Search Examples

Here are additional semantic search queries focused on specific Solana topics:

```bash
# CLI
python solana_cli.py query "How does Solana achieve high throughput?"
python solana_cli.py query "What are the latest developments in Solana's governance?"
python solana_cli.py query "Tell me about Solana's approach to smart contracts"

# HTTP API
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "How does Solana achieve high throughput?"}'

curl "http://localhost:5001/query?q=How%20does%20Solana%20achieve%20high%20throughput?"

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

For category posts queries, the response will include summarized post information:

```json
{
  "query_type": "category_posts",
  "category": "Governance",
  "count": 20,
  "posts": [
    {
      "id": 12345,
      "title": "Example Post Title",
      "url": "https://forum.solana.com/t/example-post/12345",
      "views": 1000,
      "comment_count": 20,
      "original_poster": "username",
      "created_at": "2023-01-01T00:00:00Z",
      "category_name": "Governance"
    },
    // More posts...
  ]
}
```

For post evaluation queries, the response will include scores and explanations for each perspective:

```json
{
  "query_type": "post_evaluation",
  "post_id": 123,
  "post_title": "Example Post Title",
  "post_url": "https://forum.solana.com/t/example-post/123",
  "category": "Governance",
  "overall_score": 0.75,
  "evaluations": {
    "technical innovation": {
      "score": 0.8,
      "explanation": "This post introduces a novel approach to solving the scalability problem..."
    },
    "ecosystem growth": {
      "score": 0.7,
      "explanation": "The proposal would contribute to ecosystem growth by..."
    },
    "community benefit": {
      "score": 0.9,
      "explanation": "This would greatly benefit the community by..."
    },
    "economic sustainability": {
      "score": 0.6,
      "explanation": "From an economic perspective, this proposal is..."
    },
    "decentralization": {
      "score": 0.7,
      "explanation": "This approach would impact decentralization by..."
    }
  }
}
```

## Using the Interactive Mode

The interactive mode is the easiest way to explore the data and try different queries:

```bash
python solana_cli.py interactive
```

This will start a prompt where you can type natural language queries and see the results immediately. Type 'exit', 'quit', or 'q' to exit the interactive mode. 