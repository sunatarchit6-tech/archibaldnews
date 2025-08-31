import feedparser
import re
from newspaper import Article
from dateutil import parser as date_parser

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
