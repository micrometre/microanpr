from __future__ import print_function
import re
from flask import (
    Response, Blueprint, request, jsonify, render_template, send_file 
)
import redis
import json
import pandas as pd

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


@bp.route('/alprd1', methods=["POST"])
def alpr_from_video():
    request_data = request.get_json()
    host_ip = request.environ['REMOTE_ADDR']
    host_port = request.environ['SERVER_PORT']
    host_protocol = request.environ['wsgi.url_scheme']
    img_path = '/alprd1_images/'
    img_format = '.jpg'
    alpr_uuid = request_data["uuid"]
    alpr_img_url = host_protocol + "://" + host_ip + ":" + host_port + img_path + alpr_uuid + img_format
    print(alpr_img_url)
    alpr_img = ("{}.jpg".format(alpr_uuid))
    alpr_results = request_data["results"]
    alpr_plate = alpr_results[0]["plate"]
    #match = re.search(r'[A-Z][A-Z][0-9][0-9][A-Z][A-Z][A-Z]', alpr_plate)
    #if match:
       #print(match.group())  
    r.hset(
        f"alpr_plate:{alpr_plate}",
        mapping={
            "alpr_plate_id": alpr_plate,
            "alpr_plate": alpr_plate,
            "alpr_plate_img": alpr_img,
            "alpr_plate_url": alpr_img_url,
        },
    ) 
    r.hset("alpr_plate_to_id", alpr_plate, alpr_plate)
    r.hset("alpr_plate_to_img_url", alpr_plate, alpr_img_url)
    r.hset("alpr_plate_to_img", alpr_plate, alpr_img)
    try:
        data = alpr_plate
        r.publish("alprd1", json.dumps(data))
        r.publish("alprd1images", ((alpr_img_url)))
        return jsonify(status="success", message="published", data=data) # type: ignore
    except:
        return jsonify(status="fail", message="not published")    




@bp.route('/alprd1', methods=["GET"])
def alpr_sse():
    def sse_events():
        pubsub = r.pubsub()
        pubsub.subscribe("alprd1")
        for message in pubsub.listen():
                data = message["data"]
                yield "data: {}\n\n".format(str(data))
    return Response(sse_events(), mimetype="text/event-stream")

@bp.route('/download')
def download_video_db():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img_url"
        )
    test_diplomat = '^[0-9][0-9][0-9][A-Z][0-9][0-9][0-9]'
    diplomat_plates = {key: val for key, val in stored_alpr.items() if re.search(f"{test_diplomat}$", key)}
    df_diplomat = pd.DataFrame(list(diplomat_plates.items()), columns=['Key', 'Values']).sort_values(by=['Key']) 
    test_gb = '^[A-Z][A-Z][0-9][0-9][A-Z][A-Z][A-Z]$'
    gb_plates = {key: val for key, val in stored_alpr.items() if re.search(f"{test_gb}$", key)}
    df_gb = pd.DataFrame(list(gb_plates.items()), columns=['Key', 'Values']).sort_values(by=['Key']) 
    a = pd.concat([df_gb, df_diplomat])
    csv_data = a.to_csv('flaskalpr/data/upload-video.csv',header=['plate', 'img'],index=False )
    b = a.to_html()
    path = 'data/upload-video.csv'
    return send_file(path, as_attachment=True) # type: ignore


@bp.route('/db')
def alpr_video_db():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img_url"
        )
    test_diplomat = '^[0-9][0-9][0-9][A-Z][0-9][0-9][0-9]'
    diplomat_plates = {key: val for key, val in stored_alpr.items() if re.search(f"{test_diplomat}$", key)}
    df_diplomat = pd.DataFrame(list(diplomat_plates.items()), columns=['Key', 'Values']).sort_values(by=['Key']) 
    test_gb = '^[A-Z][A-Z][0-9][0-9][A-Z][A-Z][A-Z]$'
    gb_plates = {key: val for key, val in stored_alpr.items() if re.search(f"{test_gb}$", key)}
    df_gb = pd.DataFrame(list(gb_plates.items()), columns=['Key', 'Values']).sort_values(by=['Key']) 
    agrt_plates = pd.concat([df_gb, df_diplomat])
    agrt_plates_dict = agrt_plates.to_dict(orient='records')
    csv_data = agrt_plates.to_csv('flaskalpr/data/upload-video.csv',header=['plate', 'img'],index=False )
    path = 'data/upload-video.csv'
    return(agrt_plates_dict) 
