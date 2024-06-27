
from sqlite3 import IntegrityError
from flask import jsonify, redirect, render_template, request, session, Blueprint, current_app, url_for
from utilities.commonFunctions import check_session_exists
from utilities.constants import *
from .controller import UserController, AuthController

authBlueprint = Blueprint("Auth", __name__, url_prefix="/")
userBlueprint = Blueprint("User", __name__, url_prefix="/user")

class UserAuthRoutes:

    @authBlueprint.route('/', methods=GET)
    def get_user_dashboard():
        if check_session_exists():
            user_ = session['name']
            return redirect('/user-dashboard')
        return render_template('login.html')

    
        
    @authBlueprint.route('/login', methods = POST)
    def login():
        form = request.form
        user = AuthController.authenticate(form)
        if user:
            return redirect('/')
        else:
            return redirect('/')
        

    

    @authBlueprint.route('/logout', methods=GET)
    def logout():
        session['name'] = None
        return render_template('login.html', msg='Successfully Logged out...')

    @authBlueprint.route('/user-profile', methods=GET)
    def provide_profile():
        if session and 'name' in session and session['name']:
            user_ = AuthController.get_session_user(session['name'])
            if user_:
                return render_template('user-profile.html', user_=user_) 
            
        return render_template('login.html')

    @authBlueprint.route('/user-dashboard', methods=GET)
    def provide_dashboard():
        if session and 'name' in session and session['name']:
            user_ = AuthController.get_session_user(session['name'])
            if user_:
                return render_template('user-dashboard.html', user_=user_) 
            
        return render_template('login.html')

    
    


class UsersCRUDRoutes:

    @userBlueprint.route('/add', methods=POST)
    def addUser():
        try:
            body = request.json
            if UserController.add_user(body):
                return jsonify({"message" : "user added"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error": "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR
        
    @userBlueprint.route('/update', methods=PUT)
    def updateUser():
        try:
            body = request.json
            if 'user_id' in body and UserController.update(body, body['user_id']):
                return jsonify({"message" : "user updated"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error": "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR

    @userBlueprint.route('/delete/<id>')
    def deleteUser(id):
        try:
            if UserController.delete_user(int(id)):
                return jsonify({'message': "user deleted"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error": "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR

    

    @userBlueprint.route('/signup', methods = POST)
    def signup():
        try:
            form = request.form
            if UserController.add_user(form):
                return render_template('login.html', msg='You have been successfully signed up')
        except IntegrityError as i:
            current_app.logger.error(e)
        except Exception as e:
            current_app.logger.error(e)
        return redirect('/')


    @userBlueprint.route('/update', methods=POST)
    def update_user_profile():
        try:
            if check_session_exists():
                body = request.form
                current_app.logger.info(body)
                user_ = UserController.update_user(body)
                if user_:
                    return render_template('user-profile.html', user_=user_)
        except Exception as e:
            current_app.logger.error(e)

        return render_template('login.html')
    
    @userBlueprint.route('/get-users', methods=GET)
    def get_all_users():
        try:
            users = UserController.get_all_users()
            if len(users) > 0:
                return jsonify(users), HTTP_OK
            else:
                return jsonify({"message" : "no user found"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error": "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR

    
    @userBlueprint.route('/get-users', methods=POST)
    def get_users():
        try:
            form = request.json
            users = UserController.get_users_by_name(form['name'])
            if len(users) > 0:
                return jsonify(users), HTTP_OK
            else:
                return jsonify({"message" : "no user found"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error": "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR
