from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Dict, Any, Optional
from processor import analyze_trends, generate_content_plan
from scraper import scrape_reddit_trends
from models import *
from config import TARGET_SUBREDDITS
import json
import time

app = FastAPI(
    title="Trend Spotter API",
    description="An API that scrapes Reddit for trends and analyzes them with Gemini."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A simple cache to avoid re-scraping and re-analyzing
cache: Dict[str, Any] = {}
CACHE_DURATION_SECONDS = 21600 # 6 hours

@app.get("/api/get-trends", response_model=TrendResponse)
def get_trends():
    """
    Scrapes Reddit, analyzes posts with Gemini to identify trends,
    and returns a structured JSON response.
    """
    current_time = time.time()
    if 'trends_data' in cache and (current_time - cache.get('timestamp', 0)) < CACHE_DURATION_SECONDS:
        print("Returning fresh data from backend cache.")
        return cache['trends_data']

    print("Fetching new data...")

    scraped_data = scrape_reddit_trends(TARGET_SUBREDDITS, post_limit=10)
    
    if not scraped_data:
        raise HTTPException(status_code=500, detail="Failed to scrape any data from Reddit.")

    analysis_result = analyze_trends(scraped_data)
    
    if "error" in analysis_result:
        raise HTTPException(status_code=500, detail=analysis_result)

    try:
        validated_data = TrendResponse(**analysis_result)
        
        cache['trends_data'] = validated_data
        
        return validated_data

    except Exception as e: 
        print(f"Pydantic validation failed: {e}")
        print(f"RAW DATA FROM GEMINI: {analysis_result}")
        raise HTTPException(
            status_code=500, 
            detail={"error": "Gemini output failed validation.", "data": analysis_result}
        )

@app.post("/api/generate-plan", response_model=PlanResponse)
def generate_plan(request: PlanRequest):
    """
    Receives a selected trend and user inputs, then generates a
    day-by-day content creation plan using Gemini.
    """
    print("Received request to generate content plan.")
    
    plan_result = generate_content_plan(request.dict())
    
    if "error" in plan_result:
        raise HTTPException(status_code=500, detail=plan_result)
        
    try:
        validated_plan = PlanResponse(**plan_result)
        return validated_plan
    except Exception as e:
        print(f"Pydantic validation failed for plan: {e}")
        print(f"RAW DATA FROM GEMINI: {plan_result}")
        raise HTTPException(
            status_code=500, 
            detail={"error": "Gemini plan output failed validation.", "data": plan_result}
        )