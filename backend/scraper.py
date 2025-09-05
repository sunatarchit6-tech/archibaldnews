import feedparser
import re
from dateutil import parser as date_parser
from datetime import datetime, timedelta

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

RSS_FEEDS = {
    "Zerodha": "https://zerodha.com/z-connect/feed",
    "Dhan": "https://blog.dhan.co/feed/",
    "Groww": "https://groww.in/blog/feed",
    "INDmoney": "https://indmoney.com/feed",
    "Sahi Invest": "https://www.sahiinvest.com/feed",
    "Moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
    "Business Standard": "https://www.business-standard.com/rss/markets-106.rss",
    "Economic Times Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "LiveMint": "https://www.livemint.com/rss/markets",
    "BloombergQuint": "https://www.bqprime.com/rss/markets",
    "SEBI Press Releases": "https://www.sebi.gov.in/sebiweb/rss/sebi_news.rss"
}

def extract_image_from_html(entry):
    content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "")
    match = re.search(r'<img[^>]+src="([^">]+)"', content)
    return match.group(1) if match else "https://placehold.co/300x200?text=No+Image"

def auto_tag(text):
    text = text.lower()
    tags = []
    for tag, keywords in TAG_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            tags.append(tag)
    return tags

def fetch_all_rss_articles():
    all_articles = []
    now = datetime.utcnow()
    one_week_ago = now - timedelta(days=7)

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:5]:
                title = entry.get("title", "Untitled")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                author = entry.get("author", "Unknown")
                image = extract_image_from_html(entry)

                try:
                    published_raw = entry.get("published", "") or entry.get("updated", "")
                    published_dt = date_parser.parse(published_raw)
                    if published_dt < one_week_ago:
                        continue  # skip if older than 7 days
                    published = published_dt.isoformat()
                except:
                    continue  # skip articles without valid date

                tags = auto_tag(f"{title} {summary}")
                if not tags:
                    continue  # skip irrelevant articles

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

    return all_articles

# Debug only
if __name__ == "__main__":
    articles = fetch_all_rss_articles()
    print(f"\n✅ Total relevant articles fetched: {len(articles)}\n")
    for art in articles:
        print(f"• {art['title']} ({art['source']}) — Tags: {', '.join(art['tags'])}")
