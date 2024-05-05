from __future__ import print_function
from datetime import date, datetime, timedelta

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
import mysql.connector




UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'mp4', 'png', 'jpg', 'jpeg', 'gif'}
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)
alprdb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="395F844E696D423F6B7ACBBA301539668E6",
  port= 3306,
  database="alprdata"
)

bp = Blueprint('alprd1', __name__, url_prefix='/alprd1')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/alprd1', methods=["POST"])
def alpr_from_video():
    request_data = request.get_json()
    alpr_uuid = request_data["uuid"]
    #alpr_img_uuid = ("http://192.168.1.197:5000/alprd1_images/{}.jpg".format(alpr_uuid))
    alpr_img_uuid = ("http://192.168.1.122:5000/alprd1_images/{}.jpg".format(alpr_uuid))
    alpr_results = request_data["results"]
    alpr_plate = alpr_results[0]["plate"]
    alpr_obj =  {'id': alpr_uuid,  'plate' : alpr_plate, 'img' :  alpr_img_uuid }
    try:
        data = alpr_plate
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

@bp.route("/db", methods=["GET"])
def alpr_result():
        upcursor = alprdb.cursor()
        upcursor.execute("SELECT * FROM plates WHERE LENGTH(plate) = 7;")
        upresult = upcursor.fetchall()
        j = json.dumps(upresult)
        print()
        return(j)




