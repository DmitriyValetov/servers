#!/usr/bin/env python
from threading import Lock
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

import calculation_process
from  multiprocessing import Process, Pipe, Queue

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

# tqdm - progressbars

async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

process_thread = None
process_thread_lock = Lock()
calc_process = None
data_queue = Queue()

def background_process(data):
    count = 0
    global calc_process, socketio, process_thread
    parent_conn, child_conn = Pipe()
    calc_process = Process(target=calculation_process.main, args=(data, data_queue))
    calc_process.start()
    socketio.emit('my_response',
                    {'data': "Process launched", 'count': count}, namespace='/test')

    while calc_process.is_alive():
        # here should be some checks the flag of user break button push
        print('begin of messaging')
        count += 1
        if not data_queue.empty():
            data = data_queue.get()
        else:
            socketio.sleep(1)
            continue
        # text = parent_conn.recv()
        print(data)
        socketio.emit('my_response',
                      {'data': "process online: {}".format(data), 'count': count, "process":"On"},
                      namespace='/test')
        
        
        print("end of messaging")

    parent_conn.close()
    print("process ended")
    calc_process = None
    process_thread = None



def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my_response', {'data': 'Server generated event', 'count': count})


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my_event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('start_process', namespace='/test')
def start_process(message):
    session['receive_count'] = session.get('receive_count', 0) + 1

    global process_thread
    if process_thread == None:
        with process_thread_lock:
            print("starting the process")
            process_thread = socketio.start_background_task( background_process, message["data"])
    else:
        print("process already works")
        emit('my_response', {'data': "Process has already been launched", 'count': session['receive_count']})


@socketio.on('stop_process', namespace='/test')
def stop_process(message):
    """
    refactor it to stop right after the nearest iteration goes -> make a flag to false and 
    send it to sycle in background_process 
    """
    session['receive_count'] = session.get('receive_count', 0) + 1

    global calc_process, process_thread
    if calc_process and calc_process.is_alive():
        print("terminating")
        calc_process.terminate()
        # process_thread = None
        emit('my_response', {'data': "Process was terminated", 'count': session['receive_count']})
    else:
        print("nothing to terminate")
        emit('my_response', {'data': "There is no active process", 'count': session['receive_count']})


@socketio.on('my_broadcast_event', namespace='/test')
def test_broadcast_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         broadcast=True)


@socketio.on('join', namespace='/test')
def join(message):
    join_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('leave', namespace='/test')
def leave(message):
    leave_room(message['room'])
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'In rooms: ' + ', '.join(rooms()),
          'count': session['receive_count']})


@socketio.on('close_room', namespace='/test')
def close(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.',
                         'count': session['receive_count']},
         room=message['room'])
    close_room(message['room'])


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': message['data'], 'count': session['receive_count']},
         room=message['room'])


@socketio.on('disconnect_request', namespace='/test')
def disconnect_request():
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my_response',
         {'data': 'Disconnected!', 'count': session['receive_count']})
    disconnect()


@socketio.on('my_ping', namespace='/test')
def ping_pong():
    emit('my_pong')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)
    emit('my_response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True)
