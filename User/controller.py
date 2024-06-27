from flask import jsonify, session, current_app
from .model import Users
from sqlalchemy.exc import IntegrityError
from config import db

class AuthController:

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
        

    def get_session_user(user):
        try:
            return db.session.query(Users).get(user.user_id)
        except Exception as e:
            return None
class UserController:

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
    
    def update(body, uid):
        try:
            user_ = db.session.query(Users).get(uid)
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
        return None
        
    def update_user(body):
        return UserController.update(body, session['name'].user_id)

    def delete_user(id):
        try:
            user = Users.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return True
        except Exception as e:
            current_app.logger.error(i)
        return None
    
    def get_all_users():
        try:
            user_list = Users.query.all()
            # current_app.logger.info(user_list)
            return [user.get() for user in user_list]
        except Exception as e:
            current_app.logger.error(e)
        return None
        
    def get_users_by_name(name):
        try:
            #list return
            user_list = Users.query.filter(Users.name.like(f"%{name}%")).all()
            # current_app.logger.info(user_list)
            return [user.get() for user in user_list]
        except Exception as e:
            current_app.logger.error(e)
        return None