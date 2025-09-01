import praw
import os
from dotenv import load_dotenv

load_dotenv()

def scrape_reddit_trends(subreddits, post_limit=25):
    reddit = praw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent=os.getenv("REDDIT_USER_AGENT"),
    )

    all_posts_data = []
    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub)
            hot_posts = subreddit.hot(limit=post_limit)
            
            for post in hot_posts:
                post_data = {
                    "subreddit": sub,
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "url": f"https://reddit.com{post.permalink}",
                    "selftext": post.selftext[:500], # Truncate for brevity
                    "image_url": get_image_url(post)
                }
                all_posts_data.append(post_data)
        except Exception as e:
            print(f"Could not scrape {sub}: {e}")
            
    return all_posts_data

def get_image_url(post):
    """
    Intelligently finds the best possible image URL for a Reddit post.
    It prioritizes high-resolution images over thumbnails.
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    
    if any(post.url.lower().endswith(ext) for ext in image_extensions):
        return post.url
    
    if hasattr(post, 'is_gallery') and post.is_gallery:
        try:
            first_image_id = list(post.gallery_data['items'])[0]['media_id']
            return f"https://i.redd.it/{first_image_id}.jpg"
        except (KeyError, IndexError):
            pass

    if hasattr(post, 'preview'):
        try:
            return post.preview['images'][0]['source']['url']
        except (KeyError, IndexError):
            pass

    if hasattr(post, 'thumbnail') and post.thumbnail not in ['self', 'default', 'nsfw']:
        return post.thumbnail
        
    return None
