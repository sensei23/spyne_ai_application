from flask import Blueprint, jsonify, request
from utilities.constants import *
from .controller import TagController

tagBlueprint = Blueprint('Tag', __name__, url_prefix = '/tag')


@tagBlueprint.route('/add', methods = POST)
def addTag():
    body = request.json
    if TagController.add(body):
        return jsonify({'message': "tag added"}), HTTP_OK
    return jsonify({'error' : "eror occured"}), HTTP_BAD_REQUEST

