from flask import (
    Response, Blueprint, request,send_file, send_from_directory, redirect, flash,  url_for, jsonify, render_template, 
)
import os
import subprocess
import logging
from werkzeug.utils import secure_filename
import pandas as pd
import redis
import json

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)

bp = Blueprint('upload_images', __name__, url_prefix='/upload_images')
ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg', 'gif'}
logging.getLogger('flask_cors').level = logging.DEBUG

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@bp.route('/', methods=['GET', 'POST'])
def upload_file():
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
            file.save(os.path.join( 'flaskalpr/static/uploaded-images',filename))
            alpr_file = (os.path.join('flaskalpr/static/uploaded-images', filename))
            alpr_arg1 = "-c"
            alpr_arg2 = "gb"
            alpr_arg3 = "-j"
            alpr_arg4 = "-n 1"
            output = subprocess.check_output(['alpr',str(alpr_file), str(alpr_arg1), str(alpr_arg2), str(alpr_arg3), str(alpr_arg4)]).decode('utf-8')
            jl = json.loads(output)
            result = jl["results"]
            result_plate = result[0]["plate"]
            upload_id = r.incr("alpr_ids")
            r.hset("upload_plate_to_img", upload_id, result_plate) # type: ignore
            r.hset(f"upload_plate:{upload_id}",mapping={"alpr_plate": result_plate,},)
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
@bp.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

    
@bp.route("/uploaddb", methods=["GET"])
def alpr_result():
        res = r.hgetall("upload_plate_to_img")
        resj = format(res)
        return(resj)


@bp.route('/download')
def download_uploads_img():
    stored_alpr  = r.hgetall(
        "upload_plate_to_img"
        )
    df = pd.DataFrame(list(stored_alpr.items()), columns=['Key', 'Values'])
    df.to_csv('flaskalpr/data/upload-img.csv', sep='\t', encoding='utf-8' )
    print(df.to_string()) 
    path = 'data/upload-img.csv'
    return send_file(path, as_attachment=True)        