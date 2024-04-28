from flask import (
    Blueprint, request, render_template, 
)
import inotify.adapters
import json
import redis

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)
def get_images_alprd1():
    i = inotify.adapters.Inotify()
    i.add_watch('./flaskalpr/static/alprd_images')
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        #alpr_images_sse = ("http://192.168.1.122:5000/alprd1_images/{}".format(filename))
        alpr_images_sse = ("http://192.168.1.197:5000/alprd_images/{}".format(filename))
        a = alpr_images_sse.strip("\'")
        r.publish("alprd1images", ((a)))
        return ("alprd-upload", ((a)))

