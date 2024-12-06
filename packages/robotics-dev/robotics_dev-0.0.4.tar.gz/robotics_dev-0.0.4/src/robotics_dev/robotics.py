import socketio

sio = socketio.Client()

def connect(serverParam="https://robotics.dev"):
    if serverParam != "https://robotics.dev":
        server = serverParam
    else:
        server = "https://robotics.dev"
    sio.connect(server)
    return sio.sid

def twist(robot_id, linear_x, angular_z):
    payload = {
        "robot": robot_id,
        "twist": {
            "linear": {"x": linear_x, "y": 0.0, "z": 0.0},
            "angular": {"x": 0.0, "y": 0.0, "z": angular_z}
        }
    }
    sio.emit('twist', payload)

def subscribe(robot_id, callback):
    """Subscribes to messages for a given robot ID and sets up a listener."""
    event_name = f"{robot_id}/color/image_raw"

    @sio.on(event_name)
    def handle_event(data):
        """Handles the event and forwards the data to the provided callback."""
        callback(data)
