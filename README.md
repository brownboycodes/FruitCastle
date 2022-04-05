# Common API Server

This is a web application to act as a **common Backend Service** for hosting API endpoints and its corresponding data that is intended for being used by various multiple cross-platform and web apps.

## View deployed app  🚀🎉🎊

[https://commonapiserver.herokuapp.com/](https://commonapiserver.herokuapp.com/ "Common Backend Service for hosting API and data")

<br>
<p align="center">
<img title="" src="https://cdn.dribbble.com/users/92156/screenshots/14530642/media/4c0507f23b1514818736f436a872857e.png" alt="" style="width:75%">
</p>

## Installation Guidelines

Clone the repo to your computer, execute to the following commands in CMD or Bash:

```bash
git clone https://github.com/brownboycodes/common-api-server.git
```

access the downloaded directory 📁:

```bash
cd common-api-server
```

setup virtual environment for Python 🐍:

```bash
py -3 -m venv venv
```

activate virtual environment:

```bash
venv\Scripts\activate 
```

install packages 📦 required by the flask app 🐍:

```bash
pip install -r requirements.txt 
```

To test the server in `dev mode` 👨‍💻, create a file, for example- `run_dev_mode.py` and paste the following code 🐍:

```python
from src.common_api_server.main import app, socketio
from src.common_api_server.playpal.v3.v3_socket_events import *


if __name__ == "__main__":
    app.config.update(
        TESTING=True,
        SECRET_KEY='123',
        ENV='development',
    )

    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
```

🎉 Now, start the server in `development mode` 🚀:

```bash
py run_dev_mode.py
```

<br>

---

> [Common API Server](https://commonapiserver.herokuapp.com/) © 2022 was developed by Nabhodipta Garai and is owned by him.


