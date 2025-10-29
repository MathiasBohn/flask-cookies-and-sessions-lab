#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User, ArticleSchema, UserSchema

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10k'
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
    articles = [ArticleSchema().dump(a) for a in Article.query.all()]
    return make_response(articles)

@app.route('/articles/<int:id>')
def show_article(id):
    # Step 1: Initialize the session for page views
    if 'page_views' not in session:
        session['page_views'] = 0
    
    # Step 2: Increment the session on each request
    session['page_views'] = session['page_views'] + 1
    
    # Step 3: Send response based on session data
    if session['page_views'] <= 3:
        # User can view the article
        article = db.session.get(Article, id)
        return make_response(ArticleSchema().dump(article), 200)
    else:
        # User has exceeded the limit
        return make_response({'message': 'Maximum pageview limit reached'}, 401)

if __name__ == '__main__':
    app.run(port=5555)