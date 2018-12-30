from flask_socketio import emit
import logging
logging.basicConfig(level=logging.DEBUG)


def bind_listeners_in_module_1(sio):

    # / in /main is important. definite name of namespace
    @sio.on('debug_msg', namespace='/module_1') 
    def debug_main_logger(msg):
        logging.debug('Module 1 debug: ' + str(msg))