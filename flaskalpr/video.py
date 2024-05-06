from flask import (
    Blueprint, render_template, send_file
)

bp = Blueprint('video', __name__, url_prefix='/video')

@bp.route("/")
def video():
    return send_file("./static/uploaded-video/alprVideo-3.mp4")