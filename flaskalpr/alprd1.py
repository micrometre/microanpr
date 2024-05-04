from flask import (
    Response, Blueprint, request, jsonify, render_template, send_file 
)
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

import redis
import json
from flaskalpr.filewatch import  get_images_alprd1
import pandas as pd
from json import loads, dumps
UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)
ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg', 'gif'}

bp = Blueprint('alprd1', __name__, url_prefix='/alprd1')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS






@bp.route('/alprd1', methods=["POST"])
def alpr_from_video():
    get_images_alprd1()
    request_data = request.get_json()
    alpr_uuid = request_data["uuid"]
    alpr_img_uuid = ("http://192.168.1.197:5000/alprd1_images/{}.jpg".format(alpr_uuid))
    alpr_results = request_data["results"]
    alpr_plate = alpr_results[0]["plate"]
    alpr_img = get_images_alprd1()
    alpr_img_plate = alpr_img[1]
    a = json.dumps(alpr_plate)
    try:
        data = alpr_plate
        r.hset(
            f"alpr_plate:{alpr_plate}",
            mapping={
                "alpr_plate_id": alpr_plate,
                "alpr_plate": alpr_plate,
                "alpr_plate_img": alpr_img_plate,
                "alpr_plate_uuid": alpr_img_uuid,
            },
        )
        r.hset("alpr_plate_to_id", alpr_plate, alpr_plate)
        r.hset("alpr_plate_to_img", alpr_plate, alpr_img_uuid)
        r.publish("alprd1", json.dumps(data))
        r.publish("alprd1images", ((alpr_img_uuid)))
        return jsonify(status="success", message="published", data=data)
    except:
        return jsonify(status="fail", message="not published")    
    
@bp.route('/alprd1', methods=["GET"])
def sse():
    def sse_events():
        pubsub = r.pubsub()
        pubsub.subscribe("alprd1")
        for message in pubsub.listen():
                data = message["data"]
                yield "data: {}\n\n".format(str(data))
    return Response(sse_events(), mimetype="text/event-stream")




@bp.route('/download')
def download():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    df = pd.DataFrame(list(stored_alpr.items()), columns=['Key', 'Values'])
    df.to_csv('flaskalpr/data/upload-video.csv', sep='\t', encoding='utf-8' )
    print(df.to_string()) 
    path = 'data/upload-video.csv'
    return send_file(path, as_attachment=True)
    



@bp.route('/check_key', methods=['GET'])
def check_key():
    key = request.args.get('key')  # Retrieve key from request arguments
    field = request.args.get('field')  # Retrieve field from request rguments
    get_plate = r.hget(key, field)  # Check if the field exists in the hash
    plate = format(get_plate)
    get_image = r.hget("alpr_plate_to_img", get_plate)  # Check if the field exists in the hash
    img = format(get_image)
    data = [plate, img]
    return jsonify(status="success", data=data)




@bp.route('/db2')
def alpr_db2():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    print(type(stored_alpr))
    return(stored_alpr) 