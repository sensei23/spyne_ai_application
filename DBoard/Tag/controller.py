from config import db
from .model import Tag
from flask import current_app

class TagController:

    def add(body):
        try:
            tag = Tag(
                name = body['name']
            )
            db.session.add(tag)
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(e)
        return False