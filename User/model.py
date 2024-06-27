from config import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(50), unique=True, nullable=False)
    pword = db.Column(db.String(30), nullable=True)
    mobile = db.Column(db.String(10), unique = True, nullable = False)
    posts = db.relationship('Post', backref='users')
    
    def __init__(self, name, email, pword, mobile):
        self.name = name
        self.email = email
        self.pword = pword
        self.mobile = mobile

    def get(self):
        return {
            "user_id" : self.user_id,
            "mobile" : self.mobile,
            "name" : self.name,
            "email" : self.email,
        }
    
    

    