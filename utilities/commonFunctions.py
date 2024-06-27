from flask import session

def check_session_exists():
    return session and 'name' in session and session['name']