from flask import Flask
from .controllers.master import master_blueprint
from .controllers.slave_1 import slave_1_blueprint


def create_app():
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        None
    """

    app = Flask(__name__)
    app.register_blueprint(master_blueprint)
    app.register_blueprint(slave_1_blueprint)

    return app


if __name__ == '__main__':
    app = app = create_app()
    app.run()
