# Solana Forum Data Scraper

A project for the Solana hackathon that scrapes data from the Solana forum.

## Project Structure

```
.
├── data/
│   ├── raw/           # Raw CSV data files for each forum category
│   └── processed/     # Processed data in JSON format
├── docs/              # Documentation
├── src/               # Source code
│   ├── scripts/       # Python scripts for data collection and processing
│   └── utils/         # Utility functions
└── requirements.txt   # Project dependencies
```

## Getting Started

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the data scraper:
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
