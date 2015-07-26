from flask import jsonify

from app import application


@application.route('/')
@application.route('/index')
def index():
    return "Hallo, World!"
