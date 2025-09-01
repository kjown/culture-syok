from google.genai import types
from pydantic_settings import BaseSettings, SettingsConfigDict

# --- REDDIT CONFIG ---
TARGET_SUBREDDITS = [
    'TikTokCringe',     # Direct TikTok content
    'memes',            # Mainstream trend barometer
    'OutOfTheLoop',     # Context and explanations
    'GenZ',             # Direct voice of the target audience
    'malaysia',         # The Malaysian lens on global/local topics
    'Bolehland',        # The Malaysian meme scene
    'teenagers',        # Unfiltered youth culture
    'TikTok'            # More official TikTok trends
]

# --- GOOGLE GEMINI CONFIG ---
analyze_config = types.GenerateContentConfig(
    temperature=0.8,
    top_p=0.95,
    max_output_tokens=65535,
    response_mime_type="application/json",
    response_schema={
    "type": "OBJECT",
    "properties": {
        "trends": {
            "type": "ARRAY",
            "description": "A list of identified trends based on the provided data.",
            "items": {
                "type": "OBJECT",
                "description": "A single identified trend or meme.",
                "properties": {
                    "trend_name": {"type": "STRING", "description": "The name of the identified trend or meme."},
                    "description": {"type": "STRING", "description": "A concise summary of the trend and its cultural significance. Use the Google Search tool if needed for context."},
                    "marketing_angle": {"type": "STRING", "description": "The core emotional hook or marketing strategy. Explains WHY the trend is popular (e.g., 'Relatability and shared struggle', 'Nostalgia for early 2000s')."},
                    "content_idea": {"type": "STRING", "description": "One single, concrete, actionable content idea for a brand. (e.g., 'A TikTok video of your mascot attempting this dance challenge and failing humorously.')."},
                    "reference_links": {"type": "ARRAY", "description": "A list of Reddit URLs from the input data that are good examples of this trend.", "items": { "type": "STRING" }},
                    "representative_image_url": {"type": "STRING", "description": "A direct URL to an image that represents the trend. Use search if no image is provided in the source data."}
                },
                "required": ["trend_name", "description", "reference_links", "representative_image_url"]
            }
        }
    },
    "required": ["trends"]
}
)

content_config = types.GenerateContentConfig(
    temperature=1,
    top_p=1,
    max_output_tokens=65535,
    response_mime_type="application/json",
    response_schema={
        "type": "OBJECT",
        "properties": {
            "plan_title": {"type": "STRING", "description": f"A creative title for the content plan."},
            "content_medium": {"type": "STRING", "description": "The final content medium specified by the user."},
            "plan": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "day": {"type": "STRING"}, "task": {"type": "STRING"}, "details": {"type": "STRING"}
                    }, "required": ["day", "task", "details"]
                }
            }
        }, "required": ["plan_title", "content_medium", "plan"]
    }
)