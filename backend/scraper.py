import feedparser
import re
from dateutil import parser as date_parser

def extract_image_from_html(entry):
    content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
    match = re.search(r'<img[^>]+src="([^">]+)"', content)
    if match:
        return match.group(1)
    return "https://placehold.co/300x200?text=No+Image"

def fetch_all_rss_articles():
    sources = {
        "Wired": "https://www.wired.com/feed/rss",
        "TechCrunch": "https://techcrunch.com/feed/",
        "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "WSJ": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
        "The Guardian": "https://www.theguardian.com/world/rss"
    }

    all_articles = []

    for source, feed_url in sources.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:3]:
                title = entry.get("title", "Untitled")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                image = extract_image_from_html(entry)
                author = entry.get("author", "Unknown")

                try:
                    published = date_parser.parse(entry.get("published", "")).isoformat()
                except:
                    published = ""

                all_articles.append({
                    "title": title,
                    "link": link,
                    "image": image,
                    "author": author,
                    "published": published,
                    "tags": auto_tag(f"{title} {summary}"),
                    "source": source
                })

        except Exception as e:
            print(f"❌ Failed to fetch from {source}: {e}")

    return all_articles
