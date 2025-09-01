import requests
import os
from dotenv import load_dotenv
import json


load_dotenv()


access_token = os.getenv("IG_ACCESS_TOKEN")
ig_user_id = os.getenv("IG_USER_ID")


# Fetch recent posts
url = f"https://graph.facebook.com/v20.0/{ig_user_id}/media"
params = {
    "fields": "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count",
    "access_token": access_token
}
response = requests.get(url, params=params)
data = response.json()


print(data)
from google.cloud import storage


# Print posts in readable format
print("\n=== Instagram Posts ===")
for post in data.get("data", []):
    print(f"ID: {post.get('id')}")
    print(f"Caption: {post.get('caption')}")
    print(f"Type: {post.get('media_type')}")
    print(f"URL: {post.get('media_url')}")
    print(f"Permalink: {post.get('permalink')}")
    print(f"Timestamp: {post.get('timestamp')}")
    print(f"Likes: {post.get('like_count')}, Comments: {post.get('comments_count')}")
    print("-" * 50)


# Upload JSON data to Google Cloud Storage
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ayam-debugging-engagement-api-1bd6ccd512be.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ayam-debugging-engagement-api-1bd6ccd512be.json")

client = storage.Client()
bucket = client.get_bucket("ayam_debugging")

blob = bucket.blob("instagram.json")  # File name in GCS
blob.upload_from_string(
    json.dumps(data, ensure_ascii=False, indent=4),
    content_type="application/json"
)

print(f"\n🚀 Uploaded {len(data.get('data', []))} Instagram posts directly to Google Cloud Storage!")


# --- Scheduling Example ---
# To fetch data regularly, install 'schedule' package:
# pip install schedule

# import schedule
# import time

# def fetch_tweets():
#     # Place your fetching code here (uncomment above)
#     pass

# schedule.every().hour.do(fetch_tweets)  # Change interval as needed

# while True:
#     schedule.run_pending()
#     time.sleep(60)
