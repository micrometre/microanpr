import redis
import re

r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)



def alpr_db():
    stored_alpr  = r.hgetall(
        "alpr_plate_to_img_url"
        )
    test_dict = {'LD09AOA': 1, 'CE08PNP': 2, 'GT06ALL': 4, 'geeks': 5, 'areks': 8, 'freaks': 10}
    test_suf = '^[A-Z][A-Z][0-9][0-9][A-Z][A-Z][A-Z]$'

    res = {key: val for key, val in stored_alpr.items() if re.search(f"{test_suf}$", key)}
    print("Filtered dictionary keys are : " + str(res))
 

alpr_db()