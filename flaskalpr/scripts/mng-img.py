import redis
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)

img_keep=[]


def alpr_db():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img"
        )
    for values in stored_alpr:
        img_keep.append(stored_alpr.values())
        print(img_keep)
        print(len(img_keep))
    return(stored_alpr) 

alpr_db()