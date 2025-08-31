from flask import Flask, jsonify
from flask_cors import CORS
import os

# 👇 Ensure correct relative import (adjust if your folder name is different)
from scraper import fetch_all_rss_articles

app = Flask(__name__)
CORS(app)

@app.route('/news/today')
def get_news():
    try:
        articles = fetch_all_rss_articles()
        return jsonify(articles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
