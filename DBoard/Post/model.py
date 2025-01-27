import datetime
from config import db
from DBoard.Tag.model import post_tag


class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(500))
    # file_path = db.Column(db.String(80), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.datetime.now())
    # comments = db.relationship('Comment', backref = 'post')
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    tags = db.relationship('Tag', secondary=post_tag, backref='posts')

    def get(self):
        return {
            'id': self.id,
            'text': self.text,
            # 'filename': self.filename,
            'created_on' : self.created_on,
            'user_id' : self.user_id,
            'tags' : [tag.get() for tag in self.tags],
        }