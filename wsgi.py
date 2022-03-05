from src.common_api_server.main import app, socketio
from src.common_api_server.paypal_concept_data.v3.v3_socket_events import *

if __name__ == "__main__":
    # app.run()
    socketio.run(app)
