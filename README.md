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
├── setup.py           # Package installation script
├── solana_cli.py      # CLI wrapper script
├── solana_api.py      # API server wrapper script
├── solana_download.py # Data scraper wrapper script
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
   
   There are three ways to run the scraper:

   #### Method 1: Using the wrapper script (recommended)
   ```bash
   python solana_download.py
   ```

   #### Method 2: Install as a package
   ```bash
   # Install the package in development mode
   pip install -e .

   # Run the scraper
   solana-download
   ```

   #### Method 3: Run the script directly
   ```bash
   python -m src.scripts.download_data
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
4. **Post Evaluation**: For evaluating posts from different perspectives using OpenAI's API

### Running the MCP Server

There are three ways to run the MCP server:

#### Method 1: Using the wrapper scripts (recommended)

```bash
# Run the CLI
python solana_cli.py interactive

# Run the API server
python solana_api.py
```

#### Method 2: Install as a package

```bash
# Install the package in development mode
pip install -e .

# Run the CLI
solana-cli interactive

# Run the API server
solana-api
```

#### Method 3: Run the scripts directly

```bash
# Run the CLI
python -m src.cli interactive

# Run the API server
python -m src.api_server
```

### Using the MCP Server

#### Command-Line Interface

```bash
# Start interactive mode
python solana_cli.py interactive

# Process a natural language query
python solana_cli.py query "What are the latest posts in the Governance category?"

# Get all posts from a specific category
python solana_cli.py category "Governance"

# Evaluate a post from different perspectives
python solana_cli.py evaluate 123
```

#### HTTP API

```bash
# Start the API server
python solana_api.py
```

Then send requests to the API endpoint:

```bash
# Natural language query (POST method)
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the most viewed post on Solana?"}'

# Natural language query (GET method)
curl "http://localhost:5001/query?q=What%20is%20the%20most%20viewed%20post%20on%20Solana?"

# Get all posts from a specific category
curl "http://localhost:5001/query?type=category&category=Governance"

# Evaluate a post from different perspectives
curl "http://localhost:5001/query?type=evaluate&post_id=123"
```

The API server now uses a single `/query` endpoint for all types of queries. It analyzes the query content and invokes the appropriate function based on the query type.

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

Or add it to your `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```
