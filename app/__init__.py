from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)
sio = SocketIO(app, async_mode='eventlet')
app.config["SECRET_KEY"] = "2501"
core = dict()


from app import routes
from app import events