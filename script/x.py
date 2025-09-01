bearer_token = os.getenv("X_BEARER_TOKEN")
username = os.getenv("X_USERNAME")


import requests
from dotenv import load_dotenv
import os
import json
from google.cloud import storage


# Load environment variables
load_dotenv()
bearer_token = os.getenv("X_BEARER_TOKEN")
username = os.getenv("X_USERNAME")


# Get your user ID
user_url = f"https://api.twitter.com/2/users/by/username/{username}"
headers = {"Authorization": f"Bearer {bearer_token}"}
user_response = requests.get(user_url, headers=headers)
user_id = user_response.json()["data"]["id"]
print("User lookup status:", user_response.status_code)
print("User info:", json.dumps(user_response.json(), indent=4))


# Get all tweets from your account
tweets_url = f"https://api.twitter.com/2/users/{user_id}/tweets"
params = {
    "tweet.fields": "created_at,public_metrics",
    "max_results": 100
}
tweets_response = requests.get(tweets_url, headers=headers, params=params)
tweets_data = tweets_response.json()


# Print tweets on terminal for review
print("\n=== Tweets ===")
for tweet in tweets_data.get("data", []):
    print(f"ID: {tweet['id']}")
    print(f"Text: {tweet['text']}")
    print(f"Created at: {tweet['created_at']}")
    print(f"Likes: {tweet['public_metrics']['like_count']}, "
          f"Retweets: {tweet['public_metrics']['retweet_count']}, "
          f"Replies: {tweet['public_metrics']['reply_count']}, "
          f"Quotes: {tweet['public_metrics']['quote_count']}")
    print("-" * 50)


# Save tweets data locally as JSON
# with open("tweets.json", "w", encoding="utf-8") as f:
#     json.dump(tweets_data, f, ensure_ascii=False, indent=4)     
# print("\n💾 Saved tweets data locally to tweets.json!")


# Upload JSON data to Google Cloud Storage
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ayam-debugging-engagement-api-1bd6ccd512be.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ayam-debugging-engagement-api-1bd6ccd512be.json")


client = storage.Client()
bucket = client.get_bucket("ayam_debugging")
blob = bucket.blob("tweets.json")  # File name in GCS
blob.upload_from_string(
    json.dumps(tweets_data, ensure_ascii=False, indent=4),
    content_type="application/json"
)
print(f"\n🚀 Uploaded {len(tweets_data.get('data', []))} tweets directly to Google Cloud Storage!")


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
