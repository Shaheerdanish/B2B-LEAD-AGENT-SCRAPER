🚀 AI B2B Lead & Outreach Agent

A high-performance Micro-SaaS built to automate B2B lead generation and personalized cold outreach.

This tool eliminates the manual grind of prospecting. It dynamically scrapes search engines for niche local businesses, extracts their details, and pipes that data directly into an LLM to generate highly targeted, 3-sentence cold emails designed to convert.

✨ Core Features

Dynamic Data Extraction: Uses the duckduckgo-search HTML backend to bypass aggressive scraping timeouts and rate limits without needing premium API keys.

Built-in Fail-Safe: Automatically injects structural dummy data if an IP shadow-ban occurs, ensuring the pipeline never breaks during client demos.

AI Agent Integration: Leverages the OpenAI API (GPT-4o-mini) with strict system prompts to act as a ruthless B2B copywriter, generating zero-fluff personalized pitches based on the scraped business descriptions.

Memory-Safe Export: Utilizes Streamlit's @st.cache_data to lock the final dataframe in memory, allowing users to download the deliverable as a clean CSV without triggering redundant API calls.

🛠️ The Tech Stack

Frontend: Streamlit (Rapid UI/UX deployment)

Backend: Python 3

Data Processing: Pandas

Web Scraping: DuckDuckGo Search API

AI/LLM: OpenAI Python SDK

💻 Local Setup & Installation

Follow these steps to run the agent on your local machine.

1. Clone the repository:

git clone https://github.com/YOUR_USERNAME/ai-lead-agent.git
cd ai-lead-agent


2. Isolate your environment:

python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt


4. Secure your API keys:
Create a .env file in the root directory and add your OpenAI key:

OPENAI_API_KEY="sk-proj-YOUR_OPENAI_KEY_HERE"


5. Launch the Dashboard:

streamlit run app.py


☁️ Cloud Deployment (Streamlit Community Cloud)

To deploy this live for client demonstrations:

Push this repository to GitHub (ensure your .env file is in your .gitignore).

Log into Streamlit Community Cloud.

Connect your repository and set the main filepath to app.py.

CRITICAL: Before clicking Deploy, go to Advanced Settings > Secrets and securely inject your API key:

OPENAI_API_KEY="sk-proj-YOUR_OPENAI_KEY_HERE"


Deploy and share your public link!

Built as a scalable B2B automation tool.
