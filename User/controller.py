from flask import redirect, session, render_template, current_app

from .model import Users
from sqlalchemy.exc import IntegrityError
from utilities.constants import *
# from utilities.database_queries import data_add
from config import db

def add_user(body):
    mobile = body['mobile']
    pword = body['pword']
    name = body['name']
    email = body['email']
    user_obj = Users(
            mobile=mobile,
            pword=pword,
            name=name,
            email=email
        )
    try:
        db.session.add(user_obj)
        db.session.commit()
        return True
    except Exception as e:
        pass
    return False
    
def update_user(body):
    # user = body['user']
    # name = body['name']
    # email = body['email']

    try:
        user_ = db.session.query(Users).get(session['name'].user_id)
        for key, value in body.items():
            setattr(user_, key, value)
        db.session.commit()
        db.session.flush()
        current_app.logger.info('successfully updated user')
        return user_
    
    except IntegrityError as i:
        current_app.logger.error(i)
    except Exception as e:
        current_app.logger.error(i)
        # print("in profile update...", e)
    return None

def authenticate(form):
    try:
        email = form['email']
        pword = form['pword']
        current_app.logger.info('checking email and pass')
        user_ = Users.query.filter_by(email=email, pword=pword).first()
        if user_:
            session['name'] = user_
            return True
        return False
    
    except Exception as e:
        print("in authenticate...\n", e)
        return False
        
def forgot_password(form):
    uname = form['user']
    user_ = Users.query.filter_by(user=uname).first()
    # if user_:
    #     email_service(user_.email, 'Reset your Password', user_.user_id)
    return redirect('/login')

def reset_password(form):
    pword = form['pword']
    user_id = int(form['user_id'])
    user_ = Users.query.get(user_id)
    if(user_):
        user_.pword = pword
        db.session.commit()
    return redirect('/login')

def check_user(user):
    user_ = Users.query.filter_by(user=user).first()
    if user_: return True
    return False

def get_session_user(user):
    try:
        return db.session.query(Users).get(user.user_id)
    except Exception as e:

        return None