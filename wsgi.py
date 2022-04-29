import os
from src.fruit_castle.main import app, socketio
from src.fruit_castle.hadwin.v3.v3_socket_events import *

if __name__ == "__main__":
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
    socketio.run(app)
