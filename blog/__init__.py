import os
from flask import Flask, render_template

def create_app(test_config = None):

    #create an instance of the app
    app = Flask(__name__, instance_relative_config=True)

    #configure the app 
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'blog.sqlite') #join 
    )

    #if we aren't testing, then load app instance config file
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        #load the test config if passed in
        app.config.from_mapping(test_config)
    
    #ensure that the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    return app
