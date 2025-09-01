import requests
import os
from dotenv import load_dotenv
import json
from google.cloud import storage
import schedule
import time

def fetch_and_upload_facebook_data():
    load_dotenv()
    FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
    PAGE_ID = os.getenv("PAGE_ID")
    if not FACEBOOK_ACCESS_TOKEN or not PAGE_ID:
        print("Missing FACEBOOK_ACCESS_TOKEN or PAGE_ID in environment variables.")
        return

    BASE_URL = f"https://graph.facebook.com/v20.0/{PAGE_ID}"

    # Fetch recent posts
    def get_page_posts():
        url = f"{BASE_URL}/posts"
        params = {
            "fields": "id,message,created_time,permalink_url,likes.summary(true),comments.summary(true)",
            "access_token": FACEBOOK_ACCESS_TOKEN
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch Facebook posts: {response.text}")
            return {}
        return response.json()

    # Fetch insights (reach, impressions, engagement)
    def get_page_insights():
        url = f"{BASE_URL}/insights"
        params = {
            "metric": "page_impressions,page_engaged_users,page_fans,page_post_engagements",
            "period": "day",
            "access_token": FACEBOOK_ACCESS_TOKEN
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"Failed to fetch Facebook insights: {response.text}")
            return {}
        return response.json()

    print("\n=== Facebook Posts ===")
    posts = get_page_posts()
    for post in posts.get("data", []):
        print(f"Post ID: {post['id']}")
        print(f"Message: {post.get('message', '')}")
        print(f"Likes: {post['likes']['summary']['total_count']}")
        print(f"Comments: {post['comments']['summary']['total_count']}")
        print("----")

    print("\nFetching Insights...")
    insights = get_page_insights()
    for insight in insights.get("data", []):
        print(f"{insight['name']} - {insight['values']}")

    # Upload posts and insights to Google Cloud Storage
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ayam-debugging-engagement-api-1bd6ccd512be.json")
    client = storage.Client()
    bucket = client.get_bucket("ayam_debugging")

    # Upload posts
    blob_posts = bucket.blob("facebook_post.json")
    blob_posts.upload_from_string(
        json.dumps(posts, ensure_ascii=False, indent=4),
        content_type="application/json"
    )
    print(f"\n🚀 Uploaded {len(posts.get('data', []))} Facebook posts to Google Cloud Storage!")

    # Upload insights
    blob_insights = bucket.blob("facebook_insights.json")
    blob_insights.upload_from_string(
        json.dumps(insights, ensure_ascii=False, indent=4),
        content_type="application/json"
    )
    print(f"🚀 Uploaded Facebook insights to Google Cloud Storage!")


# Schedule the job every hour (change interval as needed)
schedule.every().hour.do(fetch_and_upload_facebook_data)

print("Starting scheduled Facebook data fetch/upload...")
fetch_and_upload_facebook_data()  # Initial run
while True:
    schedule.run_pending()
    time.sleep(60)
