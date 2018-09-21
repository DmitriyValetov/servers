from app import app, sio
from flask_socketio import emit, disconnect
from .teams.teams import teams, search_team, save_team


@sio.on('team_position', namespace='/flask')
def team_position(msg):
    print('team position: ', msg)
    team = search_team(msg['team_key'])
    if team:
        team.geo_position.append([msg['lat'], msg['longt']])
        save_team(team)

    # sio.emit('ping', {'data': 'ping'})
    disconnect()
    
    
@sio.on('debug_msg', namespace='/flask')
def debug_msg(msg):
    print('debug_msg: ', msg)