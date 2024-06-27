
from sqlite3 import IntegrityError
from flask import redirect, render_template, request, session, Blueprint, current_app, url_for
from utilities.commonFunctions import check_session_exists
from utilities.constants import *
from .controller import authenticate, add_user, update_user, forgot_password, reset_password, get_session_user
import os


blueprint = Blueprint("User", __name__, url_prefix="/")

@blueprint.route('/', methods=GET)
def get_user_dashboard():
    if check_session_exists():
        user_ = session['name']
        return redirect('/user-dashboard')
    return render_template('login.html')

@blueprint.route('/signup', methods = POST)
def signup():
    form = request.form
    try:
        if add_user(form):
            return render_template('login.html', msg='You have been successfully signed up')
    except IntegrityError as i:
        #something
        return redirect('/')
    except Exception as e:
        print("in signup...", e)
    return redirect('/')

    
@blueprint.route('/login', methods = POST)
def login():
    form = request.form
    user = authenticate(form)
    if user:
        return redirect('/')
    else:
        return redirect('/')
    

@blueprint.route('/update', methods=POST)
def update_user_profile():
    if check_session_exists():
        body = request.form
        # print("LOG:", body['email'])
        current_app.logger.info(body)
        user_ = update_user(body)
        if user_:
            return render_template('user-profile.html', user=user_)
        # else:
        #     return render_template('index.html')
        
    return render_template('login.html')

@blueprint.route('/logout', methods=GET)
def logout():
    session['name'] = None
    return render_template('login.html', msg='Successfully Logged out...')

@blueprint.route('/user-profile', methods=GET)
def provide_profile():
    if session and 'name' in session and session['name']:
        user_ = get_session_user(session['name'])
        if user_:
            return render_template('user-profile.html', user=user_) 
        
    return render_template('login.html')

@blueprint.route('/user-dashboard', methods=GET)
def provide_dashboard():
    if session and 'name' in session and session['name']:
        user_ = get_session_user(session['name'])
        if user_:
            return render_template('user-dashboard.html', user_=user_) 
        
    return render_template('login.html')