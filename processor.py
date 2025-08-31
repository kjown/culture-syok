import requests
import json
import os
import base64
from google import genai
from google.genai import types
from config import analyze_config, content_config

client = genai.Client(
  api_key=os.environ.get("GEMINI_API_KEY"),
)
model = "gemini-2.5-flash"

def analyze_trends(scraped_data):
    """
    Analyzes data scraped to evaluate trends and marketable ideas
    """
    data_string = json.dumps(scraped_data, indent=2)

    prompt = f"""
    You are a "Relevant Trend Spotter and Analyzer" for a marketing insights platform. Your task is to analyze a raw JSON dump of recent popular Reddit posts and identify emerging trends, memes, and significant discussion topics.

    RULES:
    1.  Analyze the provided JSON data below which contains a list of posts from various subreddits.
    2.  Identify 3-5 distinct, overarching trends or memes. Do not just list individual posts. Synthesize the information. 
    3.  For each trend, provide a concise 'description' explaining what it is and why it's trending. This trend needs to be marketable and can be posted on social media to gain traction.
    4.  Keep everything PG and friendly, e.g. no violence, gore, etc but allow humour
    5.  For the `marketing angle`, identify the core emotion. Is it nostalgia, humor, relatability, community pride? What is the strategic hook for a brand?
    6.  For the `content_idea`, provide ONE single, specific, creative, and ready-to-use idea. It should be so clear a marketer could start working on it immediately. Be specific about the format (e.g., "An Instagram Reel," "A Twitter poll," "A TikTok video using this sound").
    7.  Provide one or two "reference_links" from the provided data that best exemplify this trend.
    8.  For each trend, find the most visually representative and highest quality image from the data and include its 'image_url' in a new field called 'representative_image_url'. If no suitable image exists for a trend, use your search tool for an image using keywords.
    9.  All output should be relevant to a Malaysian audience (local or global trends, memes, slangs, etc they would recognize).
    10. Your final output MUST be a single, valid JSON object. It should be a list of trend objects. Do not include any text or markdown before or after the JSON object.

    Here is the Reddit data:
    {data_string}
    """
    
    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part(text=prompt)
                ]
            )
        ]

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=analyze_config,
        )
        response_text = response.text.strip()
        return json.loads(response_text)

    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Failed to parse text: {response.text}")
        return {"error": f"An error occurred: {e}"}

def generate_content_plan(request_data):
    """
    Generates a detailed, day-by-day content plan based on a trend
    and the user's finalized creative brief.
    """

    trend = request_data.get('trend', {})
    product = request_data.get('product')
    objective = request_data.get('objective')
    call_to_action = request_data.get('call_to_action')
    content_medium = request_data.get('content_medium')
    tone = request_data.get('tone')

    prompt = f"""
    You are an expert Social Media Manager and Content Strategist for the Malaysian market.
    Your task is to create a detailed, step-by-step content plan based on the following creative brief.

    CREATIVE BRIEF
    - Trend Context: "{trend.get('trend_name')}" ({trend.get('description')})
    - Core Marketing Angle: "{trend.get('marketing_angle')}"
    - Product to Market: "{product}"
    - Campaign Objective: "{objective}"
    - Content Medium/Format: "{content_medium}"
    - Desired Tone: "{tone}"
    - Required Call to Action: "{call_to_action}"

    YOUR TASK 
    Based ONLY on the creative brief above, generate a practical, day-by-day plan from initial concept to final posting. The tasks MUST be tailored to the specified `Content Medium/Format`. The final content idea must be creative, authentic, and laser-focused on achieving the `Campaign Objective`.
    """
    try:
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part(text=prompt)
                ]
            )
        ]

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=content_config,
        )
        response_text = response.text.strip()
        return json.loads(response_text)

    except Exception as e:
        print(f"An error occurred with the Gemini API: {e}")
        if 'response' in locals() and hasattr(response, 'text'):
            print(f"Failed to parse text: {response.text}")
        return {"error": f"An error occurred: {e}"}
