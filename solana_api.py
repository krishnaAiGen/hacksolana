#!/usr/bin/env python3
"""
Wrapper script for the Solana Forum MCP API Server.

This script makes it easier to run the API server from the project root.
"""

import os
import sys
from src.api_server import run_app

if __name__ == "__main__":
    run_app() 