from flask import (
    Response, Blueprint, request, jsonify, render_template, 
)
import redis
import json
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)

bp = Blueprint('alprd1_images', __name__, url_prefix='/alprd1_images')


@bp.route("/", methods=["GET"])
def alprd_images():
    def alpr_sse_events():
        pubsub = r.pubsub()
        pubsub.subscribe("alprd1images")
        for message in pubsub.listen():
                data = message["data"]
                yield "data: {}\n\n".format(str(data))
    return Response(alpr_sse_events(), mimetype="text/event-stream")