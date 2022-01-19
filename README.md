# Common API Server

This is a web application to act as a **common Backend Service** for hosting API endpoints and its corresponding data that is intended for being used by various multiple cross-platform and web apps. The project is expected to be introduced to Open Source Contribution by June 2022.



## View deployed app  🚀🎉🎊

[https://commonapiserver.herokuapp.com/](https://commonapiserver.herokuapp.com/ "Common Backend Service for hosting API and data")

<br>

<img src="https://cdn.dribbble.com/users/2119/screenshots/15525031/media/954e4e74031d65559eecf0cf29d2b20b.jpg?compress=1&resize=1600x1200&vertical=top" style="height:400px;width:100%">



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

To test the server in `dev mode` 👨‍💻, create a file for example `run_dev_mode.py` and paste the following code 🐍:

```python
from src.common_api_server.main import app

if __name__=="__main__":
    app.config.update(
        TESTING=True,
        SECRET_KEY='123',
        ENV = 'development'
    )
    app.run(host="0.0.0.0", port=5000,debug=True)

```

🎉 Now, start the server in `development mode` 🚀:

```bash
py run_dev_mode.py
```

