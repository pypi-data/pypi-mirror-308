import socketio

sio = socketio.Client()

def connect(serverParam="https://robotics.dev"):
    if serverParam != "https://robotics.dev":
        server = serverParam
    else:
        server = "https://robotics.dev"
    sio.connect(server)
    return sio.sid

def twist(robot, linear_x, angular_z):
    payload = {
        "robot": robot,
        "twist": {
            "linear": {"x": linear_x, "y": 0.0, "z": 0.0},
            "angular": {"x": 0.0, "y": 0.0, "z": angular_z}
        }
    }
    sio.emit('twist', payload)
