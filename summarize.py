from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variable
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

def summarize_transcription(transcription_text):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please provide a comprehensive summary of the following podcast transcription. I'd like the summary to be about five paragraphs. :\n\n{transcription_text}"}
        ]
    )
    return str(completion.choices[0].message)

def summarize_article(link):
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Please provide a comprehensive summary of the article. I'd like the summary to be about five paragraphs. :\n\n{link}"}
        ]
    )
    return str(completion.choices[0].message)