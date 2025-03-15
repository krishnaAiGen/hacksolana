# Solana Forum MCP Server Usage Guide

This document explains how to use the Solana Forum MCP Server to query Solana forum data using the Multiple Context Protocol (MCP).

## Prerequisites

- Python 3.6 or higher
- Required Python packages (install using `pip install -r requirements.txt`):
  - mcp
  - httpx
  - pandas
  - requests

## Installation

### Installing uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver. To install uv:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Installing MCP

Using uv (recommended):

```bash
# Add MCP to your project
uv add "mcp[cli]"
```

Using pip:

```bash
# Install MCP
pip install mcp
```

### Installing Project Dependencies

Using uv:

```bash
# Install dependencies
uv pip install -r requirements.txt
```

Using pip:

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the MCP Server

To run the MCP server:

```bash
# Using uv
uv run solana_mcp.py

# Or using python directly
python solana_mcp.py
```

This will start the MCP server using the stdio transport, which allows AI assistants to communicate with the server.

## Using with Claude Desktop

To use the Solana MCP server with Claude Desktop:

1. Create a `claude_desktop_config.json` file in your home directory:

```json
{
  "mcpServers": {
    "solana": {
      "command": "/path/to/your/uv",
      "args": [
        "--directory",
        "/path/to/your/hacksolana",
        "run",
        "solana_mcp.py"
      ]
    }
  }
}
```

Replace `/path/to/your/uv` with the path to your uv installation (e.g., `~/.local/bin/uv`) and `/path/to/your/hacksolana` with the absolute path to your project directory.

2. Start Claude Desktop and connect to the Solana MCP server.

3. You can now use the Solana MCP tools in your conversations with Claude.

## Available MCP Tools

The Solana Forum MCP server provides the following tools:

### 1. get_latest_posts

Get the latest posts from the Solana forum, optionally filtered by category.

```python
async def get_latest_posts(category: Optional[str] = None, limit: int = 5) -> str
```

Example usage:
```
get_latest_posts(category="Development", limit=3)
```

### 2. get_most_viewed_posts

Get the most viewed posts from the Solana forum, optionally filtered by category.

```python
async def get_most_viewed_posts(category: Optional[str] = None, limit: int = 5) -> str
```

Example usage:
```
get_most_viewed_posts(limit=10)
```

### 3. get_most_commented_posts

Get the most commented posts from the Solana forum.

```python
async def get_most_commented_posts(limit: int = 5) -> str
```

Example usage:
```
get_most_commented_posts(limit=5)
```

### 4. get_forum_statistics

Get general statistics about the Solana forum.

```python
async def get_forum_statistics() -> str
```

Example usage:
```
get_forum_statistics()
```

### 5. semantic_search

Search for posts semantically related to a query.

```python
async def semantic_search(query_text: str, limit: int = 5) -> str
```

Example usage:
```
semantic_search(query_text="Solana performance improvements", limit=3)
```

### 6. get_posts_by_category

Get posts from a specific category.

```python
async def get_posts_by_category(category: str, limit: int = 20) -> str
```

Example usage:
```
get_posts_by_category(category="Technology", limit=5)
```

### 7. evaluate_post

Evaluate a specific post for sentiment, quality, and relevance.

```python
async def evaluate_post(post_id: int) -> str
```

Example usage:
```
evaluate_post(post_id=3)
```

### 8. universal_query

Process any type of query about Solana forum data.

```python
async def universal_query(query_text: str) -> str
```

Example usage:
```
universal_query(query_text="What are the latest posts about Solana tokenomics?")
```

## Using with AI Assistants

The MCP server is designed to be used with AI assistants that support the MCP specification. To use the server with an AI assistant:

1. Start the MCP server:
   ```bash
   uv run solana_mcp.py
   ```

2. Connect your AI assistant to the MCP server using the stdio transport.

3. The AI assistant can now use the MCP tools to query Solana forum data.

## Example Queries

Here are some example queries you can make using the MCP server:

- "What are the latest posts in the Development category?"
- "Show me the most viewed posts about Solana tokenomics"
- "Get forum statistics"
- "Search for posts about smart contracts"
- "Evaluate post with ID 3"

## Troubleshooting

### Import Errors

If you encounter an error like `ModuleNotFoundError: No module named 'src'`, it means Python can't find the `src` module. There are two solutions:

1. **Use the wrapper script**: Use `solana_mcp.py` in the project root
2. **Install the package**: Run `pip install -e .` to install the package in development mode

### OpenAI API Key

For the post evaluation functionality, you need to set the OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

Or add it to your `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

## Further Resources

For more information about the Model Context Protocol, visit the [MCP documentation](https://github.com/anthropics/anthropic-tools/tree/main/mcp). 