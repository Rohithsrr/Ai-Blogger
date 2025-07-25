# 🤖 Automated Blogger Publisher with Google Trends & Gemini AI

This Python script automates the process of creating and publishing blog posts on Blogger. It fetches a trending topic from Google Trends for India, generates a detailed, SEO-optimized article using the Gemini Pro AI model, and then automatically publishes it to your blog.

## ✨ Features

-   **Automated Content Pipeline**: Fetches, writes, and publishes content without manual intervention.
-   **Trending Topics**: Scrapes the latest trending topics from the Google Trends India RSS feed.
-   **AI-Powered Content**: Uses Google's Gemini Pro model to generate high-quality, detailed blog posts.
-   **Avoids Duplicates**: Keeps track of published topics in `used_topics.txt` to prevent reposting.
-   **Easy Authentication**: Uses OAuth 2.0 for secure access to the Blogger API, storing credentials for future use.
-   **Ready to Publish**: The generated content is formatted in HTML, ready for immediate publishing.

---

## ⚙️ How It Works

The script follows these steps:

1.  **Authenticate**: It checks for existing Blogger API credentials (`token.pkl`). If not found, it opens a browser window for you to log in and authorize access.
2.  **Fetch Topic**: It connects to the Google Trends RSS feed for India (`geo=IN`) and scrapes the current list of trending search topics.
3.  **Select Topic**: It filters out any topics that have been used before (by checking `used_topics.txt`) and randomly selects a new topic from the remaining list.
4.  **Generate Content**: It sends a detailed prompt to the Gemini Pro API, asking it to write a ~1500 word blog post on the selected topic.
5.  **Publish Post**: It uses the Blogger API to insert the newly generated title and HTML content as a new post on your specified blog.
6.  **Log Topic**: After successful publishing, it saves the topic to `used_topics.txt` to avoid using it again.

---

## 🚀 Setup and Installation

Follow these steps to get the project running on your local machine.

### Prerequisites

-   Python 3.7 or higher
-   A Google Account
-   A Blogger blog

### 1. Clone the Repository

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
cd your-repository-name
```

### 2. Install Dependencies

It's recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required packages
pip install google-api-python-client google-auth-oauthlib requests beautifulsoup4 google-generativeai
```

### 3. Configure Google Blogger API Credentials

You need to enable the Blogger API and get credentials for your application.

1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a new project.
3.  Go to **APIs & Services > Library**, search for "**Blogger API v3**", and **Enable** it.
4.  Go to **APIs & Services > OAuth consent screen**.
    -   Choose **External** and click **Create**.
    -   Fill in the required fields (app name, user support email). You can leave most fields blank.
    -   Add your email address under **Test users**.
5.  Go to **APIs & Services > Credentials**.
    -   Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
    -   Select **Desktop app** as the Application type.
    -   Click **Create**.
    -   A popup will appear. Click **DOWNLOAD JSON**.
6.  Rename the downloaded file to `client_secret.json` and place it in the project's root directory.

### 4. Get Your Gemini API Key

1.  Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Click **Create API key in new project**.
3.  Copy the generated API key.
4.  Open the Python script and paste your key into this line:
    ```python
    genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
    ```

### 5. Configure Your Blog ID

1.  Go to your Blogger dashboard.
2.  Look at the URL in your browser's address bar. It will look something like `blogger.com/blog/posts/#################`.
3.  The long string of numbers is your **Blog ID**.
4.  Open the Python script and paste your Blog ID into this line:
    ```python
    BLOG_ID = 'YOUR_BLOG_ID_HERE'
    ```

---

##
