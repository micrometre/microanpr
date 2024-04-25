from flask import (
    Response, Blueprint, request, jsonify, render_template, send_file 
)
import redis
import json
from flaskalpr.filewatch import  get_images_alprd1
import pandas as pd
from json import loads, dumps
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)

bp = Blueprint('alprd1', __name__, url_prefix='/alprd1')



@bp.route('/alprd1', methods=["POST"])
def alpr_from_video():
    get_images_alprd1()
    request_data = request.get_json()
    alpr_results = request_data["results"]
    alpr_plate = alpr_results[0]["plate"]
    alpr_img = get_images_alprd1()
    alpr_img_plate = alpr_img[1]
    try:
        data = alpr_plate
        r.hset(
            f"alpr_plate:{alpr_plate}",
            mapping={
                "alpr_plate_id": alpr_plate,
                "alpr_plate": alpr_plate,
                "alpr_plate_img": alpr_img_plate,
            },
        )
        r.hset("alpr_plate_to_id", alpr_plate, alpr_plate)
        r.hset("alpr_plate_to_img", alpr_plate, alpr_img_plate)
        r.publish("alprd1", json.dumps(data))
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

@bp.route('/mobile', methods=["GET"])
def camera_sse_moblie():
    return render_template('mobile.html')



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
    

@bp.route('/db-table')
def alpr_db_table():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    df = pd.DataFrame(list(stored_alpr.items()), columns=['Key', 'Values'])
    a = format(stored_alpr)
    print(a) 
    return render_template('data.html',  tables=[df.to_html(classes='data')],  titles=df.columns.values)
         

@bp.route('/db')
def alpr_db():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    df = pd.DataFrame(list(stored_alpr.items()))
    b = df.to_json(orient='values')
    c = loads(b)
    d = dumps(c)
    print(type(d)) 
    return(c) 
         
@bp.route('/check_key', methods=['GET'])
def check_key():
    key = request.args.get('key')  # Retrieve key from request arguments
    field = request.args.get('field')  # Retrieve field from request arguments
    get_plate = r.hget(key, field)  # Check if the field exists in the hash
    plate = format(get_plate)
    get_image = r.hget("alpr_plate_to_img", get_plate)  # Check if the field exists in the hash
    img = format(get_image)
    data = [plate, img]
    return jsonify(status="success", data=data)