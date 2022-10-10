from os import getenv

host = getenv('FLASK_RUN_HOST', "0.0.0.0")
port = getenv('FLASK_RUN_PORT', "80")

bind = f"{host}:{port}"

workers = 1
threads = 4
timeout = 60