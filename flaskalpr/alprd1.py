from __future__ import print_function
from datetime import date, datetime, timedelta
import re
from flask import (
    Response, Blueprint, request, jsonify, render_template, send_file 
)
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import redis
import json
import pandas as pd
from json import loads, dumps
from flask_sse import sse 
from flask import current_app, g
import os, subprocess
import glob, os

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg', 'gif'}
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)
bp = Blueprint('alprd1', __name__, url_prefix='/alprd1')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def alpr_img_keep():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    for key, value in stored_alpr.items():
        a = f"{value}."    
        b = glob.glob( "flaskalpr/static/alprd1_images/*.*")
        c = f"{b}."    
        print(type(c))
        print(a)
    return(stored_alpr) 






@bp.route('/alprd1', methods=["POST"])
def alpr_from_video():
    alpr_img_keep()
    request_data = request.get_json()
    alpr_uuid = request_data["uuid"]
    #alpr_img_uuid = ("http://192.168.1.122:5000/alprd1_images/{}.jpg".format(alpr_uuid))
    alpr_img_uuid = ("http://34.105.172.98:5000/alprd1_images/{}.jpg".format(alpr_uuid))
    alpr_results = request_data["results"]
    alpr_plate = alpr_results[0]["plate"]
    match = re.search(r'[A-Z][A-Z][0-9][0-9][A-Z][A-Z][A-Z]', alpr_plate)
    if match:
        #print(match.group())  
        r.hset(
            f"alpr_plate:{alpr_plate}",
            mapping={
                "alpr_plate_id": alpr_plate,
                "alpr_plate": alpr_plate,
                "alpr_plate_img": alpr_img_uuid,
            },
        ) 
        r.hset("alpr_plate_to_id", alpr_plate, alpr_plate)
        r.hset("alpr_plate_to_img", alpr_plate, alpr_img_uuid)
    try:
        data = alpr_plate
        r.publish("alprd1", json.dumps(data))
        r.publish("alprd1images", ((alpr_img_uuid)))
        return jsonify(status="success", message="published", data=data) # type: ignore
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

@bp.route('/db')
def alpr_db():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    d1 = {'Name': ['Pankaj', 'Meghna'], 'ID': [1, 2] }
    #df = pd.DataFrame(d1)
    df = pd.DataFrame(list(stored_alpr.items()), columns=['Key', 'Values']) # type: ignore
    csv_data = df.to_csv(header=['plate', 'img'])
    print(csv_data)
    return(stored_alpr) 

@bp.route('/download')
def download():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    df = pd.DataFrame(list(stored_alpr.items()), columns=['Key', 'Values']) # type: ignore
    csv_data = df.to_csv('flaskalpr/data/upload-video.csv',header=['plate', 'img'])
    path = 'data/upload-video.csv'
    return send_file(path, as_attachment=True) # type: ignore


