from flask import current_app
from .model import Post
from config import db

class PostController:

    def add(body):
        try:
            post = Post(
                text = body['text'],
                user_id = body['user_id']
            )
            db.session.add(post)
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(e)
        return False
    
    def update(body):
        try:
            post = Post.query.get(body['id'])
            for key, value in body.items():
                setattr(post, key, value)
            db.session.commit()
            db.session.flush()
            return True
        except Exception as e:
            current_app.logger.error(e)
        return False
    
    def delete(id):
        try:
            post = Post.query.get(id)
            db.session.delete(post)
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(e)
        return False
    
    def searchByText(text):
        try:
            matching_posts = Post.query.filter(Post.text.like(f'%{text}%'))
            return [post.get() for post in matching_posts]
        except Exception as e:
            current_app.logger.error(e)
        return None
    
    def searchByTags(tags):
        # try:
        #     matching_posts = Post.query.filter(Post.text.like(f'%{text}%'))
        #     return [post.get() for post in matching_posts]
        # except Exception as e:
        #     current_app.logger.error(e)
        return None