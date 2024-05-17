from flask import (
    Blueprint, render_template, send_file
)

from flask import Flask, render_template, json, jsonify, request
from flask_sse import sse
from flask import current_app, g

bp = Blueprint('stream', __name__, url_prefix='/stream')



@bp.route('/')
def index():
    return render_template("stream.html")

@bp.route('/hello')
def publish_hello():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"
