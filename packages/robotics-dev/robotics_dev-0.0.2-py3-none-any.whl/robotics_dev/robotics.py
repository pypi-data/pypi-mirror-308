import socketio

sio = socketio.Client()

def connect(server):
    if not server:
        server = "https://robotics.dev"
    sio.connect(server)
    return sio.sid
