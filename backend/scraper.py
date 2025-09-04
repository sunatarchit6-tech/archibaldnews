import feedparser
import re
from newspaper import Article
from dateutil import parser as date_parser

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

def extract_article_data(link, entry):
    try:
        article = Article(link)
        article.download()
        article.parse()

        author = article.authors[0] if article.authors else entry.get("author", "Unknown")

        if article.publish_date:
            published = date_parser.parse(article.publish_date.isoformat()).isoformat()
        elif "published" in entry:
            published = date_parser.parse(entry["published"]).isoformat()
        else:
            published = ""

        image = article.top_image if article.top_image else extract_image_from_html(entry)

        return {
            "image": image,
            "author": author,
            "published": published
        }

    except Exception as e:
        print(f"⚠️ Error extracting article data: {e}")

        fallback_author = entry.get("author", "Unknown")
        fallback_image = extract_image_from_html(entry)
        fallback_published = ""

        if "published" in entry:
            try:
                fallback_published = date_parser.parse(entry["published"]).isoformat()
            except:
                fallback_published = ""

        return {
            "image": fallback_image,
            "author": fallback_author,
            "published": fallback_published
        }

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

                article_data = extract_article_data(link, entry)

                all_articles.append({
                    "title": title,
                    "link": link,
                    "image": article_data["image"],
                    "author": article_data["author"],
                    "published": article_data["published"],
                    "tags": auto_tag(f"{title} {summary}"),
                    "source": source
                })

        except Exception as e:
            print(f"❌ Failed to fetch from {source}: {e}")

    return all_articles
