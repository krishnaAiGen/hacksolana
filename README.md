# Solana Forum MCP Server

A Multiple Context Protocol (MCP) server for querying Solana forum data. This project implements the MCP specification to provide a flexible interface for AI assistants to interact with Solana forum data.

## What is MCP?

Multiple Context Protocol (MCP) is a specification for building tools that can be used by AI assistants. It provides a standardized way for AI models to interact with external systems and data sources. This project implements an MCP server for Solana forum data, allowing AI assistants to query and analyze forum posts, statistics, and more.

The Model Context Protocol allows applications to provide context for LLMs in a standardized way, separating the concerns of providing context from the actual LLM interaction. The MCP Python SDK implements the full MCP specification, making it easy to:

- Build MCP clients that can connect to any MCP server
- Create MCP servers that expose resources, prompts and tools
- Use standard transports like stdio and SSE
- Handle all MCP protocol messages and lifecycle events

## Project Structure

```
.
├── src/               # Source code
│   ├── __init__.py    # Package initialization
│   ├── utils/         # Utility functions
│   │   └── __init__.py # Utils package initialization
│   ├── mcp_server.py  # Multiple Context Protocol server implementation
│   ├── api_server.py  # HTTP API server
│   └── cli.py         # Command-line interface
├── solana_mcp.py      # MCP server wrapper script
├── setup.py           # Package installation script
└── requirements.txt   # Project dependencies
```

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

## Getting Started

1. Run the MCP server:
   ```bash
   # Using uv
   uv run solana_mcp.py
   
   # Or using python directly
   python solana_mcp.py
   ```

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

## MCP Tools

The Solana Forum MCP server provides the following tools:

### Example Queries

#### Latest Posts Queries

1. "What are the latest posts?"
2. "Show me recent posts in the Governance category"
3. "What's new in the sRFC category?"

#### Most Viewed Posts Queries

1. "What are the most viewed posts?"
2. "Show me popular posts in the Research category"
3. "What are the top posts on Solana?"

#### Category Posts Queries

1. "Give me all posts on Governance"
2. "All posts in Research"
3. "Posts from Announcements"

#### Post Evaluation Queries

1. "Give me all posts on Governance"
2. "For this post id 123, give me its evaluation"
3. "Evaluate post 456"

#### Most Commented Posts Queries

1. "Which posts have the most comments?"
2. "Show me the most discussed topics"
3. "What are the most active discussions?"

#### Statistics Queries

1. "Show me forum statistics"
2. "What are the stats for the Solana forum?"
3. "Give me a summary of the forum data"

#### Semantic Search Queries

1. "Tell me about Solana validators"
2. "What are people saying about staking?"
3. "Find posts about performance improvements"

#### Topic-Specific Semantic Search Examples

1. "How does Solana achieve high throughput?"
2. "What are the latest developments in Solana's governance?"
3. "Tell me about Solana's approach to smart contracts"

### 1. get_latest_posts

1. Get the latest posts from the Solana forum, optionally filtered by category.

```python
async def get_latest_posts(category: Optional[str] = None, limit: int = 5) -> str
```

### 2. get_most_viewed_posts

Get the most viewed posts from the Solana forum, optionally filtered by category.

```python
async def get_most_viewed_posts(category: Optional[str] = None, limit: int = 5) -> str
```

### 3. get_most_commented_posts

Get the most commented posts from the Solana forum.

```python
async def get_most_commented_posts(limit: int = 5) -> str
```

### 4. get_forum_statistics

Get general statistics about the Solana forum.

```python
async def get_forum_statistics() -> str
```

### 5. semantic_search

Search for posts semantically related to a query.

```python
async def semantic_search(query_text: str, limit: int = 5) -> str
```

### 6. get_posts_by_category

Get posts from a specific category.

```python
async def get_posts_by_category(category: str, limit: int = 20) -> str
```

### 7. evaluate_post

Evaluate a specific post for sentiment, quality, and relevance.

```python
async def evaluate_post(post_id: int) -> str
```

### 8. universal_query

Process any type of query about Solana forum data.

```python
async def universal_query(query_text: str) -> str
```

## Using the MCP Server with AI Assistants

The MCP server can be used with AI assistants that support the MCP specification. Here's how to use it:

1. Start the MCP server:
   ```bash
   uv run solana_mcp.py
   ```

2. Connect your AI assistant to the MCP server using the stdio transport.
1
3. The AI assistant can now use the MCP tools to query Solana forum data.


## Implementation Details

The Solana Forum MCP server is implemented using the FastMCP library, which provides a simple way to create MCP servers. The server uses a mock implementation of the SolanaForumMCPServer class, which provides methods for querying Solana forum data.

Each MCP tool is implemented as an async function that calls the corresponding method on the SolanaForumMCPServer instance. The results are formatted into a readable string and returned to the AI assistant.

## Extending the MCP Server

You can extend the MCP server by adding new tools or enhancing existing ones. To add a new tool, simply define a new async function and decorate it with `@mcp.tool()`. The function should take the necessary parameters and return a string result.

```python
@mcp.tool()
async def new_tool(param1: str, param2: int) -> str:
    """Tool description.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    """
    # Implement the tool
    result = solana_server.some_method(param1, param2)
    
    # Format the result
    formatted_result = format_result(result)
    
    return formatted_result
```

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