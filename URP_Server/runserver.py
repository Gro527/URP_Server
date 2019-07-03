"""
This script runs the URP_Server application using a development server.
"""

from os import environ
from URP_Server import app
from URP_Server.db import dbconnect



if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    with app.app_context():
        dbconnect.get_conn()
    app.run(HOST, PORT, debug=True)
