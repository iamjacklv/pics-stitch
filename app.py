
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/api/blog-posts', methods=['GET'])
def get_blog_posts():
    posts = BlogPost.query.order_by(BlogPost.date.desc()).all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'date': post.date.isoformat()
    } for post in posts])

@app.route('/api/blog-posts', methods=['POST'])
def create_blog_post():
    data = request.get_json()
    new_post = BlogPost(
        title=data['title'],
        content=data['content']
    )
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Blog post created successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
