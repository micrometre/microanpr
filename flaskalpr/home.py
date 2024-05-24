from flask import (
    Blueprint, render_template
)

import redis
from flaskalpr.auth import login_required
import pandas as pd
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
)

bp = Blueprint('home', __name__, url_prefix='/')



@bp.route('/')
@login_required
def alpr_home():
   return render_template('index.html')      


@bp.route('/login', methods=['GET', 'POST'])
def login_page():
    return {
        "token": 'test'
    }


