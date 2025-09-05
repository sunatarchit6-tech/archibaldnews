import feedparser
import re
from dateutil import parser as date_parser
from datetime import datetime, timedelta

# Define relevant keywords for filtering and tagging
TAG_KEYWORDS = {
    "Broker News": [
        "broker", "zerodha", "groww", "angel one", "upstox", "dhan", "sahi", "icici direct",
        "hdfc securities", "new broker", "discount broker", "full service broker"
    ],
    "Fintech": [
        "fintech", "upi", "digital wallet", "payment app", "neo bank", "paytm", "phonepe",
        "google pay", "cred", "investment app", "personal finance", "fintech startup"
    ],
    "SEBI/Regulation": [
        "sebi", "regulation", "compliance", "market rules", "nse", "bse", "circular", "rbi",
        "margin trading", "leverage", "penalty", "surveillance", "audit", "insider trading"
    ],
    "Stock Market News": [
        "nifty", "sensex", "stock market", "derivatives", "f&o", "options", "intraday",
        "stocks", "ipos", "earnings", "quarterly results", "exchange", "market trend"
    ],
    "Competitor Updates": [
        "zerodha", "kite", "nudge", "pulse", "varsity", "sensibull", "streak",
        "dhan", "options trader", "tag", "strategy builder",
        "groww", "indmoney", "sahi invest"
    ]
}

# Define RSS feed sources
RSS_FEEDS = {

    # Market/finance news
    "Moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
    "Business Standard": "https://www.business-standard.com/rss/markets-106.rss",
    "Economic Times Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "LiveMint": "https://www.livemint.com/rss/markets",
    "BloombergQuint": "https://www.bqprime.com/rss/markets",
    "SEBI Press Releases": "https://www.sebi.gov.in/sebiweb/rss/sebi_news.rss",
    "Sahi Invest": "https://www.sahiinvest.com/feed"
}

# Extract image URL from HTML
def extract_image_from_html(entry):
    content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
    match = re.search(r'<img[^>]+src="([^">]+)"', content)
    return match.group(1) if match else "https://placehold.co/300x200?text=No+Image"

# Tag based on keywords
def auto_tag(text):
    text = text.lower()
    tags = []
    for tag, keywords in TAG_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            tags.append(tag)
    return tags

# Main RSS parsing logic
def fetch_all_rss_articles():
    all_articles = []
    one_week_ago = datetime.now() - timedelta(days=7)

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            print(f"🔗 Fetching from: {source} — {len(feed.entries)} entries")

            for entry in feed.entries[:8]:  # fetch top 8 per source
                title = entry.get("title", "Untitled")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                author = entry.get("author", "Unknown")
                image = extract_image_from_html(entry)

                # Parse published date and filter by time
                try:
                    published_str = entry.get("published", "") or entry.get("updated", "")
                    published_date = date_parser.parse(published_str)
                    if published_date < one_week_ago:
                        continue
                    published = published_date.isoformat()
                except:
                    continue  # skip if date can't be parsed

                tags = auto_tag(f"{title} {summary}")
                if not tags:
                    continue  # skip if no relevant tags

                print(f"✅ Found: {title} ({source}) — Tags: {tags}")
                all_articles.append({
                    "title": title,
                    "link": link,
                    "image": image,
                    "author": author,
                    "published": published,
                    "tags": tags,
                    "source": source
                })

        except Exception as e:
            print(f"❌ Failed to fetch from {source}: {e}")

    print(f"\n✅ Total relevant articles fetched: {len(all_articles)}\n")
    return all_articles

# Run standalone for testing
if __name__ == "__main__":
    fetch_all_rss_articles()
