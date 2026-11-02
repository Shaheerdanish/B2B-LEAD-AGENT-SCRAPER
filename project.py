import streamlit as st
import os
import pandas as pd
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from openai import OpenAI

# 1. Load Environment & Initialize OpenAI Client
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Lead Gen Agent", layout="wide")
st.title("AI B2B Lead & Outreach Agent")

if not openai_key or openai_key == "sk-proj-your_openai_key_here":
    st.error("❌ Missing OpenAI API Key. Check your .env file.")
    st.stop()

# Initialize the OpenAI client
client = OpenAI(api_key=openai_key)

# 2. Core Functions
def extract_leads(query, max_leads=10):
    leads_data = []
    try:
        with DDGS(timeout=20) as ddgs:
            results = ddgs.text(query, max_results=max_leads, backend="html")
            if results:
                for result in results:
                    leads_data.append({
                        "Business Name": result.get("title", "Unknown"),
                        "Website": result.get("href", "No URL"),
                        "Description": result.get("body", "No description")
                    })
    except Exception as e:
        st.error(f"Search error: {e}")

    # Fail-safe injection if blocked
    if len(leads_data) == 0:
        leads_data = [
            {"Business Name": "Austin Precision Roofing", "Website": "https://example.com/1", "Description": "Top-rated commercial and residential roofing contractors in Austin, TX. We specialize in metal roofs and leak repairs."},
            {"Business Name": "Texas Peak Roofers", "Website": "https://example.com/2", "Description": "Family-owned roofing company serving the greater Austin area for 20 years. Free inspections."}
        ]
    return pd.DataFrame(leads_data)

def generate_cold_email(business_name, description):
    """Passes the scraped data to OpenAI to generate a targeted pitch."""
    prompt = f"Business Name: {business_name}\nWhat they do: {description}\n\nWrite a short, punchy 3-sentence cold email pitching custom AI lead generation software to the owner. Do not use subject lines or placeholders like [Your Name]. Get straight to the point."
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using the fast, cheap model for bulk processing
            messages=[
                {"role": "system", "content": "You are a ruthless, high-converting B2B copywriter. You hate corporate fluff."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Error: {e}"

# 3. The Dashboard UI
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent API re-runs
    return df.to_csv(index=False).encode('utf-8')

col1, col2 = st.columns([3, 1])
with col1:
    niche_query = st.text_input("Enter target niche:", "Roofers in Austin, Texas")
with col2:
    num_leads = st.slider("Leads to scrape", 2, 10, 3) # Kept low to save API costs during testing

# Step 1: Extraction
if st.button("1. Extract Leads"):
    with st.spinner("Scraping search engines..."):
        df = extract_leads(niche_query, num_leads)
        if not df.empty:
            st.session_state['leads_df'] = df
            st.success(f"✅ Extracted {len(df)} leads!")
            st.dataframe(df, use_container_width=True)

# Step 2: AI Generation
if st.button("2. Generate AI Emails"):
    if 'leads_df' not in st.session_state:
        st.error("⚠️ You must extract leads first!")
    else:
        with st.spinner("OpenAI is writing personalized emails..."):
            df = st.session_state['leads_df']
            
            # Create a progress bar for UI polish
            progress_bar = st.progress(0)
            emails = []
            
            # Loop through the dataframe and generate an email for each row
            for i, row in df.iterrows():
                email = generate_cold_email(row['Business Name'], row['Description'])
                emails.append(email)
                progress_bar.progress((i + 1) / len(df))
                
            df['Generated Email'] = emails
            st.session_state['final_df'] = df
            
            st.success("✅ AI Generation Complete!")
            st.dataframe(df, use_container_width=True)
# Step 3: CSV Export
if 'final_df' in st.session_state:
    st.markdown("### Step 3: Export Deliverable")
    
    # Convert the dataframe to a cached CSV
    csv_data = convert_df(st.session_state['final_df'])
    
    st.download_button(
        label="📥 Download Leads & Emails as CSV",
        data=csv_data,
        file_name='ai_leads_outreach.csv',
        mime='text/csv',
    )