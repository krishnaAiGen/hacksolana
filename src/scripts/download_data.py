import requests
import json
import time
import csv
import os
from datetime import datetime
import re

class SolanaForumAPIClient:
    def __init__(self, base_url="https://forum.solana.com"):
        self.base_url = base_url
        self.api_base = f"{base_url}"
        self.headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.categories = {}
        self.posts_by_category = {}
        
        # Categories from the images
        self.target_categories = [
            "Governance", "sRFC", "RFP", "SIMD", "Releases", 
            "Research", "Announcements"
        ]

    def get_categories(self):
        """Fetch categories using the Discourse API"""
        url = f"{self.api_base}/categories.json"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to fetch categories: {response.status_code}")
                return False
                
            data = response.json()
            category_list = data.get('category_list', {}).get('categories', [])
            
            for category in category_list:
                category_name = category.get('name', '')
                # Only include categories that match our target list
                if category_name in self.target_categories:
                    category_id = category.get('id')
                    if category_id:
                        self.categories[category_id] = {
                            'id': category_id,
                            'name': category_name,
                            'slug': category.get('slug', ''),
                            'description': category.get('description_text', ''),
                            'topic_count': category.get('topic_count', 0)
                        }
            
            print(f"Found {len(self.categories)} target categories")
            return True
            
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return False

    def get_topics_for_category(self, category_id, page=0, per_page=30, max_pages=10):
        """Fetch topics for a specific category using the Discourse API"""
        category = self.categories.get(category_id)
        if not category:
            print(f"Category with ID {category_id} not found")
            return []
            
        topics = []
        
        for current_page in range(page, max_pages):
            url = f"{self.api_base}/c/{category['id']}.json"
            params = {
                'page': current_page
            }
            
            try:
                print(f"Fetching page {current_page} for category '{category['name']}'")
                response = requests.get(url, headers=self.headers, params=params)
                
                if response.status_code != 200:
                    print(f"Failed to fetch topics for category '{category['name']}' on page {current_page}: {response.status_code}")
                    break
                    
                data = response.json()
                topic_list = data.get('topic_list', {}).get('topics', [])
                
                if not topic_list:
                    print(f"No more topics for category '{category['name']}'")
                    break
                    
                for topic in topic_list:
                    # Skip pinned topics if they appear on pages after the first
                    if current_page > 0 and topic.get('pinned', False):
                        continue
                    
                    # Get detailed post information
                    topic_details = self.get_topic_details(topic.get('id'))
                    
                    if not topic_details:
                        continue
                        
                    topic_data = {
                        'id': topic.get('id'),
                        'title': topic.get('title'),
                        'url': f"{self.base_url}/t/{topic.get('slug')}/{topic.get('id')}",
                        'created_at': topic.get('created_at'),
                        'posts_count': topic.get('posts_count', 0),
                        'views': topic.get('views', 0),
                        'reply_count': topic.get('reply_count', 0),
                        'last_posted_at': topic.get('last_posted_at'),
                        'category_id': category_id,
                        'category_name': category['name']
                    }
                    
                    # Add the description, comments, and other detailed information
                    topic_data.update(topic_details)
                    
                    topics.append(topic_data)
                
                # If we didn't get a full page of results, we've reached the end
                if len(topic_list) < per_page:
                    break
                    
                # Be nice to the server
                time.sleep(1)
                
            except Exception as e:
                print(f"Error fetching topics for category '{category['name']}' on page {current_page}: {e}")
                break
        
        return topics

    def get_topic_details(self, topic_id):
        """Get detailed information about a topic including description and comments"""
        if not topic_id:
            return None
            
        url = f"{self.api_base}/t/{topic_id}.json"
        
        try:
            response = requests.get(url, headers=self.headers)
            if response.status_code != 200:
                print(f"Failed to fetch content for topic ID {topic_id}: {response.status_code}")
                return None
                
            data = response.json()
            
            # Get all posts from the stream
            post_stream = data.get('post_stream', {})
            posts = post_stream.get('posts', [])
            
            if not posts or len(posts) == 0:
                return None
                
            # First post is the description/main content
            first_post = posts[0]
            description = self.clean_html(first_post.get('cooked', ''))
            
            # Collect comments (all posts except the first one)
            comments = []
            for post in posts[1:]:
                comment_text = self.clean_html(post.get('cooked', ''))
                username = post.get('username', 'Anonymous')
                created_at = post.get('created_at', '')
                
                comments.append({
                    'username': username,
                    'text': comment_text,
                    'created_at': created_at
                })
            
            # Format all comments as a single string for CSV export
            comments_text = ""
            for i, comment in enumerate(comments):
                comments_text += f"[{comment['username']}]: {comment['text']}\n\n"
            
            # Get the original poster
            original_poster = first_post.get('username', 'Anonymous')
            
            # Get activity details
            details = {
                'description': description,
                'comments': comments_text,
                'comment_count': len(comments),
                'original_poster': original_poster,
                'activity': data.get('last_posted_at', '')
            }
            
            return details
            
        except Exception as e:
            print(f"Error fetching details for topic ID {topic_id}: {e}")
            return None
    
    def clean_html(self, html_content):
        """Clean HTML content to plain text"""
        if not html_content:
            return ""
            
        # Replace common HTML elements with space or newlines
        text = html_content.replace('<p>', '\n').replace('</p>', '\n')
        text = text.replace('<br>', '\n').replace('<br/>', '\n')
        
        # Remove image tags completely
        text = re.sub(r'<img.*?>', '', text)
        
        # Remove all other HTML tags
        text = re.sub(r'<.*?>', '', text)
        
        # Clean up excessive whitespace
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r' +', ' ', text)
        
        return text.strip()

    def scrape_all_categories(self, max_pages_per_category=5):
        """Fetch topics from all target categories"""
        if not self.categories:
            success = self.get_categories()
            if not success:
                return False
        
        for category_id, category_info in self.categories.items():
            print(f"Scraping category: {category_info['name']} (ID: {category_id})")
            
            if category_info['topic_count'] == 0:
                print(f"Category '{category_info['name']}' has no topics, skipping")
                self.posts_by_category[category_info['name']] = []
                continue
                
            topics = self.get_topics_for_category(category_id, max_pages=max_pages_per_category)
            self.posts_by_category[category_info['name']] = topics
            
            print(f"Found {len(topics)} topics in category '{category_info['name']}'")
            
            # Be nice to the server
            time.sleep(2)
        
        return True

    def save_to_json(self, filename="../data/processed/solana_forum_posts.json"):
        """Save scraped data to JSON file"""
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.posts_by_category, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {filename}")

    def save_to_csv(self, directory="../data/raw"):
        """Save scraped data to CSV files, one per category"""
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for category_name, posts in self.posts_by_category.items():
            if not posts:
                continue
                
            # Create safe filename from category name
            safe_category_name = "".join([c if c.isalnum() else "_" for c in category_name])
            filename = os.path.join(directory, f"{safe_category_name}.csv")
            
            fieldnames = [
                'id', 'title', 'url', 'description', 'comments', 'original_poster',
                'views', 'reply_count', 'comment_count', 'posts_count', 
                'created_at', 'activity', 'category_name', 'category_id', 'last_posted_at'
            ]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for post in posts:
                    # Create a new dict with only the fields we want in the CSV
                    row_data = {}
                    for field in fieldnames:
                        row_data[field] = post.get(field, "")
                    writer.writerow(row_data)
            
            print(f"Saved {len(posts)} posts from category '{category_name}' to {filename}")
        
# Example usage
if __name__ == "__main__":
    client = SolanaForumAPIClient()
    
    # Fetch categories and their posts
    success = client.scrape_all_categories(max_pages_per_category=5)
    
    if success:
        # Save data in JSON format
        client.save_to_json()
        
        # Save data in CSV format, one file per category
        client.save_to_csv()
        
        
