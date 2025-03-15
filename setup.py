from setuptools import setup, find_packages

setup(
    name="solana-forum-mcp",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.3.0",
        "scikit-learn>=0.24.2",
        "nltk>=3.6.2",
        "flask>=2.0.1",
        "flask-cors>=3.0.10",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "solana-cli=src.cli:main",
            "solana-api=src.api_server:run_app",
            "solana-download=src.scripts.download_data:main",
        ],
    },
    python_requires=">=3.6",
    author="Solana Hackathon Team",
    author_email="example@example.com",
    description="A Model Context Protocol server for Solana forum data",
    keywords="solana, mcp, forum, data",
    url="https://github.com/yourusername/hacksolana",
) 