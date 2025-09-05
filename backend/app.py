from flask import Flask, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime
from scraper import fetch_all_rss_articles

app = Flask(__name__)
CORS(app)

CACHE_FILE = "cached_articles.json"

@app.route('/news/today')
def get_cached_news():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                articles = json.load(f)
                return jsonify(articles)
        except Exception as e:
            print("⚠️ Failed to load cache:", e)

    # fallback: fetch fresh if cache fails
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
