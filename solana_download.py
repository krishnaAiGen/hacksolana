#!/usr/bin/env python3
"""
Wrapper script for the Solana Forum Data Scraper.

This script makes it easier to run the data scraper from the project root.
"""

import os
import sys
from src.scripts.download_data import main

if __name__ == "__main__":
    main() 