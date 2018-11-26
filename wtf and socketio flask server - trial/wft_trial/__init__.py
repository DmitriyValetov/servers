from flask import Flask
from flask_socketio import SocketIO

# config class
from .configs import Config


def create_app():    
    # bind ordinal routes
    app = Flask(__name__)


    # load configs from Config class
    app.config.from_object(Config)
    # or so:
    # app.config['SECRET_KEY'] = Config.SECRET_KEY 
    # app.config['WTF_CSRF_SECRET_KEY'] = Config.WTF_CSRF_SECRET_KEY

    from .routes import  bind_all_routes
    bind_all_routes(app)


    # bind events for websocket realtime processes
    sio = SocketIO(app, async_mode=Config.async_mode)
    from .events import bind_all_events
    bind_all_events(sio)

    return app, sio

def runner():
    app, sio =  create_app() 
    sio.run(app, debug = Config.debug)