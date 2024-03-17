from flask import Flask, jsonify, Blueprint
from GoogleNews import GoogleNews

bp = Blueprint('news', __name__)

@bp.route('/news', methods=['GET'])
def get_news():
    googlenews = GoogleNews(lang="en", period="7d")
    googlenews.get_news("stocks")
    news_results = googlenews.results(sort=True)

    news_data = []
    for entry in news_results:
        article_data = {
            'title': entry['title'],
            'days_ago': entry['date'],
            'link': entry['link'],
            'media_source': entry['media']
        }
        news_data.append(article_data)

    return jsonify(news_data)

