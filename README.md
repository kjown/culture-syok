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

| Core API       | Frontend       | Analytics Service | AI & Automation    | APIs & Services         | Deployment |
|----------------|----------------|-------------------|--------------------|-------------------------|------------|
| [FastAPI](https://fastapi.tiangolo.com/)        | [SvelteKit](https://kit.svelte.dev/)      | [Flask](https://flask.palletsprojects.com/)             | [Google GenAI SDK](https://ai.google.dev/docs/gemini_api_overview)   | [Reddit API (PRAW)](https://praw.readthedocs.io/en/stable/)       | [Vercel](https://vercel.com/docs)     |
| [Pydantic](https://docs.pydantic.dev/)       | [Chart.js](https://www.chartjs.org/docs/latest/)       | [Gunicorn](https://gunicorn.org/)          | [n8n Workflows](https://docs.n8n.io/)      | [X (Twitter) API v2](https://developer.x.com/en/docs/api-reference-index)      | [Docker](https://docs.docker.com/)     |
| [Python 3.11+](https://www.python.org/)   | [Bootstrap](https://getbootstrap.com/docs/)      | [VADER Sentiment](https://github.com/cjhutto/vaderSentiment)   |                    | [Google Calendar API](https://developers.google.com/calendar/api/guides/overview)     |            |
| [Uvicorn](https://www.uvicorn.org/)        |                |                   |                    | [Facebook/Instagram API](https://developers.facebook.com/docs/graph-api/) |            |
|                |                |                   |                    | [Cloudinary](https://cloudinary.com/documentation)              |            |
|                |                |                   |                    | [Google Cloud APIs](https://cloud.google.com/apis)              |            |

## Setup Instructions

### Prerequisites
* Python 3.11+, Node.js, and Docker installed on your machine.
* Clone the repository:
    ```sh
    git clone [https://github.com/kjown/culture-syok.git](https://github.com/kjown/culture-syok.git)
    cd culture-syok
    ```

* **Set up Google Cloud Service Account (for GCS):**
    1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    2.  Select your project (top left).
    3.  In the sidebar, go to **IAM & Admin > Service Accounts**.
    4.  Find your service account, click the three dots on the right, and select **Manage keys**.
    5.  Click **Add Key > Create new key**.
    6.  Choose **JSON** and click **Create**. A JSON credentials file will be downloaded.
    7.  Place this downloaded JSON file in the root directory.
 
  *Note: Ensure your service account is given at least the **Storage Admin** Role*

### Local Development
To run the full CultureSyok platform locally, you will need to set up three main components: the backend, the frontend and the n8n Automation Agent.

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
| Service           | Key                     | Where to Get It                               |
|-------------------|-------------------------|-----------------------------------------------|
| **Gemini AI** | `GEMINI_API_KEY`        | [Google AI Studio](https://aistudio.google.com/apikey) |
| **Reddit** | `REDDIT_CLIENT_ID`      | [Reddit App Preferences](https://www.reddit.com/prefs/apps) |
|                   | `REDDIT_CLIENT_SECRET`  | "                                             |
|                   | `REDDIT_USER_AGENT`     | "                                             |
| **X (Twitter)** | `X_API_KEY`             | [X Developer Portal](https://developer.x.com/en) |
|                   | `X_API_SECRET_KEY`      | "                                             |
|                   | `X_BEARER_TOKEN`        | "                                             |
| **Google APIs** | `GOOGLE_CLIENT_ID`      | [Google Cloud Console](https://console.cloud.google.com/apis/credentials) |
|                   | `GOOGLE_CLIENT_SECRET`  | "                                             |
| **Cloudinary** | `CLOUDINARY_...`        | [Cloudinary Console](https://cloudinary.com/console) |
| **Facebook/IG** | `IG_ACCESS_TOKEN`, etc. | [Meta for Developers](https://developers.facebook.com/) |

**4. Install Python dependencies**
```
pip install -r requirements.txt
```
**5. Start the backend**
```
python /content-gen/run.py
python /scripts/x.py
python /scripts/instagram.py
python /scripts/facebook.py
```
*Note: Social media scripts are designed for engagement data collection, not for posting. Content generation script starts the backend server for processing trends*

**6. Install frontend dependencies**
```
npm install
```

**7. Start the frontend development server**
```
npm run dev
```

**8. Set up n8n**

* **A. Import the Workflows:**
    1.  In the n8n web UI, go to the "Workflows" section.
    2.  Click the "Import from File" button.
    3.  Upload the workflow `.json` files located in the `n8n_workflows/` directory of this project.

* **B. Configure Credentials:**
    1.  Open the imported workflow on your canvas. You will see errors on the nodes that require authentication (e.g., "Google Calendar Trigger," "HTTP Request for X/Twitter").
    2.  **For Google Calendar:** Click on the trigger node. In the "Credential" dropdown, select "Create New." Follow the pop-up authentication flow. You will need the **Client ID** and **Client Secret** from your Google Cloud Console.

  In Google Cloud Console,
    1.   Navigate to **APIs & Services > Credentials**.
    2.   Create a new **OAuth 2.0 Client ID** for a **Web application**.
    3.   Under **Authorised redirect URIs**, add the URI provided by n8n: `http://localhost:5678/rest/oauth2-credential/callback`

* **C. Activate the Workflow:**
    * Once all credentials are configured and the nodes show no errors, toggle the "Active" switch in the top right of the n8n canvas to turn your automation on.

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

## License

This project is for educational and internal use. Please review API terms of service for each platform before deploying in production.
