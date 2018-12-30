from flask_socketio import emit
import logging
logging.basicConfig(level=logging.DEBUG)


def bind_listeners_in_main(sio):

    # / in /main is important. definite name of namespace
    @sio.on('debug_msg', namespace='/main') 
    def debug_main_logger(msg):
        logging.debug('Main event debug: ' + str(msg))