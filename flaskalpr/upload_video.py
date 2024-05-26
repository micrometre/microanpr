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
            alpr_file = (os.path.join('flaskalpr/static/uploaded-video', filename))
            start_alprd = subprocess.check_output(['alprd'])
            #clean_seasion_files = subprocess.check_output(["make", "clean"], text=True)
            alpr_arg1 = "-i"
            alpr_arg2 = "-listen"
            alpr_arg3 = "1"
            alpr_arg4 = "-f"
            alpr_arg5 = "mp4"
            alpr_arg6 = "-movflags"
            alpr_arg7 = "frag_keyframe+empty_moov"
            alpr_arg8 = "http://127.0.0.1:5001"
            output = subprocess.check_output(['ffmpeg',str(alpr_arg1), str(alpr_file), str(alpr_arg2), str(alpr_arg3), str(alpr_arg4), str(alpr_arg5), str(alpr_arg6), str(alpr_arg7), str(alpr_arg8)]).decode('utf-8')
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



