import feedparser
import re
from dateutil import parser as date_parser
from datetime import datetime, timedelta

# ------------------------------
# ✅ Define keywords for tagging
# ------------------------------
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

# ------------------------------
# ✅ Define all RSS feed sources
# ------------------------------
RSS_FEEDS = {
    # Competitor blogs
    "Zerodha": "https://zerodha.com/z-connect/feed",
    "Dhan": "https://blog.dhan.co/feed/",
    "Groww": "https://groww.in/blog/feed",
    "INDmoney": "https://indmoney.com/feed",
    "Sahi Invest": "https://www.sahiinvest.com/feed",
    # Market/finance news
    "Moneycontrol": "https://www.moneycontrol.com/rss/latestnews.xml",
    "Business Standard": "https://www.business-standard.com/rss/markets-106.rss",
    "Economic Times Markets": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
    "LiveMint": "https://www.livemint.com/rss/markets",
    "BloombergQuint": "https://www.bqprime.com/rss/markets",
    "SEBI Press Releases": "https://www.sebi.gov.in/sebiweb/rss/sebi_news.rss"
}

# ------------------------------
# ✅ Extract image from HTML
# ------------------------------
def extract_image_from_html(entry):
    content = entry.get("content", [{}])[0].get("value", "") or entry.get("summary", "") or entry.get("description", "")
    match = re.search(r'<img[^>]+src="([^">]+)"', content)
    return match.group(1) if match else "https://placehold.co/300x200?text=No+Image"

# ------------------------------
# ✅ Tag based on content
# ------------------------------
def auto_tag(text):
    text = text.lower()
    tags = []
    for tag, keywords in TAG_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            tags.append(tag)
    return tags

# ------------------------------
# ✅ Main fetch function
# ------------------------------
def fetch_all_rss_articles():
    all_articles = []
    cutoff_date = datetime.now() - timedelta(days=2)

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            print(f"🔍 Processing {source} — {len(feed.entries)} entries found")

            count = 0
            for entry in feed.entries[:15]:
                title = entry.get("title", "Untitled")
                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                author = entry.get("author", "Unknown")
                image = extract_image_from_html(entry)

                try:
                    published = date_parser.parse(entry.get("published", ""))
                    if published < cutoff_date:
                        continue
                    published_iso = published.isoformat()
                except:
                    published_iso = ""

                tags = auto_tag(f"{title} {summary}")
                if not tags:
                    continue

                all_articles.append({
                    "title": title,
                    "link": link,
                    "image": image,
                    "author": author,
                    "published": published_iso,
                    "tags": tags,
                    "source": source
                })

                count += 1

            print(f"✅ {source}: {count} relevant articles added\n")

        except Exception as e:
            print(f"❌ Failed to fetch from {source}: {e}")

    return all_articles

# ------------------------------
# ✅ Run manually
# ------------------------------
if __name__ == "__main__":
    articles = fetch_all_rss_articles()
    print(f"\n📰 Total relevant articles fetched: {len(articles)}\n")
    for art in articles:
        print(f"• {art['title']} ({art['source']}) — Tags: {', '.join(art['tags'])}")
