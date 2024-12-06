import socketio
import queue
import threading

sio = socketio.Client()
event_queue = queue.Queue()

def connect(serverParam="https://robotics.dev"):
    if serverParam != "https://robotics.dev":
        server = serverParam
    else:
        server = "https://robotics.dev"
    sio.connect(server)
    threading.Thread(target=process_events, daemon=True).start()  # Start a worker thread
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
        """Puts the event data in a queue for synchronous processing."""
        event_queue.put((callback, data))

def process_events():
    """Worker thread to process events from the queue synchronously."""
    while True:
        callback, data = event_queue.get()  # Blocks until an event is available
        try:
            callback(data)  # Process the event
        finally:
            event_queue.task_done()  # Mark the task as done
