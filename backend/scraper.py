import feedparser
import re
from dateutil import parser as date_parser

# Simple tagger
def auto_tag(title):
    title = title.lower()
    tags = []

    TAG_KEYWORDS = {
        "Technology": ["ai", "google", "microsoft", "nvidia", "apple", "openai", "robot", "tech", "software", "cloud", "startup"],
        "Economics": ["inflation", "recession", "gdp", "economy", "stock", "market", "rbi", "bank", "fiscal", "budget", "finance"],
        "Geopolitics": ["gaza", "israel", "ukraine", "russia", "china", "taiwan", "nato", "diplomacy", "un", "military", "sanctions"],
        "Culture": ["movie", "film", "art", "book", "literature", "festival", "music", "theatre", "heritage", "bollywood"],
        "Society": ["gender", "caste", "religion", "education", "lgbtq", "tribal", "poverty", "urban", "rights"],
        "Business": ["ipo", "startup", "funding", "valuation", "merger", "acquisition", "corporate", "profit"],
        "World Affairs": ["global", "united nations", "treaty", "summit", "migration", "refugee", "foreign policy"]
    }

    for tag, keywords in TAG_KEYWORDS.items():
        if any(keyword in title for keyword in keywords):
            tags.append(tag)

    return tags

# Extract image
def extract_image_from_html(entry):
    content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
    match = re.search(r'<img[^>]+src="([^">]+)"', content)
    if match:
        return match.group(1)
    return "https://placehold.co/300x200?text=No+Image"

# Paywall checker
def is_paywalled(entry, link):
    paywall_keywords = ["subscribe", "sign in", "membership", "paywall", "premium", "register"]
    paywalled_domains = ["wsj.com", "economist.com", "barrons.com", "ft.com"]

    if any(domain in link for domain in paywalled_domains):
        return True

    content = entry.get("summary", "") + " " + str(entry.get("content", [{}])[0].get("value", ""))
    if any(keyword in content.lower() for keyword in paywall_keywords):
        return True

    return False

# Fetch RSS
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

                if is_paywalled(entry, link):
                    print(f"⛔ Skipping paywalled article: {link}")
                    continue

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
