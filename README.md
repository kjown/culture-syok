<h1 align="center">CultureSyok</h1>

<p align="center">
  <strong>Your AI Marketing <i>Kawan</i> for the Malaysian Market.</strong>
  <br />
  An AI-powered assistant to discover local trends, generate culturally relevant content, and streamline your entire social media workflow.
</p>

<p align="center">
  <img alt="Project Screenshot" src="https://github.com/user-attachments/assets/9ebce3b8-c851-4a5d-8980-104cf0e496c8">
</p>

---

## 🎯 The Challenge: Why Malaysian Social Media is Hard

Growth-stage companies in Malaysia often operate with small marketing teams. They face a unique set of challenges:

* **Lack of Insight into Trending Topics:** Teams are too busy executing daily tasks to monitor what’s trending locally, missing opportunities to join relevant conversations.
  
* **Time-Consuming Content Creation:** Brainstorming fresh, culturally-aware ideas for multiple platforms is a manual and lengthy process, often leading to repetitive content.
  
* **Disorganized Posting Workflow:** Juggling spreadsheets, email approvals, and separate scheduling apps leads to confusion, duplicated efforts, and missed deadlines.
  
* **Poor Measurement of Results:** Gathering and comparing inconsistent metrics from different platforms makes marketing efforts feel like guesswork, not data-driven decisions.
  
* **No Feedback Loop for Improvement:** Without a clear, unified view of performance, teams can't identify what's working and why, forcing every campaign to start from scratch.

## ✨ Our Solution: CultureSyok

* **📈 Automated Trend Detection:** We use APIs like PRAW (for Reddit) to continuously track conversations and identify rising topics in the Malaysian internet space. The tool surfaces what your audience is talking about *right now*.
  
* **🤖 AI-Powered Content Generation:** We feed these trends into Google's Gemini model to automatically generate platform-specific post ideas, captions, and creative briefs. Our AI is prompted to understand both local nuances and global trends.
  
* **🗓️ Integrated Content Planning & Scheduling:** Our platform provides a centralized calendar to plan, draft, approve, and schedule posts automatically at optimal times. (Utilizing Google Calendar API and n8n for automation)
  
* **📊 Unified Performance Dashboards with Sentiment Analysis:** We collect key metrics like likes, comments, click-through rates, etc and display them in an intuitive dashboard. Our sentiment analysis gauges filtered audience reactions audience reactions, turning raw data into actionable insights.
  
* **🔁 Continuous Improvement Loop:** We leverage our model to highlight which campaigns resonated best with audiences and recommend new angles, content formats, or posting strategies for future campaigns, making every marketing effort more effective over time.

## 🛠️ Tech Stack

| Backend       | Frontend       | AI & Automation    | APIs & Services         | Deployment |
|---------------|----------------|--------------------|-------------------------|------------|
| [FastAPI](https://fastapi.tiangolo.com/)      | [SvelteKit](https://kit.svelte.dev/)      | [Google GenAI SDK](https://googleapis.github.io/python-genai/)   | [Reddit API (PRAW)](https://praw.readthedocs.io/en/stable/)       | [Vercel](https://vercel.com/docs)     |
| [Pydantic](https://docs.pydantic.dev/)      | [Chart.js](https://www.chartjs.org/docs/latest/)       | [n8n Workflows](https://docs.n8n.io/)      | [Twitter API v2](https://developer.x.com/en/docs/api-reference-index)          | [Docker](https://docs.docker.com/)     |
| [Python 3.11+](https://www.python.org/)  | [Bootstrap](https://getbootstrap.com/docs/)      |                    | [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)     |            |
| [Uvicorn](https://www.uvicorn.org/)       |                |                    | [Cloudinary](https://cloudinary.com/documentation)              |            |

## Setup Instructions

### Local Development
To get a local copy up and running, follow these steps.

**1. Clone the repository**
```
git clone https://github.com/kjown/ayam-debugging-frontend.git
cd ayam-debugging-frontend
```
**2. Set up a Python virtual environment**
* Create and activate a Python virtual environment:
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
**3. Create an .env file in the project root**
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
REDDIT_CLIENT_ID="YOUR_CLIENT_ID"
REDDIT_CLIENT_SECRET="YOUR_CLIENT_SECRET"
REDDIT_USER_AGENT="YOUR_USER_AGENT"

# Gemini
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"

# X
X_USERNAME="YOUR_USER_NAME"
X_API_KEY="YOUR_API_KEY"
X_API_SECRET_KEY="YOUR_SECRET_KEY"
X_BEARER_TOKEN="YOUR_BEARER_TOKEN"
 
```
Get your Google Calendar credentials here: https://console.cloud.google.com/apis/credentials

Get your Cloudinary credentials here: https://cloudinary.com/console

Get your Reddit credentials by creating an app here: https://www.reddit.com/prefs/apps

Get your X credentials here: https://developer.x.com/en

Generate your API key here: https://aistudio.google.com/apikey
**4. Install Python dependencies**
```
pip install -r requirements.txt
```
**5. Start the backend (FastAPI server)**
```
python /content-gen/run.py
```

**6. Install frontend dependencies**
```
npm install
```

**7. Start the frontend development server**
```
npm run dev
```


## Challenges We Faced

### 1. Difficulty Integrating Components
The backend scraping logic, AI content generation, scheduling system, and frontend dashboard all had to work together. Making these pieces communicate reliably required more time than expected, especially when connecting APIs with different formats and authentication requirements.

### 2. Cloud Deployment Delayal
Because the entire stack was running on local machines, collaboration was harder and testing realistic scenarios (with external webhooks or cloud functions) was limited. It also meant that performance and deployment issues were not discovered early.

### 3. Financial Constraints
Business accounts for Meta and X APIs require paid subscriptions. Without these, it was difficult to gather richer analytics data or fully automate publishing to those platforms. This restricted testing to only free tiers and workarounds.

### 4. Manual Testing Inefficiency
Testing every feature manually was time-consuming and error-prone. It was difficult to repeatedly verify that scraping, AI generation, posting, and dashboard features all worked correctly together.


## Our Takeaways
### 1. Modular Design is Essential
Breaking the system into smaller, well-defined modules (scraper, AI service, scheduler, dashboard) makes integration easier. Well-documented APIs between these modules reduce friction when different parts of the team work in parallel.

### 2. Early Cloud Setup Saves Time
Even a lightweight cloud deployment (using free tiers) early in development helps catch integration and configuration issues before they become bigger problems. It also simplifies testing webhooks and multi-device workflows.

### 3. Automated Testing is Worth It
Implementing even a small suite of unit tests or API tests early would have reduced the manual testing burden. Automated tests can verify that key features continue working after code changes, saving time and reducing bugs.

### 4. Structured Sprints Keep Everyone Aligned
In the fast-paced, often chaotic environment of a hackathon, adopting a more structured Agile/Scrum approach is highly beneficial. Breaking down the project into smaller, focused sprints  creates clearer mini-deadlines. This methodology helps keep everyone on track and on the same page through short, regular check-ins, making final integration much smoother.


## 🤝 The Team

* [Tee Kai Xin](https://github.com/kaixinishappy)
* [Chang Kai Le](https://github.com/ckl515)
* [Nathaniel Inn Tsin Qian](https://github.com/nat-inn)
* [Own Kai Jian](https://github.com/kjown)
* [Wan Muhammad Hisham Bin Md Edlan Jafny](https://github.com/wmh004)
