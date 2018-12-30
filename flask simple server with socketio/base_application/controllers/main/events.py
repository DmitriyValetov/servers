from flask_socketio import emit
import logging
import json
logging.basicConfig(level=logging.DEBUG)


def bind_listeners_in_main(sio):

    # / in /main is important. definite name of namespace
    @sio.on('debug_msg', namespace='/main') 
    def debug_main_logger(msg):
        logging.debug('debug msg: ' + str(msg))


    def process_func(data: dict):
        return data



    @sio.on('data_from_client', namespace='/main') 
    def server_data_handler(data):
        """ data is json string"""
    
        data = json.loads(data)
        # data.keys() are 'selected_text', 'all_text', 'source_path'
        logging.debug('\n\n\nData from the client: ' + str(data) + '\n\n\n')
        
        result = process_func(data)

        # data_out = [ {'a': 'peace', 'b': 'two'}, {'c': 'three', 'd': 'four'}]
        data_out = json.dumps(result, indent=2) # indent for <br>
        # data_out is a json string
        logging.debug('\n\n\n Data to client: {} \n\n\n'.format(data_out))
        sio.emit('response', data_out, namespace='/main')