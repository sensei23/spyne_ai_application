from flask import redirect, session, render_template

from .model import Users
from sqlalchemy.exc import IntegrityError
from utilities.constants import *
# from utilities.database_queries import data_add
from config import db

def add_user(body):
    user = body['user']
    pword = body['pword']
    name = body['name']
    email = body['email']
    user_obj = Users(
            user=user,
            pword=pword,
            name=name,
            email=email
        )

    try:
        # data_add(user_obj)
        return render_template('login.html', msg='You have been successfully signed up')
    except IntegrityError as i:
        print(i)
        return render_template('index.html')
    except Exception as e:
        print("in signup...", e)
        return render_template('error.html')

def update_user(body):
    # user = body['user']
    # name = body['name']
    # email = body['email']
    

    try:
        # data_add(user_obj)
        user_ = db.session.query(Users).get(session['name'].user_id)
        print(user_.get())
        for key, value in body.items():
            setattr(user_, key, value)

        db.session.commit()
        db.session.flush()
        print(user_.get())
        print('here')
        # return {"message":"Password updates successfully"}
        return render_template('user-profile.html', user=user_)
    except IntegrityError as i:
        print(i)
        return render_template('index.html')
    except Exception as e:
        print("in profile update...", e)
        return render_template('error.html')

def get_dashboard(user_):
    user_type = user_.user_type
    if user_type == 1:
        return redirect('/admin/')
    elif user_type == 2:
        return redirect('/user/')    
    
def authenticate(form):
    try:
        user = form['user']
        pword = form['pword']
        print(user, pword)
        user_ = Users.query.filter_by(user=user, pword=pword).first()
        if user_:
            session['name'] = user_
            # user_type = user_.user_type
            # print('user_type:',user_type)
            return get_dashboard(user_)
        return render_template('login.html', msg='Wrong credentials')
    
    except Exception as e:
        print("in authenticate...\n", e)
        return 0
        
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