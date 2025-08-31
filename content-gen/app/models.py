from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional

class TrendItem(BaseModel):
    trend_name: str
    description: str
    marketing_angle: str
    content_idea: str
    reference_links: List[HttpUrl]
    representative_image_url: str

class TrendResponse(BaseModel):
    trends: List[TrendItem]

class PlanStep(BaseModel):
    day: str
    task: str
    details: str

class PlanResponse(BaseModel):
    plan_title: str
    content_medium: str
    plan: List[PlanStep]

class PlanRequest(BaseModel):
    trend: TrendItem
    product: str = Field(..., description="What the user is trying to market.", example="Our new 'Pandan Gula Melaka' Latte")
    objective: str = Field(..., description="The primary goal of the content.", example="Drive trial and awareness for the new drink.")
    call_to_action: str = Field(..., description="What the audience should do after seeing the content.", example="Come in and try one today! #PandanKopi")
    content_medium: str = Field(..., description="The format for the content.", example="Instagram Reel")
    tone: str = Field(..., description="The desired tone of the content.", example="Informal and Fun")