from flask import current_app
from .model import Post
from config import db
from DBoard.Tag.model import Tag
class PostController:

    def add(body):
        try:
            post = Post(
                text = body['text'],
                user_id = body['user_id'],
            )
            for tag_id in body['tags']:
                tag = Tag.query.get(tag_id)
                if tag:
                    post.tags.append(tag)
            
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
    
    def searchByTags(tag_names):
        try:
            query = Post.query.join(Post.tags).join(Tag)
            for tag_name in tag_names:
                query = query.filter(Tag.name == tag_name)
            query = query.group_by(Post.id).having(db.func.count(Tag.id) == len(tag_names))
            # for tag_name in tag_names:
            #     posts = posts.filter(Post.tags.all(Tag.name == tag_name))
            # Post.query.filter(Post.tags.all(Tag.name.in_(tag_names)))
            return [post.get() for post in query.all()]
        except Exception as e:
            current_app.logger.error(e)
        return None