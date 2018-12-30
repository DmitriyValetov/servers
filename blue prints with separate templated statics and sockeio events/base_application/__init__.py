from flask import Flask
from flask_socketio import SocketIO

from  .configs import Config


def create_app():
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        None
    """

    from .controllers.main import main_blueprint
    from .controllers.module_1 import module_1_blueprint

    app = Flask(__name__, static_folder=None)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(module_1_blueprint)

    from .controllers.main.events import bind_listeners_in_main
    from .controllers.module_1.events import bind_listeners_in_module_1
    sio = SocketIO(app, async_mode=Config.async_mode)
    bind_listeners_in_main(sio)
    bind_listeners_in_module_1(sio)

    return sio, app


def run_server(debug_state=Config.debug):
    sio, app = create_app()
    sio.run(app, debug=debug_state)    


if __name__ == '__main__':
    run_server()