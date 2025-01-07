import json
from flask import (
    Response, Blueprint, request, redirect, flash,  url_for, jsonify, render_template, 
)
import os, subprocess
import logging
from werkzeug.utils import secure_filename
import redis


r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)

bp = Blueprint('upload_video', __name__, url_prefix='/upload_video')
ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg', 'gif'}
logging.getLogger('flask_cors').level = logging.DEBUG



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@bp.route('/', methods=['GET', 'POST'])
def upload_video_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) # type: ignore
            file.save(os.path.join( 'flaskalpr/static/uploaded-video',filename))
            command = 'ffmpeg -i flaskalpr/static/uploaded-video/alprVideo1.mp4 -listen 1 -f mp4 -movflags frag_keyframe+empty_moov  http://127.0.0.1:5001'
            try:
                output = subprocess.check_output(command, shell=True, text=True) # type: ignore
                print((output))
            except subprocess.CalledProcessError as e:
                output = f"Error: {e}"
            return redirect(url_for('home.alpr_home'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



