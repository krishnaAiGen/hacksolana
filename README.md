# Solana Forum Data Scraper

A project for the Solana hackathon that scrapes data from the Solana forum and provides a Multiple Context Protocol (MCP) server for querying the data.

## Project Structure

```
.
├── data/
│   ├── raw/           # Raw CSV data files for each forum category
│   └── processed/     # Processed data in JSON format
├── docs/              # Documentation
│   ├── mcp_server.md  # MCP server documentation
│   └── query.md       # Example queries documentation
├── examples/          # Example scripts
├── src/               # Source code
│   ├── __init__.py    # Package initialization
│   ├── scripts/       # Python scripts for data collection and processing
│   │   └── __init__.py # Scripts package initialization
│   ├── utils/         # Utility functions
│   │   └── __init__.py # Utils package initialization
│   ├── mcp_server.py  # Multiple Context Protocol server
│   ├── api_server.py  # HTTP API server
│   └── cli.py         # Command-line interface
├── .env               # Environment variables (not tracked by Git)
├── .env.example       # Example environment variables
└── requirements.txt   # Project dependencies
```

## Getting Started

1. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Customize the values in `.env` if needed.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the data scraper:
   ```
   python src/scripts/download_data.py
   ```

## Data Description

This project collects data from the following Solana forum categories:
- Governance
- sRFC (Solana Request for Comments)
- RFP (Request for Proposals)
- SIMD
- Releases
- Research
- Announcements

The data includes post titles, descriptions, comments, view counts, and other metadata.

## Multiple Context Protocol (MCP) Server

The MCP server provides a flexible interface for querying Solana forum data using different approaches:

1. **Function-based Processing**: For simple queries like getting the latest posts
2. **SQL-like Queries**: Using Pandas DataFrames for structured queries like finding the most viewed posts
3. **Vector Search**: For semantic queries and natural language understanding

### Using the MCP Server

#### Command-Line Interface

```bash
# Start interactive mode
python src/cli.py interactive

# Process a natural language query
python src/cli.py query "What are the latest posts in the Governance category?"
```

#### HTTP API

```bash
# Start the API server
python src/api_server.py
```

Then send requests to the API endpoints:

```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the most viewed post on Solana?"}'
```

See [MCP Server Documentation](docs/mcp_server.md) for more details on the server architecture and [Query Examples](docs/query.md) for a comprehensive list of example queries.

## Package Structure

The project is organized as a Python package, allowing you to import and use its components in other scripts:

```python
# Import utility functions
from src.utils import load_json, save_json, get_data_directory

# Import the scraper client
from src.scripts import SolanaForumAPIClient

# Import the MCP server
from src.mcp_server import SolanaForumMCPServer
```

## Utility Functions

The project includes utility functions for working with the data:

```python
# Load JSON data
from src.utils import load_json
data = load_json('solana_forum_posts')

# Save JSON data
from src.utils import save_json
save_json(data, 'processed_data')

# Get data directory paths
from src.utils import get_data_directory
raw_dir = get_data_directory('raw')
```

## Examples

Check out the `examples/` directory for sample scripts that demonstrate how to use the package:

```bash
# Run the example data processing script
python examples/process_data.py

# Run the MCP server example
python examples/mcp_example.py
```
