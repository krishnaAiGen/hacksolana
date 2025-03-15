"""
Multiple Context Protocol (MCP) server for Solana Forum Data.

This server provides an interface to query the Solana forum data
using different approaches based on the query type.
"""

import json
import re
import os
import datetime
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Import utility functions
from src.utils import load_json, get_data_directory

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

class SolanaForumMCPServer:
    """
    MCP Server for handling different types of queries on Solana forum data.
    
    This server implements three different approaches:
    1. In-memory data processing with Python functions
    2. Pandas DataFrame for SQL-like queries
    3. Vector-based search for semantic queries
    """
    
    def __init__(self, data_file: str = "solana_forum_posts"):
        """
        Initialize the MCP server with the Solana forum data.
        
        Args:
            data_file: Name of the JSON file containing the forum data
        """
        self.data = load_json(data_file)
        self.posts = self._flatten_posts()
        self.df = pd.DataFrame(self.posts)
        self._prepare_vector_search()
        print(f"Loaded {len(self.posts)} posts from {len(self.data)} categories")
        
    def _flatten_posts(self) -> List[Dict[str, Any]]:
        """
        Flatten the nested category-based posts into a single list.
        
        Returns:
            List of all posts across all categories
        """
        flattened_posts = []
        for category, posts in self.data.items():
            for post in posts:
                post_copy = post.copy()
                # Ensure category is included in each post
                if 'category_name' not in post_copy:
                    post_copy['category_name'] = category
                flattened_posts.append(post_copy)
        return flattened_posts
    
    def _prepare_vector_search(self):
        """
        Prepare the vector search functionality by creating TF-IDF vectors
        for post titles and descriptions.
        """
        # Combine title and description for better semantic search
        self.text_data = [
            f"{post.get('title', '')} {post.get('description', '')}"
            for post in self.posts
        ]
        
        # Create TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000,
            ngram_range=(1, 2)
        )
        
        # Create the TF-IDF matrix
        self.tfidf_matrix = self.vectorizer.fit_transform(self.text_data)
        print(f"Created vector search index with {self.tfidf_matrix.shape[1]} features")
    
    def query(self, query_text: str) -> Dict[str, Any]:
        """
        Process a natural language query and route it to the appropriate handler.
        
        Args:
            query_text: The natural language query from the user
            
        Returns:
            Dictionary containing the query results and metadata
        """
        query_text = query_text.lower().strip()
        
        # Determine query type and route to appropriate handler
        if re.search(r'latest|recent|new', query_text):
            if re.search(r'category|discussion|forum', query_text):
                # Extract category if mentioned
                category = self._extract_category_from_query(query_text)
                return self.get_latest_posts(category)
            else:
                return self.get_latest_posts()
                
        elif re.search(r'most viewed|popular|top', query_text):
            if re.search(r'category|discussion|forum', query_text):
                category = self._extract_category_from_query(query_text)
                return self.get_most_viewed_posts(category)
            else:
                return self.get_most_viewed_posts()
                
        elif re.search(r'comments|discussed|active', query_text):
            return self.get_most_commented_posts()
            
        elif re.search(r'statistics|stats|summary', query_text):
            return self.get_forum_statistics()
            
        else:
            # Default to semantic search for other queries
            return self.semantic_search(query_text)
    
    def _extract_category_from_query(self, query_text: str) -> Optional[str]:
        """
        Extract category name from the query if present.
        
        Args:
            query_text: The query text to analyze
            
        Returns:
            Category name if found, None otherwise
        """
        # List of all categories
        categories = list(self.data.keys())
        
        # Check if any category is mentioned in the query
        for category in categories:
            if category.lower() in query_text.lower():
                return category
                
        return None
    
    def get_latest_posts(self, category: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        """
        Get the latest posts, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            limit: Maximum number of posts to return
            
        Returns:
            Dictionary with query results
        """
        # Function-based approach
        if category:
            filtered_posts = [p for p in self.posts if p.get('category_name') == category]
        else:
            filtered_posts = self.posts
            
        # Sort by created_at date (most recent first)
        sorted_posts = sorted(
            filtered_posts,
            key=lambda x: x.get('created_at', ''),
            reverse=True
        )
        
        result_posts = sorted_posts[:limit]
        
        return {
            'query_type': 'latest_posts',
            'category': category,
            'count': len(result_posts),
            'posts': result_posts
        }
    
    def get_most_viewed_posts(self, category: Optional[str] = None, limit: int = 5) -> Dict[str, Any]:
        """
        Get the most viewed posts, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            limit: Maximum number of posts to return
            
        Returns:
            Dictionary with query results
        """
        # SQL-like approach using pandas
        df = self.df
        
        if category:
            df = df[df['category_name'] == category]
            
        # Sort by views (highest first)
        df = df.sort_values(by='views', ascending=False)
        
        result_posts = df.head(limit).to_dict('records')
        
        return {
            'query_type': 'most_viewed_posts',
            'category': category,
            'count': len(result_posts),
            'posts': result_posts
        }
    
    def get_most_commented_posts(self, limit: int = 5) -> Dict[str, Any]:
        """
        Get posts with the most comments.
        
        Args:
            limit: Maximum number of posts to return
            
        Returns:
            Dictionary with query results
        """
        # SQL-like approach using pandas
        df = self.df.sort_values(by='comment_count', ascending=False)
        result_posts = df.head(limit).to_dict('records')
        
        return {
            'query_type': 'most_commented_posts',
            'count': len(result_posts),
            'posts': result_posts
        }
    
    def get_forum_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics about the forum data.
        
        Returns:
            Dictionary with forum statistics
        """
        # Calculate statistics
        total_posts = len(self.posts)
        total_views = sum(post.get('views', 0) for post in self.posts)
        total_comments = sum(post.get('comment_count', 0) for post in self.posts)
        
        # Posts per category
        category_counts = Counter(post.get('category_name') for post in self.posts)
        
        # Find most active users
        user_post_counts = Counter(post.get('original_poster') for post in self.posts)
        most_active_users = user_post_counts.most_common(5)
        
        return {
            'query_type': 'forum_statistics',
            'total_posts': total_posts,
            'total_views': total_views,
            'total_comments': total_comments,
            'posts_per_category': dict(category_counts),
            'most_active_users': most_active_users
        }
    
    def semantic_search(self, query_text: str, limit: int = 5) -> Dict[str, Any]:
        """
        Perform semantic search on the forum data.
        
        Args:
            query_text: The query text to search for
            limit: Maximum number of posts to return
            
        Returns:
            Dictionary with search results
        """
        # Transform query to TF-IDF vector
        query_vector = self.vectorizer.transform([query_text])
        
        # Calculate cosine similarity between query and all posts
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Get indices of top results
        top_indices = similarities.argsort()[-limit:][::-1]
        
        # Get the top posts
        result_posts = [self.posts[i] for i in top_indices]
        
        # Include similarity scores
        for i, post in enumerate(result_posts):
            post['similarity_score'] = float(similarities[top_indices[i]])
        
        return {
            'query_type': 'semantic_search',
            'query': query_text,
            'count': len(result_posts),
            'posts': result_posts
        }

# Example usage
if __name__ == "__main__":
    server = SolanaForumMCPServer()
    
    # Example queries
    queries = [
        "What are the latest posts in the Governance category?",
        "What is the most viewed post on Solana?",
        "Which posts have the most comments?",
        "Show me forum statistics",
        "Tell me about Solana validators"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = server.query(query)
        print(f"Query type: {result['query_type']}")
        print(f"Found {result['count']} results")
        
        if 'posts' in result:
            for i, post in enumerate(result['posts']):
                print(f"\n{i+1}. {post.get('title')}")
                if 'similarity_score' in post:
                    print(f"   Relevance: {post['similarity_score']:.2f}")
                print(f"   Views: {post.get('views')}, Comments: {post.get('comment_count')}")
                print(f"   URL: {post.get('url')}")
        else:
            print(result) 