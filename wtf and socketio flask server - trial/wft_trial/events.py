from flask_socketio import emit

from .configs import Config
from .forms import MyForm

def bind_all_events(sio):

    @sio.on('debug_msg', namespace='/')
    def test(msg):
        print('\n\nreceived: {}\n\n'.format(msg))
        emit('server_response', {'data': "response msg"})


    @sio.on('connecting_msg', namespace='/')
    def test(msg):
        print('\n\nreceived: {}\n\n'.format(msg))
        emit('server_response', {'data': "connected!"})

    @sio.on('greeting', namespace='/')
    def test(msg):
        # this is not a submitting
        # form = MyForm()
        # received_name = form.name.data

        received_name = msg['data']

        print('\n\nreceived: {}\n\n'.format(msg))

        if received_name in Config.names:
            emit('greeting', {'data': "Hello, {}, I know you!".format(received_name)})
        else:
            Config.names.append(received_name)
            emit('greeting', {'data': "Hello, newbye!"})