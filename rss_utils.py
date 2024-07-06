import feedparser
from bs4 import BeautifulSoup

def extract_strong_tags_with_href(html_string):
    # Parse the HTML string with BeautifulSoup
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # Find all <strong> tags
    strong_tags = soup.find_all('strong')
    
    # Extract the text and href attribute (if exists) inside each <strong> tag
    strong_texts_with_href = []
    for tag in strong_tags:
        text = tag.get_text()
        href = tag.find('a')['href'] if tag.find('a') else None
        strong_texts_with_href.append({'text': text, 'href': href})
    
    return strong_texts_with_href


# Refresh rss feeds
def refresh_rss(feed_url):
    feed = feedparser.parse(feed_url)
    return feed.entries[:10]

def get_seroter_daily_entries():
    feed_url = 'https://seroter.wordpress.com/feed'
    entries = []
    for entry in refresh_rss(feed_url):
        if "Daily Reading List" in entry.get("title"):
            entries.append(entry.get("title"))
    return entries

def expand_entry(title):
    feed_url = 'https://seroter.wordpress.com/feed'
    for entry in refresh_rss(feed_url):
        if entry.get("title") == title:
            post = entry.get("content")
            return extract_strong_tags_with_href(post[0]['value'])

def main(feed_url):
    # Main function for rss feeds
    for entry in refresh_rss(feed_url):
        if entry.get("title") == "Daily Reading List \u2013 June 24, 2024 (#345)":
            for content in entry.get("content"):
                print(extract_strong_tags_with_href(content['value']))

if __name__ == "__main__":
    feed_url = 'https://seroter.wordpress.com/feed'
    main(feed_url)