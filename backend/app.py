from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime
from scraper import fetch_all_rss_articles

app = Flask(__name__)
CORS(app)

# Explicit path to avoid cache issues
CACHE_FILE = os.path.join(os.path.dirname(__file__), "cached_articles.json")


@app.route('/news/today', methods=["GET"])
def get_cached_news():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                articles = json.load(f)
                # Filter for today only
                today = datetime.today().date().isoformat()
                today_articles = [a for a in articles if a.get("published", "").startswith(today)]
                return jsonify(today_articles)
        except Exception as e:
            print("⚠️ Failed to load cache:", e)

    # fallback: fetch if cache missing
    try:
        articles = fetch_all_rss_articles()
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/news/fetch-and-cache', methods=["POST"])
def fetch_and_cache_news():
    try:
        articles = fetch_all_rss_articles()
        with open(CACHE_FILE, "w") as f:
            json.dump(articles, f)
        return jsonify({
            "status": "ok",
            "articles_fetched": len(articles),
            "cached_at": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Port binding for Render
if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
