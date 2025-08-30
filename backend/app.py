from flask import Flask, jsonify
from flask_cors import CORS
from scraper import fetch_all_rss_articles  # 🔥 Import real scraper

app = Flask(__name__)
CORS(app)

@app.route('/news/today')
def get_today_news():
    data = fetch_all_rss_articles()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

