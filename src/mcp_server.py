"""
Multiple Context Protocol (MCP) server for Solana Forum Data.

This server provides an interface to query the Solana forum data
using different approaches based on the query type.
"""

import json
import re
import os
import sys
import datetime
import requests
from typing import Dict, List, Any, Optional, Tuple, Union
from collections import Counter
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

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
    
    def __init__(self, data_file: str = "solana_forum_posts", openai_api_key: Optional[str] = None):
        """
        Initialize the MCP server with the Solana forum data.
        
        Args:
            data_file: Name of the JSON file containing the forum data
            openai_api_key: Optional OpenAI API key for post evaluation
        """
        self.data = load_json(data_file)
        self.posts = self._flatten_posts()
        self.df = pd.DataFrame(self.posts)
        self._prepare_vector_search()
        self.openai_api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
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
        
        # Check for category posts query
        category_match = re.search(r'(give me all posts on|all posts in|posts from) (\w+)', query_text)
        if category_match:
            category = category_match.group(2).capitalize()
            return self.get_posts_by_category(category)
            
        # Check for post evaluation query
        evaluation_match = re.search(r'(for this post id|evaluate post|post id) (\d+)', query_text)
        if evaluation_match:
            post_id = int(evaluation_match.group(2))
            return self.evaluate_post(post_id)
        
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
        
    def get_posts_by_category(self, category: str, limit: int = 20) -> Dict[str, Any]:
        """
        Get all posts from a specific category with summarized information.
        
        Args:
            category: The category to get posts from
            limit: Maximum number of posts to return
            
        Returns:
            Dictionary with posts from the specified category
        """
        # Check if category exists
        if category not in self.data and category.lower() not in [c.lower() for c in self.data.keys()]:
            # Try to find a close match
            for c in self.data.keys():
                if category.lower() in c.lower() or c.lower() in category.lower():
                    category = c
                    break
            else:
                return {
                    'query_type': 'category_posts',
                    'category': category,
                    'count': 0,
                    'error': f"Category '{category}' not found",
                    'available_categories': list(self.data.keys()),
                    'posts': []
                }
        
        # Get posts from the category
        if category in self.data:
            posts = self.data[category]
        else:
            # Find the category with case-insensitive matching
            for c in self.data.keys():
                if c.lower() == category.lower():
                    posts = self.data[c]
                    category = c
                    break
            else:
                posts = []
        
        # Sort by views (highest first)
        sorted_posts = sorted(posts, key=lambda x: x.get('views', 0), reverse=True)
        
        # Limit the number of posts
        result_posts = sorted_posts[:limit]
        
        # Create summarized posts with only essential information
        summarized_posts = []
        for post in result_posts:
            summarized_post = {
                'id': post.get('id'),
                'title': post.get('title'),
                'url': post.get('url'),
                'views': post.get('views', 0),
                'comment_count': post.get('comment_count', 0),
                'original_poster': post.get('original_poster'),
                'created_at': post.get('created_at'),
                'category_name': post.get('category_name', category)
            }
            summarized_posts.append(summarized_post)
        
        return {
            'query_type': 'category_posts',
            'category': category,
            'count': len(summarized_posts),
            'posts': summarized_posts
        }
    
    def evaluate_post(self, post_id: int) -> Dict[str, Any]:
        """
        Evaluate a post from five different perspectives.
        
        Args:
            post_id: The ID of the post to evaluate
            
        Returns:
            Dictionary with evaluation results
        """
        # Find the post by ID
        post = None
        for p in self.posts:
            if p.get('id') == post_id:
                post = p
                break
        
        if not post:
            return {
                'query_type': 'post_evaluation',
                'post_id': post_id,
                'error': f"Post with ID {post_id} not found"
            }
        
        # Check if OpenAI API key is available
        if not self.openai_api_key:
            return {
                'query_type': 'post_evaluation',
                'post_id': post_id,
                'error': "OpenAI API key not provided. Set the OPENAI_API_KEY environment variable or pass it to the constructor."
            }
        
        # Prepare the post content for evaluation
        post_content = f"Title: {post.get('title', '')}\n\nDescription: {post.get('description', '')}"
        
        # Define the perspectives
        perspectives = [
            "technical innovation",
            "ecosystem growth",
            "community benefit",
            "economic sustainability",
            "decentralization"
        ]
        
        # Evaluate the post from each perspective
        evaluations = {}
        
        for perspective in perspectives:
            score, explanation = self._evaluate_from_perspective(post_content, perspective)
            evaluations[perspective] = {
                'score': score,
                'explanation': explanation
            }
        
        # Calculate overall score (average of all perspectives)
        overall_score = sum(eval_data['score'] for eval_data in evaluations.values()) / len(perspectives)
        
        return {
            'query_type': 'post_evaluation',
            'post_id': post_id,
            'post_title': post.get('title'),
            'post_url': post.get('url'),
            'category': post.get('category_name'),
            'overall_score': overall_score,
            'evaluations': evaluations
        }
    
    def _evaluate_from_perspective(self, post_content: str, perspective: str) -> Tuple[float, str]:
        """
        Evaluate a post from a specific perspective using OpenAI API.
        
        Args:
            post_content: The content of the post to evaluate
            perspective: The perspective to evaluate from
            
        Returns:
            Tuple of (score, explanation)
        """
        prompt = f"""
        Please evaluate the following Solana forum post from the perspective of {perspective}.
        
        {post_content}
        
        Evaluate on a scale of 0.0 to 1.0, where:
        - 0.0 means the post has no value or is harmful from this perspective
        - 0.5 means the post has moderate value from this perspective
        - 1.0 means the post has exceptional value from this perspective
        
        Provide your evaluation in the following format:
        Score: [numerical score between 0.0 and 1.0]
        Explanation: [your explanation for the score]
        """
        
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.openai_api_key}"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are an expert evaluator of Solana blockchain forum posts."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 300
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                return 0.5, f"Error calling OpenAI API: {response.text}"
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Extract score and explanation
            score_match = re.search(r'Score:\s*([\d.]+)', content)
            explanation_match = re.search(r'Explanation:\s*(.*)', content, re.DOTALL)
            
            if score_match:
                score = float(score_match.group(1))
                # Ensure score is within bounds
                score = max(0.0, min(1.0, score))
            else:
                score = 0.5
                
            if explanation_match:
                explanation = explanation_match.group(1).strip()
            else:
                explanation = content
                
            return score, explanation
            
        except Exception as e:
            return 0.5, f"Error evaluating post: {str(e)}"

# Example usage
if __name__ == "__main__":
    server = SolanaForumMCPServer()
    
    # Example queries
    queries = [
        "What are the latest posts in the Governance category?",
        "What is the most viewed post on Solana?",
        "Which posts have the most comments?",
        "Show me forum statistics",
        "Tell me about Solana validators",
        "Give me all posts on Governance",
        "For this post id 123, give me its evaluation"
    ]
    
    for query in queries:
        print(f"\nQuery: {query}")
        result = server.query(query)
        print(f"Query type: {result['query_type']}")
        print(f"Found {result.get('count', 0)} results")
        
        if 'posts' in result:
            for i, post in enumerate(result['posts']):
                print(f"\n{i+1}. {post.get('title')}")
                if 'similarity_score' in post:
                    print(f"   Relevance: {post['similarity_score']:.2f}")
                print(f"   Views: {post.get('views')}, Comments: {post.get('comment_count')}")
                print(f"   URL: {post.get('url')}")
        else:
            print(result) 