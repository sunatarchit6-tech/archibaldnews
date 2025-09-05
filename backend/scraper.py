import feedparser
import re
from dateutil import parser as date_parser

# ✅ Define auto_tag to prevent NameError
def auto_tag(title):
    title = title.lower()
    tags = []

    TAG_KEYWORDS = {
        "Indian Politics": [
            "modi", "bjp", "congress", "aap", "parliament", "loksabha", "rajyasabha", "election",
            "nda", "upsc", "indian government", "cabinet", "governor", "cm", "sc verdict",
            "politician", "voting", "reservation", "supreme court", "lok sabha", "rajya sabha",
            "policy", "delhi politics"
        ],
        "Geopolitics": [
            "nato", "gaza", "israel", "ukraine", "russia", "china", "taiwan", "iran", "hamas",
            "hezbollah", "un", "sanctions", "geopolitics", "conflict", "defence", "military",
            "global security", "diplomacy", "nuclear"
        ],
        "Technology": [
            "ai", "artificial intelligence", "nvidia", "google", "microsoft", "apple", "openai",
            "chatgpt", "robotics", "software", "hardware", "coding", "developer", "cloud",
            "semiconductors", "data", "cybersecurity", "tech", "startups"
        ],
        "Economics": [
            "inflation", "deflation", "interest rate", "recession", "stock market", "banking",
            "gdp", "unemployment", "cpi", "economy", "fiscal", "budget", "reserve bank", "rbi",
            "finance", "economic policy", "markets", "tax", "monetary"
        ],
        "Culture": [
            "film", "movie", "cinema", "music", "art", "book", "literature", "festival",
            "tradition", "theatre", "dance", "celebration", "painting", "documentary",
            "cultural event", "heritage", "bollywood"
        ],
        "Society": [
            "sociology", "gender", "inequality", "caste", "religion", "discrimination",
            "social justice", "rights", "feminism", "dalit", "minorities", "lgbtq", "poverty",
            "education", "urbanization", "migration", "tribal", "diversity", "social issue",
            "patriarchy"
        ],
        "Philosophy": [
            "philosophy", "ethics", "morality", "existential", "stoic", "stoicism", "nietzsche",
            "sartre", "plato", "aristotle", "utilitarian", "kant", "freedom", "meaning of life",
            "consciousness", "human nature", "logic", "reason"
        ],
        "Business": [
            "startup", "ipo", "merger", "acquisition", "corporate", "business", "entrepreneur",
            "funding", "venture capital", "deal", "valuation", "board", "leadership", "strategy",
            "industry", "profit", "b2b", "brand"
        ],
        "World Affairs": [
            "global", "international", "world", "united nations", "diplomacy", "foreign policy",
            "conflict", "climate", "treaty", "summit", "g20", "global economy", "world bank",
            "imf", "migration", "refugee", "peace talks"
        ]
    }

    for tag, keywords in TAG_KEYWORDS.items():
        if any(keyword in title for keyword in keywords):
            tags.append(tag)

    return tags

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
