import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Get the API key from the environment variable
OpenAI.api_key = os.getenv('OPENAI_API_KEY')

def get_summary(content: str, content_type: str) -> str:
    """
    Generate a summary using the OpenAI API.
    
    Args:
        content (str): The content to be summarized (transcription text or article link).
        content_type (str): The type of content ('transcription' or 'article').
        
    Returns:
        str: The generated summary.
    """
    client = OpenAI()
    prompt = f"Please provide a comprehensive summary of the following {content_type}. I'd like the summary to be about five paragraphs:\n\n{content}"
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return str(completion.choices[0].message)

def summarize_transcription(transcription_text: str) -> str:
    return get_summary(transcription_text, 'podcast transcription')

def summarize_article(link: str) -> str:
    return get_summary(link, 'article')