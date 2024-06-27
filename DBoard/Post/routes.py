
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, current_app
from .controller import PostController
from utilities.constants import *

postBlueprint = Blueprint("Post", __name__, url_prefix="/post")

class PostRoutes:

    @postBlueprint.route('/add', methods=POST)
    def addPost():
        try:
            body = request.form
            if PostController.add(body):
                return jsonify({"message" : "Post added"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error" : "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR


    @postBlueprint.route('/update/', methods=PUT)
    def updatePost():
        try:
            body = request.form
            if 'id' in body and PostController.update(body):
                return jsonify({"message" : "Post updated"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error" : "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR


    @postBlueprint.route('/delete/<id>', methods=POST)
    def deletePost(id):
        try:
            id = int(id)
            if PostController.delete(id):
                return jsonify({"message" : "Post deleted"}), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error" : "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR

    @postBlueprint.route('/search/text', methods=POST)
    def searchText():
        try:
            body = request.json
            posts = PostController.searchByText(body['text'])
            if posts:
                return jsonify(posts), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error" : "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR

    @postBlueprint.route('/search/tags', methods=POST)
    def searchTags():
        try:
            body = request.json
            posts = PostController.searchByTags(body['tags'])
            if posts:
                return jsonify(posts), HTTP_OK
        except Exception as e:
            current_app.logger.error(e)
        return jsonify({"error" : "unexpected error"}), HTTP_INTERNAL_SERVER_ERROR

