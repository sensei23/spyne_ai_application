import os
from flask import Flask
import logging
from config import db, session_obj
from User.routes import userBlueprint, authBlueprint
from DBoard.Post.routes import postBlueprint

app = Flask(__name__)

app.config['SECRET_KEY'] = '10101010101010'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".png"]
# app.config["UPLOAD_PATH"] = "image_uploads"

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_SQLALCHEMY"] = db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

session_obj.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(userBlueprint)
app.register_blueprint(authBlueprint)
app.register_blueprint(postBlueprint)