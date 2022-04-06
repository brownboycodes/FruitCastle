from src.fruit_castle.main import app, socketio
from src.fruit_castle.playpal.v3.v3_socket_events import *

if __name__ == "__main__":
    socketio.run(app)
