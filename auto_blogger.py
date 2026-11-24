import os
import pickle
import requests
import datetime
from bs4 import BeautifulSoup
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Blogger settings
BLOG_ID = 'your blog_id'  # Your Blog ID

# Auth scopes
SCOPES = ['https://www.googleapis.com/auth/blogger']

# Load or create credentials
def get_blogger_service():
    creds = None
    if os.path.exists('token.pkl'):
        # Security hardening: Avoid insecure pickle deserialization (CWE-502)
        if os.path.exists('token.json'):
            from google.oauth2.credentials import Credentials
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "' your client_secret.json file here'", SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('blogger', 'v3', credentials=creds)

# Scrape trending topic from Google Trends (with error handling)
import random

import random
import requests
from bs4 import BeautifulSoup
USED_TOPICS_FILE = 'used_topics.txt'

def load_used_topics():
    if os.path.exists(USED_TOPICS_FILE):
        with open(USED_TOPICS_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f.readlines())
    return set()

def save_used_topic(topic):
    with open(USED_TOPICS_FILE, 'a', encoding='utf-8') as f:
        f.write(topic + '\n')


def get_trending_topic(max_retries=10):
    print("🔍 Fetching trending topic from Google Trends...")
    url = "https://trends.google.co.in/trending/rss?geo=IN"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)

    if res.status_code != 200:
        raise Exception(f"❌ Error: Failed to fetch data from Google Trends. Status code: {res.status_code}")

    soup = BeautifulSoup(res.text, 'xml')
    all_topics = [item.title.text for item in soup.find_all("item")]
    used_topics = load_used_topics()

    # Filter out already used topics
    new_topics = [topic for topic in all_topics if topic not in used_topics]

    if not new_topics:
        raise Exception("⚠️ No new trending topics found.")

    topic = random.choice(new_topics)
    print(f"📌 Selected trending topic: {topic}")
    return topic



# Generate post content using Gemini via HuggingFace endpoint (free)
import google.generativeai as genai

# Set the NEW Gemini API key
genai.configure(api_key="your gemini api_key here")

def generate_blog_post(topic):
    print("🤖 Generating blog post using Gemini Pro...")

    # Use Gemini 1.5 Pro (correct and stable as of 2025)
    model = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

    prompt = f"""
    Write a detailed blog post (around 1500 words) on the topic: "{topic} news today".
    The blog should be SEO-optimized, informative, and engaging.It should reach to the most of the crowd .
    Also Use the information which is latest. Dont generalise. focus on that latest news in detail.
    Use proper HTML formatting with:
    - <h2> subheadings
    - bullet points
    - well-structured paragraphs
    - a short conclusion
    - Make sure to include relevant keywords naturally.
    - Use a friendly and conversational tone.
    - Include a brief introduction and conclusion.

    Output ONLY HTML.
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Error during Gemini generation: {e}")
        return f"<h2>{topic}</h2><p>AI content could not be generated. Try again later.</p>"



# Publish to Blogger
def post_to_blogger(service, title, content):
    post = {
        'title': title,
        'content': content,
        'labels': ['AI Generated', 'Trending'],
        'published': datetime.datetime.now().isoformat() + 'Z'
    }
    posts = service.posts()
    result=posts.insert(blogId=BLOG_ID, body=post, isDraft=False).execute()
    print(f"✅ Blog '{title}' published successfully.")
    


# Main execution
if __name__ == '__main__':
    service = get_blogger_service()
    try:
        topic = get_trending_topic()
        content = generate_blog_post(topic)
        post_to_blogger(service, topic, content)
        save_used_topic(topic)
    except Exception as e:
        print(f"❌ Error: {e}")
        

