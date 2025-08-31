# Project Title

## Setup Instructions
### 1. Clone the repository
```
git clone https://github.com/kjown/ayam-debugging-frontend.git
cd ayam-debugging-frontend
```
### 2. Set up a Python virtual environment
It’s recommended to use a virtual environment to isolate dependencies:
```
python -m venv venv
```

Activate it:

On macOS/Linux:
```
source venv/bin/activate
```

On Windows (Command Prompt):
```
venv\Scripts\activate
```
### 3. Create an .env file in the project root
```
# Google Calendar
GOOGLE_CLIENT_ID="YOUR_CLIENT_ID"
GOOGLE_CLIENT_SECRET="YOUR_CLIENT_SECRET"
ORIGIN="http://localhost:5173"
 
# Cloudinary
CLOUDINARY_CLOUD_NAME="YOUR_CLOUDINARY_CLOUD_NAME"
CLOUDINARY_API_KEY="YOUR_CLOUDINARY_API_KEY"
CLOUDINARY_API_SECRET="YOUR_CLOUDINARY_API_SECRET"

# Reddit
REDDIT_CLIENT_ID= YOUR_CLIENT_ID
REDDIT_CLIENT_SECRET= YOUR_CLIENT_SECRET
REDDIT_USER_AGENT='YOUR_USER_AGENT'

# Gemini
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
 
```
Get your google calendar credentials here: https://console.cloud.google.com/apis/credentials

Get your cloudinary credentials here: https://cloudinary.com/console

Get your reddit credentials by creating an app here: https://www.reddit.com/prefs/apps

Generate your API key here: https://aistudio.google.com/apikey
### 4. Install Python dependencies
```
pip install -r requirements.txt
```
### 5. Start the backend (FastAPI server)
```
uvicorn main:app --reload
```

### 6. Install frontend dependencies
```
npm install
```

### 7. Start the frontend development server
```
npm run dev
```

## Team Members
1. ⁠Tee Kai Xin
2. ⁠Chang Kai Le
3. Nathaniel Inn Tsin Qian
4. Own Kai Jian
5. ⁠Wan Muhammad Hisham Bin Md Edlan Jafny

## Problems 
### 1. Lack of insight into trending topics
Growth-stage companies often operate with small marketing teams that are too busy executing daily tasks to monitor what’s trending online. As a result, they miss opportunities to align content with topics that are currently drawing attention. Without these insights, their posts feel disconnected from audience conversations and fail to gain traction.

### 2. Time-consuming content creation
Brainstorming fresh ideas, drafting copy, and customizing posts for each social media channel is a manual and lengthy process. Teams frequently run out of ideas or fall back on repetitive content that does not stand out. This slows down campaign execution and reduces consistency.

### 3. Disorganized posting workflow
Marketing teams often juggle multiple disconnected tools to plan, approve, and publish content. Ideas may sit in spreadsheets, draft posts get reviewed over email or chat, and scheduling happens in separate applications. This fragmented process leads to confusion, duplicated efforts, and missed deadlines. Without a unified workflow, it becomes difficult to coordinate tasks, maintain version control, and ensure posts go live at the right time across different platforms.

### 4. Poor measurement of results
Even if campaigns are launched successfully, teams struggle to gather performance data in one place. Metrics from different social media platforms are inconsistent and difficult to compare. Without a clear view of impressions, engagement, and conversions, marketing efforts feel like guesswork rather than data-driven decisions.

### 5.⁠ ⁠No feedback loop for improvement
Because performance data is fragmented, teams do not know what is working and why. They cannot identify which topics resonate with the audience or which post formats generate the highest engagement. Without structured learning, every campaign starts from scratch instead of building on past success.

## Proposed solutions
### 1.⁠ ⁠Automated trend detection
Implement web scraping tools such as PRAW for Reddit, along with other APIs, to continuously track conversations and identify rising topics. By scoring topics based on engagement velocity and relevance, the tool surfaces what audiences are talking about right now. This helps companies stay current and publish content that naturally attracts attention.

### 2.⁠ ⁠AI-powered content generation
Feed these identified trends into AI models to automatically generate post ideas, captions, and creative briefs tailored to specific platforms. The AI can adapt tone, length, and style for LinkedIn, Twitter (X), Instagram, TikTok, or blogs, giving teams high-quality starting drafts that save hours of manual work.

### 3.⁠ ⁠Integrated content planning and scheduling
Provide a centralized platform where teams can plan campaigns on a visual calendar, draft and approve content in one place, and schedule posts to go live automatically at optimal times. This reduces friction, improves coordination, and ensures content is published consistently without last-minute rushes.

### 4.⁠ ⁠Performance dashboards with sentiment analysis
Collect metrics such as impressions, likes, shares, comments, and click-through rates directly from social media APIs and display them in an easy-to-understand dashboard. AI-based sentiment analysis can evaluate comments and reactions to gauge audience mood and detect potential issues early. The dashboard turns raw data into actionable insights.

### 5.⁠ ⁠Continuous improvement loop
Leverage AI to highlight which campaigns performed best and explain why certain posts resonated. The system can recommend new angles, content formats, or posting strategies for future campaigns. This creates a feedback loop where every marketing effort becomes smarter and more effective over time.

## Challenges

### 1. Difficulty integrating different components
The backend scraping logic, AI content generation, scheduling system, and frontend dashboard all had to work together. Making these pieces communicate reliably required more time than expected, especially when connecting APIs with different formats and authentication requirements.

### 2. No deployment to cloud platforms yet
Because the entire stack was running on local machines, collaboration was harder and testing realistic scenarios (with external webhooks or cloud functions) was limited. It also meant that performance and deployment issues were not discovered early.

### 3. Financial constraints limiting API access
Business accounts for Meta and X APIs require paid subscriptions. Without these, it was difficult to gather richer analytics data or fully automate publishing to those platforms. This restricted testing to only free tiers and workarounds.

### 4. Manual testing inefficiency
Testing every feature manually was time-consuming and error-prone. It was difficult to repeatedly verify that scraping, AI generation, posting, and dashboard features all worked correctly together.


## Learnings
### 1. Modular design is essential
Breaking the system into smaller, well-defined modules (scraper, AI service, scheduler, dashboard) makes integration easier. Well-documented APIs between these modules reduce friction when different parts of the team work in parallel.

### 2. Early cloud setup saves time later
Even a lightweight cloud deployment (using free tiers) early in development helps catch integration and configuration issues before they become bigger problems. It also simplifies testing webhooks and multi-device workflows.

### 3. Automated testing is worth the investment
Implementing even a small suite of unit tests or API tests early would have reduced the manual testing burden. Automated tests can verify that key features continue working after code changes, saving time and reducing bugs.

## Tech Stacks
1. ⁠Svetlekit
2. ⁠⁠Chart.js
3. ⁠⁠n8n
4. ⁠⁠Gemini LLM
5. ⁠⁠Docker
6. PRAW
7. ⁠FastAPI
8. ⁠⁠Ngrok
9. ⁠GenAI SDK
10. Twitter API v2
11. Google Calendar API
12. Cloudinary
