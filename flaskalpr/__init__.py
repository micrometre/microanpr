import os

from flask import Flask

from flask_cors import CORS


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, static_folder='static', static_url_path='', instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        HOST="dev",
        REDIS_URL = "redis://localhost:6379",
        DATABASE=os.path.join(app.instance_path, "flaskralpr.sqlite"),
    )
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources=r'/*', headers='Content-Type')

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import  home, video, alprd1, alprd1_images, upload_images, upload_video, db, auth, stream
    db.init_app(app)
    app.register_blueprint(home.bp)
    app.register_blueprint(video.bp)
    app.register_blueprint(alprd1.bp)
    app.register_blueprint(alprd1_images.bp)
    app.register_blueprint(upload_images.bp)
    app.register_blueprint(upload_video.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(stream.bp)


    app.add_url_rule("/", endpoint="index")

 
    return app
