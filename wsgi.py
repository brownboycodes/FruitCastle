from src.fruit_castle.main import app, socketio
from src.fruit_castle.playpal.v3.v3_socket_events import *
from flask_compress import Compress

compress=Compress()

if __name__ == "__main__":
    compress.init_app(app)
    socketio.run(app)
