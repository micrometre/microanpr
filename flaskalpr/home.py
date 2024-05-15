from flask import (
    Blueprint, g,request, json, redirect, url_for, render_template, send_file, flash
)
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

import os
import redis
from flaskalpr.auth import login_required
from flaskalpr.db import get_db  
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
        "token": 'test123'
    }


@bp.route('/create', methods=('GET', 'POST'))
#@login_required
def create_ops():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for('home.create'))
        flash(error)   
     return render_template('ops/create.html')
