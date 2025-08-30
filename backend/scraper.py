import feedparser
import re

def auto_tag(title):
    title = title.lower()
    tags = []

    if any(word in title for word in ["modi", "parliament", "bjp", "congress", "election", "india"]):
        tags.append("Indian Politics")
    if any(word in title for word in ["nato", "israel", "gaza", "ukraine", "china", "geopolitics"]):
        tags.append("Geopolitics")
    if any(word in title for word in ["ai", "startup", "tech", "nvidia", "google", "microsoft", "software"]):
        tags.append("Technology")
    if any(word in title for word in ["inflation", "finance", "markets", "recession", "stock", "bank"]):
        tags.append("Economics")
    if any(word in title for word in ["culture", "film", "music", "book", "festival"]):
        tags.append("Culture")
    if any(word in title for word in ["sociology", "inequality", "caste", "gender"]):
        tags.append("Sociology")
    if any(word in title for word in ["philosophy", "ethics", "existential", "moral", "nietzsche", "stoic"]):
        tags.append("Philosophy")
    if any(word in title for word in ["business", "startup", "ipo", "merger", "corporate"]):
        tags.append("Business")
    if any(word in title for word in ["world", "global", "diplomacy", "conflict"]):
        tags.append("World Affairs")

    return tags


def extract_image(entry):
    # 1. Try media:content
    if 'media_content' in entry:
        return entry['media_content'][0].get('url', '')

    # 2. Try media:thumbnail
    if 'media_thumbnail' in entry:
        return entry['media_thumbnail'][0].get('url', '')

    # 3. Try image in 'content' or 'summary'
    content = entry.get('content', [{}])[0].get('value', '') or entry.get('summary', '')
    img_match = re.search(r'<img[^>]+src="([^">]+)"', content)
    if img_match:
        return img_match.group(1)

    # 4. Try image in links
    for link in entry.get("links", []):
        if link.get("type", "").startswith("image"):
            return link.get("href", "")

    # 5. Fallback placeholder image
    return "https://placehold.co/300x200?text=No+Image"


def fetch_all_rss_articles():
    sources = {
        "Wired": "https://www.wired.com/feed/rss",
        "The Hindu": "https://www.thehindu.com/news/national/feeder/default.rss",
        "Reuters": "http://feeds.reuters.com/reuters/topNews",
        "Washington Post": "http://feeds.washingtonpost.com/rss/national",
        "The New Yorker": "https://www.newyorker.com/feed/news",
        "NYTimes": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
        "Newslaundry": "https://www.newslaundry.com/feed",
        "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
        "WSJ": "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
        "The Economist": "https://www.economist.com/the-world-this-week/rss.xml",
        "The Guardian": "https://www.theguardian.com/world/rss",
        "Caravan Magazine": "https://caravanmagazine.in/rss",
        "The Wire": "https://thewire.in/feed"
    }

    all_articles = []

    for source, feed_url in sources.items():
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                all_articles.append({
                    "title": entry.get("title", "Untitled"),
                    "link": entry.get("link", ""),
                    "image": extract_image(entry),
                    "tags": auto_tag(entry.get("title", "") + " " + entry.get("summary", "")),
                    "source": source
                })
        except Exception as e:
            print(f"❌ Failed to fetch from {source}: {e}")

    return all_articles
