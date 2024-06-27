
from flask import redirect, render_template, request, session, Blueprint
from utilities.constants import *


blueprint = Blueprint("User", __name__, url_prefix="/user")

@blueprint.route('/', methods=GET)
def get_user_dashboard():
    
    return "hello"