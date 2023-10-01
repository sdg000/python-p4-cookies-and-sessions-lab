#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200



@app.route('/articles')
def index_articles():

    articles = Article.query.all()
    articles_dict = [article.to_dict() for article in articles]
    response = make_response(jsonify(articles_dict), 200)
    return response



# View Function to limit user article view to 3
@app.route('/articles/<int:id>')
def show_article(id):

    # step 1: if user viewing for first time, set counter to 0 or get current counter value
    session['page_views'] = session.get('page_views', 0)

    # step 2: increase the value of counter by 1
    session['page_views'] += 1

    # step 3: check if counter is more than 3, render error
    if session['page_views'] > 3:
        response = make_response(
            {'message': 'Maximum pageview limit reached'},
            401
        )
        return response
    
    # else if counter is not more than 3, attempt to fetch and serve article using Article ID
    article = Article.query.filter(Article.id == id).first()

    if article:
        response = make_response(
            jsonify(article.to_dict()),
            200
        )
        return response
    else:
        response = make_response(
            {'message': 'Article not found'},
            200
        )
        return response


if __name__ == '__main__':
    app.run(port=5555)
